#!/usr/bin/env python3
"""Create a single Diátaxis documentation page from bundled templates.

This script creates one page at a time. It intentionally does not create four
empty Diátaxis sections by default.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEMPLATE_FILES = {
    "tutorial": "tutorial.md",
    "how-to": "how-to-guide.md",
    "reference": "reference.md",
    "explanation": "explanation.md",
    "landing-page": "landing-page.md",
    "audit-report": "audit-report.md",
    "doc-index": "doc-index.md",
}


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[`'\"’]", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "untitled"


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def template_path(doc_type: str) -> Path:
    return skill_root() / "assets" / "templates" / TEMPLATE_FILES[doc_type]


def render_template(text: str, title: str, doc_type: str) -> str:
    # Keep placeholder-rich templates mostly intact, but replace the title line
    # and common frontmatter title. Authors can fill the remaining placeholders.
    text = re.sub(r'title:\s*"[^"]+"', f'title: "{title}"', text, count=1)
    if doc_type == "tutorial":
        h1 = f"# Tutorial: {title}" if not title.lower().startswith("tutorial") else f"# {title}"
    elif doc_type == "how-to":
        h1 = f"# {title if title.lower().startswith('how to') else 'How to ' + title[0].lower() + title[1:]}"
    else:
        h1 = f"# {title}"
    text = re.sub(r"^# .+$", h1, text, count=1, flags=re.MULTILINE)
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a Diátaxis documentation page from a bundled template.")
    parser.add_argument("doc_type", choices=sorted(TEMPLATE_FILES), help="Template type to create")
    parser.add_argument("title", help="Page title")
    parser.add_argument("--out-dir", default=".", help="Output directory")
    parser.add_argument("--filename", help="Output filename. Defaults to a slugified title with .md")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing file")
    args = parser.parse_args(argv)

    source = template_path(args.doc_type)
    if not source.exists():
        print(f"Template not found: {source}", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = args.filename or f"{slugify(args.title)}.md"
    target = out_dir / filename

    if target.exists() and not args.force:
        print(f"Refusing to overwrite existing file: {target}. Use --force to overwrite.", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    rendered = render_template(text, args.title, args.doc_type)
    target.write_text(rendered, encoding="utf-8")
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
