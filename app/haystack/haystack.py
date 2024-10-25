import sys
from haystack import Pipeline, Document
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.embedders import OpenAIDocumentEmbedder, OpenAITextEmbedder
from haystack.components.writers import DocumentWriter
from haystack.components.retrievers import InMemoryEmbeddingRetriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.utils import Secret

from ..core.config import Settings

settings = Settings()

import logging

logger = logging.getLogger(__name__)

class RAG:
    def __init__(self):
        self.prompt_template = """
        Given these documents, answer the question.
        Documents:
        {% for doc in documents %}
            Document {{ loop.index }}:
            Document metadata: {{ doc.meta }}
            {{ doc.content }}
        {% endfor %}
        Question: {{question}}
        Answer:

        Note: Each document is a JSON tweet object represented as a string, containing three keys: Id, Author, and Content.
        The total number of documents corresponds to the number of tweets.
        The AI should base its answers on the information contained in these document/tweet units.
        """
        self.document_store = InMemoryDocumentStore(embedding_similarity_function='cosine')
        self.indexing_pipeline = Pipeline()
        self.query_pipeline = Pipeline()
    
    def embedding(self, file_contents: list[Document]) -> list[Document]:
        self.document_store = InMemoryDocumentStore(embedding_similarity_function='cosine')
        self.documents = []
        total_size = 0
        for i, file_content in enumerate(file_contents):
            doc = Document(content=file_content['Content'], meta={'Id': file_content['Id'], 'Author': file_content['Author']})
            self.documents.append(doc)
            doc_size = sys.getsizeof(doc.content)
            total_size += doc_size
            logger.info(f"Document {i+1}: size = {doc_size} bytes")

        logger.info(f"Total number of documents: {len(self.documents)}")
        logger.info(f"Total size of all documents: {total_size} bytes")
        logger.info(f"Average document size: {total_size / len(self.documents):.2f} bytes")

        self.indexing_pipeline.add_component("embedder", OpenAIDocumentEmbedder(api_key=Secret.from_token(settings.OPENAI_API_KEY), meta_fields_to_embed=['Id', 'Author']))
        self.indexing_pipeline.add_component("writer", DocumentWriter(document_store=self.document_store))
        self.indexing_pipeline.connect("embedder", "writer")
        embedding_results = self.indexing_pipeline.run({"embedder": {"documents": self.documents}})
        logger.info(f"Embedding result: {embedding_results}")

        self.query_pipeline.add_component("text_embedder", OpenAITextEmbedder(api_key=Secret.from_token(settings.OPENAI_API_KEY)))
        self.query_pipeline.add_component("retriever", InMemoryEmbeddingRetriever(document_store=self.document_store, top_k=len(self.documents)))
        self.query_pipeline.add_component("prompt_builder", PromptBuilder(template=self.prompt_template))
        self.query_pipeline.add_component("llm", OpenAIGenerator(api_key=Secret.from_token(settings.OPENAI_API_KEY)))
        self.query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        self.query_pipeline.connect("retriever.documents", "prompt_builder")
        self.query_pipeline.connect("prompt_builder", "llm")

        logger.info(f"Documents in store: {self.document_store.count_documents()}")
        logger.info(f"Pipeline connections: {self.query_pipeline.graph.edges}") 

    def get_answer(self, question: str) -> str:
        logger.info(f"Number of documents in store: {self.document_store.count_documents()}")
        query_pipeline_output = self.query_pipeline.run(
            {
                "text_embedder": {"text": question},
                "prompt_builder": {"question": question}
             }
        )
        logger.info(f"Query pipeline output: {query_pipeline_output}")
        return query_pipeline_output["llm"]["replies"][0]