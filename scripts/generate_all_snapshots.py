#!/usr/bin/env python3
"""
Universal snapshot generator for all Open- projects.
Generates beautiful HTML project pages from repo README + docs.
NO EXTERNAL DEPENDENCIES - pure Python stdlib.
"""

import os
import re
import json
import html
from datetime import datetime
from pathlib import Path

# Project configurations
PROJECTS = {
    "openresponses": {
        "repo_path": "/Users/gunnarhostetler/Documents/GitHub/OpenResponses",
        "title": "OpenResponses",
        "tagline": "SwiftUI-powered AI assistant for OpenAI Responses API with computer use, code interpreter, and MCP integrations.",
        "app_store_url": None,  # Not yet on App Store
        "github_url": "https://github.com/Gunnarguy/OpenResponses",
        "accent_color": "#6366f1",
        "icon": "openresponses-icon.png"
    },
    "openintelligence": {
        "repo_path": "/Users/gunnarhostetler/Documents/GitHub/OpenIntelligence",
        "title": "OpenIntelligence",
        "tagline": "On-device RAG engine for iOS with Vision OCR, Apple Intelligence routing, and privacy-first telemetry.",
        "app_store_url": None,
        "github_url": "https://github.com/Gunnarguy/RAGMLCore",
        "accent_color": "#10b981",
        "icon": "ragmlcore-icon.png"
    },
    "opencone": {
        "repo_path": "/Users/gunnarhostetler/Documents/GitHub/OpenCone",
        "title": "OpenCone",
        "tagline": "Semantic search and RAG workflow app with Pinecone integration for iOS.",
        "app_store_url": "https://apps.apple.com/us/app/opencone/id6744467668",
        "github_url": "https://github.com/Gunnarguy/OpenCone",
        "accent_color": "#f59e0b",
        "icon": "opencone-icon.png"
    },
    "openassistant": {
        "repo_path": "/Users/gunnarhostetler/Documents/GitHub/OpenAssistant",
        "title": "OpenAssistant",
        "tagline": "Native iOS app for OpenAI Assistants API interaction.",
        "app_store_url": "https://apps.apple.com/us/app/openassistant/id6692613772",
        "github_url": "https://github.com/Gunnarguy/OpenAssistant",
        "accent_color": "#8b5cf6",
        "icon": "openassistant-icon.png"
    }
}

PORTFOLIO_PATH = "/Users/gunnarhostetler/Documents/GitHub/Gunnarguy-Portfolio"


def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def extract_features(content):
    """Extract features from README."""
    features = []
    # Look for ## Features or ## Core Features section
    match = re.search(r'##\s*(Core\s+)?Features?\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if match:
        section = match.group(2)
        for line in section.split('\n'):
            feat = re.match(r'^[-*]\s+\*\*([^*]+)\*\*[:\s]*(.+)?', line)
            if feat:
                features.append({"name": feat.group(1).strip(), "description": (feat.group(2) or "").strip()})
            elif re.match(r'^[-*]\s+(.+)', line):
                plain = re.match(r'^[-*]\s+(.+)', line)
                if plain and len(plain.group(1)) > 10:
                    features.append({"name": plain.group(1)[:50], "description": ""})
    return features[:8]


def extract_tech_stack(content):
    """Extract tech/tools mentioned."""
    tech = []
    keywords = ["SwiftUI", "Swift", "Combine", "OpenAI", "Pinecone", "RAG", "Vision", "CoreML",
                "Apple Intelligence", "MCP", "Computer Use", "Code Interpreter", "MVVM", "EventKit"]
    for kw in keywords:
        if kw.lower() in content.lower():
            tech.append(kw)
    return tech[:10]


def simple_md_to_html(md):
    """Basic markdown to HTML."""
    content = html.escape(md)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
    content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    return content


def generate_page(project_id, config):
    """Generate HTML page for a project."""
    readme = read_file_safe(os.path.join(config["repo_path"], "README.md"))
    features = extract_features(readme)
    tech = extract_tech_stack(readme)

    # Check for docs folder
    docs_path = os.path.join(config["repo_path"], "docs")
    has_docs = os.path.isdir(docs_path)

    feature_cards = ""
    for f in features:
        feature_cards += f'''
        <div class="feature-card">
            <h3>{html.escape(f["name"])}</h3>
            <p>{html.escape(f["description"])}</p>
        </div>'''

    tech_tags = "".join(f'<span class="tech-tag">{html.escape(t)}</span>' for t in tech)

    app_store_btn = ""
    if config.get("app_store_url"):
        app_store_btn = f'''<a href="{config["app_store_url"]}" class="btn btn-appstore" target="_blank">
            <i class="fab fa-app-store-ios"></i> App Store
        </a>'''

    docs_section = ""
    if has_docs:
        docs_section = '''
        <section id="docs" class="section section-alt">
            <div class="container">
                <h2>Documentation</h2>
                <p>Explore the full documentation in the <a href="docs/">docs folder</a>.</p>
            </div>
        </section>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config["title"]} - Project Deep Dive | Gunnar Hostetler</title>
    <meta name="description" content="{html.escape(config["tagline"])}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
:root {{
    --bg-primary: #0a0a0f; --bg-secondary: #12121a; --bg-card: #1a1a24;
    --text-primary: #fff; --text-secondary: #a0a0b0;
    --accent: {config["accent_color"]}; --accent-light: {config["accent_color"]}99;
    --border-color: #2a2a3a;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Inter', sans-serif; background: var(--bg-primary); color: var(--text-primary); line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 0 2rem; }}
.project-nav {{ position: fixed; top: 0; left: 0; right: 0; background: rgba(10,10,15,0.95); backdrop-filter: blur(10px); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center; z-index: 1000; border-bottom: 1px solid var(--border-color); }}
.back-link {{ color: var(--text-secondary); text-decoration: none; display: flex; align-items: center; gap: 0.5rem; }}
.back-link:hover {{ color: var(--accent); }}
.nav-links {{ display: flex; gap: 1.5rem; }}
.nav-links a {{ color: var(--text-secondary); text-decoration: none; font-size: 0.9rem; }}
.nav-links a:hover {{ color: var(--accent); }}
.project-hero {{ padding: 8rem 0 4rem; background: linear-gradient(180deg, var(--bg-secondary), var(--bg-primary)); text-align: center; }}
.project-hero h1 {{ font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; background: linear-gradient(135deg, #fff, var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
.hero-subtitle {{ font-size: 1.25rem; color: var(--text-secondary); max-width: 700px; margin: 0 auto 2rem; }}
.hero-actions {{ display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }}
.btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: 500; transition: all 0.2s; }}
.btn-primary {{ background: var(--accent); color: white; }}
.btn-primary:hover {{ filter: brightness(1.1); transform: translateY(-2px); }}
.btn-secondary {{ background: var(--bg-card); color: var(--text-primary); border: 1px solid var(--border-color); }}
.btn-secondary:hover {{ border-color: var(--accent); }}
.btn-appstore {{ background: #000; color: white; border: 1px solid #333; }}
.btn-appstore:hover {{ background: #1a1a1a; }}
.section {{ padding: 5rem 0; }}
.section-alt {{ background: var(--bg-secondary); }}
.section h2 {{ font-size: 2rem; margin-bottom: 2rem; text-align: center; }}
.features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }}
.feature-card {{ background: var(--bg-card); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border-color); transition: border-color 0.2s; }}
.feature-card:hover {{ border-color: var(--accent); }}
.feature-card h3 {{ color: var(--accent); margin-bottom: 0.5rem; font-size: 1.1rem; }}
.feature-card p {{ color: var(--text-secondary); font-size: 0.95rem; }}
.tech-stack {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 0.75rem; margin-top: 2rem; }}
.tech-tag {{ background: var(--bg-card); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.85rem; border: 1px solid var(--border-color); }}
.project-footer {{ padding: 2rem 0; text-align: center; border-top: 1px solid var(--border-color); }}
.project-footer a {{ color: var(--accent); text-decoration: none; }}
.sync-time {{ font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.5rem; }}
@media (max-width: 768px) {{ .project-hero h1 {{ font-size: 2.5rem; }} .nav-links {{ display: none; }} .hero-actions {{ flex-direction: column; align-items: center; }} }}
    </style>
</head>
<body>
    <nav class="project-nav">
        <a href="../../index.html" class="back-link"><i class="fas fa-arrow-left"></i> Portfolio</a>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="{config["github_url"]}" target="_blank"><i class="fab fa-github"></i></a>
        </div>
    </nav>

    <header class="project-hero">
        <div class="container">
            <h1>{config["title"]}</h1>
            <p class="hero-subtitle">{html.escape(config["tagline"])}</p>
            <div class="hero-actions">
                <a href="{config["github_url"]}" class="btn btn-primary" target="_blank">
                    <i class="fab fa-github"></i> View on GitHub
                </a>
                {app_store_btn}
            </div>
            <div class="tech-stack">{tech_tags}</div>
        </div>
    </header>

    <section id="features" class="section">
        <div class="container">
            <h2>Features</h2>
            <div class="features-grid">{feature_cards if feature_cards else '<p style="text-align:center;color:var(--text-secondary);">See the README for full feature list.</p>'}</div>
        </div>
    </section>

    {docs_section}

    <footer class="project-footer">
        <p>Part of the <a href="../../index.html#projects">Open- Series</a> by Gunnar Hostetler</p>
        <p class="sync-time">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
    </footer>
</body>
</html>'''


def copy_docs(project_id, config, output_dir):
    """Copy docs folder if it exists."""
    docs_src = os.path.join(config["repo_path"], "docs")
    docs_dst = os.path.join(output_dir, "docs")

    if os.path.isdir(docs_src):
        os.makedirs(docs_dst, exist_ok=True)
        for item in os.listdir(docs_src):
            src_path = os.path.join(docs_src, item)
            if os.path.isfile(src_path) and item.endswith('.md'):
                with open(src_path, 'r') as f:
                    content = f.read()
                with open(os.path.join(docs_dst, item), 'w') as f:
                    f.write(content)
        return True
    return False


def main():
    print("🚀 Generating snapshots for all Open- projects...")

    for project_id, config in PROJECTS.items():
        print(f"\n📦 Processing {config['title']}...")

        if not os.path.isdir(config["repo_path"]):
            print(f"  ⚠️  Repo not found: {config['repo_path']}")
            continue

        output_dir = os.path.join(PORTFOLIO_PATH, "projects", project_id)
        os.makedirs(output_dir, exist_ok=True)

        # Generate index.html
        page_html = generate_page(project_id, config)
        with open(os.path.join(output_dir, "index.html"), 'w') as f:
            f.write(page_html)
        print(f"  ✓ Generated index.html")

        # Copy docs
        if copy_docs(project_id, config, output_dir):
            print(f"  ✓ Copied docs/")

        # Copy README
        readme = read_file_safe(os.path.join(config["repo_path"], "README.md"))
        if readme:
            os.makedirs(os.path.join(output_dir, "docs"), exist_ok=True)
            with open(os.path.join(output_dir, "docs", "README.md"), 'w') as f:
                f.write(readme)
            print(f"  ✓ Copied README.md")

        # Generate manifest
        manifest = {
            "project": project_id,
            "title": config["title"],
            "generated_at": datetime.now().isoformat(),
            "source_repo": config["github_url"]
        }
        with open(os.path.join(output_dir, "manifest.json"), 'w') as f:
            json.dump(manifest, f, indent=2)

    print(f"\n✅ All snapshots generated in {PORTFOLIO_PATH}/projects/")


if __name__ == "__main__":
    main()
