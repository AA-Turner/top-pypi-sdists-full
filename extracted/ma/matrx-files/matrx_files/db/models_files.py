# File: matrx_files/db/models_files.py
from matrx_orm import BigIntegerField, BooleanField, DateField, DateTimeField, EnumField, FloatField, ForeignKey, IntegerField, JSONBField, MatrxEntity, Model, TextArrayField, TextField, UUIDField, model_registry, BaseDTO, BaseManager
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

class AccountTiers(MatrxEntity):
    tier_key = TextField(primary_key=True, null=False)
    name = TextField(null=False)
    is_default_for_users = BooleanField(null=False, default=False)
    is_default_for_guests = BooleanField(null=False, default=False)
    max_storage_bytes = BigIntegerField()
    max_file_size_bytes = BigIntegerField()
    max_files = IntegerField()
    max_versions_per_file = IntegerField()
    max_daily_uploads = IntegerField()
    max_daily_upload_bytes = BigIntegerField()
    max_share_links_per_resource = IntegerField()
    max_bulk_items = IntegerField()
    rate_limit_uploads_per_min = IntegerField()
    rate_limit_downloads_per_min = IntegerField()
    rate_limit_general_per_min = IntegerField()
    features = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    id = UUIDField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False)
    shown_to = EnumField(enum_class=ShownTo, )
    deleted_at = DateTimeField()
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'user_account': {'from_model': 'UserAccount', 'from_field': 'tier_id', 'referenced_field': 'tier_key', 'related_name': 'user_account', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "account_tiers"
    _db_schema = "files"
    _entity_token = "files_account_tier"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



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

class Folders(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    folder_path = TextField(null=False)
    folder_name = TextField(null=False)
    parent_id = ForeignKey(to_model='Folders', to_column='id', to_schema='files', )
    visibility = EnumField(enum_class=Visibility, null=False)
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    is_system = BooleanField(null=False, default=False)
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    version = IntegerField(null=False, default=1)
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'files': {'from_model': 'Files', 'from_field': 'parent_folder_id', 'referenced_field': 'id', 'related_name': 'files', 'from_schema': 'files'}, 'sync_mappings': {'from_model': 'SyncMappings', 'from_field': 'folder_id', 'referenced_field': 'id', 'related_name': 'sync_mappings', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "folders"
    _db_schema = "files"
    _entity_token = "folder"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class Idempotency(MatrxEntity):
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', primary_key=True, null=False)
    idempotency_key = TextField(primary_key=True, null=False)
    request_hash = TextField(null=False)
    endpoint = TextField(null=False)
    status_code = IntegerField(null=False)
    response_body = JSONBField(null=False)
    resource_id = UUIDField()
    resource_type = TextField()
    created_at = DateTimeField(null=False)
    expires_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "idempotency"
    _db_schema = "files"
    _entity_token = "idempotency"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
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

class MachineWrittenPrefixes(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    prefix = TextField(null=False)
    label = TextField(null=False)
    writer = TextField(null=False)
    description = TextField()
    deselect_by_default = BooleanField(null=False, default=True)
    is_active = BooleanField(null=False, default=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "machine_written_prefixes"
    _db_schema = "files"
    _entity_token = "files_machine_written_prefix"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class RateLimitBuckets(MatrxEntity):
    actor_id = UUIDField(primary_key=True, null=False)
    bucket_kind = TextField(primary_key=True, null=False)
    minute_bucket = DateTimeField(primary_key=True, null=False)
    counter = IntegerField(null=False, default=0)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "rate_limit_buckets"
    _db_schema = "files"
    _entity_token = "rate_limit_buckets"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"

class UploadsInflight(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    file_id = UUIDField(null=False)
    file_path = TextField(null=False)
    bucket = TextField(null=False)
    key = TextField(null=False)
    multipart_upload_id = TextField(null=False)
    upload_length = BigIntegerField(null=False)
    upload_offset = BigIntegerField(null=False, default=0)
    visibility = TextField(null=False, default='personal')
    mime_type = TextField()
    file_name = TextField(null=False)
    idempotency_key = TextField()
    metadata = JSONBField(null=False, default={})
    parts = JSONBField(null=False, default=[])
    status = TextField(null=False, default='in_progress')
    expires_at = DateTimeField(null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "uploads_inflight"
    _db_schema = "files"
    _entity_token = "uploads_inflight"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"

class UserStorageUsage(MatrxEntity):
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', primary_key=True, null=False)
    bytes_used = BigIntegerField(null=False, default=0)
    files_count = IntegerField(null=False, default=0)
    daily_upload_count = IntegerField(null=False, default=0)
    daily_upload_bytes = BigIntegerField(null=False, default=0)
    daily_reset_at = DateField(null=False)
    updated_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    id = UUIDField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "user_storage_usage"
    _db_schema = "files"
    _entity_token = "user_storage_usage"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "personal"

class WebhookDispatchState(MatrxEntity):
    id = BooleanField(primary_key=True, null=False, default=True)
    last_activity_log_id = BigIntegerField(null=False, default=0)
    updated_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "webhook_dispatch_state"
    _db_schema = "files"
    _entity_token = "webhook_dispatch_state"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"

class Webhooks(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    target_url = TextField(null=False)
    secret = TextField(null=False)
    description = TextField()
    is_active = BooleanField(null=False, default=True)
    event_types = TextArrayField()
    resource_types = TextArrayField()
    last_attempt_at = DateTimeField()
    last_success_at = DateTimeField()
    consecutive_failures = IntegerField(null=False, default=0)
    max_consecutive_failures = IntegerField(null=False, default=50)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    custom_fields = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'webhook_deliveries': {'from_model': 'WebhookDeliveries', 'from_field': 'webhook_id', 'referenced_field': 'id', 'related_name': 'webhook_deliveries', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "webhooks"
    _db_schema = "files"
    _entity_token = "webhooks"
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

class Files(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    file_path = TextField(null=False)
    file_name = TextField(null=False)
    mime_type = TextField()
    size_bytes = BigIntegerField()
    checksum = TextField()
    visibility = EnumField(enum_class=Visibility, null=False)
    current_version = IntegerField(null=False, default=1)
    parent_folder_id = ForeignKey(to_model=Folders, to_column='id', to_schema='files', )
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    parent_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    derivation_kind = TextField()
    derivation_metadata = JSONBField(null=False, default={})
    storage_uri = TextField(null=False)
    duplicate_of_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    canonical_processed_document_id = ForeignKey(to_model='ProcessedDocuments', to_column='id', to_schema='docproc', )
    width = IntegerField()
    height = IntegerField()
    duration_ms = IntegerField()
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    origin_device_id = ForeignKey(to_model='AppInstances', to_column='id', to_schema='public', )
    client_modified_at = DateTimeField()
    artifact_kind = TextField()
    provider_session_id = TextField()
    custom_fields = JSONBField(null=False, default={})
    parent_record_type = TextField()
    parent_record_id = UUIDField()
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'file_rag_jobs': {'from_model': 'FileRagJobs', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'file_rag_jobs', 'from_schema': 'files'}, 'file_versions': {'from_model': 'FileVersions', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'file_versions', 'from_schema': 'files'}, 'analysis': {'from_model': 'Analysis', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'analysis', 'from_schema': 'files'}, 'analysis_result': {'from_model': 'AnalysisResult', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'analysis_result', 'from_schema': 'files'}, 'entities': {'from_model': 'Entities', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'entities', 'from_schema': 'files'}, 'overrides': {'from_model': 'Overrides', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'overrides', 'from_schema': 'files'}, 'page_annotations': {'from_model': 'PageAnnotations', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'page_annotations', 'from_schema': 'files'}, 'pages': {'from_model': 'Pages', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'pages', 'from_schema': 'files'}, 'structure': {'from_model': 'Structure', 'from_field': 'file_id', 'referenced_field': 'id', 'related_name': 'structure', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "files"
    _db_schema = "files"
    _entity_token = "file"
    _is_versioned = True
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

class SyncMappings(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    device_id = ForeignKey(to_model='AppInstances', to_column='id', to_schema='public', null=False)
    folder_id = ForeignKey(to_model=Folders, to_column='id', to_schema='files', )
    local_path = TextField(null=False)
    local_path_display = TextField()
    direction = TextField(null=False, default='two_way')
    desired_state = TextField(null=False, default='active')
    state = TextField(null=False, default='pending')
    state_reason = TextField()
    state_changed_at = DateTimeField()
    last_seen_at = DateTimeField()
    last_synced_at = DateTimeField()
    items_total = BigIntegerField()
    bytes_total = BigIntegerField()
    knobs = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
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
    _database = "matrx_files"
    _table_name = "sync_mappings"
    _db_schema = "files"
    _entity_token = "files_sync_mapping"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class UserAccount(MatrxEntity):
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', primary_key=True, null=False)
    tier_id = ForeignKey(to_model=AccountTiers, to_column='tier_key', to_schema='files', null=False)
    custom_limits = JSONBField(null=False, default={})
    is_blocked = BooleanField(null=False, default=False)
    blocked_reason = TextField()
    notes = TextField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    id = UUIDField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "user_account"
    _db_schema = "files"
    _entity_token = "files_user_account"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "personal"

class WebhookDeliveries(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    webhook_id = ForeignKey(to_model=Webhooks, to_column='id', to_schema='files', null=False)
    attempt = IntegerField(null=False, default=1)
    status = TextField(null=False, default='pending')
    http_status = IntegerField()
    latency_ms = IntegerField()
    error_message = TextField()
    next_attempt_at = DateTimeField()
    created_at = DateTimeField(null=False)
    completed_at = DateTimeField()
    activity_log_id = ForeignKey(to_model='ActivityLog', to_column='id', to_schema='platform', )
    net_request_id = BigIntegerField()
    signature = TextField()
    dispatched_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "webhook_deliveries"
    _db_schema = "files"
    _entity_token = "webhook_deliveries"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class Analysis(MatrxEntity):
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', primary_key=True, null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    mime_type = TextField()
    status = TextField(null=False, default='pending')
    analyzer_version = TextField(null=False, default='v1.0.0')
    detectors_run = JSONBField(null=False, default={})
    progress = JSONBField(null=False, default={'total': 0, 'complete': 0})
    classification = JSONBField()
    page_count = IntegerField()
    summary_counts = JSONBField(null=False, default={})
    text_source_map = JSONBField()
    thumbnail_url = TextField()
    metadata = JSONBField(null=False, default={})
    started_at = DateTimeField(null=False)
    completed_at = DateTimeField()
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    id = UUIDField(null=False, unique=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "analysis"
    _db_schema = "files"
    _entity_token = "file_analysis"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class FileRagJobs(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    status = TextField(null=False, default='pending')
    trigger_source = TextField(null=False, default='auto')
    scheduled_for = DateTimeField(null=False)
    started_at = DateTimeField()
    completed_at = DateTimeField()
    attempt_count = IntegerField(null=False, default=0)
    skipped_reason = TextField()
    error = JSONBField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "file_rag_jobs"
    _db_schema = "files"
    _entity_token = "file_rag_job"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class FileVersions(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    version_number = IntegerField(null=False)
    storage_uri = TextField(null=False)
    size_bytes = BigIntegerField()
    checksum = TextField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    change_summary = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    page_receipt = JSONBField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "file_versions"
    _db_schema = "files"
    _entity_token = "file_version"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class Pages(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    page_index = IntegerField(null=False)
    source_page_index = IntegerField(null=False)
    status = TextField(null=False, default='active')
    excluded_reason = TextField()
    excluded_at = DateTimeField()
    excluded_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    user_modified = BooleanField(null=False, default=False)
    width_pt = FloatField()
    height_pt = FloatField()
    rotation = IntegerField(null=False, default=0)
    text_source = TextField(null=False, default='unknown')
    ocr_confidence = FloatField()
    thumbnail_url = TextField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    processed_document_page_id = ForeignKey(to_model='ProcessedDocumentPages', to_column='id', to_schema='docproc', )
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'analysis_result': {'from_model': 'AnalysisResult', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'analysis_result', 'from_schema': 'files'}, 'overrides': {'from_model': 'Overrides', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'overrides', 'from_schema': 'files'}, 'page_annotations': {'from_model': 'PageAnnotations', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'page_annotations', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "pages"
    _db_schema = "files"
    _entity_token = "file_pages"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Structure(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    bucket_id = TextField(null=False)
    path = TextField(null=False)
    is_folder = BooleanField(null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', )
    parent_path = TextField()
    name = TextField(null=False)
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "structure"
    _db_schema = "files"
    _entity_token = "structure"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class AnalysisResult(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    detector_kind = TextField(null=False)
    detector_version = TextField(null=False, default='v1')
    confidence_tier = TextField(null=False, default='n/a')
    status = TextField(null=False, default='success')
    text_sources = TextArrayField(null=False, default=[])
    elapsed_ms = IntegerField(null=False, default=0)
    summary = JSONBField(null=False, default={})
    payload = JSONBField()
    payload_uri = TextField()
    payload_bytes = BigIntegerField(null=False, default=0)
    error = TextField()
    created_at = DateTimeField(null=False)
    page_id = ForeignKey(to_model=Pages, to_column='id', to_schema='files', )
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'page_annotations': {'from_model': 'PageAnnotations', 'from_field': 'parent_result_id', 'referenced_field': 'id', 'related_name': 'page_annotations', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "analysis_result"
    _db_schema = "files"
    _entity_token = "analysis_result"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class Overrides(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    page_id = ForeignKey(to_model=Pages, to_column='id', to_schema='files', )
    override_kind = TextField(null=False)
    override_value = JSONBField(null=False)
    notes = TextField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "overrides"
    _db_schema = "files"
    _entity_token = "file_overrides"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Entities(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    label = TextField(null=False)
    label_category = TextField(null=False, default='custom')
    canonical_value = TextField(null=False)
    normalized_value = JSONBField()
    source_annotation_id = ForeignKey(to_model='PageAnnotations', to_column='id', to_schema='files', )
    is_user_named = BooleanField(null=False, default=True)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'page_annotations': {'from_model': 'PageAnnotations', 'from_field': 'entity_id', 'referenced_field': 'id', 'related_name': 'page_annotations', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "entities"
    _db_schema = "files"
    _entity_token = "file_entities"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class PageAnnotations(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    file_id = ForeignKey(to_model=Files, to_column='id', to_schema='files', null=False)
    owner_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    page_number = IntegerField(null=False)
    bbox = JSONBField(null=False)
    label = TextField(null=False)
    label_category = TextField(null=False, default='custom')
    extracted_text = TextField()
    extracted_text_source = TextField(null=False, default='native')
    normalized_value = JSONBField()
    source = TextField(null=False, default='user')
    status = TextField(null=False, default='active')
    redact = BooleanField(null=False, default=False)
    notes = TextField()
    parent_result_id = ForeignKey(to_model=AnalysisResult, to_column='id', to_schema='files', )
    redaction_span_id = TextField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    last_edited_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    page_id = ForeignKey(to_model=Pages, to_column='id', to_schema='files', )
    is_user_locked = BooleanField(null=False, default=True)
    entity_id = ForeignKey(to_model=Entities, to_column='id', to_schema='files', )
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'entities': {'from_model': 'Entities', 'from_field': 'source_annotation_id', 'referenced_field': 'id', 'related_name': 'entities', 'from_schema': 'files'}}
    _database = "matrx_files"
    _table_name = "page_annotations"
    _db_schema = "files"
    _entity_token = "file_page_annotations"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

# Read-only model for the files.sync_mapping_admin_status VIEW (auto-generated — views are not writable).
class SyncMappingAdminStatus(Model):
    id = UUIDField()
    user_id = UUIDField()
    device_id = UUIDField()
    organization_id = UUIDField()
    direction = TextField()
    desired_state = TextField()
    state = TextField()
    state_changed_at = DateTimeField()
    last_seen_at = DateTimeField()
    last_synced_at = DateTimeField()
    items_total = BigIntegerField()
    bytes_total = BigIntegerField()
    created_at = DateTimeField()
    _read_only = True
    _primary_keys = ['id']
    _table_name = "sync_mapping_admin_status"
    _db_schema = "files"
    _database = "matrx_files"

__all__ = [
    "AccountTiers",
    "Folders",
    "Idempotency",
    "MachineWrittenPrefixes",
    "RateLimitBuckets",
    "UploadsInflight",
    "UserStorageUsage",
    "WebhookDispatchState",
    "Webhooks",
    "Files",
    "SyncMappings",
    "UserAccount",
    "WebhookDeliveries",
    "Analysis",
    "FileRagJobs",
    "FileVersions",
    "Pages",
    "Structure",
    "AnalysisResult",
    "Overrides",
    "Entities",
    "PageAnnotations",
    "Visibility",
    "ShownTo",
    "SyncMappingAdminStatus",
]


model_registry.register_all(
[
        AccountTiers,
        Folders,
        Idempotency,
        MachineWrittenPrefixes,
        RateLimitBuckets,
        UploadsInflight,
        UserStorageUsage,
        WebhookDispatchState,
        Webhooks,
        Files,
        SyncMappings,
        UserAccount,
        WebhookDeliveries,
        Analysis,
        FileRagJobs,
        FileVersions,
        Pages,
        Structure,
        AnalysisResult,
        Overrides,
        Entities,
        PageAnnotations,
        SyncMappingAdminStatus
    ],
    skip_existing=True
)



@dataclass
class AccountTiersDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: AccountTiers):
        return cls(id=model.get_cache_key())


class AccountTiersManager(BaseManager):
    def __init__(self):
        super().__init__(AccountTiers, AccountTiersDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: AccountTiers) -> None:
        pass



@dataclass
class FoldersDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Folders):
        return cls(id=model.get_cache_key())


class FoldersManager(BaseManager):
    def __init__(self):
        super().__init__(Folders, FoldersDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Folders) -> None:
        pass



@dataclass
class IdempotencyDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Idempotency):
        return cls(id=model.get_cache_key())


class IdempotencyManager(BaseManager):
    def __init__(self):
        super().__init__(Idempotency, IdempotencyDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Idempotency) -> None:
        pass



@dataclass
class MachineWrittenPrefixesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: MachineWrittenPrefixes):
        return cls(id=model.get_cache_key())


class MachineWrittenPrefixesManager(BaseManager):
    def __init__(self):
        super().__init__(MachineWrittenPrefixes, MachineWrittenPrefixesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: MachineWrittenPrefixes) -> None:
        pass



@dataclass
class RateLimitBucketsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: RateLimitBuckets):
        return cls(id=model.get_cache_key())


class RateLimitBucketsManager(BaseManager):
    def __init__(self):
        super().__init__(RateLimitBuckets, RateLimitBucketsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: RateLimitBuckets) -> None:
        pass



@dataclass
class UploadsInflightDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: UploadsInflight):
        return cls(id=model.get_cache_key())


class UploadsInflightManager(BaseManager):
    def __init__(self):
        super().__init__(UploadsInflight, UploadsInflightDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: UploadsInflight) -> None:
        pass



@dataclass
class UserStorageUsageDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: UserStorageUsage):
        return cls(id=model.get_cache_key())


class UserStorageUsageManager(BaseManager):
    def __init__(self):
        super().__init__(UserStorageUsage, UserStorageUsageDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: UserStorageUsage) -> None:
        pass



@dataclass
class WebhookDispatchStateDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: WebhookDispatchState):
        return cls(id=model.get_cache_key())


class WebhookDispatchStateManager(BaseManager):
    def __init__(self):
        super().__init__(WebhookDispatchState, WebhookDispatchStateDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: WebhookDispatchState) -> None:
        pass



@dataclass
class WebhooksDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Webhooks):
        return cls(id=model.get_cache_key())


class WebhooksManager(BaseManager):
    def __init__(self):
        super().__init__(Webhooks, WebhooksDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Webhooks) -> None:
        pass



@dataclass
class FilesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Files):
        return cls(id=model.get_cache_key())


class FilesManager(BaseManager):
    def __init__(self):
        super().__init__(Files, FilesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Files) -> None:
        pass



@dataclass
class SyncMappingsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: SyncMappings):
        return cls(id=model.get_cache_key())


class SyncMappingsManager(BaseManager):
    def __init__(self):
        super().__init__(SyncMappings, SyncMappingsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: SyncMappings) -> None:
        pass



@dataclass
class UserAccountDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: UserAccount):
        return cls(id=model.get_cache_key())


class UserAccountManager(BaseManager):
    def __init__(self):
        super().__init__(UserAccount, UserAccountDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: UserAccount) -> None:
        pass



@dataclass
class WebhookDeliveriesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: WebhookDeliveries):
        return cls(id=model.get_cache_key())


class WebhookDeliveriesManager(BaseManager):
    def __init__(self):
        super().__init__(WebhookDeliveries, WebhookDeliveriesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: WebhookDeliveries) -> None:
        pass



@dataclass
class AnalysisDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Analysis):
        return cls(id=model.get_cache_key())


class AnalysisManager(BaseManager):
    def __init__(self):
        super().__init__(Analysis, AnalysisDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Analysis) -> None:
        pass



@dataclass
class FileRagJobsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: FileRagJobs):
        return cls(id=model.get_cache_key())


class FileRagJobsManager(BaseManager):
    def __init__(self):
        super().__init__(FileRagJobs, FileRagJobsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: FileRagJobs) -> None:
        pass



@dataclass
class FileVersionsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: FileVersions):
        return cls(id=model.get_cache_key())


class FileVersionsManager(BaseManager):
    def __init__(self):
        super().__init__(FileVersions, FileVersionsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: FileVersions) -> None:
        pass



@dataclass
class PagesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Pages):
        return cls(id=model.get_cache_key())


class PagesManager(BaseManager):
    def __init__(self):
        super().__init__(Pages, PagesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Pages) -> None:
        pass



@dataclass
class StructureDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Structure):
        return cls(id=model.get_cache_key())


class StructureManager(BaseManager):
    def __init__(self):
        super().__init__(Structure, StructureDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Structure) -> None:
        pass



@dataclass
class AnalysisResultDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: AnalysisResult):
        return cls(id=model.get_cache_key())


class AnalysisResultManager(BaseManager):
    def __init__(self):
        super().__init__(AnalysisResult, AnalysisResultDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: AnalysisResult) -> None:
        pass



@dataclass
class OverridesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Overrides):
        return cls(id=model.get_cache_key())


class OverridesManager(BaseManager):
    def __init__(self):
        super().__init__(Overrides, OverridesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Overrides) -> None:
        pass



@dataclass
class EntitiesDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: Entities):
        return cls(id=model.get_cache_key())


class EntitiesManager(BaseManager):
    def __init__(self):
        super().__init__(Entities, EntitiesDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: Entities) -> None:
        pass



@dataclass
class PageAnnotationsDTO(BaseDTO):
    id: str

    @classmethod
    async def from_model(cls, model: PageAnnotations):
        return cls(id=model.get_cache_key())


class PageAnnotationsManager(BaseManager):
    def __init__(self):
        super().__init__(PageAnnotations, PageAnnotationsDTO)

    def _initialize_manager(self):
        super()._initialize_manager()

    async def _initialize_runtime_data(self, item: PageAnnotations) -> None:
        pass