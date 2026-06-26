---
name: diataxis-documentation
description: Apply the Diataxis framework to plan, write, review, restructure, or audit technical documentation; classify content as tutorials, how-to guides, reference, or explanation; maintain clear boundaries between documentation modes.
license: CC-BY-SA-4.0
compatibility: Core skill needs no special environment. Optional helper scripts in scripts/ require Python 3 (standard library only, no network access).
metadata:
  source: https://diataxis.fr/
---

# Diátaxis Documentation

Use this skill when the user asks you to create, revise, audit, classify, migrate, or organize technical documentation using Diátaxis. It is suitable for software documentation, API docs, CLI docs, product docs, internal engineering docs, scientific software docs, and any documentation for a craft or tool.

This skill is intentionally vendor-neutral: it follows the [Agent Skills standard](https://agentskills.io/specification) and uses only the common package shape (`SKILL.md`, optional `references/`, optional `assets/`, optional `scripts/`) so it can run in Claude Code, Codex, and Pi. In Pi it can also be invoked directly with `/skill:diataxis-documentation` (optionally with arguments, e.g. `/skill:diataxis-documentation audit docs/`).

## Core model

Diátaxis organizes documentation by the user's need, not by the author's mental model of the product.

Ask two questions:

1. Does the content inform **action** or **cognition**?
2. Does it serve **acquisition** of skill or **application** of skill?

Use the compass:

| User need | Content informs | User is | Documentation type |
|---|---|---|---|
| Learning | Action | Acquiring skill | Tutorial |
| Goal | Action | Applying skill | How-to guide |
| Information | Cognition | Applying skill | Reference |
| Understanding | Cognition | Acquiring skill | Explanation |

## Always preserve mode boundaries

When writing or editing documentation:

- **Tutorials** are lessons. They guide a learner through a safe, successful learning experience. They are practical, concrete, reliable, and deliberately narrow.
- **How-to guides** are directions for already-competent users at work. They help the user accomplish a real-world task or solve a real-world problem.
- **Reference** is authoritative technical description. It is neutral, factual, structured like the thing it describes, and consulted rather than read.
- **Explanation** is reflective discussion. It provides context, reasons, background, design rationale, trade-offs, and conceptual understanding.

If a document mixes modes, do not simply smooth over the mixture. Identify the competing user needs, split or move the material, and add cross-links.

## Default workflow

1. **Identify the user's situation.** Are they learning, doing a task, checking facts while working, or seeking understanding?
2. **Choose one primary mode.** A page may link to other modes, but it should not try to satisfy all needs at once.
3. **Apply the matching standard.** Use the short guidance below, and read the relevant reference file when the task is substantial.
4. **Make the smallest useful improvement.** Prefer one publishable improvement over a large speculative reorganization, unless the user explicitly asks for a full migration plan.
5. **Check mode purity.** Remove or move teaching, task steps, reference facts, or conceptual discussion that belong elsewhere.

## Short guidance by mode

### Tutorial

Use when the reader needs a learning experience.

- Start by saying what the learner will make, do, or experience.
- Lead with concrete steps and visible results.
- Use a reliable, controlled path with no choices unless unavoidable.
- Give expected outputs and checks so the learner knows they are on track.
- Keep explanation minimal and link to explanation pages instead.
- Prefer “we will build/create/do...” over promises like “you will learn...”.

### How-to guide

Use when the reader already knows the domain and wants to get work done.

- Title it as a task, often “How to ...”.
- Focus on a real user goal or problem, not a product feature tour.
- Give a logical sequence of actions, including conditional branches where real-world cases vary.
- Omit teaching, background, broad explanation, and exhaustive option lists; link out instead.
- Assume competence, but warn about risks and prerequisites that affect the task.

### Reference

Use when the reader needs exact information while working.

- Describe only: commands, APIs, options, parameters, return values, errors, schemas, configuration keys, limits, guarantees, defaults.
- Mirror the structure of the product, API, CLI, protocol, or system.
- Use standard, repeatable patterns.
- Be accurate, complete, neutral, and concise.
- Include examples only as compact illustrations, not as lessons or task walkthroughs.

### Explanation

Use when the reader wants to understand a topic.

- Answer “why?”, “what does this mean?”, “how should I think about this?”, and “what trade-offs exist?”.
- Make connections across concepts, history, design decisions, alternatives, and implications.
- Admit perspective and judgement where it helps understanding.
- Keep the topic bounded; move procedures to how-to guides and facts to reference.

## Progressive disclosure references

Read these files when the task needs more depth:

- `references/principles.md` - full Diátaxis model, four modes, boundaries, and anti-patterns.
- `references/workflows.md` - workflows for creating, reviewing, refactoring, and testing docs.
- `references/checklists.md` - audit checklists, rubrics, and mode-purity checks.
- `references/style-guide.md` - language, titles, examples, cross-linking, and editing patterns.
- `references/information-architecture.md` - navigation, landing pages, complex hierarchies, and user-first structure.
- `references/migration-playbook.md` - practical migration plan for existing docs sets.

Templates are in `assets/templates/`. Use them as starting points, not as rigid forms.

Scripts are in `scripts/` and are optional. Use them only when they help with repository-scale work. They use Python standard library only and do not access the network.

## Repository workflow

When working in a code repository:

1. Inspect the docs tree and any existing documentation conventions.
2. Do not invent product facts. For reference material, verify against source code, schemas, CLI output, tests, generated API docs, or user-provided sources.
3. For audits, optionally run `python scripts/diataxis_audit.py <docs-path>` from this skill directory or copy the script into a temporary workspace.
4. Propose or make small, reviewable changes unless asked for a larger restructuring.
5. Preserve project style, file naming, build tooling, and link conventions.

## Output expectations

For classification or audits, report:

- current mode and intended user need
- evidence for the classification
- boundary problems or mixed-mode risks
- recommended target mode
- smallest useful next change

For new or rewritten documentation, include:

- a title appropriate to the mode
- assumptions about the reader and prerequisites
- the content itself
- cross-links or placeholders for related modes when helpful

## Hard rules

- Do not create four empty top-level sections just because Diátaxis has four modes.
- Do not force every page into a rigid global hierarchy if user needs suggest a different structure.
- Do not mix tutorial and how-to content; “basic vs advanced” is not the distinction.
- Do not mix reference and explanation; “theory” can still serve either work or study.
- Do not bury essential reference facts inside explanation or tutorial text.
- Do not overload tutorials with explanation or options.
- Do not turn how-to guides into product-feature tours.
