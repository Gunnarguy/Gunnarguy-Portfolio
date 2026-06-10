#!/usr/bin/env python3
"""
Generate static snapshot docs pages for the Open- series.
Pulls Markdown from GitHub and writes pre-rendered HTML into /projects/<slug>/index.html
"""
from __future__ import annotations

import datetime as dt
import os
import re
import sys
import urllib.request
from dataclasses import dataclass
from typing import Iterable, List, Optional

try:
    import markdown  # type: ignore
except Exception as exc:  # pragma: no cover
    print("Missing dependency: markdown. Install with: pip install -r scripts/requirements.txt")
    raise SystemExit(1) from exc


@dataclass
class DocItem:
    title: str
    path: str


@dataclass
class RepoConfig:
    slug: str
    title: str
    tagline: str
    owner: str
    repo: str
    ref: str
    app_store_url: Optional[str]
    docs: List[DocItem]


CONFIG: List[RepoConfig] = [
    RepoConfig(
        slug="openresponses",
        title="OpenResponses",
        tagline="The OpenAI Responses API Playground for iOS.",
        owner="Gunnarguy",
        repo="OpenResponses",
        ref="main",
        app_store_url=None,
        docs=[
            DocItem("README", "README.md"),
            DocItem("Roadmap", "docs/ROADMAP.md"),
            DocItem("Architecture", "docs/ARCHITECTURE.md"),
        ],
    ),
    RepoConfig(
        slug="openintelligence",
        title="OpenIntelligence",
        tagline="The first iOS app to run RAG through Apple Intelligence.",
        owner="Gunnarguy",
        repo="OpenIntelligence",
        ref="main",
        app_store_url="https://apps.apple.com/us/app/openintelligence/id6756559175",
        docs=[
            DocItem("README", "README.md"),
            DocItem("Roadmap", "docs/ROADMAP.md"),
            DocItem("Architecture", "docs/ARCHITECTURE.md"),
        ],
    ),
    RepoConfig(
        slug="opencone",
        title="OpenCone",
        tagline="App Store RAG pipeline combining Pinecone serverless indexes with streaming Responses answers.",
        owner="Gunnarguy",
        repo="OpenCone",
        ref="main",
        app_store_url="https://apps.apple.com/us/app/opencone/id6744467668",
        docs=[
            DocItem("README", "README.md"),
            DocItem("Roadmap", "docs/ROADMAP.md"),
            DocItem("Architecture", "docs/ARCHITECTURE.md"),
        ],
    ),
    RepoConfig(
        slug="openassistant",
        title="OpenAssistant",
        tagline="Legacy Assistants v2 client with tool coverage, vector stores, and threaded chat UI.",
        owner="Gunnarguy",
        repo="OpenAssistant",
        ref="main",
        app_store_url="https://apps.apple.com/us/app/openassistant/id6692613772",
        docs=[
            DocItem("README", "README.md"),
            DocItem("Roadmap", "docs/ROADMAP.md"),
            DocItem("Architecture", "docs/ARCHITECTURE.md"),
        ],
    ),
]


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECTS_DIR = os.path.join(ROOT, "projects")


def fetch_raw(owner: str, repo: str, ref: str, path: str) -> str:
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "snapshot-generator"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def md_to_html(md: str) -> str:
    return markdown.markdown(
        md,
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "codehilite",
            "sane_lists",
        ],
        extension_configs={"codehilite": {"guess_lang": False}},
    )


def render_doc_section(cfg: RepoConfig, doc: DocItem) -> str:
    source_url = f"https://github.com/{cfg.owner}/{cfg.repo}/blob/{cfg.ref}/{doc.path}"
    section_id = f"doc-{slugify(doc.title)}"

    try:
        raw = fetch_raw(cfg.owner, cfg.repo, cfg.ref, doc.path)
        html = md_to_html(raw)
        missing_class = ""
        status_note = ""
    except Exception as exc:
        html = (
            "<p><strong>Could not load this document.</strong></p>"
            f"<p>Path: <code>{doc.path}</code></p>"
            f"<p>{exc}</p>"
        )
        missing_class = " docs-section-missing"
        status_note = "<span class=\"docs-status-pill\">Missing</span>"

    return f"""
      <section class=\"docs-section{missing_class}\" id=\"{section_id}\">
        <div class=\"docs-section-header\">
          <h2>{doc.title}</h2>
          <div class=\"docs-section-meta\">
            <a href=\"{source_url}\" target=\"_blank\" rel=\"noopener\">View source</a>
            {status_note}
          </div>
        </div>
        <div class=\"docs-section-body\">
          {html}
        </div>
      </section>
    """


def render_page(cfg: RepoConfig) -> str:
    now = dt.datetime.utcnow().strftime("%b %d, %Y")
    repo_url = f"https://github.com/{cfg.owner}/{cfg.repo}"

    doc_links = "".join(
        f"<li><a href=\"#doc-{slugify(doc.title)}\">{doc.title}</a></li>" for doc in cfg.docs
    )
    sections = "\n".join(render_doc_section(cfg, doc) for doc in cfg.docs)

    app_store_link = (
        f"<a class=\"btn-link\" href=\"{cfg.app_store_url}\" target=\"_blank\" rel=\"noopener\">App Store</a>"
        if cfg.app_store_url
        else ""
    )

    return f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{cfg.title} Docs - Gunnar Hostetler</title>
    <meta name=\"description\" content=\"Snapshot documentation for {cfg.title}.\" />

    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
    <link
      href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap\"
      rel=\"stylesheet\"
    />

    <link rel=\"stylesheet\" href=\"../../styles.css\" />
    <link rel=\"icon\" type=\"image/x-icon\" href=\"../../favicon.ico\" />
  </head>
  <body>
    <header class=\"header\">
      <nav class=\"nav\">
        <div class=\"nav-brand\">
          <h1><a href=\"../../index.html\">Gunnar Hostetler</a></h1>
        </div>
        <ul class=\"nav-menu\">
          <li><a href=\"../../index.html#home\">Home</a></li>
          <li><a href=\"../../index.html#about\">About</a></li>
          <li><a href=\"../../index.html#skills\">Skills</a></li>
          <li><a href=\"../../index.html#projects\">Projects</a></li>
          <li><a href=\"../../index.html#experience\">Experience</a></li>
          <li><a href=\"../../index.html#contact\">Contact</a></li>
        </ul>
        <div class=\"nav-toggle\">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </nav>
    </header>

    <main class=\"docs-main\">
      <div class=\"container\">
        <div class=\"docs-hero\">
          <p class=\"docs-kicker\">Snapshot • {now}</p>
          <h1>{cfg.title} Docs</h1>
          <p>{cfg.tagline}</p>
          <div class=\"docs-actions\">
            <a class=\"btn-link\" href=\"{repo_url}\" target=\"_blank\" rel=\"noopener\">GitHub Repo</a>
            {app_store_link}
            <a class=\"btn-link\" href=\"../../index.html#projects\">Back to Projects</a>
          </div>
        </div>

        <div class=\"docs-layout\">
          <aside class=\"docs-sidebar\">
            <div class=\"docs-sidebar-title\">Sections</div>
            <ul class=\"docs-nav\">
              {doc_links}
            </ul>
            <div class=\"docs-status\">Generated from GitHub on {now}.</div>
          </aside>

          <article class=\"md-content\">
            {sections}
          </article>
        </div>
      </div>
    </main>

    <script src=\"https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js\"></script>
    <script>
      const navToggle = document.querySelector('.nav-toggle');
      const navMenu = document.querySelector('.nav-menu');
      if (navToggle && navMenu) {{
        navToggle.addEventListener('click', () => {{
          navMenu.classList.toggle('nav-menu-active');
          navToggle.classList.toggle('nav-toggle-active');
        }});
      }}

      const normalizeMermaid = () => {{
        document.querySelectorAll('pre > code.language-mermaid').forEach((block) => {{
          const parent = block.parentElement;
          const wrapper = document.createElement('div');
          wrapper.className = 'mermaid';
          wrapper.textContent = block.textContent || '';
          parent.replaceWith(wrapper);
        }});
        if (window.mermaid) {{
          mermaid.initialize({{ startOnLoad: true, theme: 'neutral' }});
          mermaid.init(undefined, document.querySelectorAll('.mermaid'));
        }}
      }};

      document.addEventListener('DOMContentLoaded', normalizeMermaid);
    </script>
  </body>
</html>
"""


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_page(cfg: RepoConfig) -> None:
    target_dir = os.path.join(PROJECTS_DIR, cfg.slug)
    ensure_dir(target_dir)
    path = os.path.join(target_dir, "index.html")
    html = render_page(cfg)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {path}")


def main() -> None:
    for cfg in CONFIG:
        write_page(cfg)


if __name__ == "__main__":
    main()
