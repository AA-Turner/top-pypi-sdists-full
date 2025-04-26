from vessl.llm import connection, knowledge


class RetrieverConfig(object):
    llm_knowledge: knowledge.Knowledge
    llm_model: connection.ModelConnection
    vector_db: connection.VectorDBConnection

    def __init__(self, llm_knowledge: knowledge.Knowledge, llm_model: connection.ModelConnection, vector_db: connection.VectorDBConnection):
        self.llm_knowledge = llm_knowledge
        self.llm_model = llm_model
        self.vector_db = vector_db