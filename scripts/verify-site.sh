#!/usr/bin/env bash
set -euo pipefail

mode="${1:-all}"
domain="${2:-gunnarguy.me}"
repo_slug="Gunnarguy/Gunnarguy-Portfolio"
expected_cname="gunnarguy.me"
expected_branch="main"
expected_path="/"

usage() {
  cat <<'EOF'
Usage: ./scripts/verify-site.sh [all|source|live|ci-live] [domain]

Modes:
  source   Run repository-only checks.
  live     Run DNS, Pages, deployed-content, TLS, and redirect checks.
  ci-live  Wait for the current commit's Pages build, then run live checks.
  all      Run source checks, then live checks.
EOF
}

section() {
  printf '== %s ==\n' "$1"
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 1
  fi
}

lookup_a_records() {
  if command -v dig >/dev/null 2>&1; then
    dig +short "$domain" A
    return
  fi

  if command -v nslookup >/dev/null 2>&1; then
    nslookup -type=A "$domain" | awk '/^Address: / { print $2 }'
    return
  fi

  printf 'DNS lookup tool unavailable\n'
}

extract_first_match() {
  local file="$1"
  local regex="$2"

  extract_match_from_text "$(cat "$file")" "$regex" "$file"
}

extract_match_from_text() {
  local text="$1"
  local regex="$2"
  local source_label="${3:-input}"
  local match

  match="$(grep -Eo "$regex" <<<"$text" | head -n 1 || true)"
  if [[ -z "$match" ]]; then
    printf 'Failed to extract %s from %s\n' "$regex" "$source_label" >&2
    exit 1
  fi

  printf '%s\n' "$match"
}

assert_contains() {
  local haystack="$1"
  local needle="$2"

  if ! grep -Fq -- "$needle" <<<"$haystack"; then
    printf 'Expected to find "%s" in fetched content\n' "$needle" >&2
    exit 1
  fi
}

git_file_text() {
  git show "$1:$2" 2>/dev/null || true
}

has_verify_diff_base() {
  [[ -n "${VERIFY_DIFF_BASE:-}" ]] || return 1
  git rev-parse -q --verify "${VERIFY_DIFF_BASE}^{commit}" >/dev/null 2>&1
}

diff_includes_file() {
  local file="$1"

  has_verify_diff_base || return 1
  git diff --name-only "$VERIFY_DIFF_BASE" HEAD -- "$file" | grep -q .
}

assert_ref_bumped() {
  local asset_file="$1"
  local ref_file="$2"
  local regex="$3"
  local label="$4"
  local current_ref
  local base_ref
  local base_text

  if ! diff_includes_file "$asset_file"; then
    printf '%s unchanged; skip\n' "$asset_file"
    return
  fi

  current_ref="$(extract_first_match "$ref_file" "$regex")"
  base_text="$(git_file_text "$VERIFY_DIFF_BASE" "$ref_file")"
  if [[ -z "$base_text" ]]; then
    printf 'Missing %s at base ref %s\n' "$ref_file" "$VERIFY_DIFF_BASE" >&2
    exit 1
  fi

  base_ref="$(extract_match_from_text "$base_text" "$regex" "$ref_file@$VERIFY_DIFF_BASE")"
  if [[ "$current_ref" == "$base_ref" ]]; then
    printf '%s changed but %s was not bumped (%s)\n' "$asset_file" "$label" "$current_ref" >&2
    exit 1
  fi

  printf '%s bumped: %s -> %s\n' "$label" "$base_ref" "$current_ref"
}

gh_pages_field() {
  require_cmd gh
  gh api -H 'X-GitHub-Api-Version: 2022-11-28' "repos/$repo_slug/pages" --jq "$1"
}

gh_latest_build_field() {
  require_cmd gh
  gh api -H 'X-GitHub-Api-Version: 2022-11-28' "repos/$repo_slug/pages/builds/latest" --jq "$1"
}

latest_build_contains_expected() {
  local expected_commit="$1"
  local latest_commit="$2"

  [[ -n "$latest_commit" ]] || return 1
  [[ "$latest_commit" == "$expected_commit" ]] && return 0

  if git merge-base --is-ancestor "$expected_commit" "$latest_commit" >/dev/null 2>&1; then
    return 0
  fi

  git fetch --quiet --depth=50 origin "$expected_branch" >/dev/null 2>&1 || true
  git merge-base --is-ancestor "$expected_commit" "$latest_commit" >/dev/null 2>&1
}

fetch_body() {
  curl -fsSL --retry 3 --retry-all-errors -H 'Cache-Control: no-cache' "$1"
}

https_headers() {
  curl -fsSI --retry 3 --retry-all-errors "$1"
}

http_headers() {
  curl -sSI --retry 3 --retry-all-errors "$1"
}

run_source_checks() {
  local styles_ref
  local scripts_ref
  local ga_count

  section "Source sanity"
  git diff --check

  grep -nE '<link[^>]+stylesheet|scripts\.js|G-YZ95J7YFJV' index.html

  styles_ref="$(extract_first_match index.html 'styles\.css\?v=[^"]+')"
  scripts_ref="$(extract_first_match index.html 'scripts\.js\?v=[^"]+')"
  ga_count="$(grep -c 'googletagmanager.com/gtag/js?id=G-YZ95J7YFJV' index.html || true)"

  [[ "$ga_count" == "1" ]] || {
    printf 'Expected exactly one GA tag in index.html, found %s\n' "$ga_count" >&2
    exit 1
  }

  printf 'styles ref: %s\n' "$styles_ref"
  printf 'scripts ref: %s\n\n' "$scripts_ref"

  run_asset_bump_checks
}

run_asset_bump_checks() {
  if ! has_verify_diff_base; then
    return
  fi

  section "Asset version bumps"
  assert_ref_bumped "styles.css" "index.html" 'styles\.css\?v=[^"]+' 'styles.css reference'
  assert_ref_bumped "scripts.js" "index.html" 'scripts\.js\?v=[^"]+' 'scripts.js reference'
  printf '\n'
}

run_pages_checks() {
  local status
  local cname
  local https_enforced
  local https_state
  local source_branch
  local source_path

  section "GitHub Pages config"
  gh api -H 'X-GitHub-Api-Version: 2022-11-28' "repos/$repo_slug/pages" \
    --jq '{status, cname, html_url, https_enforced, https_certificate, source}'

  status="$(gh_pages_field '.status')"
  cname="$(gh_pages_field '.cname')"
  https_enforced="$(gh_pages_field '.https_enforced')"
  https_state="$(gh_pages_field '.https_certificate.state')"
  source_branch="$(gh_pages_field '.source.branch')"
  source_path="$(gh_pages_field '.source.path')"

  if [[ "$mode" != "ci-live" ]]; then
    [[ "$status" == "built" ]] || {
      printf 'Expected Pages status built, found %s\n' "$status" >&2
      exit 1
    }
  fi
  [[ "$cname" == "$expected_cname" ]] || {
    printf 'Expected Pages cname %s, found %s\n' "$expected_cname" "$cname" >&2
    exit 1
  }
  [[ "$https_enforced" == "true" ]] || {
    printf 'Expected https_enforced=true, found %s\n' "$https_enforced" >&2
    exit 1
  }
  [[ "$https_state" == "approved" ]] || {
    printf 'Expected https_certificate.state=approved, found %s\n' "$https_state" >&2
    exit 1
  }
  [[ "$source_branch" == "$expected_branch" ]] || {
    printf 'Expected Pages branch %s, found %s\n' "$expected_branch" "$source_branch" >&2
    exit 1
  }
  [[ "$source_path" == "$expected_path" ]] || {
    printf 'Expected Pages path %s, found %s\n' "$expected_path" "$source_path" >&2
    exit 1
  }

  printf '\n'
}

wait_for_pages_build() {
  local expected_commit
  local latest_commit
  local latest_status
  local latest_error
  local attempts
  local sleep_seconds
  local saw_expected_commit

  expected_commit="${GITHUB_SHA:-$(git rev-parse HEAD)}"
  attempts="${PAGES_BUILD_ATTEMPTS:-40}"
  sleep_seconds="${PAGES_BUILD_SLEEP_SECONDS:-15}"
  saw_expected_commit=0

  section "Wait for Pages build"
  printf 'expected commit: %s\n' "$expected_commit"

  while (( attempts > 0 )); do
    latest_commit="$(gh_latest_build_field '.commit')"
    latest_status="$(gh_latest_build_field '.status')"
    latest_error="$(gh_latest_build_field '.error.message // ""')"

    printf 'latest commit=%s status=%s\n' "$latest_commit" "$latest_status"

    if [[ "$latest_commit" == "$expected_commit" ]]; then
      saw_expected_commit=1
      case "$latest_status" in
        built)
          printf '\n'
          return 0
          ;;
        errored|error|failed|canceled)
          if [[ -n "$latest_error" ]]; then
            printf 'Pages build error: %s\n' "$latest_error" >&2
          fi
          exit 1
          ;;
      esac
    elif [[ "$latest_status" == "built" ]] && latest_build_contains_expected "$expected_commit" "$latest_commit"; then
      printf 'Pages build for %s was superseded by built commit %s; continuing with latest deployed site.\n\n' "$expected_commit" "$latest_commit"
      return 0
    fi

    attempts=$((attempts - 1))
    if (( attempts == 0 )); then
      printf 'Timed out waiting for GitHub Pages to build commit %s\n' "$expected_commit" >&2
      exit 1
    fi

    sleep "$sleep_seconds"
  done
}

run_live_checks() {
  local root_html
  local title
  local styles_ref
  local scripts_ref

  title="$(extract_first_match index.html '<title>[^<]+')"
  title="${title#<title>}"
  styles_ref="$(extract_first_match index.html 'styles\.css\?v=[^"]+')"
  scripts_ref="$(extract_first_match index.html 'scripts\.js\?v=[^"]+')"

  section "DNS"
  lookup_a_records
  printf '\n'

  root_html="$(fetch_body "https://$domain/")"

  section "HTTPS content"
  assert_contains "$root_html" "$title"
  assert_contains "$root_html" "$styles_ref"
  assert_contains "$root_html" "$scripts_ref"
  assert_contains "$root_html" 'G-YZ95J7YFJV'
  assert_contains "$root_html" 'Gunnar Hostetler'
  assert_contains "$root_html" 'Selected Work'

  printf '%s\n' "$root_html" | grep -E -m 20 '<title>|Gunnar Hostetler|Selected Work|styles\.css|scripts\.js|G-YZ95J7YFJV'
  printf '\n'
}

run_tls_checks() {
  section "TLS"
  echo | openssl s_client -connect "$domain:443" -servername "$domain" 2>/dev/null \
    | openssl x509 -noout -subject -issuer -dates
  https_headers "https://$domain/" | sed -n '1,12p'
  printf '\n'
}

run_redirect_checks() {
  local headers

  section "HTTP redirect"
  headers="$(http_headers "http://$domain/")"
  printf '%s\n' "$headers" | sed -n '1,12p'
  printf '%s\n' "$headers" | grep -qi '^location: https://'
  printf '\n'
}

run_live_suite() {
  run_pages_checks
  run_live_checks
  run_tls_checks
  run_redirect_checks
}

case "$mode" in
  source)
    run_source_checks
    ;;
  live)
    run_live_suite
    ;;
  ci-live)
    run_pages_checks
    wait_for_pages_build
    run_live_checks
    run_tls_checks
    run_redirect_checks
    ;;
  all)
    run_source_checks
    run_live_suite
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac
