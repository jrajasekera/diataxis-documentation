# Diátaxis Documentation Skill

A cross-compatible [Agent Skill](https://agentskills.io/specification) that teaches an agent to apply the [Diátaxis](https://diataxis.fr/) framework — tutorial, how-to, reference, explanation — when authoring, reviewing, auditing, or migrating technical documentation.

This README is itself arranged with Diátaxis. Jump to the part that matches what you need right now:

| If you want to… | Go to | Diátaxis mode |
|---|---|---|
| understand what the skill is and why it works this way | [Understand the skill](#understand-the-skill) | Explanation |
| follow a guided first success | [Tutorial: audit your first docs set](#tutorial-audit-your-first-docs-set) | Tutorial |
| install it or carry out a specific task | [How-to guides](#how-to-guides) | How-to |
| look up files, fields, paths, or script options | [Reference](#reference) | Reference |

## Understand the skill

### What it is

This repository is not an application. It is a packaged Agent Skill: instructional Markdown plus two optional Python helper scripts. When loaded, it gives an agent a working command of Diátaxis so it can organize documentation by *user need* rather than by the author's mental model of the product.

### What it helps you do

Once the skill is loaded, you can ask the agent to:

- classify pages as tutorial, how-to, reference, or explanation
- write a new page in the correct mode
- rewrite a mixed-mode page and split out the parts that belong elsewhere
- audit a docs tree for Diátaxis boundary problems
- design user-first documentation architecture
- migrate an existing documentation set in small, reviewable steps
- review a documentation pull request

### Why it is vendor-neutral

The package uses only the common Agent Skills shape — `SKILL.md` plus optional `references/`, `assets/`, and `scripts/` — and only standard frontmatter fields. The skill name is lowercase kebab-case and avoids vendor-reserved words. As a result it loads cleanly in Claude Code, Codex, and Pi: each runtime discovers it the same way and ignores any frontmatter it does not recognize. See [Installation paths by agent](#installation-paths-by-agent) for where each runtime looks.

### How it is organized

The skill follows *progressive disclosure* — the agent reads the smallest thing first and goes deeper only when a task needs it:

- `SKILL.md` carries the concise core instructions and is always loaded.
- `references/` holds depth-on-demand: the full model, workflows, checklists, a style guide, information architecture, and a migration playbook.
- `assets/templates/` provides starter pages, one per mode plus landing-page, audit-report, and doc-index.
- `scripts/` adds optional, repository-scale helpers.

For the exact file list, see [Bundled files](#bundled-files).

## Tutorial: audit your first docs set

This short lesson gives you one guaranteed success with the skill's auditor. You will install the skill, run the heuristic audit script against its own reference files, and read a Diátaxis classification report. All you need beforehand is Python 3 and Git.

We will use the Claude Code location for this lesson; the other runtimes work the same way.

1. Clone the skill into your skills directory:

   ```bash
   git clone https://github.com/jrajasekera/diataxis-documentation.git \
     ~/.claude/skills/diataxis-documentation
   ```

2. Move into the freshly cloned skill:

   ```bash
   cd ~/.claude/skills/diataxis-documentation
   ```

3. Run the auditor against the skill's own `references/` folder:

   ```bash
   python3 scripts/diataxis_audit.py references/ --format markdown
   ```

4. Read the report. It begins like this:

   ```text
   # Diátaxis audit

   Scanned 6 files.

   | File | Title | Likely mode | Confidence | Secondary | Flags |
   |---|---|---:|---:|---|---|
   | `checklists.md` | Diátaxis checklists and rubrics | explanation | 0.33 | reference | … |
   ```

   followed by a **Suggested next actions** section with one entry per file.

**Checkpoint.** You should see a table with one row per reference file, most of them classified as `explanation`, plus flags such as “Long list detected.” If you see that table, the skill is installed and its scripts run.

You have now completed a full audit pass. Notice that the classifications are deliberate *signals to verify*, not verdicts — which is exactly how the skill teaches the agent to treat them.

Where to go next:

- To audit your own documentation, see [Audit a documentation tree](#audit-a-documentation-tree).
- To ask the agent to act on what an audit finds, see [Invoke the skill in a session](#invoke-the-skill-in-a-session).

## How-to guides

Practical directions for someone who already knows what they want to do.

### Install the skill

Clone the repository into your agent's personal skills directory. For Claude Code:

```bash
git clone https://github.com/jrajasekera/diataxis-documentation.git \
  ~/.claude/skills/diataxis-documentation
```

For Codex or Pi, change only the target directory — see [Installation paths by agent](#installation-paths-by-agent) for every personal and project path. If you would rather not use Git, download the files and copy the `diataxis-documentation/` folder into the same directory.

To register the skill with Pi *without* copying it, point Pi at an existing skills directory in `~/.pi/settings.json` (or a project `.pi/settings.json`):

```json
{
  "skills": ["~/.claude/skills"]
}
```

If your agent does not pick up the new skill, restart the agent session.

### Update an installed skill

If you installed with Git, pull the latest version from inside the skill directory:

```bash
cd ~/.claude/skills/diataxis-documentation
git pull
```

### Invoke the skill in a session

Ask for the skill by name and state the documentation task. In Pi you can also force it with `/skill:diataxis-documentation` and pass arguments directly, for example `/skill:diataxis-documentation audit docs/`.

Example prompts:

```text
Use the diataxis-documentation skill to audit docs/ and recommend the first five improvements.
```

```text
Use diataxis-documentation to rewrite this page as a how-to guide and move the explanation and reference material into separate stubs.
```

```text
Use the Diátaxis skill to create a tutorial for a new developer's first successful API call.
```

### Audit a documentation tree

Run the auditor against any docs path. It reads Markdown-like files and prints Diátaxis mode signals:

```bash
python3 scripts/diataxis_audit.py docs/ --format markdown
```

Use `--format json` for machine-readable output, or `--max-files N` to cap how many files are scanned. For the full argument list, see [`diataxis_audit.py`](#diataxis_auditpy).

### Scaffold a new page from a template

Create a single page from a bundled template:

```bash
python3 scripts/diataxis_scaffold.py how-to "How to rotate API keys" --out-dir docs/how-to
```

The first argument is the template type. The script deliberately refuses to create four empty mode sections, in keeping with the framework. For every type and option, see [`diataxis_scaffold.py`](#diataxis_scaffoldpy).

## Reference

Authoritative facts about the package and its scripts.

### Package layout

```text
diataxis-documentation/
  SKILL.md            core instructions, always loaded
  references/         depth-on-demand guidance
  assets/templates/   starter pages, one per mode plus landing pages
  scripts/            optional Python helpers
```

### SKILL.md frontmatter fields

`SKILL.md` uses only standard Agent Skills fields:

| Field | Value or purpose |
|---|---|
| `name` | Skill identifier; lowercase kebab-case (`diataxis-documentation`). |
| `description` | One-line summary used for skill discovery. |
| `license` | `CC-BY-SA-4.0`. |
| `compatibility` | Notes that the core skill needs no special environment and the scripts require Python 3, standard library only. |
| `metadata` | Holds `source: https://diataxis.fr/`. |

No vendor-specific keys are used, so the same file loads in all three runtimes.

### Installation paths by agent

| Agent | Personal skills directory | Project skills directory |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Pi | `~/.pi/agent/skills/` | `.pi/skills/` (loads after the project is trusted) |

Pi also reads `~/.agents/skills/`, so a Codex personal install is picked up automatically.

### Bundled files

The distributable file set is listed in `manifest.txt`:

- `SKILL.md` — core instructions loaded by the agent.
- `references/principles.md` — the full framework, modes, boundaries, and anti-patterns.
- `references/workflows.md` — workflows for creating, reviewing, refactoring, and testing docs.
- `references/checklists.md` — audit checklists, rubrics, and mode-purity checks.
- `references/style-guide.md` — titles, phrasing, examples, and cross-linking patterns.
- `references/information-architecture.md` — navigation, landing pages, and complex hierarchies.
- `references/migration-playbook.md` — a staged migration approach.
- `assets/templates/` — starter templates for each mode plus landing-page, audit-report, and doc-index.
- `scripts/diataxis_audit.py` — heuristic repository audit script.
- `scripts/diataxis_scaffold.py` — creates one new page from a template.
- `LICENSE.md`, `NOTICE.md`, `SECURITY.md` — license, attribution, and security policy.

Both scripts use the Python standard library only and make no network calls.

### `diataxis_audit.py`

Classify Markdown-like docs by Diátaxis mode signals. The classification is a triage aid, not an authority.

```text
python3 scripts/diataxis_audit.py PATHS [PATHS ...] [--format {markdown,json}] [--max-files N]
```

| Argument | Description |
|---|---|
| `PATHS` | One or more files or directories to audit. |
| `--format {markdown,json}` | Output format. Defaults to `markdown`. |
| `--max-files N` | Maximum number of files to scan. |

### `diataxis_scaffold.py`

Create one Diátaxis page from a bundled template.

```text
python3 scripts/diataxis_scaffold.py TYPE "Title" [--out-dir DIR] [--filename NAME] [--force]
```

| Argument | Description |
|---|---|
| `TYPE` | One of `tutorial`, `how-to`, `reference`, `explanation`, `landing-page`, `audit-report`, `doc-index`. |
| `Title` | Page title. |
| `--out-dir DIR` | Output directory. |
| `--filename NAME` | Output filename. Defaults to a slugified title with `.md`. |
| `--force` | Overwrite an existing file. |

## License and attribution

This skill is an original operationalization and paraphrased summary of Diátaxis, based on the framework by Daniele Procida (published at <https://diataxis.fr/>). It is licensed under [CC-BY-SA-4.0](LICENSE.md); attribution details are in [`NOTICE.md`](NOTICE.md).

This package is not affiliated with or endorsed by Daniele Procida.
