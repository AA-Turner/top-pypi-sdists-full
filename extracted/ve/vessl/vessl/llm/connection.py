from typing import Literal, Optional

from openapi_client import (
    ProtoLLMModelConnection,
    ProtoLLMUserGroup,
    ProtoLLMVectorDBConnConfig,
    ProtoRevealedSecret,
    V1LLMPermissionConfig,
)
from vessl.llm import connection_auth


class ModelSecret(object):
    kind: Literal["openai", "aws"]


class ModelSecretAWS(ModelSecret):
    kind: Literal["aws"]
    access_key: str
    secret_key: str

    def __init__(self, access_key: str, secret_key: str):
        self.kind = "aws"
        self.access_key = access_key
        self.secret_key = secret_key


class ModelSecretOpenAI(ModelSecret):
    kind: Literal["openai"]
    api_key: str

    def __init__(self, api_key: str):
        self.kind = "openai"
        self.api_key = api_key


class ModelConnection(object):
    id: int
    name: str
    model_type: Literal["embedding", "llm"]
    url: str = ""
    api_key: str | None = None
    model_secret: ModelSecret | None = None

    def __init__(self, model_connection: ProtoLLMModelConnection):
        self.id = model_connection.id
        self.name = model_connection.name
        if model_connection.type == "embedding":
            self.model_type = "embedding"
        elif model_connection.type == "llm":
            self.model_type = "llm"
        self.url = model_connection.url
        self.api_key = model_connection.api_key
        model_secret = model_connection.revealed_secret
        if model_secret is not None:
            if model_secret.kind == 'openai':
                self.model_secret = ModelSecretOpenAI(model_secret.openai.api_key.openai_api_key)
            elif model_secret.kind == 'aws':
                if model_secret.aws.credential_type == 'access_key':
                    access_key = model_secret.aws.access_key
                    self.model_secret = ModelSecretAWS(access_key.access_key_id, access_key.secret_access_key)


class VectorDBConnection(object):
    id: int
    name: str
    vector_db_type: Literal["chroma"]
    url: str
    collection_name: str
    authentication: connection_auth.ConnectionAuth

    def __init__(self, vector_db: ProtoLLMVectorDBConnConfig, collection_name: str):
        self.id = vector_db.id
        self.name = vector_db.name
        if vector_db.vdb_type == "chroma":
            self.vector_db_type = "chroma"
        self.url = vector_db.url
        self.collection_name = collection_name
        self.authentication = connection_auth.ConnectionAuth(vector_db.authentication)


class PermissionConfig(object):
    user_group_ids: Optional[list[int]]

    def __init__(self, permission_config: V1LLMPermissionConfig):
        self.user_group_ids = permission_config.user_group_ids


class UserGroup(object):
    id: int
    name: str
    description: Optional[str]
    created_by_id: int
    created_dt: float
    organization_id: int
    updated_dt: float

    def __init__(self, user_group: ProtoLLMUserGroup):
        self.id = user_group.id
        self.name = user_group.name
        self.description = user_group.description
        self.created_by_id = user_group.created_by_id
        self.created_dt = user_group.created_dt
        self.organization_id = user_group.organization_id
        self.updated_dt = user_group.updated_dt


class WorkflowConnectionConfiguration:
    embedding_model: Optional[ModelConnection]
    llm_model: Optional[ModelConnection]
    vector_db: Optional[VectorDBConnection]
    permission: Optional[PermissionConfig]

    def __init__(self, model: Optional[ProtoLLMModelConnection], model_secret: Optional[ProtoRevealedSecret],
                 vector_db: Optional[ProtoLLMVectorDBConnConfig],
                 permission: Optional[V1LLMPermissionConfig], vector_db_collection_name: Optional[str]):
        if model:
            if model.type == "embedding":
                self.embedding_model = ModelConnection(model, model_secret)
            elif model.type == "llm":
                self.llm_model = ModelConnection(model, model_secret)
        if vector_db:
            self.vector_db = VectorDBConnection(vector_db, vector_db_collection_name)
        if permission:
            self.permission = PermissionConfig(permission)
