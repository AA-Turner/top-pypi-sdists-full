# File: matrx_rag/db/models_rag.py
from matrx_orm import BigIntegerField, BooleanField, DateField, DateTimeField, DecimalField, EnumField, FloatArrayField, FloatField, ForeignKey, IntegerArrayField, IntegerField, JSONBField, MatrxEntity, Model, SmallIntegerField, TextField, UUIDArrayField, UUIDField, VectorField, model_registry, BaseDTO, BaseManager
from enum import StrEnum
from dataclasses import dataclass
from typing import ClassVar



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class ContextItemSuggestions(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    scope_type_id = UUIDField(null=False)
    suggested_key = TextField(null=False)
    display_name = TextField(null=False)
    rationale = TextField()
    example_value = TextField()
    example_source_kind = TextField()
    example_source_id = TextField()
    confidence = FloatField(null=False, default=0.5)
    status = TextField(null=False, default='pending')
    created_at = DateTimeField(null=False)
    decided_at = DateTimeField()
    decided_by = UUIDField()
    suppressed_until = DateTimeField()
    sweep_run_id = UUIDField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "context_item_suggestions"
    _db_schema = "rag"
    _entity_token = "context_item_suggestion"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class DataStores(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    name = TextField(null=False)
    short_code = TextField()
    description = TextField()
    kind = TextField(null=False, default='general')
    settings = JSONBField(null=False, default={})
    is_active = BooleanField(null=False, default=True)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    discoverable = BooleanField(null=False, default=False)
    visibility = EnumField(enum_class=Visibility, null=False)
    metadata = JSONBField(null=False, default={})
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    deleted_at = DateTimeField()
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'data_store_members': {'from_model': 'DataStoreMembers', 'from_field': 'data_store_id', 'referenced_field': 'id', 'related_name': 'data_store_members', 'from_schema': 'rag'}}
    _database = "matrx_rag"
    _table_name = "data_stores"
    _db_schema = "rag"
    _entity_token = "data_store"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class EmbeddingCache(MatrxEntity):
    cache_key = TextField(primary_key=True, null=False)
    model = TextField(null=False)
    embedding = VectorField(dimensions=1536, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    hit_count = IntegerField(null=False, default=0)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "embedding_cache"
    _db_schema = "rag"
    _entity_token = "embedding_cache"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "entity"

class IngestRun(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    actor_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    field_id = TextField()
    triggered_by = TextField(null=False)
    urgency = TextField(null=False, default='auto')
    status = TextField(null=False, default='running')
    skip_reason = TextField()
    error = TextField()
    started_at = DateTimeField(null=False)
    finished_at = DateTimeField()
    duration_ms = IntegerField()
    binary_pipeline = BooleanField(null=False, default=False)
    chars_in = IntegerField(null=False, default=0)
    pages_in = IntegerField()
    chunks_written = IntegerField(null=False, default=0)
    chunks_reused = IntegerField(null=False, default=0)
    embeddings_written = IntegerField(null=False, default=0)
    embedding_model = TextField(null=False)
    embedding_calls = IntegerField(null=False, default=0)
    embedding_tokens = IntegerField(null=False, default=0)
    embedding_cache_hits = IntegerField(null=False, default=0)
    embedding_cost_usd = DecimalField(null=False, default=0)
    embedding_cost_saved_usd = DecimalField(null=False, default=0)
    extraction_calls = IntegerField(null=False, default=0)
    extraction_cost_usd = DecimalField(null=False, default=0)
    enrich_ran = BooleanField(null=False, default=False)
    enrichment_calls = IntegerField(null=False, default=0)
    enrichment_cost_usd = DecimalField(null=False, default=0)
    suggestions_created = IntegerField(null=False, default=0)
    est_cost_usd = DecimalField(null=False, default=0)
    total_cost_usd = DecimalField(null=False, default=0)
    cost_is_exact = BooleanField(null=False, default=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    cleanup_calls = IntegerField(null=False, default=0)
    cleanup_cost_usd = DecimalField(null=False, default=0)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "ingest_run"
    _db_schema = "rag"
    _entity_token = "rag_ingest_run"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "ledger"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KgAlerts(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    target_scope_id = UUIDField(null=False)
    target_slot_key = TextField()
    kind = TextField(null=False)
    severity = TextField(null=False, default='fyi')
    description = TextField(null=False)
    suggested_action = TextField()
    evidence = TextField()
    confidence = FloatField(null=False, default=0.5)
    status = TextField(null=False, default='pending')
    created_at = DateTimeField(null=False)
    decided_at = DateTimeField()
    decided_by = UUIDField()
    viewed_at = DateTimeField()
    deleted_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_alerts"
    _db_schema = "rag"
    _entity_token = "kg_alert"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class KgChunks(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    field_id = TextField()
    parent_chunk_id = ForeignKey(to_model='KgChunks', to_column='id', to_schema='rag', )
    chunk_index = IntegerField(null=False, default=0)
    chunk_kind = TextField(null=False, default='text')
    content_text = TextField(null=False)
    content_tsv = TextField()
    token_count = IntegerField()
    language = TextField()
    mime_type = TextField()
    valid_from = DateTimeField(null=False)
    valid_to = DateTimeField()
    source_hash = TextField(null=False)
    chunker_name = TextField(null=False)
    chunker_version = TextField(null=False)
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    processed_document_id = ForeignKey(to_model='ProcessedDocuments', to_column='id', to_schema='docproc', )
    primary_page_id = ForeignKey(to_model='ProcessedDocumentPages', to_column='id', to_schema='docproc', )
    document_char_start = IntegerField()
    document_char_end = IntegerField()
    page_numbers = IntegerArrayField()
    page_spans = JSONBField()
    overlap_previous_chars = IntegerField()
    overlap_next_chars = IntegerField()
    token_estimate = IntegerField()
    priority = SmallIntegerField(null=False, default=0)
    derivation_kind = TextField(null=False, default='initial_extract')
    derived_from_chunk_id = ForeignKey(to_model='KgChunks', to_column='id', to_schema='rag', )
    agent_id = ForeignKey(to_model='Definition', to_column='id', to_schema='agent', )
    extraction_run_id = ForeignKey(to_model='PageExtractionRuns', to_column='id', to_schema='docproc', )
    extraction_result_id = ForeignKey(to_model='PageExtractionResults', to_column='id', to_schema='docproc', )
    content_sha256 = TextField()
    ner_extracted_at = DateTimeField()
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'embeddings_google_gemini_2_1536': {'from_model': 'EmbeddingsGoogleGemini21536', 'from_field': 'chunk_id', 'referenced_field': 'id', 'related_name': 'embeddings_google_gemini_2_1536', 'from_schema': 'rag'}, 'embeddings_oai_3_small_1536': {'from_model': 'EmbeddingsOai3Small1536', 'from_field': 'chunk_id', 'referenced_field': 'id', 'related_name': 'embeddings_oai_3_small_1536', 'from_schema': 'rag'}, 'embeddings_voyage_4_large_1024': {'from_model': 'EmbeddingsVoyage4Large1024', 'from_field': 'chunk_id', 'referenced_field': 'id', 'related_name': 'embeddings_voyage_4_large_1024', 'from_schema': 'rag'}, 'embeddings_voyage_code_3_1024': {'from_model': 'EmbeddingsVoyageCode31024', 'from_field': 'chunk_id', 'referenced_field': 'id', 'related_name': 'embeddings_voyage_code_3_1024', 'from_schema': 'rag'}, 'kg_chunk_entities': {'from_model': 'KgChunkEntities', 'from_field': 'chunk_id', 'referenced_field': 'id', 'related_name': 'kg_chunk_entities', 'from_schema': 'rag'}, 'kg_edges': {'from_model': 'KgEdges', 'from_field': 'source_chunk_id', 'referenced_field': 'id', 'related_name': 'kg_edges', 'from_schema': 'rag'}, 'kg_value_matches': {'from_model': 'KgValueMatches', 'from_field': 'evidence_chunk_id', 'referenced_field': 'id', 'related_name': 'kg_value_matches', 'from_schema': 'rag'}, 'scope_item_value_suggestions': {'from_model': 'ScopeItemValueSuggestions', 'from_field': 'evidence_chunk_id', 'referenced_field': 'id', 'related_name': 'scope_item_value_suggestions', 'from_schema': 'rag'}}
    _database = "matrx_rag"
    _table_name = "kg_chunks"
    _db_schema = "rag"
    _entity_token = "kg_chunks"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "detail"

class KgClusters(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    label = TextField(null=False)
    summary = TextField()
    kind = TextField(null=False, default='theme')
    level = SmallIntegerField(null=False, default=0)
    parent_cluster_id = ForeignKey(to_model='KgClusters', to_column='id', to_schema='rag', )
    member_count = IntegerField(null=False, default=0)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    centroid = VectorField(dimensions=1024, )
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'kg_entities': {'from_model': 'KgEntities', 'from_field': 'cluster_id', 'referenced_field': 'id', 'related_name': 'kg_entities', 'from_schema': 'rag'}}
    _database = "matrx_rag"
    _table_name = "kg_clusters"
    _db_schema = "rag"
    _entity_token = "kg_clusters"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KgSuggestionAck(MatrxEntity):
    suggestion_id = TextField(primary_key=True, null=False)
    created_at = DateTimeField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', primary_key=True, null=False)
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    id = UUIDField(null=False)
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_suggestion_ack"
    _db_schema = "rag"
    _entity_token = "kg_suggestion_ack"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KgSweepQueue(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    change_type = TextField(null=False)
    entity_id = UUIDField(null=False)
    scope_type_id = UUIDField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    status = TextField(null=False, default='pending')
    enqueued_at = DateTimeField(null=False)
    claim_at = DateTimeField(null=False)
    claimed_at = DateTimeField()
    sweep_run_id = UUIDField()
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    visibility = EnumField(enum_class=Visibility, null=False)
    created_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_sweep_queue"
    _db_schema = "rag"
    _entity_token = "kg_sweep_queue"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KgSweepRun(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    run_id = UUIDField(null=False, unique=True)
    trigger_type = TextField(null=False)
    trigger_entity_id = UUIDField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    scope_type_id = UUIDField()
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    status = TextField(null=False, default='pending')
    change_count = IntegerField(null=False, default=0)
    documents_considered = IntegerField(null=False, default=0)
    entities_enumerated = IntegerField(null=False, default=0)
    entities_excluded_resolved = IntegerField(null=False, default=0)
    entities_after_dedup = IntegerField(null=False, default=0)
    entities_selected = IntegerField(null=False, default=0)
    entities_deferred = IntegerField(null=False, default=0)
    batches = IntegerField(null=False, default=0)
    llm_calls = IntegerField(null=False, default=0)
    tokens_in = BigIntegerField(null=False, default=0)
    tokens_out = BigIntegerField(null=False, default=0)
    cost_usd = DecimalField(null=False, default=0)
    suggestions_created = IntegerField(null=False, default=0)
    started_at = DateTimeField(null=False)
    completed_at = DateTimeField()
    error = JSONBField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_sweep_run"
    _db_schema = "rag"
    _entity_token = "kg_sweep_run"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class KgSweepState(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    scope_type_id = UUIDField()
    last_sweep_at = DateTimeField()
    last_sweep_run_id = UUIDField()
    entity_watermark = DateTimeField()
    sweeps_total = IntegerField(null=False, default=0)
    suggestions_generated_total = IntegerField(null=False, default=0)
    suggestions_accepted_total = IntegerField(null=False, default=0)
    suggestions_dismissed_total = IntegerField(null=False, default=0)
    next_eligible_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    custom_fields = JSONBField(null=False, default={})
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    visibility = EnumField(enum_class=Visibility, null=False, default='internal')
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_sweep_state"
    _db_schema = "rag"
    _entity_token = "kg_sweep_state"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class LibraryAuditLog(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    actor_user_id = UUIDField()
    action = TextField(null=False)
    data_store_id = UUIDField()
    industry_id = UUIDField()
    target_organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', )
    detail = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    entity_type = TextField()
    entity_id = UUIDField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "library_audit_log"
    _db_schema = "rag"
    _entity_token = "rag_library_audit_log"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "ledger"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class LibraryDocs(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    title = TextField(null=False)
    short_code = TextField()
    kind = TextField(null=False)
    jurisdiction = TextField()
    body = TextField(null=False)
    storage_uri = TextField()
    source_url = TextField()
    doc_version = TextField()
    effective_from = DateField()
    effective_to = DateField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    deleted_at = DateTimeField()
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "library_docs"
    _db_schema = "rag"
    _entity_token = "library_doc"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class NerCanonicalizerShadow(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    run_id = UUIDField()
    input_pair_count = IntegerField(null=False, default=0)
    agent_input_json = JSONBField()
    agent_output_json = JSONBField()
    agent_merge_group_count = IntegerField(null=False, default=0)
    deterministic_groups_json = JSONBField()
    deterministic_merge_group_count = IntegerField(null=False, default=0)
    comparison_json = JSONBField()
    agreed_merge_surface_count = IntegerField(null=False, default=0)
    agent_only_merge_surface_count = IntegerField(null=False, default=0)
    deterministic_only_merge_surface_count = IntegerField(null=False, default=0)
    agent_model = TextField()
    agent_cost_usd = DecimalField()
    agent_elapsed_ms = IntegerField()
    agent_error = TextField()
    status = TextField(null=False, default='completed')
    created_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "ner_canonicalizer_shadow"
    _db_schema = "rag"
    _entity_token = "ner_shadow"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class RerankCache(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    cache_key = TextField(null=False)
    model = TextField(null=False)
    document_count = IntegerField(null=False)
    scores = JSONBField(null=False)
    hit_count = IntegerField(null=False, default=0)
    last_hit_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "rerank_cache"
    _db_schema = "rag"
    _entity_token = "rerank_cache"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class RetrievalAudit(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    query = TextField(null=False)
    query_hash = TextField(null=False)
    pipeline_config = JSONBField(null=False, default={})
    returned_chunk_ids = UUIDArrayField(null=False, default=[])
    rerank_scores = FloatArrayField()
    latency_ms = IntegerField()
    generation_id = UUIDField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "retrieval_audit"
    _db_schema = "rag"
    _entity_token = "retrieval_audit"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class ScopeSuggestions(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    scope_type_id = UUIDField()
    scope_type_label = TextField(null=False)
    suggested_name = TextField(null=False)
    suggested_slot_values = JSONBField(null=False, default={})
    reasoning = TextField()
    confidence = FloatField(null=False, default=0.5)
    status = TextField(null=False, default='pending')
    created_at = DateTimeField(null=False)
    decided_at = DateTimeField()
    decided_by = UUIDField()
    suppressed_until = DateTimeField()
    sweep_run_id = UUIDField()
    deleted_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "scope_suggestions"
    _db_schema = "rag"
    _entity_token = "scope_suggestion"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class DataStoreMembers(MatrxEntity):
    data_store_id = ForeignKey(to_model=DataStores, to_column='id', to_schema='rag', primary_key=True, null=False)
    source_kind = TextField(primary_key=True, null=False)
    source_id = TextField(primary_key=True, null=False)
    added_by = UUIDField(null=False)
    added_at = DateTimeField(null=False)
    notes = TextField()
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    id = UUIDField(null=False, unique=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "data_store_members"
    _db_schema = "rag"
    _entity_token = "data_store_members"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class EmbeddingsGoogleGemini21536(MatrxEntity):
    chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    owner_id = UUIDField(null=False)
    embedding = VectorField(dimensions=1536, null=False)
    embedded_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    id = UUIDField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "embeddings_google_gemini_2_1536"
    _db_schema = "rag"
    _entity_token = "embeddings_google_gemini_2_1536"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class EmbeddingsOai3Small1536(MatrxEntity):
    chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    embedding = VectorField(dimensions=1536, null=False)
    embedded_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    id = UUIDField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "embeddings_oai_3_small_1536"
    _db_schema = "rag"
    _entity_token = "embeddings_oai_3_small_1536"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class EmbeddingsVoyage4Large1024(MatrxEntity):
    chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    owner_id = UUIDField(null=False)
    embedding = VectorField(dimensions=1024, null=False)
    embedded_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    id = UUIDField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "embeddings_voyage_4_large_1024"
    _db_schema = "rag"
    _entity_token = "embeddings_voyage_4_large_1024"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class EmbeddingsVoyageCode31024(MatrxEntity):
    chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    embedding = VectorField(dimensions=1024, null=False)
    embedded_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    id = UUIDField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "embeddings_voyage_code_3_1024"
    _db_schema = "rag"
    _entity_token = "embeddings_voyage_code_3_1024"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class KgEntities(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    kind = TextField(null=False)
    name = TextField(null=False)
    canonical_id = TextField()
    cluster_id = ForeignKey(to_model=KgClusters, to_column='id', to_schema='rag', )
    attrs = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    confidence_avg = FloatField()
    mention_count = IntegerField(null=False, default=0)
    importance = FloatField()
    is_concept = BooleanField()
    embedding = VectorField(dimensions=1024, )
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'kg_chunk_entities': {'from_model': 'KgChunkEntities', 'from_field': 'entity_id', 'referenced_field': 'id', 'related_name': 'kg_chunk_entities', 'from_schema': 'rag'}, 'kg_edges': {'from_model': 'KgEdges', 'from_field': 'src_id', 'referenced_field': 'id', 'related_name': 'kg_edges', 'from_schema': 'rag'}, 'kg_entity_aliases': {'from_model': 'KgEntityAliases', 'from_field': 'entity_id', 'referenced_field': 'id', 'related_name': 'kg_entity_aliases', 'from_schema': 'rag'}, 'scope_association_suggestions': {'from_model': 'ScopeAssociationSuggestions', 'from_field': 'kg_entity_id', 'referenced_field': 'id', 'related_name': 'scope_association_suggestions', 'from_schema': 'rag'}, 'scope_item_value_suggestions': {'from_model': 'ScopeItemValueSuggestions', 'from_field': 'kg_entity_id', 'referenced_field': 'id', 'related_name': 'scope_item_value_suggestions', 'from_schema': 'rag'}}
    _database = "matrx_rag"
    _table_name = "kg_entities"
    _db_schema = "rag"
    _entity_token = "kg_entities"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KgValueMatches(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    kg_entity_id = UUIDField()
    target_scope_id = UUIDField(null=False)
    target_context_item_id = UUIDField(null=False)
    target_slot_key = TextField(null=False)
    matched_value = TextField(null=False)
    current_value_snapshot = TextField()
    mention_count = IntegerField(null=False, default=1)
    evidence_chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', )
    confidence = FloatField(null=False, default=1.0)
    created_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_value_matches"
    _db_schema = "rag"
    _entity_token = "kg_value_match"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class KgEdges(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    src_id = ForeignKey(to_model=KgEntities, to_column='id', to_schema='rag', null=False)
    dst_id = ForeignKey(to_model=KgEntities, to_column='id', to_schema='rag', null=False)
    kind = TextField(null=False)
    weight = FloatField()
    source_chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', )
    attrs = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "kg_edges"
    _db_schema = "rag"
    _entity_token = "kg_edges"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class KgEntityAliases(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    entity_id = ForeignKey(to_model=KgEntities, to_column='id', to_schema='rag', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    kind = TextField(null=False)
    surface_form = TextField(null=False)
    normalized_key = TextField(null=False)
    mention_count = IntegerField(null=False, default=0)
    first_seen_at = DateTimeField(null=False)
    last_seen_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'kg_chunk_entities': {'from_model': 'KgChunkEntities', 'from_field': 'alias_id', 'referenced_field': 'id', 'related_name': 'kg_chunk_entities', 'from_schema': 'rag'}}
    _database = "matrx_rag"
    _table_name = "kg_entity_aliases"
    _db_schema = "rag"
    _entity_token = "kg_entity_aliases"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class ScopeItemValueSuggestions(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    target_scope_id = UUIDField(null=False)
    target_context_item_id = UUIDField(null=False)
    target_slot_key = TextField(null=False)
    suggested_value = TextField(null=False)
    current_value_snapshot = TextField()
    kg_entity_id = ForeignKey(to_model=KgEntities, to_column='id', to_schema='rag', )
    evidence_chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', )
    match_kind = TextField(null=False)
    confidence = FloatField(null=False)
    status = TextField(null=False, default='pending')
    context_snippet = TextField()
    created_at = DateTimeField(null=False)
    decided_at = DateTimeField()
    decided_by = UUIDField()
    suppressed_until = DateTimeField()
    decision_note = TextField()
    viewed_at = DateTimeField()
    is_starred = BooleanField(null=False, default=False)
    sweep_run_id = UUIDField()
    deleted_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "scope_item_value_suggestions"
    _db_schema = "rag"
    _entity_token = "scope_item_value_suggestion"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class KgChunkEntities(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    chunk_id = ForeignKey(to_model=KgChunks, to_column='id', to_schema='rag', null=False)
    entity_id = ForeignKey(to_model=KgEntities, to_column='id', to_schema='rag', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    span_start = IntegerField()
    span_end = IntegerField()
    confidence = FloatField()
    attrs = JSONBField(null=False, default={})
    alias_id = ForeignKey(to_model=KgEntityAliases, to_column='id', to_schema='rag', )
    custom_fields = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scope_association_suggestions': {'from_model': 'ScopeAssociationSuggestions', 'from_field': 'kg_chunk_entity_id', 'referenced_field': 'id', 'related_name': 'scope_association_suggestions', 'from_schema': 'rag'}}
    _database = "matrx_rag"
    _table_name = "kg_chunk_entities"
    _db_schema = "rag"
    _entity_token = "kg_chunk_entities"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class ScopeAssociationSuggestions(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    kg_entity_id = ForeignKey(to_model=KgEntities, to_column='id', to_schema='rag', )
    kg_chunk_entity_id = ForeignKey(to_model=KgChunkEntities, to_column='id', to_schema='rag', )
    target_scope_id = UUIDField()
    target_scope_item_id = UUIDField()
    target_slot_name = TextField()
    suggested_value = TextField()
    match_kind = TextField(null=False)
    confidence = FloatField(null=False)
    status = TextField(null=False, default='pending')
    context_snippet = TextField()
    created_at = DateTimeField(null=False)
    decided_at = DateTimeField()
    decided_by = UUIDField()
    suppressed_until = DateTimeField()
    decision_note = TextField()
    viewed_at = DateTimeField()
    is_starred = BooleanField(null=False, default=False)
    sweep_run_id = UUIDField()
    deleted_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "scope_association_suggestions"
    _db_schema = "rag"
    _entity_token = "scope_association_suggestion"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

# Read-only model for the rag.data_store_grants VIEW (auto-generated — views are not writable).
class DataStoreGrants(Model):
    id = UUIDField()
    data_store_id = UUIDField()
    audience = TextField()
    industry_id = UUIDField()
    organization_id = UUIDField()
    granted_by = UUIDField()
    created_at = DateTimeField()
    _read_only = True
    _primary_keys = ['id']
    _table_name = "data_store_grants"
    _db_schema = "rag"
    _database = "matrx_rag"

__all__ = [
    "ContextItemSuggestions",
    "DataStores",
    "EmbeddingCache",
    "IngestRun",
    "KgAlerts",
    "KgChunks",
    "KgClusters",
    "KgSuggestionAck",
    "KgSweepQueue",
    "KgSweepRun",
    "KgSweepState",
    "LibraryAuditLog",
    "LibraryDocs",
    "NerCanonicalizerShadow",
    "RerankCache",
    "RetrievalAudit",
    "ScopeSuggestions",
    "DataStoreMembers",
    "EmbeddingsGoogleGemini21536",
    "EmbeddingsOai3Small1536",
    "EmbeddingsVoyage4Large1024",
    "EmbeddingsVoyageCode31024",
    "KgEntities",
    "KgValueMatches",
    "KgEdges",
    "KgEntityAliases",
    "ScopeItemValueSuggestions",
    "KgChunkEntities",
    "ScopeAssociationSuggestions",
    "Visibility",
    "ShownTo",
    "DataStoreGrants",
]


model_registry.register_all(
[
        ContextItemSuggestions,
        DataStores,
        EmbeddingCache,
        IngestRun,
        KgAlerts,
        KgChunks,
        KgClusters,
        KgSuggestionAck,
        KgSweepQueue,
        KgSweepRun,
        KgSweepState,
        LibraryAuditLog,
        LibraryDocs,
        NerCanonicalizerShadow,
        RerankCache,
        RetrievalAudit,
        ScopeSuggestions,
        DataStoreMembers,
        EmbeddingsGoogleGemini21536,
        EmbeddingsOai3Small1536,
        EmbeddingsVoyage4Large1024,
        EmbeddingsVoyageCode31024,
        KgEntities,
        KgValueMatches,
        KgEdges,
        KgEntityAliases,
        ScopeItemValueSuggestions,
        KgChunkEntities,
        ScopeAssociationSuggestions,
        DataStoreGrants
    ],
    skip_existing=True
)



@dataclass
class ContextItemSuggestionsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: ContextItemSuggestions):
        return cls(id=model.get_cache_key())


class ContextItemSuggestionsManager(BaseManager):
    def __init__(self):
        super().__init__(ContextItemSuggestions, ContextItemSuggestionsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: ContextItemSuggestions) -> None:
        pass



@dataclass
class DataStoresDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: DataStores):
        return cls(id=model.get_cache_key())


class DataStoresManager(BaseManager):
    def __init__(self):
        super().__init__(DataStores, DataStoresDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: DataStores) -> None:
        pass



@dataclass
class EmbeddingCacheDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: EmbeddingCache):
        return cls(id=model.get_cache_key())


class EmbeddingCacheManager(BaseManager):
    def __init__(self):
        super().__init__(EmbeddingCache, EmbeddingCacheDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: EmbeddingCache) -> None:
        pass



@dataclass
class IngestRunDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: IngestRun):
        return cls(id=model.get_cache_key())


class IngestRunManager(BaseManager):
    def __init__(self):
        super().__init__(IngestRun, IngestRunDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: IngestRun) -> None:
        pass



@dataclass
class KgAlertsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgAlerts):
        return cls(id=model.get_cache_key())


class KgAlertsManager(BaseManager):
    def __init__(self):
        super().__init__(KgAlerts, KgAlertsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgAlerts) -> None:
        pass



@dataclass
class KgChunksDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgChunks):
        return cls(id=model.get_cache_key())


class KgChunksManager(BaseManager):
    def __init__(self):
        super().__init__(KgChunks, KgChunksDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgChunks) -> None:
        pass



@dataclass
class KgClustersDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgClusters):
        return cls(id=model.get_cache_key())


class KgClustersManager(BaseManager):
    def __init__(self):
        super().__init__(KgClusters, KgClustersDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgClusters) -> None:
        pass



@dataclass
class KgSuggestionAckDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgSuggestionAck):
        return cls(id=model.get_cache_key())


class KgSuggestionAckManager(BaseManager):
    def __init__(self):
        super().__init__(KgSuggestionAck, KgSuggestionAckDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgSuggestionAck) -> None:
        pass



@dataclass
class KgSweepQueueDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgSweepQueue):
        return cls(id=model.get_cache_key())


class KgSweepQueueManager(BaseManager):
    def __init__(self):
        super().__init__(KgSweepQueue, KgSweepQueueDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgSweepQueue) -> None:
        pass



@dataclass
class KgSweepRunDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgSweepRun):
        return cls(id=model.get_cache_key())


class KgSweepRunManager(BaseManager):
    def __init__(self):
        super().__init__(KgSweepRun, KgSweepRunDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgSweepRun) -> None:
        pass



@dataclass
class KgSweepStateDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgSweepState):
        return cls(id=model.get_cache_key())


class KgSweepStateManager(BaseManager):
    def __init__(self):
        super().__init__(KgSweepState, KgSweepStateDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgSweepState) -> None:
        pass



@dataclass
class LibraryAuditLogDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: LibraryAuditLog):
        return cls(id=model.get_cache_key())


class LibraryAuditLogManager(BaseManager):
    def __init__(self):
        super().__init__(LibraryAuditLog, LibraryAuditLogDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: LibraryAuditLog) -> None:
        pass



@dataclass
class LibraryDocsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: LibraryDocs):
        return cls(id=model.get_cache_key())


class LibraryDocsManager(BaseManager):
    def __init__(self):
        super().__init__(LibraryDocs, LibraryDocsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: LibraryDocs) -> None:
        pass



@dataclass
class NerCanonicalizerShadowDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: NerCanonicalizerShadow):
        return cls(id=model.get_cache_key())


class NerCanonicalizerShadowManager(BaseManager):
    def __init__(self):
        super().__init__(NerCanonicalizerShadow, NerCanonicalizerShadowDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: NerCanonicalizerShadow) -> None:
        pass



@dataclass
class RerankCacheDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: RerankCache):
        return cls(id=model.get_cache_key())


class RerankCacheManager(BaseManager):
    def __init__(self):
        super().__init__(RerankCache, RerankCacheDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: RerankCache) -> None:
        pass



@dataclass
class RetrievalAuditDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: RetrievalAudit):
        return cls(id=model.get_cache_key())


class RetrievalAuditManager(BaseManager):
    def __init__(self):
        super().__init__(RetrievalAudit, RetrievalAuditDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: RetrievalAudit) -> None:
        pass



@dataclass
class ScopeSuggestionsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: ScopeSuggestions):
        return cls(id=model.get_cache_key())


class ScopeSuggestionsManager(BaseManager):
    def __init__(self):
        super().__init__(ScopeSuggestions, ScopeSuggestionsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: ScopeSuggestions) -> None:
        pass



@dataclass
class DataStoreMembersDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: DataStoreMembers):
        return cls(id=model.get_cache_key())


class DataStoreMembersManager(BaseManager):
    def __init__(self):
        super().__init__(DataStoreMembers, DataStoreMembersDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: DataStoreMembers) -> None:
        pass



@dataclass
class EmbeddingsGoogleGemini21536DTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: EmbeddingsGoogleGemini21536):
        return cls(id=model.get_cache_key())


class EmbeddingsGoogleGemini21536Manager(BaseManager):
    def __init__(self):
        super().__init__(EmbeddingsGoogleGemini21536, EmbeddingsGoogleGemini21536DTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: EmbeddingsGoogleGemini21536) -> None:
        pass



@dataclass
class EmbeddingsOai3Small1536DTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: EmbeddingsOai3Small1536):
        return cls(id=model.get_cache_key())


class EmbeddingsOai3Small1536Manager(BaseManager):
    def __init__(self):
        super().__init__(EmbeddingsOai3Small1536, EmbeddingsOai3Small1536DTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: EmbeddingsOai3Small1536) -> None:
        pass



@dataclass
class EmbeddingsVoyage4Large1024DTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: EmbeddingsVoyage4Large1024):
        return cls(id=model.get_cache_key())


class EmbeddingsVoyage4Large1024Manager(BaseManager):
    def __init__(self):
        super().__init__(EmbeddingsVoyage4Large1024, EmbeddingsVoyage4Large1024DTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: EmbeddingsVoyage4Large1024) -> None:
        pass



@dataclass
class EmbeddingsVoyageCode31024DTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: EmbeddingsVoyageCode31024):
        return cls(id=model.get_cache_key())


class EmbeddingsVoyageCode31024Manager(BaseManager):
    def __init__(self):
        super().__init__(EmbeddingsVoyageCode31024, EmbeddingsVoyageCode31024DTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: EmbeddingsVoyageCode31024) -> None:
        pass



@dataclass
class KgEntitiesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgEntities):
        return cls(id=model.get_cache_key())


class KgEntitiesManager(BaseManager):
    def __init__(self):
        super().__init__(KgEntities, KgEntitiesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgEntities) -> None:
        pass



@dataclass
class KgValueMatchesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgValueMatches):
        return cls(id=model.get_cache_key())


class KgValueMatchesManager(BaseManager):
    def __init__(self):
        super().__init__(KgValueMatches, KgValueMatchesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgValueMatches) -> None:
        pass



@dataclass
class KgEdgesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgEdges):
        return cls(id=model.get_cache_key())


class KgEdgesManager(BaseManager):
    def __init__(self):
        super().__init__(KgEdges, KgEdgesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgEdges) -> None:
        pass



@dataclass
class KgEntityAliasesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgEntityAliases):
        return cls(id=model.get_cache_key())


class KgEntityAliasesManager(BaseManager):
    def __init__(self):
        super().__init__(KgEntityAliases, KgEntityAliasesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgEntityAliases) -> None:
        pass



@dataclass
class ScopeItemValueSuggestionsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: ScopeItemValueSuggestions):
        return cls(id=model.get_cache_key())


class ScopeItemValueSuggestionsManager(BaseManager):
    def __init__(self):
        super().__init__(ScopeItemValueSuggestions, ScopeItemValueSuggestionsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: ScopeItemValueSuggestions) -> None:
        pass



@dataclass
class KgChunkEntitiesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: KgChunkEntities):
        return cls(id=model.get_cache_key())


class KgChunkEntitiesManager(BaseManager):
    def __init__(self):
        super().__init__(KgChunkEntities, KgChunkEntitiesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: KgChunkEntities) -> None:
        pass



@dataclass
class ScopeAssociationSuggestionsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: ScopeAssociationSuggestions):
        return cls(id=model.get_cache_key())


class ScopeAssociationSuggestionsManager(BaseManager):
    def __init__(self):
        super().__init__(ScopeAssociationSuggestions, ScopeAssociationSuggestionsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: ScopeAssociationSuggestions) -> None:
        pass