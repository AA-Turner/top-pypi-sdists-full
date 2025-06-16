import logging
import os
from typing import List, Dict

# LlamaIndex components
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.langchain import LangChainLLM
from langchain_groq import ChatGroq
from llama_index.core.schema import Document

# Custom data models
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.rag.rag_interface import RagInterface
from ragformance.rag.config import MultiEmbeddingLLMRagConfig

logger = logging.getLogger(__name__)

# A custom class that supports multiple embedding models and LLMs for querying a shared corpus.
class MultiEmbeddingLLM(RagInterface):
    def __init__(self, config: MultiEmbeddingLLMRagConfig):
        self.config = config
        # Holds indexes per embedding model name
        self.indexes: Dict[str, VectorStoreIndex] = {}
        # Holds embedding models keyed by name
        self.embeddings: Dict[str, HuggingFaceEmbedding] = {}
        # The uploaded corpus documents
        self.documents: List[DocModel] = []
        # Note: self.config is now a MultiEmbeddingLLMRagConfig instance


    # Load a corpus and create a vector index for each embedding model in the config
    def upload_corpus(self, corpus: List[DocModel]) -> int:
        self.documents = corpus

        # Extract config values from self.config (Pydantic model)
        embedding_models_cfg = self.config.EMBEDDING_MODELS
        corpus_key = self.config.CORPUS_TEXT_KEY

        # Loop through each embedding model and build a vector index
        for emb_name, model_name in embedding_models_cfg.items():
            logger.info(f"Loading embedding model '{emb_name}': {model_name}")
            embedding = HuggingFaceEmbedding(model_name=model_name)

            # Convert custom DocModel to LlamaIndex Document
            docs = [
                Document(
                    text=getattr(doc, corpus_key), # Using getattr for safety, though direct access should work if key is always 'text'
                    doc_id=doc.id,
                    metadata={"doc_id": doc.id}
                )
                for doc in corpus
            ]

            # Create index using this embedding model
            index = VectorStoreIndex.from_documents(docs, embed_model=embedding)

            self.indexes[emb_name] = index
            self.embeddings[emb_name] = embedding

        logger.info(f"{len(self.indexes)} indexes created from {len(self.documents)} documents.")
        return len(self.documents)

    # Query each (embedding, LLM) combination and collect responses
    def ask_queries(self, queries: List[AnnotatedQueryModel]) -> List[AnswerModel]:
        if not self.indexes:
            raise RuntimeError("You must call upload_corpus() before ask_queries().")

        # Access config values from self.config (Pydantic model)
        # Use os.getenv as a fallback for groq_api_key, but prefer the config
        groq_key = self.config.GROQ_API_KEY or os.getenv("groq_api_key")
        if not groq_key:
            # If still not found, then raise error.
             if not self.config.GROQ_API_KEY:
                raise ValueError("Missing 'GROQ_API_KEY' in config and 'groq_api_key' environment variable.")
             groq_key = self.config.GROQ_API_KEY


        queries_key = self.config.QUERIES_TEXT_KEY
        llms_cfg = self.config.LLMS
        top_k = self.config.SIMILARITY_TOP_K # This is SIMILARITY_TOP_K from the Pydantic model

        answers: List[AnswerModel] = []

        # Iterate over queries
        for query in queries:
            # Extract query text
            query_text = getattr(query, queries_key, None) or getattr(query, "query_text", None)
            if not query_text:
                logger.warning(f"Missing query text for query_id={query.id}, skipping.")
                continue

            # For each embedding model used
            for emb_name, index in self.indexes.items():
                embedding = self.embeddings[emb_name]

                # For each LLM used
                for llm_name, llm_model in llms_cfg.items():
                    try:
                        # Initialize the LLM with Groq backend
                        llm = LangChainLLM(llm=ChatGroq(api_key=groq_key, model_name=llm_model))

                        # Create a query engine using this (embedding, LLM) pair
                        query_engine = index.as_query_engine(
                            llm=llm,
                            embed_model=embedding,
                            similarity_top_k=top_k,
                            response_mode="compact"
                        )

                        # Run the query
                        response = query_engine.query(query_text)

                        # Extract document IDs from source nodes
                        retrieved_ids = [
                            node.node.metadata.get("doc_id", node.node.node_id)
                            for node in response.source_nodes
                        ]

                        # Wrap the response in the AnswerModel schema
                        answer = AnswerModel(
                            _id=str(query.id),
                            query=query,
                            model_answer=response.response,
                            retrieved_documents_ids=retrieved_ids,
                            embedding_model_name=emb_name,
                            llm_model_name=llm_name,
                        )
                        answers.append(answer)

                    except Exception as e:
                        logger.error(f"Error for {emb_name} / {llm_name} (query_id={query.id}): {e}")

        return answers
