import logging
import os
import json

import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from doc_utils.llm import get_authors, get_keywords, get_summaries


from sqlalchemy.orm import Session

from doc_utils.orm import Document, Summary, Embedding, get_engine
from doc_utils.db import get_engine

endpoint = "https://<my-custom-subdomain>.cognitiveservices.azure.com/"
credential = AzureKeyCredential("<api_key>")
document_analysis_client = DocumentAnalysisClient(endpoint, credential)


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    poller = document_analysis_client.begin_analyze_document("prebuilt-document", myblob.read())
    result = poller.result()
    text = result.content


    summaries = get_summaries(text)

    # Fill document and summary tables
    engine = get_engine()
    doc = Document(blob_path=myblob.name, full_text=result.content, summary=outputs["output_text"])
    with Session(engine) as session:
        session.add(doc) 
        session.commit()
        session.refresh(doc)
    
    summaries = []
    with Session(engine) as session:
        for summary_text in summaries["intermediate_steps"]:
            summary = Summary(doc_id=doc.id, full_text=summary_text)
            session.add(summary)
            session.commit()
            session.refresh(summary)
            summaries.append(summary)

    # Create embeddings

    with Session(engine) as session:
        for summary in summaries:
            sum_embedding = Embedding(doc_id=doc.id, summary_id=summary.id, embedding=json.dumps(get_embedding(summary.full_text)))
            session.add(sum_embedding)
            session.commit()

    return
    
        
    
