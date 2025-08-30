import fitz

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append(f"[Page {i + 1}]\n{text.strip()}")
    return pages