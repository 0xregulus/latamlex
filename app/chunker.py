from pathlib import Path
import json


def chunk_text(text, max_tokens=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + max_tokens, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap

    return chunks


def process_all_texts(countries=["argentina", "brasil", "mexico", "chile"]):
    for country in countries:
        input_dir = Path(f"data/{country}/clean")
        output_dir = Path(f"data/{country}/chunks")
        output_dir.mkdir(parents=True, exist_ok=True)

        for txt_file in input_dir.glob("*.txt"):
            with open(txt_file, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)

            jsonl_path = output_dir / (txt_file.stem + ".jsonl")
            with open(jsonl_path, "w", encoding="utf-8") as f:
                for i, chunk in enumerate(chunks):
                    json.dump({"id": f"{txt_file.stem}-{i}", "text": chunk}, f)
                    f.write("\n")

            print(f"Chunked: {txt_file.name} -> {jsonl_path}")


if __name__ == "__main__":
    process_all_texts()