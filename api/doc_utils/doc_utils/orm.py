from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Text, ARRAY
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    blob_path: Mapped[str] = mapped_column(Text)
    full_text: Mapped[str] = mapped_column(Text)
    file_hash: Mapped[str] = mapped_column(Text)
    title: Mapped[Optional[str]] = mapped_column(Text)
    authors: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    keywords: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    page_summaries: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    summary: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, blob_path={self.blob_path!r}, summary={self.summary!r})"


class Snippet(Base):
    __tablename__ = "snippets"

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    snippet_type: Mapped[str] = mapped_column(Text)
    full_text: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Snippet(id={self.id!r}, doc_id={self.doc_id!r}, snippet_type={self.summary!r})"


class Embedding(Base):
    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    doc_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    snippet_id: Mapped[Optional[int]] = mapped_column(ForeignKey("snippets.id"))
    embedding: Mapped[str] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"Embedding(id={self.id!r}, doc_id={self.doc_id!r}, snippet_id={self.snippet_id!r})"
