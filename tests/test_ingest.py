from app.ingest import extract_text_from_pdf
from pathlib import Path

def test_extract_text_from_pdf_returns_string():
    sample_pdf = Path("data/argentina/raw/comunicacion_a7759.pdf")
    if not sample_pdf.exists():
        return  # evitar falla si el archivo no está
    text = extract_text_from_pdf(sample_pdf)
    assert isinstance(text, str)
    assert len(text) > 0