# Copilot Instructions for Gunnarguy-Portfolio

## Project Overview

This repository hosts the personal professional portfolio for Gunnar Hostetler. It is a static website that serves as a landing page for various iOS and AI projects (Open- series).

## Architecture & Structure

- **Root**: `index.html` is the main entry point. `styles.css` handles the styling.
- **Projects (`projects/`)**: Contains sub-pages for individual projects (e.g., `openassistant`, `opencone`). each containing an `index.html` and `manifest.json`.
  - These pages are **generated** from external Markdown sources using Python scripts.
  - Do not manually edit the content in `projects/*/index.html` if it's meant to be generated.
- **Scripts (`scripts/`)**: Python automation tools used to fetch content and generate the static project pages.
- **Assets**: Images and other assets are stored in `assets/` and the `Private & Shared/` directory (namespaced from Notion exports).

## Developer Workflows

### 1. Updating the Main Portfolio

- Edit `index.html` for content changes on the landing page.
- Edit `styles.css` for global styling.
- **Note**: The codebase uses vanilla HTML/CSS/JS. No build step is required for the main page.

### 2. Generating Project Documentation

The project pages are generated using Python scripts that convert Markdown to HTML.

- **Setup**: Install dependencies:
  ```bash
  pip install -r scripts/requirements.txt
  ```
- **Generate All Snapshots**:
  ```bash
  python3 scripts/generate_all_snapshots.py
  ```
- **Generate Single Snapshot**:
  ```bash
  python3 scripts/generate_snapshot.py <project_slug>
  ```
  _(Check the script for specific arguments)_

### 3. Handling Assets

- Be careful with file paths in `Private & Shared/` as they contain spaces and special characters.
- Use URL encoding (e.g., `%20`, `%26`) when referencing them in HTML.

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript.
- **Build Tools**: Python 3 (standard library + `markdown` content conversion).
- **Styling**: Custom CSS (no preprocessors).

## Conventions

- **Path Handling**: Always use absolute paths or careful relative paths due to the nested structure of `projects/`.
- **Scripts**: The `scripts/` directory is the source of truth for how documentation is built. Refer to `generate_snapshot.py` to understand the HTML templating logic.
- **Manifests**: Each project has a `manifest.json`, likely for web app capabilities or metadata.
