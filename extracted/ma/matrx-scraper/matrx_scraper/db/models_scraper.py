# File: matrx_scraper/db/models_scraper.py
from matrx_orm import BooleanField, CharField, DateTimeField, DecimalField, EnumField, ForeignKey, IntegerField, JSONBField, MatrxEntity, Model, TextField, UUIDField, model_registry, BaseDTO, BaseManager
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

class ComparisonRun(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    kind = TextField(null=False)
    request = JSONBField(null=False, default={})
    item_count = IntegerField(null=False, default=0)
    status = TextField(null=False, default='running')
    progress = JSONBField(null=False, default=[])
    facts = JSONBField(null=False, default={})
    result = JSONBField()
    error_code = TextField()
    error = TextField()
    started_at = DateTimeField()
    finished_at = DateTimeField()
    lease_until = DateTimeField(null=False)
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
    _database = "matrx_scraper"
    _table_name = "comparison_run"
    _db_schema = "scraper"
    _entity_token = "scraper_comparison_run"
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

class DataFetchJob(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    source_key = TextField(null=False)
    dataset_id = TextField()
    inputs = JSONBField(null=False, default=[])
    max_records = IntegerField(null=False)
    table_id = UUIDField()
    table_name = TextField()  # type: ignore[override]
    key_column = TextField()
    snapshot_id = TextField()
    status = TextField(null=False, default='queued')
    records_billed = IntegerField(null=False, default=0)
    billed_at = DateTimeField()
    rows_created = IntegerField(null=False, default=0)
    rows_updated = IntegerField(null=False, default=0)
    values_as_text = IntegerField(null=False, default=0)
    cost_usd = DecimalField()
    result = JSONBField()
    error_code = TextField()
    error = TextField()
    started_at = DateTimeField()
    finished_at = DateTimeField()
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
    lease_until = DateTimeField(null=False)
    call_id = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    provider_ready_at = DateTimeField()
    collected_at = DateTimeField()
    saved_at = DateTimeField()
    stage_log = JSONBField(null=False, default=[])
    duration_ms = IntegerField()
    row_key_field = TextField()
    member_result = JSONBField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'data_fetch_job_row': {'from_model': 'DataFetchJobRow', 'from_field': 'job_id', 'referenced_field': 'id', 'related_name': 'data_fetch_job_row', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "data_fetch_job"
    _db_schema = "scraper"
    _entity_token = "scraper_data_fetch_job"
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

class DataSource(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    key = TextField(null=False)
    label = TextField(null=False)
    group_name = TextField(null=False)
    subgroup = TextField()
    description = TextField(null=False)
    input_kind = TextField(null=False, default='url')
    input_spec = JSONBField(null=False, default={})
    output_fields = JSONBField(null=False, default=[])
    key_column = TextField()
    url_pattern = JSONBField()
    auto_route = BooleanField(null=False, default=False)
    enabled = BooleanField(null=False, default=True)
    featured = BooleanField(null=False, default=False)
    verified_live = BooleanField(null=False, default=False)
    known_issue = TextField()
    supports_collection = BooleanField(null=False, default=True)
    sort_order = IntegerField(null=False, default=0)
    dataset_id = TextField(null=False)
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
    usd_per_record = DecimalField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    method = TextField()
    provider = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "data_source"
    _db_schema = "scraper"
    _entity_token = "scraper_data_source"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class ScrapeDomain(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    url = CharField()
    common_name = CharField()
    scrape_allowed = BooleanField(default=True)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField()
    policy_action = TextField()
    min_content_chars = IntegerField()
    min_real_content_chars = IntegerField()
    content_selector = TextField()
    policy_notes = TextField()
    category = TextField()
    category_reason = TextField()
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scrape_domain_settings': {'from_model': 'ScrapeDomainSettings', 'from_field': 'domain_id', 'referenced_field': 'id', 'related_name': 'scrape_domain_settings', 'from_schema': 'scraper'}, 'scrape_path_pattern': {'from_model': 'ScrapePathPattern', 'from_field': 'scrape_domain_id', 'referenced_field': 'id', 'related_name': 'scrape_path_pattern', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "scrape_domain"
    _db_schema = "scraper"
    _entity_token = "scrape_domain"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = False
    _rls_variant = "reference"

class ScrapeFailureLog(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    target_url = TextField(null=False)
    domain_name = TextField(null=False)
    failure_reason = TextField(null=False)
    failure_category = TextField()
    status_code = IntegerField()
    error_log = TextField()
    proxy_used = BooleanField(null=False, default=False)
    proxy_type = TextField()
    attempt_count = IntegerField(null=False, default=1)
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scrape_retry_queue': {'from_model': 'ScrapeRetryQueue', 'from_field': 'failure_log_id', 'referenced_field': 'id', 'related_name': 'scrape_retry_queue', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "scrape_failure_log"
    _db_schema = "scraper"
    _entity_token = "scrape_failure_log"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
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

class ScrapeParsedPage(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    page_name = CharField(null=False)
    validity = CharField(null=False)
    remote_path = CharField()
    local_path = CharField()
    scraped_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    expires_at = DateTimeField()
    url = TextField()
    domain = TextField()
    content = JSONBField()
    char_count = IntegerField()
    content_type = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    canonical_url = TextField()
    content_hash = TextField()
    title = TextField()
    final_url = TextField()
    capture_method = TextField()
    captured_by_rung = TextField()
    origin_client = TextField()
    rung_trail = JSONBField(null=False, default=[])
    html_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    processed_document_id = ForeignKey(to_model='ProcessedDocuments', to_column='id', to_schema='docproc', )
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_parsed_page"
    _db_schema = "scraper"
    _entity_token = "scrape_parsed_page"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class DataFetchJobRow(MatrxEntity):
    job_id = ForeignKey(to_model=DataFetchJob, to_column='id', to_schema='scraper', primary_key=True, null=False)
    row_key = TextField(primary_key=True, null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "data_fetch_job_row"
    _db_schema = "scraper"
    _entity_token = "scraper_data_fetch_job_row"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"

class ScrapeDomainSettings(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    domain_id = ForeignKey(to_model=ScrapeDomain, to_column='id', to_schema='scraper', null=False, unique=True)
    enabled = BooleanField(null=False, default=True)
    proxy_type = TextField(null=False, default='datacenter')
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_domain_settings"
    _db_schema = "scraper"
    _entity_token = "scrape_domain_settings"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = False
    _rls_variant = "reference"

class ScrapePathPattern(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    scrape_domain_id = ForeignKey(to_model=ScrapeDomain, to_column='id', to_schema='scraper', )
    path_pattern = CharField(default='/*')
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField()
    policy_action = TextField()
    min_content_chars = IntegerField()
    min_real_content_chars = IntegerField()
    content_selector = TextField()
    policy_notes = TextField()
    category = TextField()
    category_reason = TextField()
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scrape_path_override': {'from_model': 'ScrapePathOverride', 'from_field': 'path_pattern_id', 'referenced_field': 'id', 'related_name': 'scrape_path_override', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "scrape_path_pattern"
    _db_schema = "scraper"
    _entity_token = "scrape_path_pattern"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = False
    _rls_variant = "reference"

class ScrapeRetryQueue(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    target_url = TextField(null=False)
    domain_name = TextField(null=False)
    failure_log_id = ForeignKey(to_model=ScrapeFailureLog, to_column='id', to_schema='scraper', )
    failure_reason = TextField(null=False)
    original_failure_at = DateTimeField(null=False)
    request_context = JSONBField(null=False, default={})
    status = TextField(null=False, default='pending')
    tier = TextField(null=False, default='desktop')
    claimed_by = TextField()
    claimed_at = DateTimeField()
    claim_expires_at = DateTimeField()
    attempt_count = IntegerField(null=False, default=0)
    last_error = TextField()
    completed_at = DateTimeField()
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_retry_queue"
    _db_schema = "scraper"
    _entity_token = "scrape_retry_queue"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "system"

class ScrapePathOverride(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    path_pattern_id = ForeignKey(to_model=ScrapePathPattern, to_column='id', to_schema='scraper', null=False)
    is_active = BooleanField(null=False, default=True)
    config_type = TextField(null=False)
    selector_type = TextField(null=False)
    match_type = TextField(null=False)
    action = TextField(null=False)
    values = JSONBField(null=False, default=[])
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_path_override"
    _db_schema = "scraper"
    _entity_token = "scrape_path_override"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = False
    _rls_variant = "reference"

__all__ = [
    "ComparisonRun",
    "DataFetchJob",
    "DataSource",
    "ScrapeDomain",
    "ScrapeFailureLog",
    "ScrapeParsedPage",
    "DataFetchJobRow",
    "ScrapeDomainSettings",
    "ScrapePathPattern",
    "ScrapeRetryQueue",
    "ScrapePathOverride",
    "Visibility",
    "ShownTo",
]


model_registry.register_all(
[
        ComparisonRun,
        DataFetchJob,
        DataSource,
        ScrapeDomain,
        ScrapeFailureLog,
        ScrapeParsedPage,
        DataFetchJobRow,
        ScrapeDomainSettings,
        ScrapePathPattern,
        ScrapeRetryQueue,
        ScrapePathOverride
    ],
    skip_existing=True
)