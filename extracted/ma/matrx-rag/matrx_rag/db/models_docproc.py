# File: matrx_rag/db/models_docproc.py
from matrx_orm import BooleanField, DateTimeField, DecimalField, EnumField, FloatField, ForeignKey, IntegerField, JSONBField, MatrxEntity, SmallIntegerField, TextArrayField, TextField, UUIDField, model_registry, BaseDTO, BaseManager
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

class ProcessedDocuments(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    source_kind = TextField(null=False)
    source_id = TextField(null=False)
    parent_processed_id = ForeignKey(to_model='ProcessedDocuments', to_column='id', to_schema='docproc', )
    derivation_kind = TextField(null=False, default='initial_extract')
    derivation_metadata = JSONBField(null=False, default={})
    name = TextField(null=False)
    mime_type = TextField()
    total_pages = IntegerField()
    source_hash = TextField(null=False)
    storage_uri = TextField()
    content = TextField()
    clean_content = TextField()
    structured_json = JSONBField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    file_content_hash = TextField()
    extractor_name = TextField(null=False, default='pymupdf')
    extractor_version = TextField(null=False, default='v1')
    cleaner_name = TextField()
    cleaner_version = TextField()
    params_hash = TextField()
    canonical_clean_id = ForeignKey(to_model='ProcessedDocuments', to_column='id', to_schema='docproc', )
    rag_boost = SmallIntegerField(null=False, default=0)
    replace_reason = TextField()
    clean_content_completed_at = DateTimeField()
    clean_content_cost_usd = DecimalField()
    archived_at = DateTimeField()
    archived_reason = TextField()
    deleted_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    custom_fields = JSONBField(null=False, default={})
    origin_client = TextField()
    capture_method = TextField()
    canonical_identity = TextField()
    content_hash = TextField()
    original_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    kept_at = DateTimeField()
    kept_by = UUIDField()
    intelligence_policy = TextField()
    visibility = EnumField(enum_class=Visibility, null=False)
    version = IntegerField(null=False, default=1)
    captured_at = DateTimeField(null=False)
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'derive_runs': {'from_model': 'DeriveRuns', 'from_field': 'processed_document_id', 'referenced_field': 'id', 'related_name': 'derive_runs', 'from_schema': 'docproc'}, 'page_extraction_jobs': {'from_model': 'PageExtractionJobs', 'from_field': 'processed_document_id', 'referenced_field': 'id', 'related_name': 'page_extraction_jobs', 'from_schema': 'docproc'}, 'processed_document_pages': {'from_model': 'ProcessedDocumentPages', 'from_field': 'processed_document_id', 'referenced_field': 'id', 'related_name': 'processed_document_pages', 'from_schema': 'docproc'}}
    _database = "matrx_rag"
    _table_name = "processed_documents"
    _db_schema = "docproc"
    _entity_token = "processed_document"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class ProcessedDocumentPages(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    processed_document_id = ForeignKey(to_model=ProcessedDocuments, to_column='id', to_schema='docproc', null=False)
    page_index = IntegerField(null=False)
    page_number = IntegerField(null=False)
    width = FloatField()
    height = FloatField()
    rotation = IntegerField()
    raw_text = TextField(null=False)
    raw_char_count = IntegerField(null=False, default=0)
    extraction_method = TextField()
    blocks = JSONBField()
    words = JSONBField()
    cleaned_text = TextField(null=False)
    cleaned_char_count = IntegerField(null=False, default=0)
    section_kind = TextField()
    section_title = TextField()
    is_continuation = BooleanField(null=False, default=False)
    used_ocr = BooleanField(null=False, default=False)
    extraction_confidence = FloatField()
    image_cld_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    image_dpi = IntegerField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    section_subtype = TextField()
    verified_at = DateTimeField()
    verification_flags = TextArrayField()
    custom_fields = JSONBField(null=False, default={})
    portion_kind = TextField(null=False, default='page')
    locator = JSONBField(null=False, default={})
    speaker = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_rag"
    _table_name = "processed_document_pages"
    _db_schema = "docproc"
    _entity_token = "processed_document_page"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

__all__ = [
    "ProcessedDocuments",
    "ProcessedDocumentPages",
    "Visibility",
    "ShownTo",
]


model_registry.register_all(
[
        ProcessedDocuments,
        ProcessedDocumentPages
    ],
    skip_existing=True
)