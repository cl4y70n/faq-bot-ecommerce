# rag.py - retrieve top-K and call LLM (abstracted)
import os
from chromadb.config import Settings
import chromadb
from sentence_transformers import SentenceTransformer
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import numpy as np

client = chromadb.Client(Settings())
collection = client.get_collection('products')
embed_model = SentenceTransformer(os.getenv('HF_EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2'))

PROMPT = """You are a helpful e-commerce assistant. Use the retrieved snippets to answer concisely.

Retrieved snippets:
{snippets}

Question: {question}

Answer concisely, cite sources as [product_id:chunk_index]. If info not available, reply "I don't know, ask support".
"""

def retrieve_snippets(query, k=4):
    q_emb = embed_model.encode([query])[0].tolist()
    results = collection.query(query_embeddings=[q_emb], n_results=k)
    docs = results['documents'][0]
    mets = results['metadatas'][0]
    ids = results['ids'][0]
    snippets = []
    for d, m, id_ in zip(docs, mets, ids):
        snippets.append({'doc': d, 'meta': m, 'id': id_})
    return snippets

def answer_query(question):
    snippets = retrieve_snippets(question, k=4)
    joined = "\n---\n".join([f"[{s['meta'].get('product_id')}:{s['meta'].get('chunk_index')}] {s['doc']}" for s in snippets])
    prompt = PROMPT.format(snippets=joined, question=question)
    # call LLM
    provider = os.getenv('LLM_PROVIDER', 'openai')
    if provider == 'openai':
        llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
        chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=['snippets','question'], template=PROMPT))
        out = chain.run(snippets=joined, question=question)
    else:
        # fallback simple answer
        out = "I don't know, ask support."
    sources = [s['meta'] for s in snippets]
    return out, sources
