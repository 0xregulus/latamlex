import json
import faiss
import time
from pathlib import Path
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os


openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", "12000"))
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))


def load_index_and_metadata(country):
    vector_dir = Path(f"vectorstore/{country}")
    index = faiss.read_index(str(vector_dir / "index.faiss"))
    with open(vector_dir / "metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata["ids"]


def load_chunks_by_id(country, ids):
    chunk_dir = Path(f"data/{country}/chunks")
    chunks = {}
    for file in chunk_dir.glob("*.jsonl"):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                if item["id"] in ids:
                    chunks[item["id"]] = item["text"]
    return chunks


def retrieve_similar_chunks(query, country, model, top_k=TOP_K_RETRIEVAL):
    start = time.time()
    index, chunk_ids = load_index_and_metadata(country)
    query_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(query_emb, top_k)

    top_ids = [chunk_ids[i] for i in I[0]]
    top_chunks = load_chunks_by_id(country, top_ids)
    print(f"[Retrieval] Retrieved {len(top_ids)} chunks in {time.time() - start:.2f} sec")

    return [(top_chunks[chunk_ids[i]], chunk_ids[i], D[0][idx]) for idx, i in enumerate(I[0])]


def generate_answer(query, context_chunks):
    start = time.time()
    context_parts = []
    total_chars = 0
    for chunk, _, _ in context_chunks:
        if total_chars + len(chunk) > MAX_CONTEXT_CHARS:
            break
        context_parts.append(chunk)
        total_chars += len(chunk)

    context = "\n\n".join(context_parts)
    sources = [chunk_id for _, chunk_id, _ in context_chunks]

    print(f"[Context] {len(context)} chars (~{len(context.split())} words)")

    prompt = f"""Contesta la siguiente pregunta usando únicamente la información provista.
        Contexto:
        {context}

        Pregunta:
        {query}

        Respuesta (incluye una sección de Fuentes al final):
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    answer = response.choices[0].message.content
    sources_text = "\n\nFuentes:\n" + "\n".join(sources)
    references = "\n\nReferencias utilizadas:\n" + "\n\n".join(
        [f"[{chunk_id}]: {chunk}" for chunk, chunk_id, _ in context_chunks]
    )
    
    print(f"[Generation] LLM response generated in {time.time() - start:.2f} sec")

    return answer + sources_text + "\n\n" + references 


def ask_question(query, country):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = retrieve_similar_chunks(query, country, model)
    answer = generate_answer(query, chunks)
    return answer


if __name__ == "__main__":
    question = "¿Qué dice la Comunicación A7759 sobre las stablecoins?"
    print(ask_question(question, country="argentina"))