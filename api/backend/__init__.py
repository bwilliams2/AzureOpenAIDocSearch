import logging
import os
import json
from typing import Union, Optional

import azure.functions as func

from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import text
import sqlalchemy as sa

from doc_utils.orm import Document, Embedding
from doc_utils.db import get_engine
from doc_utils.llm import get_embedding, Chat, DocumentChat


app = FastAPI()

blob_connection_str = os.getenv("BLOB_CONNECTION_STR")


class DBDocument(BaseModel):
    id: int
    blob_path: str
    full_text: Optional[str]
    file_hash: str
    title: str
    authors: list[str]
    keywords: list[str]
    page_summaries: Optional[str]
    summary: str


def document_mapper(doc: Document):
    doc = doc.__dict__.copy()
    del doc["_sa_instance_state"]
    del doc["page_summaries"]
    del doc["full_text"]
    return doc


@app.get("/search")
async def embedding_search(
    content: str, skip: int = 0, limit: int = 10
) -> list[DBDocument]:
    print("searching")
    embedding = json.dumps(get_embedding(content))
    engine = get_engine()
    with Session(engine) as session:
        cte = (
            sa.select(
                Embedding.doc_id,
                text(f"MIN(embedding <=> '{embedding}') AS vector_distance"),
            )
            .group_by(Embedding.doc_id)
            .order_by(text("vector_distance"))
            .offset(skip)
            .limit(limit)
            .cte(name="distances")
        )
        results = (
            session.query(Document)
            .join(cte, cte.c.doc_id == Document.id)
            .order_by(text("distances.vector_distance"))
            .all()
        )
        docs = [document_mapper(doc) for doc in results]
    return docs


@app.post("/qna")
async def submit_chat(chat: Chat) -> Chat:
    engine = get_engine()
    with Session(engine) as session:
        doc = session.query(Document).filter(Document.id == chat.doc_id).first()
    chat.document = doc.summary

    chat_gen = DocumentChat(chat)
    next_chat = chat_gen.predict()

    return next_chat


@app.post("/newdocument")
async def upload_document(file: UploadFile = File()):
    return {"file_size": file.filename}


@app.post("/qna")
async def document_chat():
    return


async def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the ASGI handler."""
    return await func.AsgiMiddleware(app).handle_async(req, context)
