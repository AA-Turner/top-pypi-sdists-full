# File: matrx_scraper/db/models_scraper.py
from matrx_orm import BooleanField, CharField, DateTimeField, ForeignKey, IntegerField, JSONBField, Model, TextField, UUIDField, model_registry, BaseDTO, BaseManager
from dataclasses import dataclass
from typing import ClassVar

class ScrapeDomain(Model):
    id = UUIDField(primary_key=True, null=False)
    url = CharField()
    common_name = CharField()
    scrape_allowed = BooleanField(default=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    is_public = BooleanField(default=False)
    policy_action = TextField()
    min_content_chars = IntegerField()
    min_real_content_chars = IntegerField()
    content_selector = TextField()
    policy_notes = TextField()
    category = TextField()
    category_reason = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scrape_domain_settings': {'from_model': 'ScrapeDomainSettings', 'from_field': 'domain_id', 'referenced_field': 'id', 'related_name': 'scrape_domain_settings', 'from_schema': 'scraper'}, 'scrape_path_pattern': {'from_model': 'ScrapePathPattern', 'from_field': 'scrape_domain_id', 'referenced_field': 'id', 'related_name': 'scrape_path_pattern', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "scrape_domain"
    _db_schema = "scraper"

class ScrapeFailureLog(Model):
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scrape_retry_queue': {'from_model': 'ScrapeRetryQueue', 'from_field': 'failure_log_id', 'referenced_field': 'id', 'related_name': 'scrape_retry_queue', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "scrape_failure_log"
    _db_schema = "scraper"

class ScrapeParsedPage(Model):
    id = UUIDField(primary_key=True, null=False)
    page_name = CharField(null=False)
    validity = CharField(null=False)
    remote_path = CharField()
    local_path = CharField()
    scraped_at = DateTimeField()
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField()
    updated_at = DateTimeField()
    is_public = BooleanField(default=False)
    expires_at = DateTimeField()
    url = TextField()
    domain = TextField()
    content = JSONBField()
    char_count = IntegerField()
    content_type = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_parsed_page"
    _db_schema = "scraper"

class ScrapeDomainSettings(Model):
    id = UUIDField(primary_key=True, null=False)
    domain_id = ForeignKey(to_model=ScrapeDomain, to_column='id', to_schema='scraper', null=False, unique=True)
    enabled = BooleanField(null=False, default=True)
    proxy_type = TextField(null=False, default='datacenter')
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_domain_settings"
    _db_schema = "scraper"

class ScrapePathPattern(Model):
    id = UUIDField(primary_key=True, null=False)
    scrape_domain_id = ForeignKey(to_model=ScrapeDomain, to_column='id', to_schema='scraper', )
    path_pattern = CharField(default='/*')
    created_at = DateTimeField()
    updated_at = DateTimeField()
    is_public = BooleanField(default=False)
    policy_action = TextField()
    min_content_chars = IntegerField()
    min_real_content_chars = IntegerField()
    content_selector = TextField()
    policy_notes = TextField()
    category = TextField()
    category_reason = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'scrape_path_override': {'from_model': 'ScrapePathOverride', 'from_field': 'path_pattern_id', 'referenced_field': 'id', 'related_name': 'scrape_path_override', 'from_schema': 'scraper'}}
    _database = "matrx_scraper"
    _table_name = "scrape_path_pattern"
    _db_schema = "scraper"

class ScrapeRetryQueue(Model):
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_retry_queue"
    _db_schema = "scraper"

class ScrapePathOverride(Model):
    id = UUIDField(primary_key=True, null=False)
    path_pattern_id = ForeignKey(to_model=ScrapePathPattern, to_column='id', to_schema='scraper', null=False)
    is_active = BooleanField(null=False, default=True)
    config_type = TextField(null=False)
    selector_type = TextField(null=False)
    match_type = TextField(null=False)
    action = TextField(null=False)
    values = JSONBField(null=False, default=[])
    created_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_scraper"
    _table_name = "scrape_path_override"
    _db_schema = "scraper"

__all__ = [
    "ScrapeDomain",
    "ScrapeFailureLog",
    "ScrapeParsedPage",
    "ScrapeDomainSettings",
    "ScrapePathPattern",
    "ScrapeRetryQueue",
    "ScrapePathOverride",
]


model_registry.register_all(
[
        ScrapeDomain,
        ScrapeFailureLog,
        ScrapeParsedPage,
        ScrapeDomainSettings,
        ScrapePathPattern,
        ScrapeRetryQueue,
        ScrapePathOverride
    ],
    skip_existing=True
)