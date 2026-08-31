from pypdf import PdfReader


def extract_resume_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)

    text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    return "\n".join(text)