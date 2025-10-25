# FAQ Bot for E-commerce (MVP) — FastAPI + RAG

**Overview**
Lightweight FAQ chatbot for e-commerce stores using RAG (LangChain + Chroma) with a simulated Shopify dataset.
Built with FastAPI, Redis cache, and Docker Compose for local demo.

**Quickstart**
1. Copy `.env.example` to `.env` and set `API_KEY`.
2. Run: `docker compose up --build`
3. Open demo: `http://localhost:8000/static/demo.html`
4. API docs: `http://localhost:8000/docs`

**Features**
- Ingest products (simulated Shopify JSON)
- Index product descriptions into Chroma (embeddings)
- RAG-driven responses via LangChain prompt templates
- Redis caching for repeated queries
- Simple chat widget (static HTML) for demo

**Structure**
- `app/` backend code
- `data/` sample products
- `docker-compose.yml`, `Dockerfile`, `.env.example`

