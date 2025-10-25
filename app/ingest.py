import json
from pathlib import Path
from .indexer import index_product_chunks

SAMPLE_PRODUCTS_PATH = 'data/sample_products.json'

def ingest_products_from_file(path: str):
    p = Path(path)
    data = json.loads(p.read_text(encoding='utf-8'))
    count = 0
    for prod in data.get('products', []):
        text = f"{prod.get('title','')}\n{prod.get('description','')}"
        # index into vector DB
        index_product_chunks(prod['id'], text, metadata={'title': prod.get('title')})
        count += 1
    return count
