# Contributing

Keep the project easy to read, install, and fork. Prefer a narrow improvement to the learning workflow over a new framework or dependency.

For a change, explain the concrete learning failure, provide a short original or authorized fixture, and show the changed behavior. Preserve source grounding, explicit analogy boundaries, and the learner's opportunity to answer.

## Before submitting

1. Read the current skill and the relevant reference before editing. Keep shared rules in the entrypoint and conditional details in references.
2. Use the learner's language in examples; English project documentation and Chinese demonstrations are both welcome.
3. Run `python tests/validate_repo.py` from the repository root.
4. Run affected cases in [the evaluation guide](tests/skill-evaluation-cases.md), recording prompts, actual outputs, source coverage, and pass/fail reasoning. Keep private transcripts local.
5. Inspect `git diff --check` and the staged file list. Include no source PDF, copied chapter, credentials, personal paths, or learner information.

The installed Codex `skill-creator` validator can provide an additional frontmatter check if available; it is not a required runtime dependency. Behavioral review must judge actual fidelity and learning behavior, not just whether headings appear.

Original synthetic fixtures belong in `tests/fixtures/` as text. Generated test PDFs belong in ignored `test-output/`; `tests/make_test_pdf.py` recreates one locally. Do not relax the ignore policy to commit a book.

State testing limits: static validation, a single-model smoke test, and delayed learner recall are different evidence. Do not label unexecuted evaluation cases as passed.

By contributing, you agree to license your original contribution under the repository's MIT license. Do not submit third-party material that you are not authorized to redistribute.
