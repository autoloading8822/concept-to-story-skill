"""Dependency-free integrity checks, not a behavioral or retention evaluator."""

from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/concept-to-story"


def git(*arguments):
    result = subprocess.run(["git", "-C", str(ROOT), *arguments], capture_output=True, text=True, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(arguments)} failed")
    return result.stdout


def main():
    failures = []
    required = [
        ".agents/skills/concept-to-story/SKILL.md",
        ".agents/skills/concept-to-story/references/pedagogy.md",
        ".agents/skills/concept-to-story/references/story-design.md",
        ".agents/skills/concept-to-story/references/source-fidelity.md",
        ".agents/skills/concept-to-story/assets/lesson-template.md",
        "README.md", "LICENSE", "CONTRIBUTING.md", ".gitignore",
        "examples/values-learning-demo.md", "examples/generic-demo.md",
        "tests/skill-evaluation-cases.md", "tests/fixtures/learning-source.md",
        "tests/make_test_pdf.py", "tests/validate_repo.py",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            failures.append(f"Missing {relative}")
    if failures:
        raise SystemExit("\n".join(failures))

    skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    # This repo deliberately uses a two-scalar YAML subset; not a general YAML parser.
    metadata = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n", skill_text)
    if not metadata or metadata[1] != SKILL.name or len(metadata[2]) > 1024:
        failures.append("Invalid repository frontmatter contract (name/description)")
    elif ": " in metadata[2] or " #" in metadata[2]:
        failures.append("Plain description contains YAML-special syntax; validate and adjust the contract")

    tracked = git("ls-files", "-z").split("\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").split("\0")
    paths = [ROOT / name for name in sorted(set(tracked + untracked)) if name]
    forbidden_suffixes = {".pdf", ".epub", ".mobi", ".docx", ".pem", ".key"}
    private_roots = {"private", "input", "inputs", "output", "outputs", "notes", "tmp", "test-output", ".local"}
    for path in paths:
        relative = path.relative_to(ROOT)
        if path.is_symlink():
            failures.append(f"Review symbolic link before publishing: {relative}")
            continue
        if path.suffix.lower() in forbidden_suffixes or relative.parts[0] in private_roots or path.name.startswith(".env"):
            failures.append(f"Private/source artifact included: {relative}")
        if path.suffix != ".md":
            continue
        contents = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", contents):
            url = urlsplit(target)
            if url.scheme or not url.path:
                continue
            destination = (path.parent / unquote(url.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                failures.append(f"Broken or out-of-repository link in {relative}: {target}")
        if "[TODO:" in contents:
            failures.append(f"Unfinished scaffold in {relative}")

    probes = ["private/book.PDF", "book.pdf", "book.Pdf", "notes/extract.md", "test-output/learning-source.pdf", ".env"]
    for probe in probes:
        try:
            git("check-ignore", "--no-index", "--", probe)
        except RuntimeError:
            failures.append(f"Expected ignore protection missing: {probe}")
    # Copyright or behavioral accuracy cannot be inferred from filenames.
    print(f"Inspected {len(paths)} publishable files and {len(probes)} ignore probes.")
    if failures:
        raise SystemExit("FAIL\n" + "\n".join(failures))
    print("PASS: structure, frontmatter contract, local file links, and source-file exclusion checks.")
    print("NOT TESTED by this script: semantic fidelity, automatic triggering, or long-term memory.")


if __name__ == "__main__":
    main()
