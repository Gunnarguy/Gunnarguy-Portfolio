#!/usr/bin/env python3
"""Fetch GitHub stats locally and write data/github-stats.json.
Uses gh CLI token if available for 5000 req/hr instead of 60."""
import json, urllib.request, datetime, sys, subprocess

OWNER = "Gunnarguy"
REPOS = [
    "LinkedOut",
    "MedMod",
    "OpenResponses",
    "OpenIntelligence",
    "PlaudBlender",
    "OpenCone",
    "OpenAssistant",
]

# Try to get auth token from gh CLI
token = None
try:
    token = (
        subprocess.check_output(["gh", "auth", "token"], stderr=subprocess.DEVNULL)
        .decode()
        .strip()
    )
    print("Using authenticated token (5000 req/hr)")
except Exception:
    print("No gh token found, using unauthenticated (60 req/hr)")


def gh_get(url):
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


result = {"repos": {}}

for repo in REPOS:
    print(f"Fetching {repo}...", end=" ")
    try:
        info = gh_get(f"https://api.github.com/repos/{OWNER}/{repo}")
        all_commits = []
        page = 1
        while page <= 20:
            commits = gh_get(
                f"https://api.github.com/repos/{OWNER}/{repo}/commits?per_page=100&page={page}"
            )
            if not commits:
                break
            for c in commits:
                all_commits.append(
                    {
                        "sha": c["sha"],
                        "message": c["commit"]["message"].split("\n")[0],
                        "date": c["commit"]["author"]["date"],
                        "author": c["commit"]["author"]["name"],
                    }
                )
            if len(commits) < 100:
                break
            page += 1
        result["repos"][repo] = {
            "created_at": info["created_at"],
            "description": info.get("description", ""),
            "stars": info.get("stargazers_count", 0),
            "commits": all_commits,
        }
        print(f"{len(all_commits)} commits")
    except Exception as e:
        print(f"FAILED: {e}")

existing = None
try:
    with open("data/github-stats.json", "r") as f:
        existing = json.load(f)
except FileNotFoundError:
    existing = None

if existing and existing.get("repos") == result["repos"]:
    print("\nNo repo stat changes detected; leaving data/github-stats.json untouched")
    sys.exit(0)

output = {
    "generated": datetime.datetime.now(datetime.UTC).isoformat().replace("+00:00", "Z"),
    "repos": result["repos"],
}

with open("data/github-stats.json", "w") as f:
    json.dump(output, f)
print(f"\nWrote data/github-stats.json ({len(output['repos'])} repos)")
