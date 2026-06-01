# Copilot Instructions for Gunnarguy-Portfolio

## Non-Negotiable Site Role

Gunnarguy.me is **The Creator** in Gunnar Hostetler's web ecosystem.

- **Gunnarguy.me** = The Creator: personal software engineer portfolio, case studies, career story, technical proof.
- **Gunzino.me** = The Publisher: publisher site for product landing pages, support, privacy/legal endpoints, and App Store review/user surfaces.
- **Fascinaiting.me** = The Platform: AI orchestration brand for local AI engines, automated pipelines, native utilities, and product initiatives.

Do not collapse these roles into each other. Gunnarguy.me must remain the professional anchor, not an App Store catalog and not the Fascinaiting platform site.

## 10x Web UX Quality Bar

Act like a senior brand architect and product-grade web designer when touching the public surface.

- Keep the first viewport clear: who Gunnar is, why his background matters, and where to go next.
- Use dense but readable information hierarchy; this is a professional portfolio, not a marketing splash page.
- Preserve first-person, concrete, lived-in copy. Avoid generic AI portfolio language.
- Prioritize case-study clarity, credibility, and navigation over decorative UI.
- Buttons, cards, and nav links need stable dimensions and no mobile text overflow.
- Do not ship unstyled HTML. The homepage must always include `styles.css` with a cache-busted query string.

## Architecture & Structure

- Root `index.html` is the main portfolio entry point.
- Root `styles.css` controls global portfolio styling.
- Root `scripts.js` controls dynamic UI behavior and telemetry helpers.
- `projects/*/index.html` pages are generated from Markdown by Python scripts. Do not manually rewrite generated project pages unless the user explicitly asks for an emergency static fix.
- `scripts/generate_snapshot.py` and `scripts/generate_all_snapshots.py` are the source of truth for generated project page templates.
- Asset paths in `Private & Shared/` contain spaces and special characters; use URL encoding when referenced in HTML.

## Content Contract

The homepage should emphasize:

- Gunnar as a high-agency software builder with healthcare operations context.
- Shipped iOS/mobile proof, App Store progression, and practical AI tooling.
- OR support, on-site ownership, Stanford/VA context, and specific technical constraints.
- Case-study deep dives and network acquisition.

Avoid:

- Turning the homepage into Gunzino's app catalog.
- Turning the homepage into Fascinaiting's AI orchestration product page.
- Generic SWE portfolio filler, inflated prestige language, or vague AI claims.

## Telemetry Rules

The GA4 property is `G-YZ95J7YFJV`.

Every meaningful interactive element should use `data-track`, `data-track-group`, and where useful `data-track-value`. Do not remove the shared GA4 click listener without replacing equivalent telemetry.

## Cache-Busting Rules

GitHub Pages and browsers can serve stale assets. Root local assets must use version query strings.

Expected homepage pattern:

```html
<link rel="stylesheet" href="styles.css?v=YYYYMMDDx" />
<script src="scripts.js?v=YYYYMMDDx"></script>
```

When changing `styles.css` or `scripts.js`, bump the related query string in `index.html`. If generated templates reference local assets, update the generator rather than only editing generated HTML.

## Generated Project Workflow

Setup:

```bash
pip install -r scripts/requirements.txt
```

Generate all snapshots:

```bash
python3 scripts/generate_all_snapshots.py
```

Generate one snapshot:

```bash
python3 scripts/generate_snapshot.py <project_slug>
```

After generator changes, inspect both the script diff and generated output.

## Deployment Rules

Gunnarguy.me is hosted by GitHub Pages from `main` at `/`.

Correct DNS state:

```text
A @ 185.199.108.153
A @ 185.199.109.153
A @ 185.199.110.153
A @ 185.199.111.153
CNAME www Gunnarguy.github.io
```

GitHub Pages must report an approved certificate and `https_enforced:true`.

## Validation Checklist

Before finalizing site changes:

```bash
git diff --check
grep -nE '<link[^>]+stylesheet|scripts\.js|G-YZ95J7YFJV' index.html
curl -fsSL -H 'Cache-Control: no-cache' https://gunnarguy.me/ | grep -E -m 20 '<title>|iOS Engineer Portfolio|styles\.css|scripts\.js|G-YZ95J7YFJV'
curl -vI https://gunnarguy.me/ 2>&1 | grep -E 'subject:|issuer:|SSL certificate verify ok|HTTP/'
```

Prefer running `./scripts/verify-site.sh` after deployment-oriented changes.

When the user asks whether it is live, answer from actual `curl`, DNS, Pages config, and certificate checks, not from GitHub commit state alone.
