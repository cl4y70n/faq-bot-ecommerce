# FAQ Bot for E-commerce (MVP)

## Overview

FAQ Bot is an intelligent chatbot for e-commerce stores that answers customer questions using product data. It leverages **RAG (Retrieval-Augmented Generation)** with **LangChain** and **Chroma** embeddings for accurate responses. The system integrates with **Shopify/WooCommerce** (simulated) and supports Redis caching. It is lightweight and can be tested locally using Docker.

---

## Features

* Ingest product data (JSON from Shopify/WooCommerce)
* Index product descriptions into Chroma for semantic search
* RAG-driven answers using LangChain and embeddings
* Redis caching for faster repeated queries
* Simple web demo with chat interface
* Logs user queries and responses in SQLite

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/faq-bot-ecommerce.git
cd faq-bot-ecommerce
```

### 2. Configure environment

Copy `.env.example` to `.env` and set your API keys:

```bash
cp .env.example .env
```

Update:

* `API_KEY` – custom API key for endpoints
* `OPENAI_API_KEY` – if using OpenAI as LLM
* `REDIS_URL` – Redis connection string
* `CHROMA_DIR` – local directory for Chroma DB
* `HF_EMBEDDING_MODEL` – Hugging Face embedding model

### 3. Run with Docker Compose

```bash
docker compose up --build
```

* API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* Demo chat: [http://localhost:8000/static/demo.html](http://localhost:8000/static/demo.html)

---

## Project Structure

```
faq-bot-ecommerce/
├─ app/                    # Backend source code
│  ├─ main.py              # FastAPI endpoints
│  ├─ ingest.py            # Product ingestion
│  ├─ indexer.py           # Chunking & embeddings
│  ├─ rag.py               # RAG pipeline for query
│  ├─ db.py                # SQLite query logs
│  └─ worker.py            # Background worker (placeholder)
├─ data/
│  └─ sample_products.json # Sample product dataset
├─ static/
│  └─ demo.html            # Simple chat interface
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## API Endpoints

### `/ingest` (POST)

Ingests products from a JSON file or default sample products.

* Headers: `x-api-key: <API_KEY>`
* File: optional upload
* Response: `{"ingested": <number_of_products>}`

### `/query` (POST)

Ask a question about products.

* Headers: `x-api-key: <API_KEY>`
* Body: `{"q": "question text"}`
* Response:

```json
{
  "answer": "generated answer",
  "sources": [{"product_id":"p1","title":"Product Title","chunk_index":0}, ...]
}
```

### `/logs` (GET)

Returns last 200 queries and responses (SQLite).

---

## Embeddings & RAG

* Uses **SentenceTransformers** (`all-MiniLM-L6-v2`) for embedding product text.
* Chunks product descriptions and stores embeddings in **Chroma**.
* RAG pipeline retrieves top-K relevant chunks and passes to LLM (OpenAI or other).
* Optional caching via Redis.

---

## Docker & Deployment

* Uses **Docker Compose** with 3 services: `web`, `redis`, `chroma`, plus optional `worker`.
* Local test/demo ready.
* Can be deployed to cloud platforms (AWS, GCP, Azure) with environment variables.

---

## Sample Products

Stored in `data/sample_products.json`:

```json
{
  "products": [
    {"id": "p1", "title": "Sneaker Classic", "description": "Comfortable sneaker with rubber sole..."},
    {"id": "p2", "title": "Waterproof Jacket", "description": "Lightweight waterproof jacket..."}
  ]
}
```

---

## Next Steps

* Connect to live Shopify/WooCommerce store via API
* Improve LLM integration (OpenAI, local LLaMA)
* Add authentication (JWT) and admin panel
* Advanced caching strategies
* Production deployment with CI/CD

---

## License

MIT License

---

Quer que eu faça isso agora?

