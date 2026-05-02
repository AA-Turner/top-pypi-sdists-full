from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetaConfig(_message.Message):
    __slots__ = ("envvar_prefix", "nested_separator", "via_launcher")
    ENVVAR_PREFIX_FIELD_NUMBER: _ClassVar[int]
    NESTED_SEPARATOR_FIELD_NUMBER: _ClassVar[int]
    VIA_LAUNCHER_FIELD_NUMBER: _ClassVar[int]
    envvar_prefix: str
    nested_separator: str
    via_launcher: bool
    def __init__(self, envvar_prefix: _Optional[str] = ..., nested_separator: _Optional[str] = ..., via_launcher: bool = ...) -> None: ...

class MetricsConfig(_message.Message):
    __slots__ = ("export",)
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    export: bool
    def __init__(self, export: bool = ...) -> None: ...

class ChatServerConfig(_message.Message):
    __slots__ = ("port",)
    PORT_FIELD_NUMBER: _ClassVar[int]
    port: int
    def __init__(self, port: _Optional[int] = ...) -> None: ...

class RocksetConfig(_message.Message):
    __slots__ = ("default_workspace", "default_collection", "default_region", "api_token", "integrations", "collections", "organization")
    class IntegrationConfig(_message.Message):
        __slots__ = ("rockset_integration_id", "supported_buckets")
        ROCKSET_INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
        SUPPORTED_BUCKETS_FIELD_NUMBER: _ClassVar[int]
        rockset_integration_id: str
        supported_buckets: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, rockset_integration_id: _Optional[str] = ..., supported_buckets: _Optional[_Iterable[str]] = ...) -> None: ...
    class IntegrationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: RocksetConfig.IntegrationConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[RocksetConfig.IntegrationConfig, _Mapping]] = ...) -> None: ...
    class CollectionArgs(_message.Message):
        __slots__ = ("integration_name", "bucket_name", "gcs_output_prefix", "create_if_missing")
        INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
        BUCKET_NAME_FIELD_NUMBER: _ClassVar[int]
        GCS_OUTPUT_PREFIX_FIELD_NUMBER: _ClassVar[int]
        CREATE_IF_MISSING_FIELD_NUMBER: _ClassVar[int]
        integration_name: str
        bucket_name: str
        gcs_output_prefix: str
        create_if_missing: bool
        def __init__(self, integration_name: _Optional[str] = ..., bucket_name: _Optional[str] = ..., gcs_output_prefix: _Optional[str] = ..., create_if_missing: bool = ...) -> None: ...
    class CollectionConfig(_message.Message):
        __slots__ = ("name", "workspace", "host", "kind", "description", "collection_args")
        NAME_FIELD_NUMBER: _ClassVar[int]
        WORKSPACE_FIELD_NUMBER: _ClassVar[int]
        HOST_FIELD_NUMBER: _ClassVar[int]
        KIND_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLLECTION_ARGS_FIELD_NUMBER: _ClassVar[int]
        name: str
        workspace: str
        host: str
        kind: str
        description: str
        collection_args: RocksetConfig.CollectionArgs
        def __init__(self, name: _Optional[str] = ..., workspace: _Optional[str] = ..., host: _Optional[str] = ..., kind: _Optional[str] = ..., description: _Optional[str] = ..., collection_args: _Optional[_Union[RocksetConfig.CollectionArgs, _Mapping]] = ...) -> None: ...
    class CollectionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: RocksetConfig.CollectionConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[RocksetConfig.CollectionConfig, _Mapping]] = ...) -> None: ...
    DEFAULT_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_REGION_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    ORGANIZATION_FIELD_NUMBER: _ClassVar[int]
    default_workspace: str
    default_collection: str
    default_region: str
    api_token: str
    integrations: _containers.MessageMap[str, RocksetConfig.IntegrationConfig]
    collections: _containers.MessageMap[str, RocksetConfig.CollectionConfig]
    organization: str
    def __init__(self, default_workspace: _Optional[str] = ..., default_collection: _Optional[str] = ..., default_region: _Optional[str] = ..., api_token: _Optional[str] = ..., integrations: _Optional[_Mapping[str, RocksetConfig.IntegrationConfig]] = ..., collections: _Optional[_Mapping[str, RocksetConfig.CollectionConfig]] = ..., organization: _Optional[str] = ...) -> None: ...

class EmbedgenConfig(_message.Message):
    __slots__ = ("default_tag", "rockset_collection_name", "chunk_text_field_name", "gcs_notification_config_embed_gen_config_key", "document_processor")
    class DocProcConfig(_message.Message):
        __slots__ = ("batch_size",)
        BATCH_SIZE_FIELD_NUMBER: _ClassVar[int]
        batch_size: int
        def __init__(self, batch_size: _Optional[int] = ...) -> None: ...
    DEFAULT_TAG_FIELD_NUMBER: _ClassVar[int]
    ROCKSET_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    CHUNK_TEXT_FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
    GCS_NOTIFICATION_CONFIG_EMBED_GEN_CONFIG_KEY_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    default_tag: str
    rockset_collection_name: str
    chunk_text_field_name: str
    gcs_notification_config_embed_gen_config_key: str
    document_processor: EmbedgenConfig.DocProcConfig
    def __init__(self, default_tag: _Optional[str] = ..., rockset_collection_name: _Optional[str] = ..., chunk_text_field_name: _Optional[str] = ..., gcs_notification_config_embed_gen_config_key: _Optional[str] = ..., document_processor: _Optional[_Union[EmbedgenConfig.DocProcConfig, _Mapping]] = ...) -> None: ...

class ChatConfig(_message.Message):
    __slots__ = ("max_messages_per_page", "get_messages_period_seconds", "completion_model", "retriever_type", "obfuscation_seed", "client")
    class ClientConfig(_message.Message):
        __slots__ = ("hostname", "port")
        HOSTNAME_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        hostname: str
        port: int
        def __init__(self, hostname: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
    MAX_MESSAGES_PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    GET_MESSAGES_PERIOD_SECONDS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_MODEL_FIELD_NUMBER: _ClassVar[int]
    RETRIEVER_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBFUSCATION_SEED_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    max_messages_per_page: int
    get_messages_period_seconds: float
    completion_model: str
    retriever_type: str
    obfuscation_seed: str
    client: ChatConfig.ClientConfig
    def __init__(self, max_messages_per_page: _Optional[int] = ..., get_messages_period_seconds: _Optional[float] = ..., completion_model: _Optional[str] = ..., retriever_type: _Optional[str] = ..., obfuscation_seed: _Optional[str] = ..., client: _Optional[_Union[ChatConfig.ClientConfig, _Mapping]] = ...) -> None: ...

class DBConfig(_message.Message):
    __slots__ = ("host", "name")
    HOST_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    host: str
    name: str
    def __init__(self, host: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class IngestConfig(_message.Message):
    __slots__ = ("store_id_metadata_key", "server", "client")
    class ServerConfig(_message.Message):
        __slots__ = ("bucket", "prefix", "obfuscation_seed")
        BUCKET_FIELD_NUMBER: _ClassVar[int]
        PREFIX_FIELD_NUMBER: _ClassVar[int]
        OBFUSCATION_SEED_FIELD_NUMBER: _ClassVar[int]
        bucket: str
        prefix: str
        obfuscation_seed: str
        def __init__(self, bucket: _Optional[str] = ..., prefix: _Optional[str] = ..., obfuscation_seed: _Optional[str] = ...) -> None: ...
    class ClientConfig(_message.Message):
        __slots__ = ("hostname", "port")
        HOSTNAME_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        hostname: str
        port: int
        def __init__(self, hostname: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
    STORE_ID_METADATA_KEY_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    store_id_metadata_key: str
    server: IngestConfig.ServerConfig
    client: IngestConfig.ClientConfig
    def __init__(self, store_id_metadata_key: _Optional[str] = ..., server: _Optional[_Union[IngestConfig.ServerConfig, _Mapping]] = ..., client: _Optional[_Union[IngestConfig.ClientConfig, _Mapping]] = ...) -> None: ...

class ExperimentConfig(_message.Message):
    __slots__ = ("gcs_run_prefix",)
    GCS_RUN_PREFIX_FIELD_NUMBER: _ClassVar[int]
    gcs_run_prefix: str
    def __init__(self, gcs_run_prefix: _Optional[str] = ...) -> None: ...

class CompletionModelConfig(_message.Message):
    __slots__ = ("engine", "model", "tokenizer")
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    TOKENIZER_FIELD_NUMBER: _ClassVar[int]
    engine: str
    model: str
    tokenizer: str
    def __init__(self, engine: _Optional[str] = ..., model: _Optional[str] = ..., tokenizer: _Optional[str] = ...) -> None: ...

class EmbeddingModelConfig(_message.Message):
    __slots__ = ("engine", "model", "cardinality", "extra")
    class ExtraConfig(_message.Message):
        __slots__ = ("device",)
        DEVICE_FIELD_NUMBER: _ClassVar[int]
        device: str
        def __init__(self, device: _Optional[str] = ...) -> None: ...
    ENGINE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    CARDINALITY_FIELD_NUMBER: _ClassVar[int]
    EXTRA_FIELD_NUMBER: _ClassVar[int]
    engine: str
    model: str
    cardinality: int
    extra: EmbeddingModelConfig.ExtraConfig
    def __init__(self, engine: _Optional[str] = ..., model: _Optional[str] = ..., cardinality: _Optional[int] = ..., extra: _Optional[_Union[EmbeddingModelConfig.ExtraConfig, _Mapping]] = ...) -> None: ...

class HuggingfaceConfig(_message.Message):
    __slots__ = ("model_proxy_url", "default_inference_timeout", "default_max_new_tokens", "api_token", "inference_endpoints")
    class InferenceEndpointsConfig(_message.Message):
        __slots__ = ("completions", "embeddings")
        class CompletionModel(_message.Message):
            __slots__ = ("hf_host", "hf_name", "hf_namespace", "models")
            HF_HOST_FIELD_NUMBER: _ClassVar[int]
            HF_NAME_FIELD_NUMBER: _ClassVar[int]
            HF_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
            MODELS_FIELD_NUMBER: _ClassVar[int]
            hf_host: str
            hf_name: str
            hf_namespace: str
            models: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, hf_host: _Optional[str] = ..., hf_name: _Optional[str] = ..., hf_namespace: _Optional[str] = ..., models: _Optional[_Iterable[str]] = ...) -> None: ...
        class CompletionsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: HuggingfaceConfig.InferenceEndpointsConfig.CompletionModel
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[HuggingfaceConfig.InferenceEndpointsConfig.CompletionModel, _Mapping]] = ...) -> None: ...
        class EmbeddingModel(_message.Message):
            __slots__ = ("hf_host", "hf_name", "hf_namespace", "models")
            HF_HOST_FIELD_NUMBER: _ClassVar[int]
            HF_NAME_FIELD_NUMBER: _ClassVar[int]
            HF_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
            MODELS_FIELD_NUMBER: _ClassVar[int]
            hf_host: str
            hf_name: str
            hf_namespace: str
            models: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, hf_host: _Optional[str] = ..., hf_name: _Optional[str] = ..., hf_namespace: _Optional[str] = ..., models: _Optional[_Iterable[str]] = ...) -> None: ...
        class EmbeddingsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: HuggingfaceConfig.InferenceEndpointsConfig.EmbeddingModel
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[HuggingfaceConfig.InferenceEndpointsConfig.EmbeddingModel, _Mapping]] = ...) -> None: ...
        COMPLETIONS_FIELD_NUMBER: _ClassVar[int]
        EMBEDDINGS_FIELD_NUMBER: _ClassVar[int]
        completions: _containers.MessageMap[str, HuggingfaceConfig.InferenceEndpointsConfig.CompletionModel]
        embeddings: _containers.MessageMap[str, HuggingfaceConfig.InferenceEndpointsConfig.EmbeddingModel]
        def __init__(self, completions: _Optional[_Mapping[str, HuggingfaceConfig.InferenceEndpointsConfig.CompletionModel]] = ..., embeddings: _Optional[_Mapping[str, HuggingfaceConfig.InferenceEndpointsConfig.EmbeddingModel]] = ...) -> None: ...
    MODEL_PROXY_URL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_INFERENCE_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MAX_NEW_TOKENS_FIELD_NUMBER: _ClassVar[int]
    API_TOKEN_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    model_proxy_url: str
    default_inference_timeout: int
    default_max_new_tokens: int
    api_token: str
    inference_endpoints: HuggingfaceConfig.InferenceEndpointsConfig
    def __init__(self, model_proxy_url: _Optional[str] = ..., default_inference_timeout: _Optional[int] = ..., default_max_new_tokens: _Optional[int] = ..., api_token: _Optional[str] = ..., inference_endpoints: _Optional[_Union[HuggingfaceConfig.InferenceEndpointsConfig, _Mapping]] = ...) -> None: ...

class RetrieverConfig(_message.Message):
    __slots__ = ("default_similarity_threshold", "default_max_chunks", "default_tag", "default_embeddings_model", "default_embeddings_model_name", "default_embeddings_engine", "type", "rockset_collection_name")
    DEFAULT_SIMILARITY_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_MAX_CHUNKS_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_TAG_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_EMBEDDINGS_MODEL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_EMBEDDINGS_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_EMBEDDINGS_ENGINE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ROCKSET_COLLECTION_NAME_FIELD_NUMBER: _ClassVar[int]
    default_similarity_threshold: float
    default_max_chunks: int
    default_tag: str
    default_embeddings_model: str
    default_embeddings_model_name: str
    default_embeddings_engine: str
    type: str
    rockset_collection_name: str
    def __init__(self, default_similarity_threshold: _Optional[float] = ..., default_max_chunks: _Optional[int] = ..., default_tag: _Optional[str] = ..., default_embeddings_model: _Optional[str] = ..., default_embeddings_model_name: _Optional[str] = ..., default_embeddings_engine: _Optional[str] = ..., type: _Optional[str] = ..., rockset_collection_name: _Optional[str] = ...) -> None: ...

class CompletionConfig(_message.Message):
    __slots__ = ("default_completion_model", "no_chunk_message", "sys_prompt_rag")
    DEFAULT_COMPLETION_MODEL_FIELD_NUMBER: _ClassVar[int]
    NO_CHUNK_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SYS_PROMPT_RAG_FIELD_NUMBER: _ClassVar[int]
    default_completion_model: str
    no_chunk_message: str
    sys_prompt_rag: str
    def __init__(self, default_completion_model: _Optional[str] = ..., no_chunk_message: _Optional[str] = ..., sys_prompt_rag: _Optional[str] = ...) -> None: ...

class WorkflowConfig(_message.Message):
    __slots__ = ("storage_prefix",)
    STORAGE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    storage_prefix: str
    def __init__(self, storage_prefix: _Optional[str] = ...) -> None: ...

class DataStagingConfig(_message.Message):
    __slots__ = ("rockset_api_server", "rockset_workspace", "rockset_collection", "rockset_integration", "gcs_bucket", "gcs_unstructured_data_prefix", "gcs_table_data_prefix", "blob_name_column", "row_number_column")
    ROCKSET_API_SERVER_FIELD_NUMBER: _ClassVar[int]
    ROCKSET_WORKSPACE_FIELD_NUMBER: _ClassVar[int]
    ROCKSET_COLLECTION_FIELD_NUMBER: _ClassVar[int]
    ROCKSET_INTEGRATION_FIELD_NUMBER: _ClassVar[int]
    GCS_BUCKET_FIELD_NUMBER: _ClassVar[int]
    GCS_UNSTRUCTURED_DATA_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GCS_TABLE_DATA_PREFIX_FIELD_NUMBER: _ClassVar[int]
    BLOB_NAME_COLUMN_FIELD_NUMBER: _ClassVar[int]
    ROW_NUMBER_COLUMN_FIELD_NUMBER: _ClassVar[int]
    rockset_api_server: str
    rockset_workspace: str
    rockset_collection: str
    rockset_integration: str
    gcs_bucket: str
    gcs_unstructured_data_prefix: str
    gcs_table_data_prefix: str
    blob_name_column: str
    row_number_column: str
    def __init__(self, rockset_api_server: _Optional[str] = ..., rockset_workspace: _Optional[str] = ..., rockset_collection: _Optional[str] = ..., rockset_integration: _Optional[str] = ..., gcs_bucket: _Optional[str] = ..., gcs_unstructured_data_prefix: _Optional[str] = ..., gcs_table_data_prefix: _Optional[str] = ..., blob_name_column: _Optional[str] = ..., row_number_column: _Optional[str] = ...) -> None: ...

class Auth0(_message.Message):
    __slots__ = ("client_id", "client_secret", "domain")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_secret: str
    domain: str
    def __init__(self, client_id: _Optional[str] = ..., client_secret: _Optional[str] = ..., domain: _Optional[str] = ...) -> None: ...

class Settings(_message.Message):
    __slots__ = ("load_dotenv", "config", "dev_mode", "metrics", "chat_server", "embedgen", "chat", "db", "ingest", "completion_models", "embedding_models", "huggingface", "retriever", "completion", "rockset", "google_identity_token", "check_name", "test_db", "workflow", "data_staging", "experiment", "auth0")
    class CompletionModelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: CompletionModelConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[CompletionModelConfig, _Mapping]] = ...) -> None: ...
    class EmbeddingModelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: EmbeddingModelConfig
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[EmbeddingModelConfig, _Mapping]] = ...) -> None: ...
    LOAD_DOTENV_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DEV_MODE_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    CHAT_SERVER_FIELD_NUMBER: _ClassVar[int]
    EMBEDGEN_FIELD_NUMBER: _ClassVar[int]
    CHAT_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    INGEST_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_MODELS_FIELD_NUMBER: _ClassVar[int]
    EMBEDDING_MODELS_FIELD_NUMBER: _ClassVar[int]
    HUGGINGFACE_FIELD_NUMBER: _ClassVar[int]
    RETRIEVER_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    ROCKSET_FIELD_NUMBER: _ClassVar[int]
    GOOGLE_IDENTITY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CHECK_NAME_FIELD_NUMBER: _ClassVar[int]
    TEST_DB_FIELD_NUMBER: _ClassVar[int]
    WORKFLOW_FIELD_NUMBER: _ClassVar[int]
    DATA_STAGING_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_FIELD_NUMBER: _ClassVar[int]
    AUTH0_FIELD_NUMBER: _ClassVar[int]
    load_dotenv: bool
    config: MetaConfig
    dev_mode: str
    metrics: MetricsConfig
    chat_server: ChatServerConfig
    embedgen: EmbedgenConfig
    chat: ChatConfig
    db: DBConfig
    ingest: IngestConfig
    completion_models: _containers.MessageMap[str, CompletionModelConfig]
    embedding_models: _containers.MessageMap[str, EmbeddingModelConfig]
    huggingface: HuggingfaceConfig
    retriever: RetrieverConfig
    completion: CompletionConfig
    rockset: RocksetConfig
    google_identity_token: str
    check_name: str
    test_db: str
    workflow: WorkflowConfig
    data_staging: DataStagingConfig
    experiment: ExperimentConfig
    auth0: Auth0
    def __init__(self, load_dotenv: bool = ..., config: _Optional[_Union[MetaConfig, _Mapping]] = ..., dev_mode: _Optional[str] = ..., metrics: _Optional[_Union[MetricsConfig, _Mapping]] = ..., chat_server: _Optional[_Union[ChatServerConfig, _Mapping]] = ..., embedgen: _Optional[_Union[EmbedgenConfig, _Mapping]] = ..., chat: _Optional[_Union[ChatConfig, _Mapping]] = ..., db: _Optional[_Union[DBConfig, _Mapping]] = ..., ingest: _Optional[_Union[IngestConfig, _Mapping]] = ..., completion_models: _Optional[_Mapping[str, CompletionModelConfig]] = ..., embedding_models: _Optional[_Mapping[str, EmbeddingModelConfig]] = ..., huggingface: _Optional[_Union[HuggingfaceConfig, _Mapping]] = ..., retriever: _Optional[_Union[RetrieverConfig, _Mapping]] = ..., completion: _Optional[_Union[CompletionConfig, _Mapping]] = ..., rockset: _Optional[_Union[RocksetConfig, _Mapping]] = ..., google_identity_token: _Optional[str] = ..., check_name: _Optional[str] = ..., test_db: _Optional[str] = ..., workflow: _Optional[_Union[WorkflowConfig, _Mapping]] = ..., data_staging: _Optional[_Union[DataStagingConfig, _Mapping]] = ..., experiment: _Optional[_Union[ExperimentConfig, _Mapping]] = ..., auth0: _Optional[_Union[Auth0, _Mapping]] = ...) -> None: ...
