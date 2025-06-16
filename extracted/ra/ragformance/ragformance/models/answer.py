from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class RelevantDocumentModel(BaseModel):
    corpus_id: str
    score: int


class AnnotatedQueryModel(BaseModel):
    id: str = Field(alias="_id")
    query_text: str

    relevant_document_ids: List[RelevantDocumentModel]
    ref_answer: str

    metadata: Optional[Dict] = None


class AnswerModel(BaseModel):
    id: str = Field(alias="_id")

    query: AnnotatedQueryModel

    # model output
    model_answer: str
    retrieved_documents_ids: List[str]
    retrieved_documents_distances: Optional[List[float]] = None
    embedding_model_name: Optional[str] = None
    llm_model_name: Optional[str] = None
