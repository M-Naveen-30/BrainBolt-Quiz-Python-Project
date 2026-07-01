"""
build_assets.py
~~~~~~~~~~~~~~~
Run ONCE to create:
   assets/logo.png         - opening logo
   assets/opening.wav      - mild welcome music (10 sec)
   answers_pdf/*.pdf       - 4 answer-key PDFs (one per topic)

Usage:
    python build_assets.py
"""
import os
import json
import math
import struct
import wave

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib            import colors
from reportlab.platypus       import (SimpleDocTemplate, Paragraph, Spacer,
                                      PageBreak, Table, TableStyle)
from reportlab.lib.units      import inch
from xml.sax.saxutils         import escape as xml_escape


def _esc(text: str) -> str:
    """Escape <, >, & so ReportLab Paragraph doesn't try to parse them."""
    return xml_escape(str(text))

# --------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR     = os.path.join(HERE, "assets")
DATA_DIR       = os.path.join(HERE, "data")
ANSWER_PDF_DIR = os.path.join(HERE, "answers_pdf")
os.makedirs(ASSETS_DIR,     exist_ok=True)
os.makedirs(ANSWER_PDF_DIR, exist_ok=True)


# --------------------------------------------------------------------
#  1.  LOGO   (PNG)
# --------------------------------------------------------------------
def _font(size, bold=False):
    candidates = (
        ["arialbd.ttf", "DejaVuSans-Bold.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold else
        ["arial.ttf", "DejaVuSans.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except (IOError, OSError):
            continue
    return ImageFont.load_default()


def make_logo():
    W, H = 820, 620
    img  = Image.new("RGB", (W, H), "#0E1230")
    d    = ImageDraw.Draw(img)

    # ambient glow circles
    for r, col in [(360, "#1A2050"), (260, "#252E78"), (180, "#3A48B5")]:
        d.ellipse([(W // 2 - r, H // 2 - r),
                   (W // 2 + r, H // 2 + r)], fill=col)

    # lightning bolt (zig-zag polygon)
    cx, cy = W // 2, H // 2
    bolt = [
        (cx -  50, cy - 170),
        (cx + 110, cy -  20),
        (cx +  20, cy -  20),
        (cx +  90, cy + 170),
        (cx -  90, cy +  20),
        (cx -  10, cy +  20),
    ]
    d.polygon(bolt, fill="#FFD23F", outline="#FFA000")

    # name
    fn = _font(86, bold=True)
    tag = _font(30, bold=True)
    tw  = d.textlength("BrainBolt", font=fn)
    d.text(((W - tw) // 2, H - 170), "BrainBolt",
           font=fn, fill="#FFFFFF")
    tw2 = d.textlength("Spark Your Mind", font=tag)
    d.text(((W - tw2) // 2, H -  90), "Spark Your Mind",
           font=tag, fill="#9CC2FF")

    out = os.path.join(ASSETS_DIR, "logo.png")
    img.save(out)
    print(f"  -> {out}")


# --------------------------------------------------------------------
#  2.  OPENING MUSIC   (a soft pentatonic chime, 10 sec WAV)
# --------------------------------------------------------------------
def make_music():
    out  = os.path.join(ASSETS_DIR, "opening.wav")
    sr   = 22050
    secs = 10
    notes = [392.00, 440.00, 523.25, 587.33, 659.25,
             587.33, 523.25, 440.00]  # G4 A4 C5 D5 E5 D5 C5 A5  (pentatonic)
    note_len = secs / len(notes)
    samples_per = int(sr * note_len)

    with wave.open(out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        frames = bytearray()
        for f in notes:
            for i in range(samples_per):
                t = i / sr
                # short attack + decay envelope -> soft chime
                env = math.exp(-3.0 * t)
                base = math.sin(2 * math.pi * f * t)
                # add a soft second harmonic
                harm = 0.3 * math.sin(2 * math.pi * (2 * f) * t)
                s = int(0.35 * 32767 * env * (base + harm))
                s = max(-32767, min(32767, s))
                frames += struct.pack("<h", s)
        w.writeframes(bytes(frames))
    print(f"  -> {out}")


# --------------------------------------------------------------------
#  3.  ANSWER-KEY PDFS   (one per topic)
# --------------------------------------------------------------------
def make_answer_pdfs():
    with open(os.path.join(DATA_DIR, "questions.json"), "r", encoding="utf-8") as f:
        bank = json.load(f)

    pretty = {
        "python":       "Python",
        "data_science": "Data Science",
        "java":         "Java",
        "full_stack":   "Full Stack",
    }

    styles = getSampleStyleSheet()
    title  = ParagraphStyle("T",  parent=styles["Title"],
                            fontSize=26, textColor=colors.HexColor("#3A48B5"))
    sub    = ParagraphStyle("S",  parent=styles["Heading2"],
                            textColor=colors.HexColor("#5E60CE"))
    qst    = ParagraphStyle("Q",  parent=styles["BodyText"],
                            fontSize=12, leading=16, spaceBefore=10,
                            textColor=colors.black)
    opt    = ParagraphStyle("O",  parent=styles["BodyText"],
                            fontSize=11, leading=15, leftIndent=20,
                            textColor=colors.HexColor("#222222"))
    ans    = ParagraphStyle("A",  parent=styles["BodyText"],
                            fontSize=11, leading=15, leftIndent=20,
                            textColor=colors.HexColor("#0a7d32"),
                            fontName="Helvetica-Bold")
    expl   = ParagraphStyle("E",  parent=styles["BodyText"],
                            fontSize=10, leading=13, leftIndent=20,
                            textColor=colors.HexColor("#444444"),
                            spaceAfter=10)

    for key, qs in bank.items():
        out = os.path.join(ANSWER_PDF_DIR, f"{key}_answers.pdf")
        doc = SimpleDocTemplate(out, pagesize=A4,
                                topMargin=0.6 * inch, bottomMargin=0.6 * inch,
                                leftMargin=0.7 * inch, rightMargin=0.7 * inch)
        story = []
        story.append(Paragraph("BrainBolt - Answer Key", title))
        story.append(Paragraph(f"Topic: {pretty[key]} ({len(qs)} Questions)", sub))
        story.append(Spacer(1, 14))

        for i, q in enumerate(qs, start=1):
            story.append(Paragraph(f"<b>Q{i}.</b> {_esc(q['q'])}", qst))
            for j, o in enumerate(q["options"]):
                letter = chr(ord("A") + j)
                marker = "  &lt;- correct" if letter == q["answer"] else ""
                story.append(Paragraph(f"{letter}. {_esc(o)}{marker}", opt))
            story.append(Paragraph(f"Answer: {q['answer']}", ans))
            if q.get("explain"):
                story.append(Paragraph(f"Why: {_esc(q['explain'])}", expl))

        doc.build(story)
        print(f"  -> {out}")


# --------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating BrainBolt assets ...")
    make_logo()
    make_music()
    make_answer_pdfs()
    print("All assets generated successfully.")
