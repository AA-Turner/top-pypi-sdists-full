from typing import Dict, List
import requests
import json

try:
    from haystack.document_stores import InMemoryDocumentStore
    from haystack.nodes import EmbeddingRetriever, FARMReader
    from haystack.pipelines import ExtractiveQAPipeline
    from haystack.schema import Document
    _HAYSTACK_AVAILABLE = True
except ImportError:
    _HAYSTACK_AVAILABLE = False
    InMemoryDocumentStore = None
    EmbeddingRetriever = None
    FARMReader = None
    ExtractiveQAPipeline = None
    Document = None

try:
    from sentence_transformers import SentenceTransformer
    _SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    _SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

from ragformance.rag.rag_interface import RagInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.rag.config import HaystackRagConfig

class OllamaLLMReader:
    def __init__(self, base_url: str, model: str, temperature: float = 0.2, max_tokens: int = 3000):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def predict(self, query: str, context: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"Question: {query}\nContext: {context}\nAnswer:",
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": True
        }

        response = requests.post(f"{self.base_url}/api/generate", json=payload, stream=True)

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code} {response.text}")

        output = ""
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = line.decode("utf-8")
                chunk = json.loads(data)
                output += chunk.get("response", "")
            except Exception as e:
                raise RuntimeError(f"Failed to parse Ollama output: {e}")

        return output.strip()

class HaystackRAG(RagInterface):
    def __init__(self, config: HaystackRagConfig) -> None:
        if not _HAYSTACK_AVAILABLE:
            raise ImportError(
                "'farm-haystack' module is not installed. "
                "Please install ragformance with the [rag-haystack] option:\n"
                "    pip install ragformance[rag-haystack]"
            )
        if not _SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError(
                "'sentence-transformers' module is not installed. "
                "Please install ragformance with the [rag-haystack] option:\n"
                "    pip install ragformance[rag-haystack]"
            )
            
        self.config = config
        # It seems SentenceTransformer is used here just to get embedding_dim.
        # Haystack's EmbeddingRetriever handles the actual embedding model.
        temp_embedding_model = SentenceTransformer(self.config.EMBEDDING_MODEL_NAME)
        dummy_vector = temp_embedding_model.encode(["dummy"])[0]
        embedding_dim = len(dummy_vector)
        
        self.document_store = InMemoryDocumentStore(use_bm25=False, embedding_dim=embedding_dim)
        self.retriever = EmbeddingRetriever(
            document_store=self.document_store,
            embedding_model=self.config.EMBEDDING_MODEL_NAME,
            use_gpu=False # Consider making this configurable if needed
        )
        
        if self.config.OLLAMA_MODEL and self.config.OLLAMA_URL:
            self.reader = OllamaLLMReader(
                base_url=self.config.OLLAMA_URL,
                model=self.config.OLLAMA_MODEL
            )
            self.use_ollama = True
        else:
            # Default to FARMReader if Ollama is not configured
            self.reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False) # Consider making model_name_or_path configurable
            self.pipeline = ExtractiveQAPipeline(reader=self.reader, retriever=self.retriever)
            self.use_ollama = False

    def upload_corpus(self, corpus: List[DocModel]) -> int:
        documents = [
            Document(
                content=doc.text,
                meta={"corpus_id": doc.id, "title": doc.title, **(doc.metadata or {})}
            )
            for doc in corpus
        ]
        self.document_store.write_documents(documents)
        self.document_store.update_embeddings(self.retriever) # This uses the retriever's embedding model
        return len(documents)

    def ask_queries(self, queries: List[AnnotatedQueryModel]) -> List[AnswerModel]: # Removed config: Dict
        results = []
        # top_k for retriever and reader could be made configurable via HaystackRagConfig
        # For now, using the existing hardcoded values (3 for retriever, 1 for reader)
        retriever_top_k = 3 
        reader_top_k = 1

        for query in queries:
            retrieved_docs = self.retriever.retrieve(query.query_text, top_k=retriever_top_k)

            if self.use_ollama:
                context = "\n".join([doc.content for doc in retrieved_docs])
                answer_text = self.reader.predict(query.query_text, context)

                doc_ids = [doc.meta.get("corpus_id") for doc in retrieved_docs]
                scores = [doc.score for doc in retrieved_docs]

            else:
                prediction = self.pipeline.run(
                    query=query.query_text,
                    params={"Retriever": {"top_k": retriever_top_k}, "Reader": {"top_k": reader_top_k}}
                )

                answers = prediction.get("answers", [])
                documents = prediction.get("documents", [])
                answer_text = answers[0].answer if answers else ""

                doc_ids = [doc.meta.get("corpus_id") for doc in documents]
                scores = [doc.score for doc in documents]

            results.append(AnswerModel(
                _id=query.id,
                query=query,
                model_answer=answer_text,
                retrieved_documents_ids=doc_ids,
                retrieved_documents_distances=scores
            ))

        return results
