# indexer: chunk text and create embeddings, upsert to chroma
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

EMBED_MODEL = os.getenv('HF_EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
client = chromadb.Client(Settings())
collection = client.get_or_create_collection(name='products')
embed_model = SentenceTransformer(EMBED_MODEL)

def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunks.append(' '.join(words[i:i+chunk_size]))
        i += chunk_size
    return chunks

def index_product_chunks(prod_id, text, metadata=None):
    chunks = chunk_text(text, chunk_size=100)
    embeddings = embed_model.encode(chunks).tolist()
    ids = [f"{prod_id}_{i}" for i in range(len(chunks))]
    metadatas = [ {**(metadata or {}), 'product_id': prod_id, 'chunk_index': i} for i in range(len(chunks))]
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=chunks)
    return len(chunks)
