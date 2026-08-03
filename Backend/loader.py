import re
from pypdf import PdfReader


def clean_text(text):
    """
    Cleans text extracted from the PDF while preserving line breaks.
    """

    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Remove extra spaces and tabs (keep newlines)
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Remove common PDF icon placeholders
    text = text.replace("/external-link-alt", "")
    text = text.replace("/github", "")
    text = text.replace("/linkedin-in", "")
    text = text.replace("/envelope", "")
    text = text.replace("/phone-alt", "")
    text = text.replace("/map-marker-alt", "")

    return text.strip()


def load_resume(pdf_path):
    """
    Reads a PDF resume and returns cleaned text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return clean_text(text)