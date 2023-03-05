import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .llm import TextExtraction, get_embedding
from .orm import Document, Snippet, Embedding


def get_engine():
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_hostname = os.getenv("DATABASE_HOSTNAME")
    database_name = os.getenv("DATABASE_NAME")
    return create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_hostname}/{database_name}')


def insert_document(
    extracted_text: TextExtraction,
    blob_path: str,
    file_hash: str
):

    engine = get_engine()
    session = Session(engine)
    try:
        doc = Document(
            blob_path=blob_path,
            full_text=extracted_text.full_text,
            file_hash=file_hash,
            title=extracted_text.title,
            authors=extracted_text.authors,
            keywords=extracted_text.keywords,
            page_summaries=extracted_text.intermediate_summaries,
            summary=extracted_text.summary
        )
        session.add(doc)
        session.commit()
        
        doc_embedding = Embedding(
            doc_id=doc.id,
            embedding=json.dumps(get_embedding(doc.summary))
        )
        embeddings = [doc_embedding]

        if len(extracted_text.keywords) > 0:
            text=" ".join(extracted_text.keywords)
            keyword_snippet = Snippet(
                doc_id=doc.id,
                snippet_type="keywords",
                text=text
            )
            session.add(keyword_snippet)
            session.commit()

            embeddings.append(
                Embedding(
                    doc_id=doc.id,
                    snippet_id=keyword_snippet.id,
                    embedding=json.dumps(get_embedding(text))
                )
            )

        if len(extracted_text.authors) > 0:
            text=" ".join(extracted_text.authors)
            author_snippet = Snippet(
                doc_id=doc.id,
                snippet_type="authors",
                text=text
            )
            session.add(author_snippet)
            session.commit()

            embeddings.append(
                Embedding(
                    doc_id=doc.id,
                    snippet_id=author_snippet.id,
                    embedding=json.dumps(get_embedding(text))
                )
            )

        for summary in extracted_text.intermediate_summaries:
            snippet = Snippet(
                doc_id=doc.id,
                snippet_type="intermediate_summary",
                text=summary
            )
            session.add(snippet)
            session.commit()

            snippet_embedding = Embedding(
                doc_id=doc.id,
                snippet_id=snippet.id,
                embedding=json.dumps(get_embedding(snippet.text))
            )
            embeddings.append(snippet_embedding)

        session.add_all(embeddings)
        session.commit()

    finally:
        session.close()

    

