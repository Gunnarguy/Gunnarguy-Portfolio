#!/usr/bin/env python3
"""
CI version of snapshot generator - reads from _repos/ checkout directory.
Runs in GitHub Actions context where repos are checked out to _repos/.
NO EXTERNAL DEPENDENCIES - pure Python stdlib.
"""

import os
import re
import json
import html
from datetime import datetime
from pathlib import Path

# Base paths for CI environment
WORKSPACE = os.environ.get("GITHUB_WORKSPACE", os.getcwd())
REPOS_DIR = os.path.join(WORKSPACE, "_repos")
OUTPUT_DIR = os.path.join(WORKSPACE, "projects")

# Project configurations
PROJECTS = {
    "linkedout": {
        "repo_name": "LinkedOut",
        "title": "LinkedOut",
        "tagline": "AI-powered job discovery app with LLM scoring, swipe UI, LinkedIn OAuth, and FastAPI backend orchestration.",
        "app_store_url": None,
        "github_url": "https://github.com/Gunnarguy/LinkedOut",
        "accent_color": "#0ea5e9",
    },
    "plaudblender": {
        "repo_name": "PlaudBlender",
        "title": "PlaudBlender",
        "tagline": "Plaud voice recordings into a searchable knowledge graph with Gemini AI, Qdrant, Dash UI, and MCP tools.",
        "app_store_url": None,
        "github_url": "https://github.com/Gunnarguy/PlaudBlender",
        "accent_color": "#14b8a6",
    },
    "openresponses": {
        "repo_name": "OpenResponses",
        "title": "OpenResponses",
        "tagline": "Third app. Rebuilt on Responses after it became obvious OpenAssistant would age out on older endpoints.",
        "app_store_url": "https://apps.apple.com/us/app/openresponses/id6757338355",
        "github_url": "https://github.com/Gunnarguy/OpenResponses",
        "accent_color": "#6366f1",
        "story_cards": [
            {
                "title": "Why it exists",
                "description": "I did not want the first app stranded on older endpoints.",
            },
            {
                "title": "How I built it",
                "description": "I kept the old app open in one window, the new one in another, and rebuilt the core flow on the Responses stack.",
            },
            {
                "title": "What changed",
                "description": "This one passed App Review on the first submission.",
            },
        ],
    },
    "openintelligence": {
        "repo_name": "OpenIntelligence",
        "title": "OpenIntelligence",
        "tagline": "Fourth app. Built because I wanted an offline version of the same document workflow on Apple's Foundation Models path.",
        "app_store_url": "https://apps.apple.com/us/app/openintelligence/id6756559175",
        "github_url": "https://github.com/Gunnarguy/OpenIntelligence",
        "accent_color": "#10b981",
        "story_cards": [
            {
                "title": "What kicked it off",
                "description": "WWDC25 made Foundation Models real for third-party apps, so I wanted to try an offline version of the same document workflow on Apple's on-device model path.",
            },
            {
                "title": "What got hard",
                "description": "Apple's public on-device sessions are capped at 4096 tokens, and that same budget has to cover instructions, retrieved evidence, tool and schema overhead, and the answer itself. That is what pushed me into a recursive multi-session reasoning loop.",
            },
            {
                "title": "Why it matters",
                "description": "It is the same document problem again, just in an offline, on-device form.",
            },
        ],
    },
    "opencone": {
        "repo_name": "OpenCone",
        "title": "OpenCone",
        "tagline": "Second app. Built when bigger document sets started stressing the earlier workflow and I wanted more retrieval control.",
        "app_store_url": "https://apps.apple.com/us/app/opencone/id6744467668",
        "github_url": "https://github.com/Gunnarguy/OpenCone",
        "accent_color": "#f59e0b",
        "story_cards": [
            {
                "title": "Why it exists",
                "description": "I wanted to work with larger document sets without the earlier flow falling apart.",
            },
            {
                "title": "How I built it",
                "description": "Same basic process as OpenAssistant, now with Pinecone docs, indexes, namespaces, and embeddings layered on top.",
            },
            {
                "title": "Why it mattered",
                "description": "It was the point where retrieval stopped being theoretical and turned into a real app.",
            },
        ],
    },
    "openassistant": {
        "repo_name": "OpenAssistant",
        "title": "OpenAssistant",
        "tagline": "First app. Built because I wanted a better way to work through docs on iPhone.",
        "app_store_url": "https://apps.apple.com/us/app/openassistant/id6692613772",
        "github_url": "https://github.com/Gunnarguy/OpenAssistant",
        "accent_color": "#8b5cf6",
        "story_cards": [
            {
                "title": "Why it exists",
                "description": "I wanted a better document workflow on iPhone than the official app gave me.",
            },
            {
                "title": "How I built it",
                "description": "Copied docs, Playground threads, red Xcode errors, rebuilds.",
            },
            {
                "title": "Why it matters",
                "description": "It is still the foundation for everything that followed.",
            },
        ],
    },
}


def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def extract_features(content):
    """Extract features from README."""
    features = []
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
    keywords = [
        "SwiftUI",
        "Swift",
        "Combine",
        "OpenAI",
        "Pinecone",
        "RAG",
        "Vision",
        "CoreML",
        "Apple Intelligence",
        "MCP",
        "Computer Use",
        "Code Interpreter",
        "MVVM",
        "EventKit",
        "FastAPI",
        "Python",
        "Gemini",
        "Qdrant",
        "Dash",
        "Cytoscape",
        "Docker",
        "MapKit",
        "LinkedIn OAuth",
        "Notion",
        "SQLite",
        "SQLAlchemy",
        "Render",
    ]
    for kw in keywords:
        if kw.lower() in content.lower():
            tech.append(kw)
    return tech[:10]


def resolve_readme(repo_path):
    """Return the best available README content for a repo."""
    candidates = [
        os.path.join(repo_path, "README.md"),
        os.path.join(repo_path, "readme.md"),
        os.path.join(repo_path, "docs", "README.md"),
        os.path.join(repo_path, "docs", "readme.md"),
    ]
    for candidate in candidates:
        content = read_file_safe(candidate)
        if content:
            return content, candidate
    return "", None


def generate_page(project_id, config, readme_content):
    """Generate HTML page for a project."""
    features = extract_features(readme_content)
    tech = extract_tech_stack(readme_content)
    story_cards = config.get("story_cards", [])

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

    story_section = ""
    story_nav_link = ""
    if story_cards:
        story_nav_link = '<a href="#story">Story</a>'
        story_html = ""
        for card in story_cards:
            story_html += f"""
        <div class="story-card">
            <h3>{html.escape(card["title"])}</h3>
            <p>{html.escape(card["description"])}</p>
        </div>"""
        story_section = f"""
    <section id="story" class="section section-alt">
        <div class="container">
            <h2>How It Happened</h2>
            <div class="story-grid">{story_html}
            </div>
        </div>
    </section>"""

    return f"""<!DOCTYPE html>
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
.story-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }}
.story-card {{ background: var(--bg-card); padding: 1.5rem; border-radius: 12px; border: 1px solid var(--border-color); }}
.story-card h3 {{ color: var(--accent); margin-bottom: 0.6rem; font-size: 1.05rem; }}
.story-card p {{ color: var(--text-secondary); font-size: 0.96rem; }}
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
            {story_nav_link}
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

    {story_section}

    <section id="features" class="section">
        <div class="container">
            <h2>Features</h2>
            <div class="features-grid">{feature_cards if feature_cards else '<p style="text-align:center;color:var(--text-secondary);">See the README for full feature list.</p>'}</div>
        </div>
    </section>

    <footer class="project-footer">
        <p>Part of the <a href="../../index.html#projects">Open- Series</a> by Gunnar Hostetler</p>
        <p class="sync-time">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")} UTC</p>
    </footer>
</body>
</html>"""


def copy_docs(repo_path, output_dir):
    """Copy markdown docs from repo."""
    docs_src = os.path.join(repo_path, "docs")
    docs_dst = os.path.join(output_dir, "docs")
    os.makedirs(docs_dst, exist_ok=True)

    copied = 0
    if os.path.isdir(docs_src):
        for item in os.listdir(docs_src):
            src_path = os.path.join(docs_src, item)
            if os.path.isfile(src_path) and item.endswith('.md'):
                with open(src_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(os.path.join(docs_dst, item), 'w', encoding='utf-8') as f:
                    f.write(content)
                copied += 1
    return copied


def main():
    print("🚀 CI Snapshot Generator")
    print(f"   Workspace: {WORKSPACE}")
    print(f"   Repos dir: {REPOS_DIR}")
    print(f"   Output dir: {OUTPUT_DIR}")

    for project_id, config in PROJECTS.items():
        repo_path = os.path.join(REPOS_DIR, config["repo_name"])
        print(f"\n📦 {config['title']}...")

        if not os.path.isdir(repo_path):
            print(f"   ⚠️  Repo not found: {repo_path}")
            continue

        output_dir = os.path.join(OUTPUT_DIR, project_id)
        os.makedirs(output_dir, exist_ok=True)

        # Read README with fallbacks
        readme, readme_path = resolve_readme(repo_path)
        if not readme:
            print(f"   ⚠️  No README found (checked root + docs)")
            continue
        readme_label = (
            os.path.relpath(readme_path, repo_path) if readme_path else "README"
        )
        print(f"   ✓ README: {readme_label}")

        # Generate index.html
        page_html = generate_page(project_id, config, readme)
        with open(os.path.join(output_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(page_html)
        print(f"   ✓ index.html")

        # Copy docs
        docs_count = copy_docs(repo_path, output_dir)
        if docs_count:
            print(f"   ✓ {docs_count} docs copied")

        # Save README to docs/
        os.makedirs(os.path.join(output_dir, "docs"), exist_ok=True)
        with open(os.path.join(output_dir, "docs", "README.md"), 'w', encoding='utf-8') as f:
            f.write(readme)

        # Generate manifest
        manifest = {
            "project": project_id,
            "title": config["title"],
            "generated_at": datetime.now().isoformat(),
            "source_repo": config["github_url"]
        }
        with open(os.path.join(output_dir, "manifest.json"), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

    print(f"\n✅ Done!")


if __name__ == "__main__":
    main()
