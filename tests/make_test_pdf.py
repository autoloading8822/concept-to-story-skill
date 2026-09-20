"""Create an original, ignored PDF fixture; optional test dependency: reportlab."""

from pathlib import Path
from xml.sax.saxutils import escape


def main():
    try:
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.pdfgen.canvas import Canvas
    except ImportError as exc:
        raise SystemExit("Optional fixture generation needs ReportLab in your test environment.") from exc

    root = Path(__file__).resolve().parents[1]
    source = root / "tests/fixtures/learning-source.md"
    target = root / "test-output/learning-source.pdf"
    if target.exists():
        raise SystemExit(f"Refusing to overwrite {target}; keep or relocate the existing fixture first.")
    target.parent.mkdir(exist_ok=True)
    styles = getSampleStyleSheet()
    # Build each page separately to enforce stable, checkable source locators.
    from io import BytesIO
    from reportlab.platypus import PageBreak

    text = source.read_text(encoding="utf-8")
    preface, body = text.split("## 1. Opportunity cost", 1)
    sections = ("## 1. Opportunity cost" + body).split("\n## ")
    sections = [part.removeprefix("## ") for part in sections]
    pages = [preface] + sections
    story = []
    for index, page in enumerate(pages):
        if index:
            story.append(PageBreak())
        paragraphs = page.strip().split("\n\n")
        for paragraph_index, paragraph in enumerate(paragraphs):
            clean = paragraph.lstrip("# ")
            style = styles["Heading1"] if paragraph_index == 0 else styles["BodyText"]
            story.append(Paragraph(escape(clean).replace("\n", "<br/>"), style))
            story.append(Spacer(1, 10))

    seen_pages = []

    def footer(canvas: Canvas, doc):
        seen_pages.append(doc.page)
        canvas.setFont("Helvetica", 9)
        canvas.drawString(54, 32, f"Synthetic fixture | PDF file page {doc.page}")

    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer, pagesize=(612, 792), rightMargin=54, leftMargin=54,
        topMargin=54, bottomMargin=54,
        title="Small Decisions, Clear Structures",
        author="Concept to Story contributors",
    )
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    if len(seen_pages) != len(pages):
        raise SystemExit(f"Fixture overflow: expected {len(pages)} pages, got {len(seen_pages)}. No PDF written.")
    with target.open("xb") as stream:
        stream.write(buffer.getvalue())
    print(f"Created {target} ({len(pages)} pages; sections 1-6 on PDF file pages 2-7).")
    print("Visually inspect it before using page numbers in a behavioral evaluation.")


if __name__ == "__main__":
    main()
