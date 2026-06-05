from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetTeamNavbarCountsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetTeamNavbarCountsResponse(_message.Message):
    __slots__ = ("projects", "accounts", "clusters", "registries", "vpcs", "storage")
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    CLUSTERS_FIELD_NUMBER: _ClassVar[int]
    REGISTRIES_FIELD_NUMBER: _ClassVar[int]
    VPCS_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    projects: int
    accounts: int
    clusters: int
    registries: int
    vpcs: int
    storage: int
    def __init__(
        self,
        projects: _Optional[int] = ...,
        accounts: _Optional[int] = ...,
        clusters: _Optional[int] = ...,
        registries: _Optional[int] = ...,
        vpcs: _Optional[int] = ...,
        storage: _Optional[int] = ...,
    ) -> None: ...

class GetProjectNavbarCountsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProjectNavbarCountsResponse(_message.Message):
    __slots__ = (
        "resolvers",
        "features",
        "named_queries",
        "active_scheduled_queries",
        "scaling_groups",
        "containers",
        "notebooks",
        "functions",
        "snapshots",
        "models",
        "open_incidents",
        "webhooks",
        "integrations",
        "secrets",
        "offline_store_connections",
        "named_prompts",
        "access_tokens",
        "ai_connections",
        "buckets",
    )
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SCHEDULED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    SCALING_GROUPS_FIELD_NUMBER: _ClassVar[int]
    CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOKS_FIELD_NUMBER: _ClassVar[int]
    FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOTS_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    OPEN_INCIDENTS_FIELD_NUMBER: _ClassVar[int]
    WEBHOOKS_FIELD_NUMBER: _ClassVar[int]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    OFFLINE_STORE_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    NAMED_PROMPTS_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKENS_FIELD_NUMBER: _ClassVar[int]
    AI_CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    BUCKETS_FIELD_NUMBER: _ClassVar[int]
    resolvers: int
    features: int
    named_queries: int
    active_scheduled_queries: int
    scaling_groups: int
    containers: int
    notebooks: int
    functions: int
    snapshots: int
    models: int
    open_incidents: int
    webhooks: int
    integrations: int
    secrets: int
    offline_store_connections: int
    named_prompts: int
    access_tokens: int
    ai_connections: int
    buckets: int
    def __init__(
        self,
        resolvers: _Optional[int] = ...,
        features: _Optional[int] = ...,
        named_queries: _Optional[int] = ...,
        active_scheduled_queries: _Optional[int] = ...,
        scaling_groups: _Optional[int] = ...,
        containers: _Optional[int] = ...,
        notebooks: _Optional[int] = ...,
        functions: _Optional[int] = ...,
        snapshots: _Optional[int] = ...,
        models: _Optional[int] = ...,
        open_incidents: _Optional[int] = ...,
        webhooks: _Optional[int] = ...,
        integrations: _Optional[int] = ...,
        secrets: _Optional[int] = ...,
        offline_store_connections: _Optional[int] = ...,
        named_prompts: _Optional[int] = ...,
        access_tokens: _Optional[int] = ...,
        ai_connections: _Optional[int] = ...,
        buckets: _Optional[int] = ...,
    ) -> None: ...
