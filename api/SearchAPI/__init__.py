import logging
import os
import json

import azure.functions as func

from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text

from doc_utils.orm import Document, Snippet, Embedding, get_engine
from doc_utils.db import get_engine
from doc_utils.openai import get_embedding




app = FastAPI()

blob_connection_str = os.getenv("BLOB_CONNECTION_STR")


@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route.",
    }

@app.get("/search/")
async def embedding_search(content: str, skip: int=0, limit:int=10):
    embedding = json.dumps(get_embedding(content))
    engine = get_engine()
    with Session(engine) as session:
        session.query(Embedding).select().order_by(text(f"embedding <-> '{embedding}'")).all()



@app.post("/newdocument")
async def upload_document(file: UploadFile=File()):
    return {"file_size": file.filename}

@app.get("/hello/{name}")
async def get_name(name: str):
    return {
        "name": name,
    }

async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(app).handle_async(req, context)