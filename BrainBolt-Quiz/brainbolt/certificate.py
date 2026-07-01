"""
certificate.py
~~~~~~~~~~~~~~
Generates a stylised PNG (Pillow) and converts it to PDF (ReportLab).

OOP showcase
------------
* INHERITANCE   -> 4 concrete certificate classes inherit BaseCertificate
* POLYMORPHISM  -> Each overrides `tier`, `accent_color`, `medal_glyph`
* ABSTRACTION   -> Caller only calls .generate(); rendering is hidden
"""
import os
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader

from .config import OUTPUT_DIR, CERT_TEMPLATE


# ----------------------------------------------------------------------
def _font(size, bold=False):
    """Return a PIL font, falling back to default if TTFs missing."""
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


# ----------------------------------------------------------------------
class BaseCertificate:
    """Abstract-style base; subclasses set tier + colour."""

    tier         = "PARTICIPATION"
    accent_color = "#7E57C2"
    medal_glyph  = "*"

    def __init__(self, user_name: str, topic_label: str,
                 score: int, total: int):
        self.user_name   = user_name
        self.topic_label = topic_label
        self.score       = score
        self.total       = total

    # ----- main entrypoint -----
    def generate(self) -> str:
        """Returns absolute path of the PDF."""
        png_path = self._render_png()
        pdf_path = self._png_to_pdf(png_path)
        return pdf_path

    # ----- internals -----
    def _render_png(self) -> str:
        W, H = 1600, 1100
        img  = Image.new("RGB", (W, H), "#FFFCF6")
        d    = ImageDraw.Draw(img)

        # double border
        d.rectangle([(40, 40), (W - 40, H - 40)], outline=self.accent_color, width=10)
        d.rectangle([(70, 70), (W - 70, H - 70)], outline="#222222", width=2)

        # corner glyphs (the medal char)
        gfont = _font(86, bold=True)
        for x, y in [(95, 90), (W - 175, 90),
                     (95, H - 200), (W - 175, H - 200)]:
            d.text((x, y), self.medal_glyph, font=gfont, fill=self.accent_color)

        # header strip
        d.rectangle([(70, 70), (W - 70, 200)], fill=self.accent_color)
        d.text((W // 2 - 360, 95), "BrainBolt", font=_font(70, bold=True), fill="white")
        d.text((W // 2 - 200, 175), "Spark Your Mind", font=_font(28), fill="white")

        # title
        d.text((W // 2 - 380, 260),
               "CERTIFICATE OF ACHIEVEMENT",
               font=_font(48, bold=True), fill="#222222")

        d.text((W // 2 - 180, 340), f"- {self.tier} TIER -",
               font=_font(36, bold=True), fill=self.accent_color)

        # body
        d.text((W // 2 - 230, 440), "This certificate is awarded to",
               font=_font(28), fill="#333333")

        # user name - centred
        name_font = _font(72, bold=True)
        name_w    = d.textlength(self.user_name, font=name_font)
        d.text(((W - name_w) // 2, 500), self.user_name,
               font=name_font, fill=self.accent_color)

        # underline
        d.line([(W // 2 - 350, 600), (W // 2 + 350, 600)],
               fill="#222222", width=2)

        # accomplishment line
        d.text((W // 2 - 470, 640),
               f"for successfully completing the {self.topic_label} quiz",
               font=_font(30), fill="#333333")

        score_str = f"with a score of  {self.score} / {self.total}"
        d.text((W // 2 - 230, 690), score_str, font=_font(30), fill="#333333")

        # date + signature blocks
        today = date.today().strftime("%d %B %Y")
        d.line([(180, 920), (520, 920)], fill="#222222", width=2)
        d.text((280, 935), "Date", font=_font(24, bold=True), fill="#222222")
        d.text((270, 880), today, font=_font(22), fill="#444444")

        d.line([(W - 520, 920), (W - 180, 920)], fill="#222222", width=2)
        d.text((W - 425, 935), "BrainBolt Team",
               font=_font(24, bold=True), fill="#222222")
        d.text((W - 415, 880), "Spark Your Mind",
               font=_font(22), fill="#444444")

        out_png = os.path.join(
            OUTPUT_DIR,
            f"{self.user_name.replace(' ', '_')}_{self.topic_label.replace(' ', '_')}_{self.tier}.png",
        )
        img.save(out_png)
        return out_png

    def _png_to_pdf(self, png_path: str) -> str:
        pdf_path = png_path.rsplit(".", 1)[0] + ".pdf"
        c = pdf_canvas.Canvas(pdf_path, pagesize=landscape(A4))
        w, h = landscape(A4)
        c.drawImage(ImageReader(png_path), 0, 0,
                    width=w, height=h, preserveAspectRatio=True, anchor="c")
        c.showPage()
        c.save()
        return pdf_path


# ----------------------------------------------------------------------
class GoldCertificate(BaseCertificate):
    tier         = "GOLD"
    accent_color = "#C8A93A"
    medal_glyph  = "1"


class SilverCertificate(BaseCertificate):
    tier         = "SILVER"
    accent_color = "#8B8B8B"
    medal_glyph  = "2"


class BronzeCertificate(BaseCertificate):
    tier         = "BRONZE"
    accent_color = "#A66A2C"
    medal_glyph  = "3"


class AppreciationCertificate(BaseCertificate):
    tier         = "APPRECIATION"
    accent_color = "#5E60CE"
    medal_glyph  = "+"


# ----------------------------------------------------------------------
def pick_certificate(score: int, total: int):
    """Factory - chooses class based on the score rules."""
    if score > 13:
        cls = GoldCertificate
    elif score >= 11:        # 11, 12, 13
        cls = SilverCertificate
    elif score >= 9:         # 9, 10
        cls = BronzeCertificate
    else:                    # < 9
        cls = AppreciationCertificate
    return cls
