# Diátaxis Documentation Skill

A cross-compatible Agent Skill for applying the Diátaxis framework to technical documentation authoring, review, auditing, and migration.

## What it helps with

Use this skill to:

- classify docs as tutorials, how-to guides, reference, or explanation
- write new docs in the correct mode
- rewrite mixed-mode pages
- audit a docs tree for Diátaxis boundary problems
- design user-first documentation architecture
- migrate an existing documentation set iteratively
- review docs pull requests

## Compatibility

This package uses the common Agent Skills layout:

```text
diataxis-documentation/
  SKILL.md
  references/
  assets/
  scripts/
```

It follows the [Agent Skills standard](https://agentskills.io/specification). The `SKILL.md` frontmatter uses only standard fields:

```yaml
name: diataxis-documentation
description: ...
license: CC-BY-SA-4.0
compatibility: ...
```

The skill name is lowercase kebab-case and avoids vendor-reserved words, so it is suitable for Claude Code, Codex, and Pi skill discovery. Pi validates against the same standard and ignores any unknown frontmatter, so the package loads cleanly in all three.

## Install

The quickest way to install from GitHub is to clone this repo directly into your
agent's skills directory. Replace `your-username` with the account that hosts the repo.

Claude Code:

```bash
git clone https://github.com/your-username/diataxis-documentation.git \
  ~/.claude/skills/diataxis-documentation
```

Codex:

```bash
git clone https://github.com/your-username/diataxis-documentation.git \
  ~/.agents/skills/diataxis-documentation
```

Pi:

```bash
git clone https://github.com/your-username/diataxis-documentation.git \
  ~/.pi/agent/skills/diataxis-documentation
```

To update later, `cd` into that directory and run `git pull`.

The manual copy steps below are equivalent if you prefer to download the files yourself.

### Claude Code

Personal skill:

```bash
mkdir -p ~/.claude/skills
cp -R diataxis-documentation ~/.claude/skills/
```

Project skill:

```bash
mkdir -p .claude/skills
cp -R diataxis-documentation .claude/skills/
```

### Codex

Personal skill:

```bash
mkdir -p ~/.agents/skills
cp -R diataxis-documentation ~/.agents/skills/
```

Project skill:

```bash
mkdir -p .agents/skills
cp -R diataxis-documentation .agents/skills/
```

### Pi

Personal skill:

```bash
mkdir -p ~/.pi/agent/skills
cp -R diataxis-documentation ~/.pi/agent/skills/
```

Pi also reads `~/.agents/skills/`, so a Codex personal install is picked up automatically.

Project skill (loads after the project is trusted):

```bash
mkdir -p .pi/skills
cp -R diataxis-documentation .pi/skills/
```

Alternatively, point Pi at an existing skills directory without copying by adding it to `~/.pi/settings.json` (or project `.pi/settings.json`):

```json
{
  "skills": ["~/.claude/skills"]
}
```

Once discovered, invoke the skill on demand or force it with `/skill:diataxis-documentation`. Append arguments to run it directly, for example `/skill:diataxis-documentation audit docs/`.

If your agent does not pick up changes immediately, restart the agent session.

## Suggested invocations

```text
Use the diataxis-documentation skill to audit docs/ and recommend the first five improvements.
```

```text
Use $diataxis-documentation to rewrite this page as a how-to guide and move explanation/reference material into separate stubs.
```

```text
Use the Diátaxis skill to create a tutorial for a new developer's first successful API call.
```

```text
Classify these documentation pages with Diátaxis and explain which ones are mixed-mode.
```

## Files

- `SKILL.md` - core instructions loaded by the agent.
- `references/principles.md` - detailed framework guidance.
- `references/workflows.md` - common documentation workflows.
- `references/checklists.md` - audit and review checklists.
- `references/style-guide.md` - titles, phrasing, examples, and cross-linking patterns.
- `references/information-architecture.md` - site structure, landing pages, and complex hierarchies.
- `references/migration-playbook.md` - staged migration approach.
- `assets/templates/` - starter templates for each documentation mode.
- `scripts/diataxis_audit.py` - heuristic repository audit script.
- `scripts/diataxis_scaffold.py` - creates a single new page from a template.

## Optional scripts

The scripts use only the Python standard library and do not access the network.

Audit a docs directory:

```bash
python diataxis-documentation/scripts/diataxis_audit.py docs/ --format markdown
```

Create a new page from a template:

```bash
python diataxis-documentation/scripts/diataxis_scaffold.py how-to "How to rotate API keys" --out-dir docs/how-to
```

## Attribution

This skill is an original operationalization and paraphrased summary of Diátaxis, based on the Diátaxis framework by Daniele Procida and the PDF supplied by the user. Diátaxis is published at https://diataxis.fr/ and the public source repository states a CC-BY-SA 4.0 license.

This package is not affiliated with or endorsed by Daniele Procida.
