
CREATE DATABASE embeddingsearch;
\c embeddingsearch

CREATE EXTENSION dblink;
CREATE EXTENSION vector;

CREATE TABLE IF NOT EXISTS embeddings (
   id SERIAL PRIMARY KEY NOT NULL,
   doc_id INT NOT NULL,
   snippet_id INT,
   embedding vector NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY NOT NULL,
    blob_path TEXT NOT NULL,
    full_text TEXT NOT NULL,
    file_hash TEXT NOT NULL,
    title TEXT,
    authors TEXT[],
    keywords TEXT[],
    page_summaries TEXT[],
    summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS snippets (
    id SERIAL PRIMARY KEY NOT NULL,
    doc_id INT NOT NULL,
    snippet_type TEXT NOT NULL,
    full_text TEXT NOT NULL
);