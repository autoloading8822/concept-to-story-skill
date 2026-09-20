# Concept to Story

**Turn abstract ideas in PDFs into stories you can actually remember.**

| Before | After |
| --- | --- |
| “Special obligations are relationship-dependent moral duties…” | 🧠 Imagine friendship as a membership card — it gives someone extra privileges, but it is not an unlimited credit card. |

*An original teaching illustration, not a quotation or a universal ethical verdict.*

A lightweight, repository-level **Codex Skill** for learning from documents you already have. It reads the source, finds the structure of an idea, and makes you practice retrieving it.

**Community project / unofficial.** Not affiliated with or endorsed by OpenAI.

[Try it in 5 minutes](#installation) · [Full example](examples/generic-demo.md) · [中文故事示例](examples/values-learning-demo.md)

## What it does

A typical PDF summarizer: **PDF → Summary**

Concept to Story:

```text
PDF → Concept → Concrete Conflict → Story → Memory Anchor
                                              ↓
                   Transfer ← Active Recall ← Real-Life Signal
```

Each lesson returns to the source, maps the story back to the theory, and names **where the analogy breaks**. That boundary is as important as the memorable image.

- Learn a difficult concept, chapter, textbook, paper, or lecture note in your preferred language.
- Get a chapter map of normally 3–7 concepts; study one at a time in batches of 1–3.
- For a whole book, start with a Book Map of normally 5–12 nodes, not dozens of stories.
- Answer one scenario question before seeing its answer, then apply the concept in a different setting.
- Keep source claims separate from fictional teaching scenes and supplementary explanations.

It does not automatically activate for summary-only requests, book recommendations, shopping, author lookup, or PDF-to-Word conversion.

## Why it exists

A definition can feel familiar while remaining hard to use. This skill is designed to give an abstract relationship a concrete retrieval cue, then check whether you can reconstruct and apply it. A vivid story alone is not enough: **source fidelity comes before story quality**.

The success criterion is practical: can you see the anchor tomorrow and recover the original structure, including its limits? This repository does not claim a measured improvement in long-term memory.

## Example

**Idea:** A special relationship can provide additional reasons to help, while leaving room for limits.

**Scene:** A friend receives help moving house, then starts treating every weekend as reserved for their requests. The helper offers one planned afternoon and declines the rest.

**Anchor:** A friendship membership card with a limit.

**Boundary:** The card is an analogy, not a claim that friendship is a commercial contract or that all obligations have the same limit.

**Observable signal:** What happens when the helper states a reasonable limit: negotiation, acceptance, or pressure?

**Recall:** A colleague thinks that because you helped once, you must cover every future shift. What distinction would you use to assess that expectation?

No answer is shown. See the [complete source-grounded synthetic lesson](examples/generic-demo.md) and [five original values lessons](examples/values-learning-demo.md). The latter is a gallery, not a recommended single teaching turn.

## Installation

**Prerequisite:** Codex with local skills support. No API key, server, or package installation is required for the skill itself. Reading a PDF still requires a reader or extraction tool in your Codex environment; scans may also need OCR.

Clone this repository and open its folder as your Codex project:

```sh
git clone https://github.com/autoloading8822/concept-to-story-skill.git
cd concept-to-story-skill
```

The skill is already in `.agents/skills/concept-to-story/`. Codex discovers repository skills there. Start a task in this project; if the skill does not appear, restart Codex and confirm the project folder. You can invoke it explicitly as `$concept-to-story` or use a matching learning request. See the [official skills documentation](https://learn.chatgpt.com/docs/build-skills) for discovery and invocation behavior (checked 2026-09-20).

**Use in an existing project:** copy only `.agents/skills/concept-to-story/` into that project's `.agents/skills/`. Preserve its other skills; if `concept-to-story` already exists, compare before replacing it. No personal/global installation is required.

## How to use with Codex

Attach a PDF you are authorized to process, or give its readable local path. Keep it outside the repository or in the ignored `private/` folder. An attachment's availability depends on your Codex client; if it cannot read the attachment, provide an accessible local path.

Suggested starting configuration, when available in your model picker: **GPT-5.6 Terra**, reasoning effort **medium**. This is a practical default for a structured reading-and-teaching task, not a benchmark result or a requirement; use another available model if needed. The skill does not call a separate LLM or pin a model.

```text
$concept-to-story 帮我学习这个 PDF 的第三章。
先列核心知识点，再讲第一个。用中文，一次只问一道题，等我回答。
```

Other requests:

- “This concept is too abstract. Give me a concrete story and show where the analogy fails.”
- “Map this whole book first. Do not teach all the nodes yet.”
- “继续。上一题先跳过，进入下一个知识点。”
- “只给我昨天的记忆锚点，让我自己回忆。”

**No PDF handy?** Attach [the original test text](tests/fixtures/learning-source.md) and ask to learn section 1. It will be labeled as synthetic Markdown source rather than as a real book PDF. For a reproducible PDF smoke test, see [the evaluation guide](tests/skill-evaluation-cases.md).

## Output format

| Section | Purpose |
| --- | --- |
| Source | Verified location and the claim's essential conditions |
| Core Idea | 1–3 plain-language sentences |
| Why It Matters | What the idea lets you understand |
| Story | A person, goal, conflict, choice, and consequence |
| Memory Anchor | One simple object, scene, or action |
| Back to the Theory | Explicit scene-to-concept mapping |
| Where the Analogy Breaks | Limits and a tempting false inference |
| Real-Life Signal | Something observable in practice |
| Active Recall | One scenario question, with the answer withheld |

**SOURCE: PDF** identifies the supplied document's claims. **SUPPLEMENTARY EXPLANATION** identifies invented teaching scenes and other additions. If evidence is insufficient, the skill says so instead of inventing pages or author positions.

## Repository structure

```text
.agents/skills/concept-to-story/
├── SKILL.md
├── references/
│   ├── pedagogy.md
│   ├── story-design.md
│   └── source-fidelity.md
└── assets/lesson-template.md
examples/
├── values-learning-demo.md
└── generic-demo.md
tests/
├── fixtures/learning-source.md
├── skill-evaluation-cases.md
├── validate_repo.py
└── make_test_pdf.py
README.md
CONTRIBUTING.md
LICENSE
.gitignore
```

## Design principles

1. **Source fidelity > story quality.** A memorable distortion is a failure.
2. **Make the learner see the relationship.** Conflict and consequence carry the mechanism.
3. **Keep the anchor simple.** An elaborate illustration is optional and usually unnecessary.
4. **Retrieve before revealing.** Wait for the learner's answer.
5. **Transfer beyond the story.** Change the setting while keeping the conceptual structure.
6. **Mark what is unknown.** Unread pages and untested understanding stay visible.

## Checks

Run the dependency-free repository checks with Python 3.10+ and Git:

```sh
python tests/validate_repo.py
```

These check repository integrity, links, and safeguards against accidentally including source documents. They do **not** score story quality or prove skill activation. The [12 behavioral evaluation cases](tests/skill-evaluation-cases.md) cover those decisions and explain how to record observed results separately from expectations.

## Limitations

- This is a set of agent instructions, not a bundled PDF/OCR engine or a standalone app.
- Extraction can lose layout, equations, or page labels. Uncertain content must be checked visually or left unconfirmed.
- A metaphor is neither proof nor a diagnosis; contested theories remain frameworks.
- Long books are read in stages. A provisional map is not a claim to have read every page.
- Responses and automatic selection vary by model and environment. Written evaluation cases are not evidence that all models pass them.
- Next-day recall requires a returning learner; an immediate demo cannot establish it.
- `.gitignore` is a convenience, not a security boundary. Review staged files before publishing.
- Local file access does not imply offline model inference; processing follows your Codex environment and data settings.

## Copyright

The repository does not include or redistribute source books or PDFs.

Users are responsible for providing documents they are authorized to access and process.

Public examples contain original fictional scenes and synthetic teaching text. Existing named concepts or metaphors are not claimed as inventions of this project. Source books, full extracts, paid scans, and private learning notes must not be committed. Only short necessary quotations should be used when appropriate; the project license does not grant rights to third-party materials.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions that improve source fidelity, analogy boundaries, and observable learning behavior are especially useful.

## License

[MIT](LICENSE).
