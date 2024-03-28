from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import fonts
import os
import argparse
import json

def toDocx(filename: str, folder: str):
    # Get all the json files in the folder
    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    # Create a Document object
    doc = Document()
    for file in files:
        # Open the json file
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            data = json.load(f)
        # Set the title config and write title
        title = doc.add_heading(level=1)
        title_run = title.add_run(data["Title"]) # add title content
        # set title font
        title_run.font.name = u"黑体"
        title_run.element.rPr.rFonts.set(qn("w:eastAsia"), u"黑体")
        title_run.font.size = Pt(24)
        # align title to center
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Set the date config and write date
        updateDate = doc.add_paragraph()
        date_run = updateDate.add_run("更新日期：" + data["Date Update"]) # add date content
        # set date font
        date_run.font.name = u"宋体"
        date_run.element.rPr.rFonts.set(qn("w:eastAsia"), u"宋体")
        date_run.font.size = Pt(16)
        # align date to center
        updateDate.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        doc.add_paragraph() # add a new line
        # Set the description config and write content
        description = doc.add_paragraph()
        description_run = description.add_run(data["Description"]) # add description content
        # set description font
        description_run.font.name = u"宋体"
        description_run.element.rPr.rFonts.set(qn("w:eastAsia"), u"宋体")
        description_run.font.size = Pt(16)
    # Save the docx file
    doc.save(filename)

def toPDF(filename: str, folder: str):
    # Get all the json files in the folder
    files = [f for f in os.listdir(folder) if f.endswith(".json")]
    # Register the font
    pdfmetrics.registerFont(TTFont("simsun", "./SimSun.ttf"))
    # Create a simple template
    pdf = SimpleDocTemplate(filename)
    # Get the default style
    styles = getSampleStyleSheet()
    # Customize the default style
    styles['Normal'].fontName = 'simsun'
    styles['Normal'].fontSize = 12
    styles['Title'].fontName = 'simsun'
    styles['Title'].fontSize = 20
    # Create a list to store the content
    content = []
    for file in files:
        # Open the json file
        with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
            data = json.load(f)
        # Add title
        content.append(Paragraph(data["Title"], styles["Title"]))
        # Add date
        content.append(Paragraph("更新日期：" + data["Date Update"], styles["Normal"]))
        # Add description
        content.append(Paragraph(data["Description"], styles["Normal"]))
    # Build the pdf file
    pdf.build(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert JSON to DOCX")
    parser.add_argument("-f", "--folder", help="Folder path", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=True)
    args = parser.parse_args()

    ext = os.path.splitext(args.output)[1]
    if ext == ".docx":
        toDocx(args.output, args.folder)
    elif ext == ".pdf":
        toPDF(args.output, args.folder)
    else:
        print("Unsupported file format")