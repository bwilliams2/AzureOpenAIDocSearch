import logging
import os
import json
from hashlib import md5

import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


from doc_utils.db import insert_document

endpoint = os.getenv("AFR_ENDPOINT")
api_key = os.getenv("AFR_KEY")
credential = AzureKeyCredential(api_key)
document_analysis_client = DocumentAnalysisClient(endpoint, credential)


def main(myblob: func.InputStream):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Name: {myblob.name}\n"
        f"Blob Size: {myblob.length} bytes"
    )
    data = myblob.read()
    poller = document_analysis_client.begin_analyze_document("prebuilt-document", data)
    result = poller.result()
    text = result.content
    file_hash = str(md5(data).hexdigest)
    insert_document(text, myblob.name, file_hash)
