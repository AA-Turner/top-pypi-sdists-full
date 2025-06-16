from typing import List
import uuid
import requests

try:
    from sentence_transformers import SentenceTransformer
except ImportError:

    def SentenceTransformer(*args, **kwargs):
        raise ImportError(
            "'sentence-transformers' module is not installed. "
            "Please install ragformance with the [all] option:\n"
            "    pip install ragformance[all]"
        )


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json

import logging

from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.models.corpus import DocModel
from ragformance.rag.rag_interface import RagInterface
from ragformance.rag.config import NaiveRagConfig

logger = logging.getLogger(__name__)


# TODO restructure the rag folder to have one fodler per rag, with a readme
class NaiveRag(RagInterface):
    def __init__(self, config: NaiveRagConfig):
        self.config = config
        self.embedding_model = SentenceTransformer(self.config.EMBEDDING_MODEL)
        self.document_embeddings = []
        self.documents: List[DocModel] = []

    def upload_corpus(self, corpus: List[DocModel]):
        self.document_embeddings.clear()
        self.documents.clear()
        self.documents.extend(corpus)

        batch_size = self.config.BATCH_SIZE

        # Extract texts from the corpus list
        texts = [doc.text for doc in corpus]

        # Process documents in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            # Generate embeddings for the batch
            batch_embeddings = self.embedding_model.encode(batch_texts)

            # Store embeddings
            self.document_embeddings.extend(batch_embeddings)

        logger.info(
            f"Document embeddings generated and stored in memory. {len(self.document_embeddings)} embeddings generated."
        )
        return len(self.document_embeddings)

    def ask_queries(self, queries: List[AnnotatedQueryModel]) -> List[AnswerModel]:
        threshold = self.config.SIMILARITY_THRESHOLD
        batch_size = self.config.BATCH_SIZE
        url = self.config.LLM_ENDPOINT
        key = self.config.LLM_KEY
        model = self.config.LLM_MODEL

        if not url or not model:  # Key can be None
            logger.warning(
                "LLM endpoint or model not provided in config. LLM calls will be skipped."
            )

        # Generate embedding for the question
        # Extract texts from the corpus list
        texts = [query.query_text for query in queries]

        query_embeddings = []

        # Process documents in batches
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            # Generate embeddings for the batch
            batch_embeddings = self.embedding_model.encode(batch_texts)

            # Store embeddings
            query_embeddings.extend(batch_embeddings)

        answers = []

        for qindex, query in enumerate(queries):
            question = query.query_text
            question_embedding = query_embeddings[qindex]

            # Ensure question_embedding is a 2D array
            question_embedding = np.array([question_embedding])
            if question_embedding.ndim == 1:
                question_embedding = question_embedding.reshape(1, -1)

            # Ensure document_embeddings is a 2D array
            document_embeddings_array = np.array(self.document_embeddings)
            if not document_embeddings_array.any():
                logger.warning(
                    f"Corpus is empty for query: {question}. Cannot compute similarities."
                )
                answer = AnswerModel.model_validate(
                    {
                        "_id": str(uuid.uuid4()),
                        "query": query,
                        "model_answer": "Corpus is empty. Please upload documents first.",
                        "retrieved_documents_ids": [],
                        "retrieved_documents_distances": [],
                    }
                )
                answers.append(answer)
                continue

            if (
                document_embeddings_array.ndim == 1
            ):  # Should not happen with current logic but good check
                document_embeddings_array = document_embeddings_array.reshape(1, -1)

            similarities = cosine_similarity(
                question_embedding, document_embeddings_array
            )
            relevant_documents_indices = np.where(similarities > threshold)[1]
            relevant_distances = similarities[0, relevant_documents_indices].tolist()

            logger.info(
                f"Query {qindex} : Found {len(relevant_documents_indices)} relevant documents."
            )

            prompt_and_query = f"Answer the question based on the context below : \n QUESTION: {question}\n"
            for index, doc_idx in enumerate(relevant_documents_indices):
                document: DocModel = self.documents[doc_idx]  # Use self.documents
                text = document.text
                prompt_and_query += f"CONTEXT {index + 1}: {text}\n"
            prompt_and_query += "ANSWER:"

            retrieved_doc_ids = [
                self.documents[i].id for i in relevant_documents_indices
            ]
            model_answer_text = "LLM endpoint or model not configured."

            if url and model:  # Check if url and model are configured
                headers = {"Content-Type": "application/json"}
                if key:  # Add Authorization header only if key is present
                    headers["Authorization"] = f"Bearer {key}"

                try:
                    response = requests.post(
                        url=url,
                        headers=headers,
                        data=json.dumps(
                            {
                                "model": model,
                                "messages": [
                                    {"role": "user", "content": prompt_and_query}
                                ],
                            }
                        ),
                    )
                    response.raise_for_status()  # Raise an exception for bad status codes
                    response_json = response.json()
                    model_answer_text = response_json["choices"][0]["message"][
                        "content"
                    ]
                except requests.exceptions.RequestException as e:
                    logger.error(f"LLM API request failed for query '{question}': {e}")
                    model_answer_text = f"LLM API request failed: {e}"

                except (
                    KeyError
                ):  # Handle cases where 'choices' or other keys might be missing
                    logger.error(
                        f"Invalid LLM response format for query '{question}'. Response: {response.text}"
                    )
                    model_answer_text = "Invalid LLM response format."

            answer = AnswerModel.model_validate(
                {
                    "_id": str(uuid.uuid4()),
                    "query": query,
                    "model_answer": model_answer_text,
                    "retrieved_documents_ids": retrieved_doc_ids,
                    "retrieved_documents_distances": relevant_distances,
                }
            )
            answers.append(answer)

        return answers
