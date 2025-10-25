from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from .ingest import ingest_products_from_file, SAMPLE_PRODUCTS_PATH
from .rag import answer_query
from .db import init_db, save_query_log, get_logs
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY', 'changeme123')
UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title='FAQ Bot E-commerce (MVP)')
app.mount('/static', StaticFiles(directory='static'), name='static')

init_db()

def api_key_auth(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Invalid API Key')
    return True

@app.post('/ingest', dependencies=[Depends(api_key_auth)])
async def ingest(file: UploadFile | None = File(None)):
    # If no file, ingest sample products
    if file:
        path = UPLOAD_DIR / file.filename
        with open(path, 'wb') as f:
            f.write(await file.read())
        count = ingest_products_from_file(str(path))
    else:
        count = ingest_products_from_file(SAMPLE_PRODUCTS_PATH)
    return {'ingested': count}

@app.post('/query', dependencies=[Depends(api_key_auth)])
async def query(payload: dict):
    q = payload.get('q') if isinstance(payload, dict) else None
    if not q:
        raise HTTPException(status_code=400, detail='q is required')
    answer, sources = answer_query(q)
    save_query_log(q, answer, sources)
    return JSONResponse({'answer': answer, 'sources': sources})

@app.get('/logs', dependencies=[Depends(api_key_auth)])
def logs():
    return get_logs()

@app.get('/', response_class=HTMLResponse)
def home():
    html = Path('static/demo.html').read_text(encoding='utf-8')
    return HTMLResponse(html)
