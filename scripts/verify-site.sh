#!/usr/bin/env bash
set -euo pipefail

domain="${1:-gunnarguy.me}"

echo "== DNS =="
dig +short "$domain" A
echo

echo "== GitHub Pages config =="
gh api repos/Gunnarguy/Gunnarguy-Portfolio/pages --jq '{status, cname, html_url, https_enforced, https_certificate}'
echo

echo "== Source sanity =="
git diff --check
grep -nE '<link[^>]+stylesheet|scripts\.js|G-YZ95J7YFJV' index.html
echo

echo "== HTTPS content =="
curl -fsSL -H 'Cache-Control: no-cache' "https://$domain/" \
  | grep -E -m 20 '<title>|iOS Engineer Portfolio|styles\.css|scripts\.js|G-YZ95J7YFJV'
echo

echo "== TLS =="
curl -vI "https://$domain/" 2>&1 \
  | grep -E 'subject:|issuer:|SSL certificate verify ok|HTTP/'
echo

echo "== HTTP redirect =="
curl -sI "http://$domain/" | sed -n '1,12p'
