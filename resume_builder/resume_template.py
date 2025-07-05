from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def create_pdf(data, filename="generated_resume.pdf"):
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    x_margin = 50
    y = height - 50

    def new_page_if_needed():
        nonlocal y
        if y < 80:
            c.showPage()
            y = height - 50

    def draw_title(title):
        nonlocal y
        new_page_if_needed()
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x_margin, y, title.upper())
        y -= 18

    def draw_text_block(text, font_size=10, bullet=False):
        nonlocal y
        c.setFont("Helvetica", font_size)
        max_width = width - 2 * x_margin
        lines = text.strip().split("\n")

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            is_prebulleted = line.startswith("•") or line.startswith("-")
            wrapped_lines = simpleSplit(line.lstrip("•- ").strip(), "Helvetica", font_size, max_width)

            for i, wrapped_line in enumerate(wrapped_lines):
                new_page_if_needed()
                if bullet and i == 0 and not is_prebulleted:
                    c.drawString(x_margin + 10, y, f"• {wrapped_line}")
                else:
                    indent = 10 if bullet and not is_prebulleted else 0
                    c.drawString(x_margin + indent, y, wrapped_line)
                y -= font_size + 2
        y -= 4

    
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, y, data["name"].upper())
    y -= 18
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(width / 2, y, data["title"])
    y -= 14
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, y, f"{data['phone']} | {data['email']}")
    y -= 12
    c.drawCentredString(width / 2, y, f"LinkedIn: {data['linkedin']} | GitHub: {data['github']}")
    y -= 20

    draw_title("Summary")
    draw_text_block(data["summary"], bullet=False)

    draw_title("Education")
    draw_text_block(data["education"], bullet=False)

    draw_title("Skills")
    draw_text_block(data["skills"], bullet=False)

    draw_title("Experience")
    draw_text_block(data["experience"], bullet=True)

    draw_title("Projects")
    draw_text_block(data["projects"], bullet=True)

    draw_title("Certifications")
    draw_text_block(data["certifications"], bullet=True)

    draw_title("Strength")
    draw_text_block(data["strengths"], bullet=True)

    draw_title("Languages")
    draw_text_block(data["languages"], bullet=False)

    c.save()
    return filename
