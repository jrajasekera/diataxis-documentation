# Diátaxis checklists and rubrics

Use these checklists for audits, reviews, and self-checks.

## Compass checklist

For each page or section, answer:

- What is the user's immediate need?
- Is the user at study or at work?
- Does the page guide action or provide knowledge?
- Which mode is primary?
- Which mode is secondary, if any?
- Does the title signal the primary mode?
- Does the opening paragraph set the correct expectation?
- Does the page contain blocks that belong somewhere else?
- What is the smallest useful change?

## Mode classification signals

| Signal | Tutorial | How-to guide | Reference | Explanation |
|---|---|---|---|---|
| Title | “Tutorial”, “Build your first...” | “How to...”, task verbs | “API”, “CLI”, “Options”, object name | “Concepts”, “Overview”, “Why”, “Architecture” |
| Reader | Learner | Competent practitioner | Practitioner checking facts | Practitioner reflecting |
| Structure | One controlled path | Task sequence with possible branches | Entries, tables, schemas, definitions | Prose, diagrams, comparisons |
| Voice | Guiding, reassuring | Direct, practical | Neutral, terse | Discursive, interpretive |
| Examples | Part of the lesson | Used to complete task | Compact illustrations | Used to explain ideas |
| Should avoid | choices, long explanations | teaching, exhaustive facts | opinions, task flow | procedures, hidden facts |

## Tutorial checklist

A tutorial should:

- [ ] Define a concrete thing the learner will make, do, or experience.
- [ ] State assumptions and setup clearly.
- [ ] Use one reliable path.
- [ ] Avoid optional branches and alternatives.
- [ ] Start action early.
- [ ] Produce visible results early and often.
- [ ] Show expected output or observable effects.
- [ ] Tell the learner what to notice.
- [ ] Use “we” where it reinforces guided learning.
- [ ] Keep concepts short and link to explanation.
- [ ] Keep facts minimal and link to reference.
- [ ] Include recovery hints for likely mistakes.
- [ ] End by naming what the learner accomplished.
- [ ] Be tested from a clean environment.

Red flags:

- [ ] “You will learn...” is the main promise.
- [ ] The first action appears late.
- [ ] It offers multiple tools, platforms, or approaches.
- [ ] It assumes expert setup knowledge.
- [ ] It contains long sections titled “Background”, “Theory”, or “Reference”.
- [ ] It cannot be completed reliably.
- [ ] It causes irreversible side effects without a safe sandbox.

## How-to guide checklist

A how-to guide should:

- [ ] Address a real user goal or problem.
- [ ] Have a task title, preferably “How to ...”.
- [ ] Define scope: when to use it and when not to.
- [ ] State prerequisites and risks.
- [ ] Assume competence without omitting task-critical details.
- [ ] Provide ordered steps that match the user's workflow.
- [ ] Include conditional branches for meaningful real-world variation.
- [ ] Keep explanation short and action-serving.
- [ ] Link to reference for options, parameters, and complete lists.
- [ ] Link to explanation for design rationale or conceptual background.
- [ ] End at a practical completion point.

Red flags:

- [ ] It is organized around a product feature rather than a user goal.
- [ ] It teaches fundamentals before doing the task.
- [ ] It contains a full API/CLI/options reference.
- [ ] It has no branches despite real-world variability.
- [ ] It is a vague “guide” or “overview” with no concrete goal.
- [ ] It starts with “What is...” or “Why...” and stays there.

## Reference checklist

Reference should:

- [ ] Be accurate against the source of truth.
- [ ] Be complete for its declared scope.
- [ ] Mirror the structure of the product, API, CLI, schema, or system.
- [ ] Use repeatable entry patterns.
- [ ] List names, types, defaults, constraints, limits, returns, errors, and version notes where relevant.
- [ ] Keep prose neutral and factual.
- [ ] Include warnings where incorrect use is risky.
- [ ] Include compact examples when they clarify use.
- [ ] Avoid task sequences except short usage forms.
- [ ] Avoid conceptual discussion except minimal clarifying notes.

Red flags:

- [ ] Entries differ in structure for no reason.
- [ ] Important defaults or limits are missing.
- [ ] It tells a story instead of describing.
- [ ] It explains design rationale at length.
- [ ] It contains numbered task steps.
- [ ] Examples become multi-step lessons.
- [ ] It is generated but not checked for usability or completeness.

## Explanation checklist

Explanation should:

- [ ] Be about a bounded topic.
- [ ] Answer “why”, “what this means”, or “how to think about it”.
- [ ] Provide context, background, causes, constraints, and implications.
- [ ] Connect the topic to other relevant ideas.
- [ ] Discuss alternatives and trade-offs.
- [ ] Use examples to illuminate, not to instruct.
- [ ] Admit perspective or judgement when helpful.
- [ ] Link to how-to guides for procedures.
- [ ] Link to reference for exact facts.
- [ ] Stay readable away from the product interface.

Red flags:

- [ ] It contains sequential instructions.
- [ ] It is the only place an operational fact is documented.
- [ ] It becomes an unbounded essay.
- [ ] It is mostly tables, parameters, or definitions.
- [ ] It avoids the real “why” question.
- [ ] It tries to teach by doing; that is tutorial material.

## Landing page checklist

A landing page should:

- [ ] Orient the reader to the material inside.
- [ ] Explain what each group of pages helps the reader do or understand.
- [ ] Use short grouped lists rather than one long list.
- [ ] Keep groups to a comfortable size, often around seven items or fewer.
- [ ] Include snippets that help users choose a page.
- [ ] Reflect user needs, not just filesystem order.
- [ ] Avoid empty sections.
- [ ] Avoid a page that is only a raw table of contents unless a mechanical index is the right tool.

## Mixed-mode checklist

For every page, scan for these mixed-mode patterns:

- [ ] Tutorial contains “advanced options”, “alternatives”, or long conceptual background.
- [ ] How-to guide contains “What is...” sections that do not directly serve the task.
- [ ] How-to guide contains full option, parameter, endpoint, or class tables.
- [ ] Reference contains “Step 1...” or “How to...” content.
- [ ] Reference contains design rationale or historical context.
- [ ] Explanation contains command sequences or procedural steps.
- [ ] Explanation contains tables of exact defaults, limits, or errors that belong in reference.
- [ ] Landing page lists more than a few items without grouping.

For each checked item, decide whether to move, link, shorten, or split.

## Documentation-set audit rubric

Score each area from 0 to 3.

| Area | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| User-need clarity | No clear need | Mixed or implicit | Mostly clear | Clear and explicit |
| Mode purity | Modes collapsed | Frequent drift | Minor drift | Strong boundaries |
| Tutorial quality | Missing or unreliable | Exists but fragile | Useful path | Safe, tested learning path |
| How-to coverage | Missing tasks | Feature-focused | Covers common tasks | Rich goal-oriented set |
| Reference quality | Missing/incorrect | Partial/inconsistent | Usable | Complete, authoritative, structured |
| Explanation quality | Missing/scattered | Shallow | Useful topics | Clear mental models and trade-offs |
| Navigation | Confusing | Some groups | Mostly sensible | User-first and easy to scan |
| Cross-linking | Missing | Random | Helpful | Mode-aware and flow-preserving |

Interpretation:

- 0-8: users probably struggle to find and trust information.
- 9-16: the docs have useful pieces but need boundary and coverage work.
- 17-21: solid foundation; focus on gaps, flow, and consistency.
- 22-24: strong Diátaxis execution; maintain through review practices.

Do not present the score as mathematical truth. Use it to focus discussion.

## Smallest useful next actions

When stuck, choose one:

- Rename a page so the title matches its mode.
- Add expected output to a tutorial step.
- Remove one optional branch from a tutorial.
- Move one option table from a how-to guide to reference.
- Add one missing default or error to reference.
- Move one “why” paragraph from reference to explanation.
- Add one conceptual link from tutorial to explanation.
- Split one long landing-page list into groups.
- Add a task-oriented intro to a how-to guide.
- Add “when to use this” to a how-to guide.

## Review comment snippets

Use precise comments:

- “This section interrupts the tutorial’s learning path. Move it to an explanation page and link it after the learner sees the result.”
- “This how-to guide needs a real-world goal in the title. Consider `How to ...`.”
- “This table is reference material. Keep only the options used in this task and link to the full reference.”
- “This API entry is becoming explanatory. Keep the facts here and move the rationale to a concept page.”
- “This explanation contains a procedure. Split it into a how-to guide and link back for background.”
- “This page appears to be both a tutorial and a deployment guide. Choose one primary need or split it.”
