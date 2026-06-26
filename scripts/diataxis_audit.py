#!/usr/bin/env python3
"""Heuristic Diátaxis audit for Markdown-like documentation.

This script classifies docs as tutorial, how-to, reference, explanation, mixed,
or unknown. It is a triage aid, not an authority. It uses only the Python
standard library and performs no network access.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

DOC_EXTENSIONS = {".md", ".mdx", ".rst", ".txt"}
IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "site",
    "public",
    "__pycache__",
    ".venv",
    "venv",
}

MODES = ("tutorial", "how-to", "reference", "explanation")

TITLE_PATTERNS = {
    "tutorial": [
        (r"\btutorial\b", 6),
        (r"\bquickstart\b", 4),
        (r"\bgetting started\b", 4),
        (r"\byour first\b", 5),
        (r"\bfirst\b", 2),
        (r"\bwalkthrough\b", 4),
        (r"\blearn\b", 3),
    ],
    "how-to": [
        (r"^\s*how\s+to\b", 7),
        (r"\bhow-to\b", 6),
        (r"\btroubleshoot(?:ing)?\b", 5),
        (r"\bconfigure\b", 4),
        (r"\binstall\b", 3),
        (r"\bdeploy\b", 4),
        (r"\bmigrate\b", 4),
        (r"\bupgrade\b", 4),
        (r"\brotate\b", 4),
        (r"\bset up\b", 4),
        (r"\buse .* to\b", 3),
    ],
    "reference": [
        (r"\breference\b", 7),
        (r"\bapi\b", 4),
        (r"\bcli\b", 4),
        (r"\bcommand(?:s)?\b", 3),
        (r"\bconfiguration\b", 4),
        (r"\bconfig\b", 3),
        (r"\boption(?:s)?\b", 4),
        (r"\bparameter(?:s)?\b", 4),
        (r"\benvironment variable(?:s)?\b", 5),
        (r"\bschema\b", 5),
        (r"\berror code(?:s)?\b", 5),
        (r"\bfield(?:s)?\b", 3),
    ],
    "explanation": [
        (r"\boverview\b", 4),
        (r"\bconcept(?:s)?\b", 5),
        (r"\barchitecture\b", 5),
        (r"\bbackground\b", 5),
        (r"^\s*why\b", 6),
        (r"\bunderstanding\b", 6),
        (r"\bdesign\b", 4),
        (r"\brationale\b", 5),
        (r"\bmental model\b", 5),
        (r"\btrade-?off(?:s)?\b", 5),
    ],
}

BODY_PATTERNS = {
    "tutorial": [
        (r"\bin this tutorial\b", 6),
        (r"\bwe will\b", 3),
        (r"\blet['’]s\b", 2),
        (r"\byou should see\b", 4),
        (r"\bexpected output\b", 3),
        (r"\bnotice that\b", 4),
        (r"\bnow (?:run|create|open|add|start|build)\b", 2),
        (r"\bif you do not see\b", 3),
    ],
    "how-to": [
        (r"\bthis guide shows (?:you )?how to\b", 6),
        (r"\bbefore you begin\b", 4),
        (r"\bprerequisite(?:s)?\b", 2),
        (r"\bto (?:configure|install|deploy|migrate|upgrade|create|delete|enable|disable|set|rotate|troubleshoot)\b", 3),
        (r"\bif .{0,80},? then\b", 3),
        (r"\bverify (?:that|the|your)\b", 3),
        (r"\btroubleshoot(?:ing)?\b", 3),
        (r"\brollback\b", 2),
        (r"\bwhen (?:you need|to use|using)\b", 2),
    ],
    "reference": [
        (r"\bparameter(?:s)?\b", 3),
        (r"\boption(?:s)?\b", 3),
        (r"\bdefault(?:s)?\b", 3),
        (r"\brequired\b", 2),
        (r"\breturn(?:s|ed)?\b", 3),
        (r"\braises\b", 3),
        (r"\berror(?:s)?\b", 2),
        (r"\btype\b", 2),
        (r"\bschema\b", 3),
        (r"\bendpoint(?:s)?\b", 3),
        (r"\bfield(?:s)?\b", 2),
        (r"\bsubcommand(?:s)?\b", 3),
    ],
    "explanation": [
        (r"\bbecause\b", 2),
        (r"\bwhy\b", 3),
        (r"\brationale\b", 4),
        (r"\btrade-?off(?:s)?\b", 4),
        (r"\bconcept(?:s|ual)?\b", 3),
        (r"\bbackground\b", 4),
        (r"\barchitecture\b", 4),
        (r"\bhistorically\b", 3),
        (r"\balternative(?:s)?\b", 2),
        (r"\bmental model\b", 4),
        (r"\bdesign decision(?:s)?\b", 4),
        (r"\bunderstand(?:ing)?\b", 2),
    ],
}

HEADING_PATTERNS = {
    "tutorial": [r"what we['’]?ll build", r"next steps", r"check your work"],
    "how-to": [r"before you begin", r"verify", r"troubleshooting", r"rollback"],
    "reference": [r"parameters", r"options", r"returns", r"errors", r"fields", r"schema", r"defaults", r"examples"],
    "explanation": [r"background", r"why", r"architecture", r"trade-?offs", r"concepts", r"mental model", r"design"],
}

@dataclass
class AuditResult:
    path: str
    title: str
    mode: str
    confidence: float
    secondary_mode: str | None
    scores: dict[str, int]
    flags: list[str]
    suggestions: list[str]


def iter_docs(paths: list[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in DOC_EXTENSIONS:
                yield path
            continue
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_dir():
                    continue
                if child.suffix.lower() not in DOC_EXTENSIONS:
                    continue
                if any(part in IGNORE_DIRS for part in child.parts):
                    continue
                yield child


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def strip_code_blocks(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def extract_title(path: Path, text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^\s*#\s+(.+?)\s*$", line)
        if match:
            return re.sub(r"[`*_{}\[\]()#]", "", match.group(1)).strip()
    # reStructuredText title: line followed by === or ---
    lines = text.splitlines()
    for i in range(len(lines) - 1):
        if lines[i].strip() and re.match(r"^[=\-~^#*]{3,}\s*$", lines[i + 1].strip()):
            return lines[i].strip()
    return path.stem.replace("-", " ").replace("_", " ").strip().title()


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if m:
            headings.append(m.group(1).strip().lower())
    return headings


def count_pattern(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def longest_list_run(lines: list[str]) -> int:
    longest = 0
    current = 0
    for line in lines:
        if re.match(r"^\s*(?:[-*+] |\d+[.)] )", line):
            current += 1
            longest = max(longest, current)
        elif line.strip() == "":
            continue
        else:
            current = 0
    return longest


def compute_scores(title: str, text: str) -> dict[str, int]:
    body = strip_code_blocks(text)
    lower_title = title.lower()
    headings = extract_headings(text)
    scores = {mode: 0 for mode in MODES}

    for mode, patterns in TITLE_PATTERNS.items():
        for pattern, weight in patterns:
            if re.search(pattern, lower_title, flags=re.IGNORECASE):
                scores[mode] += weight

    for mode, patterns in BODY_PATTERNS.items():
        for pattern, weight in patterns:
            hits = count_pattern(pattern, body)
            scores[mode] += min(hits, 5) * weight

    for mode, patterns in HEADING_PATTERNS.items():
        for heading in headings:
            for pattern in patterns:
                if re.search(pattern, heading, flags=re.IGNORECASE):
                    scores[mode] += 3

    lines = text.splitlines()
    ordered_steps = sum(1 for line in lines if re.match(r"^\s*\d+[.)]\s+", line))
    bullet_items = sum(1 for line in lines if re.match(r"^\s*[-*+]\s+", line))
    table_lines = sum(1 for line in lines if line.strip().startswith("|") and line.strip().endswith("|"))
    code_blocks = len(re.findall(r"```", text)) // 2
    frontmatterish = count_pattern(r"^\s*[a-zA-Z0-9_.-]+:\s+", body)

    if ordered_steps:
        scores["how-to"] += min(ordered_steps, 8) * 2
        scores["tutorial"] += min(ordered_steps, 8)
    if code_blocks:
        scores["tutorial"] += min(code_blocks, 5)
        scores["how-to"] += min(code_blocks, 5)
        scores["reference"] += min(code_blocks, 5)
    if table_lines:
        scores["reference"] += min(table_lines, 12)
    if frontmatterish:
        scores["reference"] += min(frontmatterish, 6)

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    long_paragraphs = sum(1 for p in paragraphs if len(p.split()) >= 80)
    if long_paragraphs:
        scores["explanation"] += min(long_paragraphs, 5) * 2

    if bullet_items > 12 and table_lines == 0:
        scores["reference"] += 2
        scores["explanation"] += 1

    return scores


def classify(scores: dict[str, int]) -> tuple[str, float, str | None]:
    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_mode, top_score = ordered[0]
    second_mode, second_score = ordered[1]

    if top_score <= 2:
        return "unknown", 0.0, None

    # Mixed if strong competing modes are close.
    if second_score >= 6 and second_score >= top_score * 0.72:
        mode = f"mixed: {top_mode} + {second_mode}"
    else:
        mode = top_mode

    confidence = (top_score - second_score) / max(top_score, 1)
    confidence = max(0.0, min(1.0, confidence))
    return mode, round(confidence, 2), second_mode if second_score > 0 else None


def make_flags(title: str, text: str, scores: dict[str, int], mode: str) -> list[str]:
    flags: list[str] = []
    lower_title = title.lower()
    body = strip_code_blocks(text)
    lines = text.splitlines()
    ordered_steps = sum(1 for line in lines if re.match(r"^\s*\d+[.)]\s+", line))
    table_lines = sum(1 for line in lines if line.strip().startswith("|") and line.strip().endswith("|"))
    code_blocks = len(re.findall(r"```", text)) // 2
    long_run = longest_list_run(lines)
    primary = mode.split(":", 1)[0] if mode.startswith("mixed") else mode

    if mode.startswith("mixed"):
        flags.append("Mixed-mode signals are strong; consider splitting or choosing one primary user need.")

    if "tutorial" in lower_title and primary not in {"tutorial", "mixed"}:
        flags.append("Title says tutorial, but content signals another mode.")
    if re.search(r"^\s*how\s+to\b", lower_title) and primary != "how-to":
        flags.append("Title says how-to, but content may not be a task guide.")
    if "reference" in lower_title and primary != "reference":
        flags.append("Title says reference, but content signals another mode.")
    if re.search(r"\b(overview|concept|architecture|background|why)\b", lower_title) and primary in {"tutorial", "how-to", "reference"}:
        flags.append("Title has explanation signals; verify the page is not hiding conceptual material.")

    if primary == "tutorial":
        if scores["explanation"] >= 8 or re.search(r"^\s*#+\s+(background|concepts|architecture|why)\b", body, re.I | re.M):
            flags.append("Tutorial may contain too much explanation; shrink and link to explanation.")
        if count_pattern(r"\b(alternative|choose|option|if you prefer|you can also)\b", body) >= 3:
            flags.append("Tutorial appears to offer choices or alternatives; keep one safe path.")
        if not re.search(r"\b(you should see|expected output|notice that|check that)\b", body, re.I):
            flags.append("Tutorial may need expected outputs or observable checks.")
    elif primary == "how-to":
        if table_lines >= 6 or scores["reference"] >= scores["how-to"] * 0.8:
            flags.append("How-to guide may contain reference material; move full facts to reference.")
        if scores["explanation"] >= scores["how-to"] * 0.7:
            flags.append("How-to guide may contain conceptual background; shrink and link to explanation.")
        if not re.search(r"\b(before you begin|prerequisite|verify|check|confirm)\b", body, re.I):
            flags.append("How-to guide may need prerequisites and verification.")
    elif primary == "reference":
        if ordered_steps >= 3:
            flags.append("Reference includes several ordered steps; move procedures to how-to guides.")
        if scores["explanation"] >= scores["reference"] * 0.75:
            flags.append("Reference may contain explanation; move rationale or background out.")
        if count_pattern(r"\b(default|required|returns|errors|parameters|options|fields)\b", body) < 2:
            flags.append("Reference may be missing standard factual fields such as defaults, parameters, returns, or errors.")
    elif primary == "explanation":
        if ordered_steps >= 3 or code_blocks >= 4:
            flags.append("Explanation may contain a procedure; move task steps to a how-to guide.")
        if table_lines >= 8 or scores["reference"] >= scores["explanation"] * 0.75:
            flags.append("Explanation may contain reference material; move exact facts to reference.")
        if not re.search(r"\b(because|why|trade-?off|rationale|design|concept|background|understand)\b", body, re.I):
            flags.append("Explanation may need a clearer why/context/mental-model focus.")

    if long_run > 7:
        flags.append(f"Long list detected ({long_run} items); consider grouping for scanability.")

    return flags


def make_suggestions(mode: str, flags: list[str]) -> list[str]:
    suggestions: list[str] = []
    primary = mode.split(":", 1)[0] if mode.startswith("mixed") else mode

    if mode.startswith("mixed"):
        suggestions.append("Use the compass to decide whether the page serves study or work, then split secondary material into the appropriate mode.")
    elif primary == "tutorial":
        suggestions.append("Test the tutorial from a clean environment and add expected outputs after key actions.")
        suggestions.append("Move optional paths and long explanations out of the lesson.")
    elif primary == "how-to":
        suggestions.append("Make the title and opening paragraph name the real-world task.")
        suggestions.append("Move full option lists to reference and keep only task-critical details here.")
    elif primary == "reference":
        suggestions.append("Verify facts against the source of truth and standardize entry structure.")
        suggestions.append("Move procedures and rationale out to how-to guides or explanation.")
    elif primary == "explanation":
        suggestions.append("Frame the page around a bounded why/context question.")
        suggestions.append("Move procedures to how-to guides and exact facts to reference.")
    else:
        suggestions.append("Clarify the intended user need and rewrite the title/intro to match one Diátaxis mode.")

    # Add targeted suggestion for each prominent flag.
    for flag in flags:
        if "expected outputs" in flag:
            suggestions.append("Add 'You should see...' or equivalent checks after commands or UI actions.")
        if "Long list" in flag:
            suggestions.append("Split the list into named groups or create a mechanical index.")
        if "prerequisites" in flag:
            suggestions.append("Add 'Before you begin' and 'Verify the result' sections.")

    # Deduplicate while preserving order.
    deduped: list[str] = []
    for suggestion in suggestions:
        if suggestion not in deduped:
            deduped.append(suggestion)
    return deduped[:5]


def audit_file(path: Path, root: Path | None = None) -> AuditResult:
    text = read_text(path)
    title = extract_title(path, text)
    scores = compute_scores(title, text)
    mode, confidence, secondary = classify(scores)
    flags = make_flags(title, text, scores, mode)
    suggestions = make_suggestions(mode, flags)
    display_path = str(path if root is None else path.relative_to(root))
    return AuditResult(
        path=display_path,
        title=title,
        mode=mode,
        confidence=confidence,
        secondary_mode=secondary,
        scores=scores,
        flags=flags,
        suggestions=suggestions,
    )


def markdown_report(results: list[AuditResult]) -> str:
    lines: list[str] = []
    lines.append("# Diátaxis audit")
    lines.append("")
    lines.append(f"Scanned {len(results)} file{'s' if len(results) != 1 else ''}.")
    lines.append("")
    lines.append("| File | Title | Likely mode | Confidence | Secondary | Flags |")
    lines.append("|---|---|---:|---:|---|---|")
    for result in results:
        flags = "<br>".join(escape_md(flag) for flag in result.flags) if result.flags else ""
        secondary = result.secondary_mode or ""
        lines.append(
            f"| `{escape_md(result.path)}` | {escape_md(result.title)} | {escape_md(result.mode)} | {result.confidence:.2f} | {escape_md(secondary)} | {flags} |"
        )
    lines.append("")

    flagged = [result for result in results if result.flags]
    if flagged:
        lines.append("## Suggested next actions")
        lines.append("")
        for result in flagged:
            lines.append(f"### `{result.path}`")
            lines.append("")
            lines.append(f"Likely mode: **{result.mode}**")
            lines.append("")
            lines.append("Flags:")
            for flag in result.flags:
                lines.append(f"- {flag}")
            lines.append("")
            lines.append("Suggestions:")
            for suggestion in result.suggestions:
                lines.append(f"- {suggestion}")
            lines.append("")

    return "\n".join(lines)


def escape_md(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Markdown-like docs for Diátaxis mode signals.")
    parser.add_argument("paths", nargs="+", help="Files or directories to audit")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="Output format")
    parser.add_argument("--max-files", type=int, default=500, help="Maximum number of files to scan")
    args = parser.parse_args(argv)

    input_paths = [Path(p).resolve() for p in args.paths]
    existing = [p for p in input_paths if p.exists()]
    missing = [str(p) for p in input_paths if not p.exists()]
    if missing:
        print(f"Missing path(s): {', '.join(missing)}", file=sys.stderr)
        return 2
    if not existing:
        print("No input paths found.", file=sys.stderr)
        return 2

    common_root = None
    dirs = [p if p.is_dir() else p.parent for p in existing]
    try:
        common_root = Path(__import__("os").path.commonpath([str(d) for d in dirs]))
    except ValueError:
        common_root = None

    files = list(iter_docs(existing))[: args.max_files]
    results = [audit_file(path, common_root) for path in sorted(files)]

    if args.format == "json":
        print(json.dumps([asdict(result) for result in results], indent=2, ensure_ascii=False))
    else:
        print(markdown_report(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
