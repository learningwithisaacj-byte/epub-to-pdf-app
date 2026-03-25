import streamlit as st
import tempfile
from ebooklib import epub
from reportlab.pdfgen import canvas
from bs4 import BeautifulSoup

st.title("📚 EPUB → PDF Converter (Cloud Ready)")

uploaded_file = st.file_uploader("Upload EPUB", type=["epub"])

def epub_to_pdf(epub_file, output_pdf):
    book = epub.read_epub(epub_file)
    c = canvas.Canvas(output_pdf)

    for item in book.get_items():
        if item.get_type() == 9:  # document
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text()

            for line in text.split("\n"):
                c.drawString(40, 800, line[:100])
                c.showPage()

    c.save()

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_epub:
        tmp_epub.write(uploaded_file.read())
        epub_path = tmp_epub.name

    pdf_path = epub_path.replace(".epub", ".pdf")

    if st.button("Convert"):
        epub_to_pdf(epub_path, pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", f, file_name="converted.pdf")
