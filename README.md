# LatamLex 🧠🌎
**Fintech & Crypto Regulatory Assistant for LATAM using LLM + RAG**

LatamLex is an intelligent assistant that answers questions about financial and crypto regulations in Argentina, Brazil, Mexico, and Chile. It uses a Retrieval-Augmented Generation (RAG) pipeline with semantic embeddings, FAISS search, and answer generation via LLM (like GPT-4).

## 🚀 Features

- ✅ Query laws, regulations, and resolutions by country
- ✅ Ingest legal PDFs and HTMLs
- ✅ Chunking and embeddings using `sentence-transformers`
- ✅ Semantic search with FAISS
- ✅ Contextual answers with source references and full fragments
- ✅ Simple interface via Streamlit
- ✅ Docker container for local demo

## 📦 Requirements

- Python 3.10+
- OpenAI API Key
- (Optional) Docker

## 🛠️ Local Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/0xregulus/latamlex.git
cd latamlex
make venv
```

Create a `.env` file with your OpenAI credentials:

```env
OPENAI_API_KEY=your_openai_key_here
MAX_CONTEXT_CHARS=12000
TOP_K_RETRIEVAL=5
```

Install dependencies and prepare the data:

```bash
make venv
make all
```

Launch the app:

```bash
make app
```

Or run everything manually:

```bash
source .venv/bin/activate
python app/ingest.py
python app/chunker.py
python app/embedder.py
streamlit run app/interface.py
```

## 🐳 Using Docker

```bash
docker build -t latamlex .
docker run -p 8501:8501 --env-file .env latamlex
```

Or with Docker Compose:

```bash
docker-compose up --build
```

Or using Makefile:

```bash
make docker      # builds and runs the container
make compose     # runs docker-compose up --build
```

## 📁 Project Structure

```
LatamLex/
├── app/                   # Core code: ingestion, chunking, embeddings, retrieval, QA, interface
│   ├── ingest.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── qa_chain.py
│   └── interface.py
├── data/                  # Input data organized by country
│   ├── argentina/
│   ├── brasil/
│   ├── mexico/
│   └── chile/
├── vectorstore/           # FAISS indexes and metadata
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## 🧪 Example Question

> What does Mexican law say about Financial Technology Institutions?

The app will retrieve the most relevant fragments from the Mexican legal documents, generate an answer, and display the sources used.

## 👨‍💻 Credits

Project created by [Facundo Rodríguez](https://github.com/0xregulus) as a demo of using LLMs and RAG in the fintech-regulatory domain.
