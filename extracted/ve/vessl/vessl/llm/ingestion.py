from typing import List

from vessl.llm import connection, document, knowledge


class IngestionConfig(object):
    llm_knowledge: knowledge.Knowledge
    llm_model: connection.ModelConnection
    vector_db: connection.VectorDBConnection
    documents: List[document.Document]

    def __init__(self, llm_knowledge: knowledge.Knowledge, llm_model: connection.ModelConnection, vector_db: connection.VectorDBConnection, documents: List[document.Document]):
        self.llm_knowledge = llm_knowledge
        self.llm_model = llm_model
        self.vector_db = vector_db
        self.documents = documents