from pathlib import Path
import json
import faiss
from sentence_transformers import SentenceTransformer


def load_chunks(jsonl_path):
    chunks = []
    ids = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            ids.append(item["id"])
            chunks.append(item["text"])
    return ids, chunks


def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def process_country(country, model):
    chunk_dir = Path(f"data/{country}/chunks")
    vector_dir = Path(f"vectorstore/{country}")
    vector_dir.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    all_ids = []

    for jsonl_file in chunk_dir.glob("*.jsonl"):
        ids, chunks = load_chunks(jsonl_file)
        all_ids.extend(ids)
        all_chunks.extend(chunks)

    embeddings = model.encode(all_chunks, show_progress_bar=True, convert_to_numpy=True)
    index = build_faiss_index(embeddings)

    faiss.write_index(index, str(vector_dir / "index.faiss"))
    with open(vector_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump({"ids": all_ids}, f, ensure_ascii=False, indent=2)

    print(f"Indexed {len(all_chunks)} chunks for {country}")


if __name__ == "__main__":
    model = SentenceTransformer("all-MiniLM-L6-v2")
    for country in ["argentina", "brasil", "mexico", "chile"]:
        process_country(country, model)