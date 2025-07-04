# Makefile for LatamLex

# Variables
PYTHON=python
PIP=pip

# Environment
venv:
	python -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip && $(PIP) install -r requirements.txt

# Document ingestion
ingest:
	. .venv/bin/activate && $(PYTHON) app/ingest.py

# Chunking
chunk:
	. .venv/bin/activate && $(PYTHON) app/chunker.py

# Embeddings
embed:
	. .venv/bin/activate && $(PYTHON) app/embedder.py

# Run Streamlit app
app:
	. .venv/bin/activate && streamlit run app/interface.py

# Run full pipeline
all: ingest chunk embed

# Clean output folders
clean:
	rm -rf data/*/clean/*
	rm -rf data/*/chunks/*
	rm -rf vectorstore

# Docker
docker:
	docker build -t latamlex .
	docker run -p 8501:8501 --env-file .env latamlex

compose:
	docker-compose up --build

# Run tests
test:
	. .venv/bin/activate && PYTHONPATH=. pytest -v

.PHONY: venv ingest chunk embed app all clean docker compose test
