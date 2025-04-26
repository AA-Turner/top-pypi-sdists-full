from typing import Optional

from openapi_client import V1LLMPermissionConfig, ProtoLLMKnowledge


class Knowledge(object):
    id: int
    name: str
    description: str
    embedding_model_id: int
    vector_db_collection_name: str
    vector_db_connection_id: int
    permission_config: Optional[V1LLMPermissionConfig]
    created_by_id: int
    cluster_id: int
    resource_spec_id: int

    def __init__(self, knowledge: ProtoLLMKnowledge):
        self.id = knowledge.id
        self.name = knowledge.name
        self.description = knowledge.description
        self.embedding_model_id = knowledge.embedding_model_id
        self.vector_db_collection_name = knowledge.vectordb_collection_name
        self.vector_db_connection_id = knowledge.vectordb_connection_id
        self.permission_config = knowledge.permission_config
        self.created_by_id = knowledge.created_by_id
        self.cluster_id = knowledge.cluster_id
        self.resource_spec_id = knowledge.resource_spec_id
