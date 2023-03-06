import os

from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain import OpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document as LLMDocument
import openai


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)["data"][0]["embedding"]


class TextExtraction(object):
    def __init__(
        self,
        text: str,
    ):
        self._text = text
        self._split_document()
        self._authors = None
        self._keywords = None
        self._summary = None
        self._intermediate_summaries = None
        self._embeddings = None
        self._title = None

    def _split_document(self):
        text_splitter = CharacterTextSplitter(separator="\n")
        texts = text_splitter.split_text(self._text)
        self._text_splits = [LLMDocument(page_content=t) for t in texts]

    @property
    def full_text(self):
        return self._text

    @property
    def text_splits(self):
        return [split.page_content for split in self._text_splits]

    @staticmethod
    def _author_chain():
        llm = OpenAI(temperature=0)
        author_template = (
            "Who are the authors of the text below? If there are no authors found,"
            "return 'WARNING: No authors identified'. Remove all numbers and special characters "
            "from response.\n\n{text}\n\nAUTHORS:"
        )
        author_prompt = PromptTemplate(
            input_variables=["text"], template=author_template
        )
        return LLMChain(llm=llm, prompt=author_prompt)

    @property
    def authors(self):
        if self._authors is None:
            author_chain = self._author_chain()

            self._authors = []
            for text_doc in self._text_splits:
                res = author_chain.run(text_doc.page_content)
                if "WARNING" not in res:
                    # Assume authors were found
                    self._authors = [author.strip() for author in res.split(",")]
                    break
        return self._authors

    @staticmethod
    def _keyword_chain():
        llm = OpenAI(temperature=0)
        keyword_template = (
            "Extract at most ten keywords from the text below. If there are no keywords found,"
            "return 'WARNING: No keywords identified'."
            "\n\n{text}\n\nKeywords:"
        )
        keyword_prompt = PromptTemplate(
            input_variables=["text"], template=keyword_template
        )
        return LLMChain(llm=llm, prompt=keyword_prompt)

    @property
    def keywords(self):
        if self._keywords is None:
            keyword_chain = self._keyword_chain()
            keywords = []
            for text_doc in self._text_splits:
                res = keyword_chain.run(text_doc.page_content)
                if "WARNING" not in res:
                    keywords += [keyword.strip() for keyword in res.split(",")]
                    break
            self._keywords = list(set(keywords))
        return self._keywords

    @staticmethod
    def _title_chain():
        llm = OpenAI(temperature=0)
        title_template = (
            "What is the title of the paper below?. If there is no title found,"
            "return 'WARNING: No title identified'."
            "\n\n{text}\n\nTITLE:"
        )
        title_prompt = PromptTemplate(input_variables=["text"], template=title_template)
        return LLMChain(llm=llm, prompt=title_prompt)

    @property
    def title(self):
        if self._title is None:
            title_chain = self._title_chain()
            title = ""
            for text_doc in self._text_splits:
                res = title_chain.run(text_doc.page_content)
                if "WARNING" not in res:
                    title += res.strip()
                    break
            self._title = title
        return self._title

    def _process_summary(self):
        llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))

        prompt_template = """Your job is to produce a concise and informative summary of the following:


        {text}


        INFORMATIVE SUMMARY:"""
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            return_intermediate_steps=True,
            map_prompt=PROMPT,
            combine_prompt=PROMPT,
        )
        outputs = chain(
            {"input_documents": self._text_splits}, return_only_outputs=True
        )
        self._summary = outputs["output_text"].strip()
        self._intermediate_summaries = [
            sum.strip() for sum in outputs["intermediate_steps"]
        ]

    @property
    def intermediate_summaries(self):
        if self._intermediate_summaries is None:
            self._process_summary()
        return self._intermediate_summaries

    @property
    def summary(self):
        if self._summary is None:
            self._process_summary()
        return self._summary
