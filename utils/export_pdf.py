from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(content):

    file_name = "project_documentation.pdf"

    pdf = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Requirement Engineering Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            content.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    pdf.build(story)

    return file_name