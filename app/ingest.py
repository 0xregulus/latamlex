from pathlib import Path
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup


def download_pdf(url, output_path):
    response = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(response.content)


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text_from_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.get_text(separator='\n')
    return content


def save_text(text, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    COUNTRIES = ["argentina", "brasil", "mexico", "chile"]

    for country in COUNTRIES:
        raw_dir = Path(f"data/{country}/raw")
        clean_dir = Path(f"data/{country}/clean")
        raw_dir.mkdir(parents=True, exist_ok=True)
        clean_dir.mkdir(parents=True, exist_ok=True)

        for file_path in raw_dir.glob("*"):
            filename = file_path.stem + ".txt"
            clean_path = clean_dir / filename

            if file_path.suffix.lower() == ".pdf":
                text = extract_text_from_pdf(file_path)
            elif file_path.suffix.lower() in [".html", ".htm"]:
                text = extract_text_from_html(file_path)
            else:
                print(f"Tipo de archivo no soportado: {file_path.name}")
                continue

            save_text(text, clean_path)
            print(f"Processed: {file_path.name} -> {clean_path}")