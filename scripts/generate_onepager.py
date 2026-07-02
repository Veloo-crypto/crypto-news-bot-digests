"""
Generates a clean, one-page Crypto News Bot PDF digest.
Usage: python generate_onepager.py <content.json> <output.pdf>

content.json shape:
{
  "date": "July 2, 2026",
  "stablecoin_items": [{"headline": "...", "summary": "...", "source": "...", "url": "..."}, ...],
  "hack_items": [{"headline": "...", "summary": "...", "source": "...", "url": "..."}, ...],
  "market_note": "optional one-line stablecoin market cap / peg note"
}
"""
import json
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT

NAVY = colors.HexColor("#0B1F3A")
TEAL = colors.HexColor("#0E7C7B")
RED = colors.HexColor("#B3261E")
GREY = colors.HexColor("#555555")
LIGHT_GREY = colors.HexColor("#EDEDED")


def build(content_path, output_path):
    with open(content_path) as f:
        data = json.load(f)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleBrand", parent=styles["Title"], fontSize=20, textColor=NAVY,
        spaceAfter=0, alignment=TA_LEFT, leading=24,
    )
    date_style = ParagraphStyle(
        "DateStyle", parent=styles["Normal"], fontSize=10, textColor=GREY,
        alignment=TA_LEFT,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"], fontSize=13, spaceBefore=10,
        spaceAfter=4, leading=15,
    )
    headline_style = ParagraphStyle(
        "Headline", parent=styles["Normal"], fontSize=10.5, textColor=colors.black,
        leading=13, spaceAfter=1, fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontSize=9.3, textColor=colors.HexColor("#2B2B2B"),
        leading=12, spaceAfter=6,
    )
    source_style = ParagraphStyle(
        "Source", parent=styles["Normal"], fontSize=8, textColor=GREY, spaceAfter=8,
    )
    note_style = ParagraphStyle(
        "Note", parent=styles["Normal"], fontSize=9, textColor=NAVY,
        leading=12, spaceAfter=2, fontName="Helvetica-Oblique",
    )

    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        topMargin=0.55 * inch, bottomMargin=0.5 * inch,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        title="Crypto News Bot Daily Digest",
    )

    story = []

    # Header
    header_table = Table(
        [[Paragraph("CRYPTO NEWS BOT", title_style),
          Paragraph(f"Daily Digest &bull; {data['date']}", date_style)]],
        colWidths=[4.3 * inch, 2.5 * inch],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceAfter=8))

    if data.get("market_note"):
        story.append(Paragraph(data["market_note"], note_style))
        story.append(Spacer(1, 6))

    # Stablecoin section
    story.append(_section_header("STABLECOIN NEWS", TEAL, section_style))
    for item in data.get("stablecoin_items", []):
        story.append(Paragraph(item["headline"], headline_style))
        story.append(Paragraph(item["summary"], body_style))
        story.append(Paragraph(f'{item.get("source","")}', source_style))

    story.append(Spacer(1, 4))

    # Hacking section
    story.append(_section_header("HACKING & SECURITY INCIDENTS", RED, section_style))
    for item in data.get("hack_items", []):
        story.append(Paragraph(item["headline"], headline_style))
        story.append(Paragraph(item["summary"], body_style))
        story.append(Paragraph(f'{item.get("source","")}', source_style))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.75, color=LIGHT_GREY, spaceAfter=4))
    footer_style = ParagraphStyle(
        "Footer", parent=styles["Normal"], fontSize=7.5, textColor=GREY,
    )
    story.append(Paragraph(
        "Auto-generated daily digest &bull; Crypto News Bot &bull; Sources linked above &bull; "
        "Not financial advice.", footer_style,
    ))

    doc.build(story)


def _section_header(text, color, style):
    return Table(
        [[Paragraph(f'<font color="white"><b>{text}</b></font>', style)]],
        colWidths=[6.8 * inch],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]),
    )


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
