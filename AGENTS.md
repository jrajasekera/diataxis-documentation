# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## What this repository is

This is **not an application** — it is a packaged **Agent Skill** that teaches an agent to apply the [Diátaxis](https://diataxis.fr/) framework (tutorial / how-to / reference / explanation) to technical documentation. The deliverable is the skill package itself: instructional Markdown plus two optional Python helper scripts. There is no build step, no test suite, and no lint configuration.

The package targets the cross-vendor [Agent Skills standard](https://agentskills.io/specification) and must load cleanly in **Codex, Codex, and Pi**. That cross-compatibility goal drives most of the constraints below.

## Architecture

The package is built around **progressive disclosure** — the agent loads the smallest thing first and reads deeper files only when a task needs them:

- `SKILL.md` — the entry point. Frontmatter + concise core instructions, always loaded. Keep it short; push detail down into `references/`.
- `references/*.md` — depth-on-demand. `principles.md` (full model), `workflows.md` (classify/review/refactor flows), `checklists.md` (audit rubrics), `style-guide.md`, `information-architecture.md`, `migration-playbook.md`. `SKILL.md` links to these by name; keep those pointers in sync when adding/renaming.
- `assets/templates/*.md` — starter pages, one per mode plus `landing-page.md`, `audit-report.md`, `doc-index.md`. Consumed by name in `scripts/diataxis_scaffold.py` (`TEMPLATE_FILES`).
- `scripts/` — optional repository-scale helpers (see below).
- `manifest.txt` — the explicit list of distributable files. It is **not auto-generated**; update it by hand whenever you add, remove, or rename a shipped file, or the package will be distributed incomplete.

## Helper scripts

Both scripts are **Python 3 standard library only** and perform **no network access** — this is a stated compatibility guarantee, so do not add third-party imports or network calls.

```bash
# Heuristic audit: classify docs as tutorial/how-to/reference/explanation/mixed
python3 scripts/diataxis_audit.py <docs-path> --format markdown   # or: --format json
python3 scripts/diataxis_audit.py <docs-path> --max-files 500

# Scaffold a single page from a bundled template (refuses to create four empty sections)
python3 scripts/diataxis_scaffold.py <type> "<title>" --out-dir <dir>
# <type> is one of: tutorial how-to reference explanation landing-page audit-report doc-index
```

`diataxis_audit.py` is keyword/heuristic scoring (`TITLE_PATTERNS`, `BODY_PATTERNS`, `HEADING_PATTERNS` → `compute_scores` → `classify`). It is a **triage aid, not an authority** — treat its mode labels and flags as signals to verify, not verdicts. `diataxis_scaffold.py` locates templates relative to its own path (`skill_root()`), so it works regardless of the caller's working directory.

There are no automated tests; verify script changes by running them against `references/` or `assets/templates/` and inspecting the output.

## Conventions and hard constraints

- **Standard frontmatter only.** `SKILL.md` frontmatter must stick to standard fields (`name`, `description`, `license`, `compatibility`, `metadata`). Do not add vendor-specific keys — unknown fields can break or get ignored across the three target agents.
- **Skill name is lowercase kebab-case** (`diataxis-documentation`) and avoids vendor-reserved words. Keep it that way for discovery in all three runtimes.
- **License is CC-BY-SA-4.0** (share-alike). This is a derivative/operationalization of Diátaxis by Daniele Procida; preserve attribution in `NOTICE.md` and `README.md`. Do not bundle the upstream source PDF.
- **The content embodies its own rules.** When editing the instructional Markdown, follow the Diátaxis discipline the skill itself prescribes (the "Hard rules" section of `SKILL.md`): don't mix modes, don't bury reference facts in explanation, etc.

## When editing this skill

Changes to instructions usually touch several files together: a behavior change in `SKILL.md` often needs a matching update in the relevant `references/` file, possibly a template, and an entry in `manifest.txt` if files were added or removed. Prefer the smallest coherent change and keep the three layers (core → references → templates) internally consistent.
