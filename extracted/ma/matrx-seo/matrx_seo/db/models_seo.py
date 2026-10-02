# File: matrx_seo/db/models_seo.py
from matrx_orm import BigIntegerField, BooleanField, CharField, DateField, DateTimeField, DecimalField, EnumField, ForeignKey, IntegerArrayField, IntegerField, JSONBField, MatrxEntity, Model, SmallIntegerField, TextArrayField, TextField, TimeField, UUIDArrayField, UUIDField, model_registry, BaseDTO, BaseManager
from enum import Enum
from dataclasses import dataclass
from typing import ClassVar



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class AiCapability(MatrxEntity):
    slug = TextField(primary_key=True, null=False)
    label = TextField(null=False)
    description = TextField(null=False)
    default_mode = TextField(null=False)
    default_timeout_hours = IntegerField()
    enforced = BooleanField(null=False, default=False)
    enforcement_note = TextField()
    position = IntegerField(null=False, default=0)
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "ai_capability"
    _db_schema = "seo"
    _entity_token = "seo_ai_capability"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class ChangeSet(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    primary_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    title = TextField(null=False)
    summary = TextField(null=False)
    rationale = TextField(null=False)
    business_outcome = TextField(null=False)
    change_kind = TextField(null=False)
    status = TextField(null=False, default='planned')
    confidence = SmallIntegerField(null=False, default=50)
    planned_for = DateTimeField()
    deployed_at = DateTimeField()
    verification_due_at = DateTimeField()
    completed_at = DateTimeField()
    source = TextField(null=False, default='manual')
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'change_assessment': {'from_model': 'ChangeAssessment', 'from_field': 'change_set_id', 'referenced_field': 'id', 'related_name': 'change_assessment', 'from_schema': 'seo'}, 'change_event': {'from_model': 'ChangeEvent', 'from_field': 'change_set_id', 'referenced_field': 'id', 'related_name': 'change_event', 'from_schema': 'seo'}, 'change_item': {'from_model': 'ChangeItem', 'from_field': 'change_set_id', 'referenced_field': 'id', 'related_name': 'change_item', 'from_schema': 'seo'}, 'change_metric': {'from_model': 'ChangeMetric', 'from_field': 'change_set_id', 'referenced_field': 'id', 'related_name': 'change_metric', 'from_schema': 'seo'}, 'change_theory': {'from_model': 'ChangeTheory', 'from_field': 'change_set_id', 'referenced_field': 'id', 'related_name': 'change_theory', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "change_set"
    _db_schema = "seo"
    _entity_token = "seo_change_set"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class ClassifierRevisionLedger(MatrxEntity):
    semantic_hash = TextField(primary_key=True, null=False)
    revision = TextField(null=False, unique=True)
    first_seen_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "classifier_revision_ledger"
    _db_schema = "seo"
    _entity_token = "classifier_revision_ledger"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "ledger"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class CollectionRun(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', null=False)
    provider = TextField(null=False)
    capability = TextField(null=False)
    operation = TextField(null=False)
    trigger = TextField(null=False, default='on_demand')
    status = TextField(null=False, default='pending')
    target_ref = TextField(null=False)
    observation_period = TextField(null=False)
    settings = JSONBField(null=False, default={})
    settings_hash = TextField(null=False)
    idempotency_key = TextField(null=False, unique=True)
    credential_reference_id = TextField()
    credential_reference_kind = TextField()
    request_id = TextField()
    execution_id = UUIDField()
    attempt_count = IntegerField(null=False, default=1)
    lease_owner = TextField()
    lease_expires_at = DateTimeField()
    requested_at = DateTimeField(null=False)
    started_at = DateTimeField()
    completed_at = DateTimeField()
    request_count = IntegerField(null=False, default=0)
    reported_cost = DecimalField()
    estimated_cost = DecimalField()
    currency = TextField(null=False, default='USD')
    error = JSONBField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    source_crawl_session_id = UUIDField()
    result = JSONBField()
    metadata = JSONBField(null=False, default={})
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    deleted_at = DateTimeField()
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'ai_visibility_response': {'from_model': 'AiVisibilityResponse', 'from_field': 'provider_run_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_response', 'from_schema': 'seo'}, 'backlink_dimension_snapshot': {'from_model': 'BacklinkDimensionSnapshot', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'backlink_dimension_snapshot', 'from_schema': 'seo'}, 'backlink_observation': {'from_model': 'BacklinkObservation', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'backlink_observation', 'from_schema': 'seo'}, 'backlink_snapshot': {'from_model': 'BacklinkSnapshot', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'backlink_snapshot', 'from_schema': 'seo'}, 'competitor': {'from_model': 'Competitor', 'from_field': 'latest_run_id', 'referenced_field': 'id', 'related_name': 'competitor', 'from_schema': 'seo'}, 'competitor_observation': {'from_model': 'CompetitorObservation', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'competitor_observation', 'from_schema': 'seo'}, 'competitor_opportunity': {'from_model': 'CompetitorOpportunity', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'competitor_opportunity', 'from_schema': 'seo'}, 'keyword_market_observation': {'from_model': 'KeywordMarketObservation', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'keyword_market_observation', 'from_schema': 'seo'}, 'link_gap_domain': {'from_model': 'LinkGapDomain', 'from_field': 'latest_run_id', 'referenced_field': 'id', 'related_name': 'link_gap_domain', 'from_schema': 'seo'}, 'page_performance': {'from_model': 'PagePerformance', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'page_performance', 'from_schema': 'seo'}, 'provider_call': {'from_model': 'ProviderCall', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'provider_call', 'from_schema': 'seo'}, 'provider_task': {'from_model': 'ProviderTask', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'provider_task', 'from_schema': 'seo'}, 'rank_observation': {'from_model': 'RankObservation', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'rank_observation', 'from_schema': 'seo'}, 'raw_payload': {'from_model': 'RawPayload', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'raw_payload', 'from_schema': 'seo'}, 'reputation_case': {'from_model': 'ReputationCase', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'reputation_case', 'from_schema': 'seo'}, 'search_performance_daily': {'from_model': 'SearchPerformanceDaily', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'search_performance_daily', 'from_schema': 'seo'}, 'serp_mention': {'from_model': 'SerpMention', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'serp_mention', 'from_schema': 'seo'}, 'serp_opportunity': {'from_model': 'SerpOpportunity', 'from_field': 'latest_run_id', 'referenced_field': 'id', 'related_name': 'serp_opportunity', 'from_schema': 'seo'}, 'serp_snapshot': {'from_model': 'SerpSnapshot', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'serp_snapshot', 'from_schema': 'seo'}, 'web_analytics_daily': {'from_model': 'WebAnalyticsDaily', 'from_field': 'run_id', 'referenced_field': 'id', 'related_name': 'web_analytics_daily', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "collection_run"
    _db_schema = "seo"
    _entity_token = "seo_collection_run"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class CoverageTracker(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    name = TextField(null=False)
    brand_key = TextField()
    brand_terms = TextArrayField(null=False, default=[])
    exclude_terms = TextArrayField(null=False, default=[])
    competitors = JSONBField(null=False, default=[])
    ignore_domains = TextArrayField(null=False, default=[])
    language = TextField()
    country = TextField()
    timespan = TextField(null=False, default='1d')
    max_records = IntegerField(null=False, default=100)
    cadence_minutes = IntegerField(null=False, default=240)
    is_active = BooleanField(null=False, default=True)
    alert_min_hit_score = SmallIntegerField(null=False, default=60)
    capture_pages = BooleanField(null=False, default=True)
    declared_by = TextField(null=False, default='user')
    declared_ref = JSONBField(null=False, default={})
    last_run_at = DateTimeField()
    last_run_status = TextField()
    last_error = TextField()
    mention_count = IntegerField(null=False, default=0)
    dedupe_key = TextField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='web', )
    lenses = TextArrayField(null=False, default=['coverage'])
    topics = TextArrayField(null=False, default=[])
    search_terms = TextArrayField(null=False, default=[])
    standing = TextArrayField(null=False, default=[])
    feed_ids = TextArrayField(null=False, default=[])
    feed_urls = TextArrayField(null=False, default=[])
    sources = TextArrayField()
    x_trends_woeids = IntegerArrayField(null=False, default=[])
    brief_source_id = UUIDField()
    alert_recipient_user_ids = UUIDArrayField(null=False, default=[])
    slack_credential_item_id = UUIDField()
    auto_run_paused_at = DateTimeField()
    auto_run_paused_reason = TextField()
    last_run_summary = JSONBField()
    workflow_trigger_id = UUIDField()
    parent_organization_id = UUIDField()
    term_meanings = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'ai_visibility_panel': {'from_model': 'AiVisibilityPanel', 'from_field': 'coverage_tracker_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_panel', 'from_schema': 'seo'}, 'coverage_mention': {'from_model': 'CoverageMention', 'from_field': 'tracker_id', 'referenced_field': 'id', 'related_name': 'coverage_mention', 'from_schema': 'seo'}, 'tracker_story': {'from_model': 'TrackerStory', 'from_field': 'tracker_id', 'referenced_field': 'id', 'related_name': 'tracker_story', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "coverage_tracker"
    _db_schema = "seo"
    _entity_token = "seo_coverage_tracker"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class EngineOwnerTask(MatrxEntity):
    engine_slug = TextField(primary_key=True, null=False)
    task_id = UUIDField(null=False)
    note = TextField()
    created_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "engine_owner_task"
    _db_schema = "seo"
    _entity_token = "engine_owner_task"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class EngineSchedule(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    engine_slug = TextField(null=False)
    scope_tier = TextField(null=False)
    scope_organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', )
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    cadence = TextField(null=False)
    run_at_utc = TimeField()
    day_of_week = SmallIntegerField()
    max_keywords_per_run = IntegerField(null=False, default=50)
    sites_per_run = IntegerField(null=False, default=3)
    enabled = BooleanField(null=False, default=False)
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    last_dispatched_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "engine_schedule"
    _db_schema = "seo"
    _entity_token = "seo_engine_schedule"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class GeoPlace(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    place_kind = TextField(null=False)
    name = TextField(null=False)
    normalized_name = TextField(null=False)
    slug = TextField(null=False)
    country_code = TextField(null=False, default='US')
    state_code = TextField()
    parent_place_id = ForeignKey(to_model='GeoPlace', to_column='id', to_schema='seo', )
    population = IntegerField()
    latitude = DecimalField()
    longitude = DecimalField()
    aliases = JSONBField(null=False, default=[])
    match_tokens = JSONBField(null=False, default=[])
    ambiguity = TextField(null=False, default='safe')
    ambiguity_reason = TextField()
    is_active = BooleanField(null=False, default=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'dimension_value_matcher': {'from_model': 'DimensionValueMatcher', 'from_field': 'place_id', 'referenced_field': 'id', 'related_name': 'dimension_value_matcher', 'from_schema': 'seo'}, 'keyword_place': {'from_model': 'KeywordPlace', 'from_field': 'place_id', 'referenced_field': 'id', 'related_name': 'keyword_place', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "geo_place"
    _db_schema = "seo"
    _entity_token = "seo_geo_place"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class GscDigRule(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    name = TextField(null=False)
    description = TextField()
    dimension = TextField(null=False, default='query')
    conditions = JSONBField(null=False, default=[])
    sort_metric = TextField(null=False, default='clicks')
    sort_dir = TextField(null=False, default='desc')
    row_limit = IntegerField(null=False, default=100)
    base_filters = JSONBField(null=False, default={})
    is_template = BooleanField(null=False, default=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    traffic_class = TextField()
    metadata = JSONBField(null=False, default={})
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False, default='internal')
    level = TextField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'dimension_value_matcher': {'from_model': 'DimensionValueMatcher', 'from_field': 'condition_rule_id', 'referenced_field': 'id', 'related_name': 'dimension_value_matcher', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "gsc_dig_rule"
    _db_schema = "seo"
    _entity_token = "seo_gsc_dig_rule"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class Keyword(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    phrase = TextField(null=False)
    normalized_phrase = TextField(null=False)
    language = TextField(null=False, default='en')
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False)
    classification_confidence = SmallIntegerField()
    classification_detail = JSONBField(null=False, default={})
    classified_at = DateTimeField()
    classifier_version = TextField()
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'ai_visibility_response': {'from_model': 'AiVisibilityResponse', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_response', 'from_schema': 'seo'}, 'change_theory': {'from_model': 'ChangeTheory', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'change_theory', 'from_schema': 'seo'}, 'keyword_classification_queue': {'from_model': 'KeywordClassificationQueue', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_classification_queue', 'from_schema': 'seo'}, 'keyword_edge': {'from_model': 'KeywordEdge', 'from_field': 'target_keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_edge', 'from_schema': 'seo'}, 'keyword_facet': {'from_model': 'KeywordFacet', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_facet', 'from_schema': 'seo'}, 'keyword_market': {'from_model': 'KeywordMarket', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_market', 'from_schema': 'seo'}, 'keyword_market_observation': {'from_model': 'KeywordMarketObservation', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_market_observation', 'from_schema': 'seo'}, 'keyword_place': {'from_model': 'KeywordPlace', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_place', 'from_schema': 'seo'}, 'keyword_topic': {'from_model': 'KeywordTopic', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'keyword_topic', 'from_schema': 'seo'}, 'rank_observation': {'from_model': 'RankObservation', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'rank_observation', 'from_schema': 'seo'}, 'rank_target': {'from_model': 'RankTarget', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'rank_target', 'from_schema': 'seo'}, 'search_performance_daily': {'from_model': 'SearchPerformanceDaily', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'search_performance_daily', 'from_schema': 'seo'}, 'serp_snapshot': {'from_model': 'SerpSnapshot', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'serp_snapshot', 'from_schema': 'seo'}, 'site_keyword_offering': {'from_model': 'SiteKeywordOffering', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'site_keyword_offering', 'from_schema': 'seo'}, 'site_keyword_value': {'from_model': 'SiteKeywordValue', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'site_keyword_value', 'from_schema': 'seo'}, 'topic_placement_queue': {'from_model': 'TopicPlacementQueue', 'from_field': 'keyword_id', 'referenced_field': 'id', 'related_name': 'topic_placement_queue', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "keyword"
    _db_schema = "seo"
    _entity_token = "seo_keyword"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class KeywordSavedView(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = UUIDField(null=False)
    name = TextField(null=False)
    surface = TextField(null=False, default='keyword_workbench')
    state = JSONBField(null=False, default={})
    position = IntegerField()
    shared = BooleanField(null=False, default=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_saved_view"
    _db_schema = "seo"
    _entity_token = "seo_keyword_saved_view"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class LandscapeBrief(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    facts = JSONBField(null=False, default={})
    service_lines = JSONBField(null=False, default=[])
    brief_markdown = TextField(null=False)
    agent_confidence = SmallIntegerField()
    confidence_reason = TextField()
    guidance = TextField(null=False)
    human_corrections = JSONBField(null=False, default=[])
    status = TextField(null=False, default='draft')
    auto_accept_at = DateTimeField()
    reviewed_at = DateTimeField()
    reviewed_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    generated_at = DateTimeField()
    agent_run_id = UUIDField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    scope = TextField(null=False, default='site')
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='web', null=False)
    inputs = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "landscape_brief"
    _db_schema = "seo"
    _entity_token = "seo_landscape_brief"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Location(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    created_at = DateTimeField(null=False)
    country_code = TextField()
    region = TextField()
    city = TextField()
    postal_code = TextField()
    latitude = DecimalField()
    longitude = DecimalField()
    timezone = TextField()
    location_code = IntegerField(unique=True)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'keyword_market': {'from_model': 'KeywordMarket', 'from_field': 'location_code', 'referenced_field': 'location_code', 'related_name': 'keyword_market', 'from_schema': 'seo'}, 'keyword_market_observation': {'from_model': 'KeywordMarketObservation', 'from_field': 'location_code', 'referenced_field': 'location_code', 'related_name': 'keyword_market_observation', 'from_schema': 'seo'}, 'rank_observation': {'from_model': 'RankObservation', 'from_field': 'location_id', 'referenced_field': 'id', 'related_name': 'rank_observation', 'from_schema': 'seo'}, 'rank_target': {'from_model': 'RankTarget', 'from_field': 'location_id', 'referenced_field': 'id', 'related_name': 'rank_target', 'from_schema': 'seo'}, 'serp_snapshot': {'from_model': 'SerpSnapshot', 'from_field': 'location_id', 'referenced_field': 'id', 'related_name': 'serp_snapshot', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "location"
    _db_schema = "seo"
    _entity_token = "location"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class MapFacet(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    key = TextField(null=False)
    label = TextField(null=False)
    description = TextField()
    applies_to = TextField(null=False)
    inherits = BooleanField(null=False, default=True)
    is_builtin = BooleanField(null=False, default=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'map_facet_value': {'from_model': 'MapFacetValue', 'from_field': 'facet_id', 'referenced_field': 'id', 'related_name': 'map_facet_value', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "map_facet"
    _db_schema = "seo"
    _entity_token = "seo_map_facet"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class PageMappingQueue(MatrxEntity):
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', primary_key=True, null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', primary_key=True, null=False)
    status = TextField(null=False, default='pending')
    mapping_source = TextField()
    priority_clicks = BigIntegerField(null=False, default=0)
    priority_impressions = BigIntegerField(null=False, default=0)
    demand_window_days = IntegerField(null=False)
    demand_as_of = DateField(null=False)
    attempts = IntegerField(null=False, default=0)
    last_error = TextField()
    suggested_topic_name = TextField()
    suggested_reason = TextField()
    claimed_at = DateTimeField()
    completed_at = DateTimeField()
    enqueued_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "page_mapping_queue"
    _db_schema = "seo"
    _entity_token = "page_mapping_queue"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"

class PageMeasurementHealth(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    strategy = TextField(null=False)
    consecutive_terminal_failures = IntegerField(null=False, default=0)
    total_terminal_failures = IntegerField(null=False, default=0)
    total_transient_failures = IntegerField(null=False, default=0)
    total_successes = IntegerField(null=False, default=0)
    last_outcome = TextField()
    last_failure_code = TextField()
    last_error = TextField()
    last_failure_at = DateTimeField()
    last_success_at = DateTimeField()
    quarantined_at = DateTimeField()
    quarantine_reason = TextField()
    quarantine_expires_at = DateTimeField()
    quarantine_count = IntegerField(null=False, default=0)
    released_at = DateTimeField()
    release_reason = TextField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "page_measurement_health"
    _db_schema = "seo"
    _entity_token = "seo_page_measurement_health"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class PrMoment(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='web', null=False)
    title = TextField(null=False)
    type = TextField(null=False)
    starts_on = DateField(null=False)
    ends_on = DateField()
    date_basis = TextField(null=False)
    source_url = TextField()
    source_capture_id = UUIDField()
    industries = TextArrayField(null=False, default=[])
    sensitivity = TextField(null=False, default='none')
    organizer = TextField()
    country_code = TextField()
    verified_at = DateTimeField()
    verification = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "pr_moment"
    _db_schema = "seo"
    _entity_token = "seo_pr_moment"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class ReferringDomainProfile(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    normalized_domain = TextField(null=False)
    display_domain = TextField(null=False)
    domain_type = TextField()
    first_seen_at = DateTimeField()
    last_seen_at = DateTimeField()
    current_backlinks = BigIntegerField(null=False, default=0)
    current_referring_pages = BigIntegerField(null=False, default=0)
    provider_metrics = JSONBField(null=False, default={})
    quality_vector = JSONBField(null=False, default={})
    opinion_score = SmallIntegerField()
    opinion_verdict = TextField(null=False, default='unknown')
    opinion_summary = TextField()
    ai_assessment = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    resolved_opinion = JSONBField(null=False, default={})
    analyzed_at = DateTimeField()
    human_reviewed_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'ai_visibility_citation': {'from_model': 'AiVisibilityCitation', 'from_field': 'referring_domain_profile_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_citation', 'from_schema': 'seo'}, 'backlink': {'from_model': 'Backlink', 'from_field': 'referring_domain_profile_id', 'referenced_field': 'id', 'related_name': 'backlink', 'from_schema': 'seo'}, 'reputation_case': {'from_model': 'ReputationCase', 'from_field': 'referring_domain_profile_id', 'referenced_field': 'id', 'related_name': 'reputation_case', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "referring_domain_profile"
    _db_schema = "seo"
    _entity_token = "seo_referring_domain_profile"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class SiteGeoArea(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    label = TextField(null=False)
    area_kind = TextField(null=False, default='city')
    match_tokens = JSONBField(null=False, default=[])
    geo_band = TextField(null=False)
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    place_ids = UUIDArrayField(null=False, default=[])
    location_ids = UUIDArrayField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_geo_area"
    _db_schema = "seo"
    _entity_token = "seo_site_geo_area"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteValueCombo(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = UUIDField(null=False)
    value_ids = UUIDArrayField(null=False)
    effect = TextField(null=False)
    amount = DecimalField()
    label = TextField()
    notes = TextField()
    origin = TextField(null=False, default='human')
    enabled = BooleanField(null=False, default=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_value_combo"
    _db_schema = "seo"
    _entity_token = "seo_site_value_combo"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteValueWorth(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = UUIDField(null=False)
    value_id = ForeignKey(to_model='Categories', to_column='id', to_schema='platform', null=False)
    effect = TextField(null=False)
    amount = DecimalField()
    origin = TextField(null=False, default='human')
    pack_id = UUIDField()
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_value_worth"
    _db_schema = "seo"
    _entity_token = "seo_site_value_worth"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteVocabulary(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    vocab_kind = TextField(null=False)
    value = TextField(null=False)
    label = TextField(null=False)
    description = TextField()
    sort = IntegerField(null=False, default=0)
    config = JSONBField(null=False, default={})
    active = BooleanField(null=False, default=True)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_vocabulary"
    _db_schema = "seo"
    _entity_token = "seo_site_vocabulary"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class StarterPack(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    slug = TextField(null=False)
    name = TextField(null=False)
    industry = TextField(null=False)
    summary = TextField()
    description = TextField()
    status = TextField(null=False, default='proposed')
    guidelines = TextField()
    geo_model = TextField(null=False, default='regional')
    source_notes = TextField()
    source_corpus = JSONBField(null=False, default=[])
    proposal = JSONBField()
    ratified_at = DateTimeField()
    ratified_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    ratification_notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    industry_id = ForeignKey(to_model='Industries', to_column='id', to_schema='iam', )
    pack_version = IntegerField(null=False, default=1)
    supersedes_pack_id = ForeignKey(to_model='StarterPack', to_column='id', to_schema='seo', )
    proposed_industry = TextField()
    proposed_by = UUIDField()
    proposed_at = DateTimeField()
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'keyword_class_rule': {'from_model': 'KeywordClassRule', 'from_field': 'pack_id', 'referenced_field': 'id', 'related_name': 'keyword_class_rule', 'from_schema': 'seo'}, 'starter_pack_item': {'from_model': 'StarterPackItem', 'from_field': 'pack_id', 'referenced_field': 'id', 'related_name': 'starter_pack_item', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "starter_pack"
    _db_schema = "seo"
    _entity_token = "seo_starter_pack"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class StoryAngle(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    angle_key = TextField(null=False)
    endowment = TextField(null=False)
    angle_type = TextField(null=False)
    headline = TextField(null=False)
    summary = TextField(null=False)
    why_now = TextField()
    target_beat = TextField()
    target_outlet_kind = TextField()
    priority = SmallIntegerField(null=False, default=0)
    confidence = SmallIntegerField(null=False, default=0)
    newsworthiness = SmallIntegerField(null=False, default=0)
    timeliness = SmallIntegerField(null=False, default=0)
    evidence_quality = SmallIntegerField(null=False, default=0)
    recommended_action = TextField(null=False)
    action_reason = TextField()
    facts = JSONBField(null=False, default=[])
    inferences = JSONBField(null=False, default=[])
    evidence_refs = JSONBField(null=False, default=[])
    proof_required = JSONBField(null=False, default=[])
    missing_evidence = JSONBField(null=False, default=[])
    contradictions = JSONBField(null=False, default=[])
    analysis = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    evidence_fingerprint = TextField()
    analysis_version = TextField()
    requires_human_review = BooleanField(null=False, default=False)
    status = TextField(null=False, default='proposed')
    analyzed_at = DateTimeField()
    human_reviewed_at = DateTimeField()
    accepted_at = DateTimeField()
    pitched_at = DateTimeField()
    landed_at = DateTimeField()
    dismissed_at = DateTimeField()
    expires_at = DateTimeField()
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'source_request': {'from_model': 'SourceRequest', 'from_field': 'story_angle_id', 'referenced_field': 'id', 'related_name': 'source_request', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "story_angle"
    _db_schema = "seo"
    _entity_token = "seo_story_angle"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class Topic(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    name = TextField(null=False)
    slug = TextField(null=False, unique=True)
    node_type = TextField(null=False)
    description = TextField()
    volatility = TextField(null=False, default='moderate')
    aliases = JSONBField(null=False, default=[])
    is_builtin = BooleanField(null=False, default=True)
    parent_id = ForeignKey(to_model='Topic', to_column='id', to_schema='seo', )
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'keyword_topic': {'from_model': 'KeywordTopic', 'from_field': 'topic_id', 'referenced_field': 'id', 'related_name': 'keyword_topic', 'from_schema': 'seo'}, 'site_topic_value': {'from_model': 'SiteTopicValue', 'from_field': 'topic_id', 'referenced_field': 'id', 'related_name': 'site_topic_value', 'from_schema': 'seo'}, 'starter_pack_item': {'from_model': 'StarterPackItem', 'from_field': 'topic_id', 'referenced_field': 'id', 'related_name': 'starter_pack_item', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "topic"
    _db_schema = "seo"
    _entity_token = "seo_topic"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class TopicalMap(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='web', null=False)
    name = TextField(null=False)
    description = TextField()
    status = TextField(null=False, default='draft')
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'map_topic': {'from_model': 'MapTopic', 'from_field': 'map_id', 'referenced_field': 'id', 'related_name': 'map_topic', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "topical_map"
    _db_schema = "seo"
    _entity_token = "seo_topical_map"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class AiVisibilityPanel(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    name = TextField(null=False)
    prompts = JSONBField(null=False, default=[])
    key_messages = JSONBField(null=False, default=[])
    engines = TextArrayField(null=False, default=['chat_gpt', 'claude', 'gemini', 'perplexity'])
    country_iso = TextField(null=False, default='US')
    city = TextField()
    cadence_days = SmallIntegerField(null=False, default=7)
    max_prompts_per_run = SmallIntegerField(null=False, default=10)
    is_active = BooleanField(null=False, default=True)
    coverage_tracker_id = ForeignKey(to_model=CoverageTracker, to_column='id', to_schema='seo', )
    declared_by = TextField(null=False, default='user')
    declared_ref = JSONBField(null=False, default={})
    last_run_at = DateTimeField()
    last_run_status = TextField()
    last_error = TextField()
    last_run_cost_usd = DecimalField()
    run_count = IntegerField(null=False, default=0)
    dedupe_key = TextField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    status = TextField(null=False, default='draft')
    current_version_id = UUIDField()
    design_run_id = UUIDField()
    tier = TextField(null=False, default='diagnostic')
    repeats = IntegerField(null=False, default=1)
    lanes = TextArrayField(null=False, default=['retrieval'])
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "ai_visibility_panel"
    _db_schema = "seo"
    _entity_token = "seo_ai_visibility_panel"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class AiVisibilityResponse(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    command_run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    provider_run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    query = TextField(null=False)
    engine = TextField(null=False)
    model_name = TextField()
    status = TextField(null=False, default='completed')
    answer_text = TextField(null=False)
    answer_pattern = TextField()
    target_mentioned = BooleanField(null=False, default=False)
    target_cited = BooleanField(null=False, default=False)
    target_citation_ordinal = IntegerField()
    citation_count = IntegerField(null=False, default=0)
    claim_count = IntegerField(null=False, default=0)
    unverified_influential_count = IntegerField(null=False, default=0)
    decision_signal_count = IntegerField(null=False, default=0)
    recommendation_count = IntegerField(null=False, default=0)
    recommendation_strength = SmallIntegerField()
    confidence = SmallIntegerField()
    provider_metadata = JSONBField(null=False, default={})
    analysis = JSONBField(null=False, default={})
    error = JSONBField()
    observed_at = DateTimeField(null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    panel_id = UUIDField()
    panel_version_id = UUIDField()
    candidate_id = TextField()
    canonical_cell_id = TextField()
    wave_id = TextField()
    repeat_index = IntegerField()
    lane = TextField()
    order_seed = BigIntegerField()
    configuration_hash = TextField()
    response_payload_hash = TextField()
    citation_payload_hash = TextField()
    validity_status = TextField()
    parser_version = TextField()
    entities_mentioned = JSONBField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'ai_visibility_citation': {'from_model': 'AiVisibilityCitation', 'from_field': 'response_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_citation', 'from_schema': 'seo'}, 'ai_visibility_claim': {'from_model': 'AiVisibilityClaim', 'from_field': 'response_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_claim', 'from_schema': 'seo'}, 'ai_visibility_signal': {'from_model': 'AiVisibilitySignal', 'from_field': 'response_id', 'referenced_field': 'id', 'related_name': 'ai_visibility_signal', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "ai_visibility_response"
    _db_schema = "seo"
    _entity_token = "seo_ai_visibility_response"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class Backlink(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    referring_domain_profile_id = ForeignKey(to_model=ReferringDomainProfile, to_column='id', to_schema='seo', )
    identity_key = TextField(null=False)
    source_url = TextField(null=False)
    source_domain = TextField()
    target_url = TextField(null=False)
    anchor_text = TextField()
    link_type = TextField()
    is_dofollow = BooleanField()
    first_seen_at = DateTimeField()
    last_seen_at = DateTimeField()
    lost_at = DateTimeField()
    state = TextField(null=False, default='active')
    source_rank = DecimalField()
    domain_rank = DecimalField()
    spam_score = DecimalField()
    provider_evidence = JSONBField(null=False, default={})
    enrichment_status = TextField(null=False, default='pending')
    enrichment_attempt_count = SmallIntegerField(null=False, default=0)
    claimed_by = TextField()
    claimed_at = DateTimeField()
    claim_expires_at = DateTimeField()
    next_enrichment_at = DateTimeField()
    last_error = JSONBField()
    source_capture = JSONBField(null=False, default={})
    deterministic_assessment = JSONBField(null=False, default={})
    ai_assessment = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    resolved_assessment = JSONBField(null=False, default={})
    assessment_version = TextField()
    captured_at = DateTimeField()
    analyzed_at = DateTimeField()
    human_reviewed_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    assessment_score = SmallIntegerField()
    assessment_relevance_score = SmallIntegerField()
    assessment_relevance_verdict = TextField()
    assessment_page_type = TextField()
    assessment_control_level = TextField()
    assessment_action = TextField()
    assessment_priority = TextField()
    assessment_risk_verdict = TextField()
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'backlink_change_event': {'from_model': 'BacklinkChangeEvent', 'from_field': 'backlink_id', 'referenced_field': 'id', 'related_name': 'backlink_change_event', 'from_schema': 'seo'}, 'backlink_observation': {'from_model': 'BacklinkObservation', 'from_field': 'backlink_id', 'referenced_field': 'id', 'related_name': 'backlink_observation', 'from_schema': 'seo'}, 'reputation_case': {'from_model': 'ReputationCase', 'from_field': 'backlink_id', 'referenced_field': 'id', 'related_name': 'reputation_case', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "backlink"
    _db_schema = "seo"
    _entity_token = "seo_backlink"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class ChangeItem(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    change_set_id = ForeignKey(to_model=ChangeSet, to_column='id', to_schema='seo', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', null=False)
    field_kind = TextField(null=False)
    label = TextField(null=False)
    expected_before = TextField()
    expected_after = TextField()
    observed_after = TextField()
    verification_status = TextField(null=False, default='pending')
    verification_method = TextField(null=False, default='crawl')
    source_snapshot_id = ForeignKey(to_model='Snapshot', to_column='id', to_schema='web', )
    verified_at = DateTimeField()
    notes = TextField()
    sort_order = IntegerField(null=False, default=0)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'change_event': {'from_model': 'ChangeEvent', 'from_field': 'change_item_id', 'referenced_field': 'id', 'related_name': 'change_event', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "change_item"
    _db_schema = "seo"
    _entity_token = "seo_change_item"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class ChangeTheory(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    change_set_id = ForeignKey(to_model=ChangeSet, to_column='id', to_schema='seo', null=False)
    parent_theory_id = ForeignKey(to_model='ChangeTheory', to_column='id', to_schema='seo', )
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', )
    title = TextField(null=False)
    hypothesis = TextField(null=False)
    mechanism = TextField(null=False)
    business_link = TextField(null=False)
    status = TextField(null=False, default='untested')
    confidence = SmallIntegerField(null=False, default=50)
    evaluation_start = DateField()
    evaluation_end = DateField()
    sort_order = IntegerField(null=False, default=0)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'change_assessment': {'from_model': 'ChangeAssessment', 'from_field': 'theory_id', 'referenced_field': 'id', 'related_name': 'change_assessment', 'from_schema': 'seo'}, 'change_event': {'from_model': 'ChangeEvent', 'from_field': 'theory_id', 'referenced_field': 'id', 'related_name': 'change_event', 'from_schema': 'seo'}, 'change_metric': {'from_model': 'ChangeMetric', 'from_field': 'theory_id', 'referenced_field': 'id', 'related_name': 'change_metric', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "change_theory"
    _db_schema = "seo"
    _entity_token = "seo_change_theory"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Competitor(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    normalized_domain = TextField(null=False)
    display_domain = TextField(null=False)
    display_name = TextField()
    discovery_source = TextField(null=False, default='provider')
    tracking_status = TextField(null=False, default='candidate')
    latest_run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    relevance_score = SmallIntegerField()
    threat_level = TextField()
    organic_keywords = IntegerField()
    keyword_intersections = IntegerField()
    estimated_traffic = DecimalField()
    average_position = DecimalField()
    serp_visibility = DecimalField()
    provider_evidence = JSONBField(null=False, default={})
    latest_autopsy = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    resolved_assessment = JSONBField(null=False, default={})
    first_observed_at = DateTimeField()
    last_observed_at = DateTimeField()
    analyzed_at = DateTimeField()
    human_reviewed_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    business_overlap = TextField()
    market_overlap = TextField()
    search_overlap_band = TextField()
    entity_role = TextField()
    posture = TextField()
    classification_status = TextField(null=False, default='unclassified')
    use_for_link_gap = BooleanField()
    custom_labels = TextArrayField(null=False, default=[])
    classification_confirmed_at = DateTimeField()
    classification_confirmed_by = UUIDField()
    peer_scale = TextField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'competitor_observation': {'from_model': 'CompetitorObservation', 'from_field': 'competitor_id', 'referenced_field': 'id', 'related_name': 'competitor_observation', 'from_schema': 'seo'}, 'competitor_opportunity': {'from_model': 'CompetitorOpportunity', 'from_field': 'competitor_id', 'referenced_field': 'id', 'related_name': 'competitor_opportunity', 'from_schema': 'seo'}, 'link_gap_match': {'from_model': 'LinkGapMatch', 'from_field': 'competitor_id', 'referenced_field': 'id', 'related_name': 'link_gap_match', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "competitor"
    _db_schema = "seo"
    _entity_token = "seo_competitor"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class CoverageMention(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    tracker_id = ForeignKey(to_model=CoverageTracker, to_column='id', to_schema='seo', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    brand_key = TextField(null=False)
    source = TextField(null=False)
    external_id = TextField()
    url = TextField(null=False)
    normalized_url = TextField(null=False)
    domain = TextField(null=False)
    title = TextField()
    medium = TextField(null=False, default='news')
    author_name = TextField()
    author_party_id = ForeignKey(to_model='Party', to_column='id', to_schema='crm', )
    language = TextField()
    published_at = DateTimeField()
    discovered_at = DateTimeField(null=False)
    capture_status = TextField(null=False, default='pending')
    captured_at = DateTimeField()
    source_capture = JSONBField(null=False, default={})
    links_to_site = BooleanField(null=False, default=False)
    link_urls = TextArrayField(null=False, default=[])
    sentiment = TextField()
    sentiment_score = SmallIntegerField()
    prominence = TextField()
    prominence_score = SmallIntegerField()
    topics = JSONBField(null=False, default=[])
    key_quote = TextField()
    analysis = JSONBField(null=False, default={})
    analyzed_at = DateTimeField()
    is_competitor = BooleanField(null=False, default=False)
    competitor_key = TextField()
    matched_terms = TextArrayField(null=False, default=[])
    hit_score = SmallIntegerField()
    hit_reason = TextField()
    outcome_event_id = ForeignKey(to_model='OutcomeEvent', to_column='id', to_schema='platform', )
    alerted_at = DateTimeField()
    dedupe_key = TextField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    news_item_id = ForeignKey(to_model='NewsItem', to_column='id', to_schema='web', )
    verdict = TextField()
    verdict_reason = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "coverage_mention"
    _db_schema = "seo"
    _entity_token = "seo_coverage_mention"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class DimensionValueMatcher(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = UUIDField(null=False)
    value_id = ForeignKey(to_model='Categories', to_column='id', to_schema='platform', null=False)
    kind = TextField(null=False)
    pattern = TextField()
    place_id = ForeignKey(to_model=GeoPlace, to_column='id', to_schema='seo', )
    fact_value_id = ForeignKey(to_model='Categories', to_column='id', to_schema='platform', )
    condition_rule_id = ForeignKey(to_model=GscDigRule, to_column='id', to_schema='seo', )
    enabled = BooleanField(null=False, default=True)
    origin = TextField(null=False, default='human')
    pack_id = UUIDField()
    notes = TextField()
    last_evaluated_at = DateTimeField()
    match_count = IntegerField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    exclusions = TextArrayField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'keyword_facet': {'from_model': 'KeywordFacet', 'from_field': 'matcher_id', 'referenced_field': 'id', 'related_name': 'keyword_facet', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "dimension_value_matcher"
    _db_schema = "seo"
    _entity_token = "seo_dimension_value_matcher"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KeywordClassRule(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    name = TextField(null=False)
    description = TextField()
    pattern = TextField()
    match_kind = TextField(default='contains')
    target_class = TextField()
    notes = TextField()
    auto_apply = BooleanField(null=False, default=False)
    is_template = BooleanField(null=False, default=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    last_applied_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    value_multiplier = DecimalField()
    match_facet = TextField()
    match_facet_value = TextField()
    pack_id = ForeignKey(to_model=StarterPack, to_column='id', to_schema='seo', )
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_class_rule"
    _db_schema = "seo"
    _entity_token = "seo_keyword_class_rule"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class KeywordClassificationQueue(MatrxEntity):
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', primary_key=True, null=False)
    target_version = TextField(null=False)
    status = TextField(null=False, default='pending')
    priority_clicks = BigIntegerField(null=False, default=0)
    priority_impressions = BigIntegerField(null=False, default=0)
    site_count = IntegerField(null=False, default=0)
    demand_window_days = IntegerField(null=False)
    demand_as_of = DateField(null=False)
    attempts = IntegerField(null=False, default=0)
    last_error = TextField()
    claimed_at = DateTimeField()
    completed_at = DateTimeField()
    enqueued_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    place_scanned_at = DateTimeField()
    place_detector_version = TextField()
    places_found = SmallIntegerField()
    demand_tier = SmallIntegerField(null=False, default=0)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_classification_queue"
    _db_schema = "seo"
    _entity_token = "keyword_classification_queue"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KeywordEdge(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    source_keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    target_keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    edge_type = TextField(null=False)
    status = TextField(null=False, default='proposed')
    origin = TextField(null=False, default='ai_research')
    confidence = SmallIntegerField()
    serp_overlap = DecimalField()
    detail = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_edge"
    _db_schema = "seo"
    _entity_token = "seo_keyword_edge"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KeywordPlace(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    place_id = ForeignKey(to_model=GeoPlace, to_column='id', to_schema='seo', null=False)
    match_kind = TextField(null=False)
    matched_text = TextField()
    confidence = SmallIntegerField(null=False, default=100)
    source = TextField(null=False, default='gazetteer')
    detector_version = TextField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_place"
    _db_schema = "seo"
    _entity_token = "seo_keyword_place"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KeywordTopic(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    topic_id = ForeignKey(to_model=Topic, to_column='id', to_schema='seo', null=False)
    is_primary = BooleanField(null=False, default=False)
    confidence = SmallIntegerField()
    assigned_by = TextField()
    notes = TextField()
    scope_tier = TextField(null=False, default='system')
    scope_site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    scope_brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='web', )
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_topic"
    _db_schema = "seo"
    _entity_token = "seo_keyword_topic"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class LinkGapDomain(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    normalized_domain = TextField(null=False)
    display_domain = TextField(null=False)
    match_count = IntegerField(null=False, default=0)
    domain_rank = DecimalField()
    spam_score = DecimalField()
    total_backlinks = BigIntegerField()
    referring_domains = BigIntegerField()
    first_seen_at = DateTimeField()
    last_seen_at = DateTimeField()
    observed_at = DateTimeField()
    latest_run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    provider_metrics = JSONBField(null=False, default={})
    review_status = TextField(null=False, default='pending')
    reviewed_at = DateTimeField()
    reviewed_by = UUIDField()
    priority_score = SmallIntegerField()
    priority_reason = TextField()
    ai_assessment = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    analyzed_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    enriched_at = DateTimeField()
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'link_gap_match': {'from_model': 'LinkGapMatch', 'from_field': 'link_gap_domain_id', 'referenced_field': 'id', 'related_name': 'link_gap_match', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "link_gap_domain"
    _db_schema = "seo"
    _entity_token = "seo_link_gap_domain"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class MapFacetValue(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    facet_id = ForeignKey(to_model=MapFacet, to_column='id', to_schema='seo', null=False)
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='web', )
    parent_id = ForeignKey(to_model='MapFacetValue', to_column='id', to_schema='seo', )
    slug = TextField(null=False)
    name = TextField(null=False)
    ref_type = TextField()
    ref_id = UUIDField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    custom = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "map_facet_value"
    _db_schema = "seo"
    _entity_token = "seo_map_facet_value"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class MapTopic(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    map_id = ForeignKey(to_model=TopicalMap, to_column='id', to_schema='seo', null=False)
    parent_id = ForeignKey(to_model='MapTopic', to_column='id', to_schema='seo', )
    slug = TextField(null=False)
    name = TextField(null=False)
    description = TextField()
    sort_order = IntegerField(null=False, default=0)
    status = TextField(null=False, default='active')
    layout = JSONBField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'page_intent_queue': {'from_model': 'PageIntentQueue', 'from_field': 'topic_id', 'referenced_field': 'id', 'related_name': 'page_intent_queue', 'from_schema': 'seo'}, 'site_keyword_value': {'from_model': 'SiteKeywordValue', 'from_field': 'topic_id', 'referenced_field': 'id', 'related_name': 'site_keyword_value', 'from_schema': 'seo'}, 'site_offering_value': {'from_model': 'SiteOfferingValue', 'from_field': 'topic_id', 'referenced_field': 'id', 'related_name': 'site_offering_value', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "map_topic"
    _db_schema = "seo"
    _entity_token = "seo_map_topic"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class ProviderCall(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    provider_call_key = TextField(null=False)
    external_task_id = TextField()
    request_count = IntegerField(null=False, default=1)
    reported_cost = DecimalField()
    estimated_cost = DecimalField()
    currency = TextField(null=False, default='USD')
    fetched_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "provider_call"
    _db_schema = "seo"
    _entity_token = "seo_provider_call"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class ProviderTask(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    external_task_id = TextField(null=False)
    endpoint = TextField()
    status = TextField(null=False)
    request_payload = JSONBField(null=False, default={})
    response_payload = JSONBField()
    request_count = IntegerField(null=False, default=1)
    provider_cost = DecimalField()
    estimated_cost = DecimalField()
    currency = TextField(null=False, default='USD')
    submitted_at = DateTimeField(null=False)
    last_polled_at = DateTimeField()
    completed_at = DateTimeField()
    error = JSONBField()
    metadata = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "provider_task"
    _db_schema = "seo"
    _entity_token = "seo_provider_task"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class RankTarget(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    engine = TextField(null=False)
    language = TextField(null=False, default='en')
    device = TextField(null=False, default='desktop')
    search_type = TextField(null=False, default='organic')
    location_id = ForeignKey(to_model=Location, to_column='id', to_schema='seo', )
    target_domain = TextField()
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    target_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    settings = JSONBField(null=False, default={})
    is_active = BooleanField(null=False, default=True)
    version = IntegerField(null=False, default=1)
    visibility = EnumField(enum_class=Visibility, null=False)
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'rank_observation': {'from_model': 'RankObservation', 'from_field': 'rank_target_id', 'referenced_field': 'id', 'related_name': 'rank_observation', 'from_schema': 'seo'}, 'serp_snapshot': {'from_model': 'SerpSnapshot', 'from_field': 'rank_target_id', 'referenced_field': 'id', 'related_name': 'serp_snapshot', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "rank_target"
    _db_schema = "seo"
    _entity_token = "seo_rank_target"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class RawPayload(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    checksum = TextField(null=False)
    size_bytes = BigIntegerField(null=False)
    content_type = TextField(null=False, default='application/json')
    payload = JSONBField()
    cloud_file_id = TextField()
    provider_schema_version = TextField()
    external_task_id = TextField()
    fetched_at = DateTimeField(null=False)
    offload_error = JSONBField()
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'backlink_dimension_snapshot': {'from_model': 'BacklinkDimensionSnapshot', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'backlink_dimension_snapshot', 'from_schema': 'seo'}, 'backlink_observation': {'from_model': 'BacklinkObservation', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'backlink_observation', 'from_schema': 'seo'}, 'backlink_snapshot': {'from_model': 'BacklinkSnapshot', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'backlink_snapshot', 'from_schema': 'seo'}, 'competitor_observation': {'from_model': 'CompetitorObservation', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'competitor_observation', 'from_schema': 'seo'}, 'keyword_market_observation': {'from_model': 'KeywordMarketObservation', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'keyword_market_observation', 'from_schema': 'seo'}, 'page_performance': {'from_model': 'PagePerformance', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'page_performance', 'from_schema': 'seo'}, 'rank_observation': {'from_model': 'RankObservation', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'rank_observation', 'from_schema': 'seo'}, 'search_performance_daily': {'from_model': 'SearchPerformanceDaily', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'search_performance_daily', 'from_schema': 'seo'}, 'serp_snapshot': {'from_model': 'SerpSnapshot', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'serp_snapshot', 'from_schema': 'seo'}, 'web_analytics_daily': {'from_model': 'WebAnalyticsDaily', 'from_field': 'raw_payload_id', 'referenced_field': 'id', 'related_name': 'web_analytics_daily', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "raw_payload"
    _db_schema = "seo"
    _entity_token = "seo_raw_payload"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class SerpOpportunity(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    normalized_domain = TextField(null=False)
    display_domain = TextField(null=False)
    mention_count = IntegerField(null=False, default=0)
    best_rank = IntegerField()
    variants = TextArrayField(null=False, default=[])
    observed_at = DateTimeField()
    latest_run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    domain_rank = DecimalField()
    spam_score = DecimalField()
    referring_domains = BigIntegerField()
    total_backlinks = BigIntegerField()
    enriched_at = DateTimeField()
    provider_metrics = JSONBField(null=False, default={})
    review_status = TextField(null=False, default='pending')
    reviewed_at = DateTimeField()
    reviewed_by = UUIDField()
    priority_score = SmallIntegerField()
    priority_reason = TextField()
    ai_assessment = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    analyzed_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    broken_link_count = IntegerField()
    link_checked_at = DateTimeField()
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'serp_mention': {'from_model': 'SerpMention', 'from_field': 'serp_opportunity_id', 'referenced_field': 'id', 'related_name': 'serp_mention', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "serp_opportunity"
    _db_schema = "seo"
    _entity_token = "seo_serp_opportunity"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteKeywordOffering(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    brand_offering_id = ForeignKey(to_model='BrandOffering', to_column='id', to_schema='web', null=False)
    is_primary = BooleanField(null=False, default=False)
    confidence = SmallIntegerField()
    assigned_by = TextField()
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_keyword_offering"
    _db_schema = "seo"
    _entity_token = "seo_site_keyword_offering"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteTopicValue(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    topic_id = ForeignKey(to_model=Topic, to_column='id', to_schema='seo', null=False)
    offering_match = TextField()
    lead_quality = TextField()
    audience_fit = TextField()
    capacity_appetite = TextField()
    brand_fit = TextField()
    weight = DecimalField()
    notes = TextField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_topic_value"
    _db_schema = "seo"
    _entity_token = "seo_site_topic_value"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class SourceRequest(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    platform = TextField(null=False)
    external_id = TextField()
    external_url = TextField()
    outlet = TextField()
    journalist_name = TextField()
    party_id = UUIDField()
    query_title = TextField(null=False)
    query_body = TextField()
    beat = TextField()
    requirements = JSONBField(null=False, default=[])
    deadline_at = DateTimeField()
    match_score = SmallIntegerField(null=False, default=0)
    match_reason = TextField()
    story_angle_id = ForeignKey(to_model=StoryAngle, to_column='id', to_schema='seo', )
    draft_response = TextField()
    draft_generated_at = DateTimeField()
    status = TextField(null=False, default='new')
    submitted_at = DateTimeField()
    won_at = DateTimeField()
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
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "source_request"
    _db_schema = "seo"
    _entity_token = "seo_source_request"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class StarterPackItem(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    pack_id = ForeignKey(to_model=StarterPack, to_column='id', to_schema='seo', null=False)
    item_kind = TextField(null=False)
    topic_id = ForeignKey(to_model=Topic, to_column='id', to_schema='seo', )
    weight = DecimalField()
    lead_quality = TextField()
    offering_match = TextField()
    value = TextField()
    label = TextField()
    description = TextField()
    config = JSONBField(null=False, default={})
    area_kind = TextField()
    match_tokens = JSONBField(null=False, default=[])
    geo_band = TextField()
    sort = IntegerField(null=False, default=0)
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False, default='public')
    dimension_slug = TextField()
    dimension_label = TextField()
    dimension_scope = TextField()
    worth_effect = TextField()
    worth_amount = DecimalField()
    matchers = JSONBField(null=False, default=[])
    offering_template_id = ForeignKey(to_model='OfferingTemplate', to_column='id', to_schema='web', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "starter_pack_item"
    _db_schema = "seo"
    _entity_token = "seo_starter_pack_item"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class TopicPlacementQueue(MatrxEntity):
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', primary_key=True, null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', primary_key=True, null=False)
    status = TextField(null=False, default='pending')
    placement_source = TextField()
    priority_clicks = BigIntegerField(null=False, default=0)
    priority_impressions = BigIntegerField(null=False, default=0)
    demand_window_days = IntegerField(null=False)
    demand_as_of = DateField(null=False)
    attempts = IntegerField(null=False, default=0)
    last_error = TextField()
    claimed_at = DateTimeField()
    completed_at = DateTimeField()
    enqueued_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "topic_placement_queue"
    _db_schema = "seo"
    _entity_token = "topic_placement_queue"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "component"

class TrackerStory(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    tracker_id = ForeignKey(to_model=CoverageTracker, to_column='id', to_schema='seo', null=False)
    story_key = TextField(null=False)
    title = TextField(null=False)
    member_item_ids = UUIDArrayField(null=False, default=[])
    member_url_keys = TextArrayField(null=False, default=[])
    outlet_count = IntegerField(null=False, default=0)
    first_seen_at = DateTimeField(null=False)
    first_surfaced_at = DateTimeField()
    last_run_id = UUIDField()
    latest = JSONBField()
    coarse_decision = TextField()
    coarse_performer = TextField()
    freshness_status = TextField()
    freshness_basis = TextField()
    withheld_reason = TextField()
    status = TextField(null=False, default='watching')
    hold_reason = TextField()
    triage_tier = TextField()
    triage_watch_reason = TextField()
    proof_gated = BooleanField()
    off_policy = BooleanField()
    newsworthiness_score = SmallIntegerField()
    newsworthiness_band = TextField()
    surfaced_override_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    surfaced_override_at = DateTimeField()
    alerted_at = DateTimeField()
    consolidated_into_story_key = TextField()
    evidence = JSONBField(null=False, default=[])
    dismissed_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    dismissed_at = DateTimeField()
    dismissed_reason = TextField()
    feedback_note = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "tracker_story"
    _db_schema = "seo"
    _entity_token = "seo_tracker_story"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class AiVisibilityCitation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    response_id = ForeignKey(to_model=AiVisibilityResponse, to_column='id', to_schema='seo', null=False)
    referring_domain_profile_id = ForeignKey(to_model=ReferringDomainProfile, to_column='id', to_schema='seo', )
    ordinal = IntegerField(null=False)
    url = TextField(null=False)
    normalized_url = TextField(null=False)
    domain = TextField()
    title = TextField()
    target_is_managed_site = BooleanField(null=False, default=False)
    cited_for = TextField()
    cited_for_claim_keys = JSONBField(null=False, default=[])
    endorsement_signal = TextField()
    evidence_quality = SmallIntegerField()
    capture_status = TextField(null=False, default='pending')
    capture_cache_key = TextField()
    source_capture = JSONBField(null=False, default={})
    captured_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "ai_visibility_citation"
    _db_schema = "seo"
    _entity_token = "seo_ai_visibility_citation"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class AiVisibilityClaim(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    response_id = ForeignKey(to_model=AiVisibilityResponse, to_column='id', to_schema='seo', null=False)
    claim_key = TextField(null=False)
    subject = TextField(null=False)
    claim_text = TextField(null=False)
    evidence_text = TextField(null=False)
    verification_status = TextField(null=False)
    influence_role = TextField(null=False)
    stance = TextField(null=False)
    significance = SmallIntegerField(null=False)
    confidence = SmallIntegerField(null=False)
    source_urls = JSONBField(null=False, default=[])
    influential_unverified = BooleanField(null=False, default=False)
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "ai_visibility_claim"
    _db_schema = "seo"
    _entity_token = "seo_ai_visibility_claim"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class AiVisibilitySignal(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    response_id = ForeignKey(to_model=AiVisibilityResponse, to_column='id', to_schema='seo', null=False)
    ordinal = IntegerField(null=False)
    category = TextField(null=False)
    signal = TextField(null=False)
    evidence_text = TextField(null=False)
    target_subject = TextField()
    source_url = TextField()
    influence = SmallIntegerField(null=False)
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "ai_visibility_signal"
    _db_schema = "seo"
    _entity_token = "seo_ai_visibility_signal"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class BacklinkSnapshot(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    dataset = TextField(null=False)
    target = TextField(null=False)
    target_type = TextField(null=False, default='domain')
    total_backlinks = BigIntegerField()
    referring_domains = BigIntegerField()
    referring_ips = BigIntegerField()
    referring_subnets = BigIntegerField()
    dofollow_backlinks = BigIntegerField()
    nofollow_backlinks = BigIntegerField()
    new_backlinks = BigIntegerField()
    lost_backlinks = BigIntegerField()
    broken_backlinks = BigIntegerField()
    rank_score = DecimalField()
    spam_score = DecimalField()
    observed_at = DateTimeField(null=False)
    extras = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'backlink_dimension_snapshot': {'from_model': 'BacklinkDimensionSnapshot', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'backlink_dimension_snapshot', 'from_schema': 'seo'}, 'backlink_observation': {'from_model': 'BacklinkObservation', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'backlink_observation', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "backlink_snapshot"
    _db_schema = "seo"
    _entity_token = "seo_backlink_snapshot"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class ChangeEvent(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    change_set_id = ForeignKey(to_model=ChangeSet, to_column='id', to_schema='seo', null=False)
    theory_id = ForeignKey(to_model=ChangeTheory, to_column='id', to_schema='seo', )
    change_item_id = ForeignKey(to_model=ChangeItem, to_column='id', to_schema='seo', )
    event_type = TextField(null=False)
    source = TextField(null=False, default='user')
    title = TextField(null=False)
    detail = TextField(null=False)
    occurred_at = DateTimeField(null=False)
    actor_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    source_snapshot_id = ForeignKey(to_model='Snapshot', to_column='id', to_schema='web', )
    source_crawl_session_id = ForeignKey(to_model='CrawlSession', to_column='id', to_schema='web', )
    details = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "change_event"
    _db_schema = "seo"
    _entity_token = "seo_change_event"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class ChangeMetric(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    change_set_id = ForeignKey(to_model=ChangeSet, to_column='id', to_schema='seo', null=False)
    theory_id = ForeignKey(to_model=ChangeTheory, to_column='id', to_schema='seo', null=False)
    label = TextField(null=False)
    metric_key = TextField(null=False)
    data_source = TextField(null=False)
    direction = TextField(null=False)
    target_value = DecimalField()
    target_change_pct = DecimalField()
    baseline_days = IntegerField(null=False, default=28)
    observation_days = IntegerField(null=False, default=28)
    minimum_data_days = IntegerField(null=False, default=7)
    is_primary = BooleanField(null=False, default=False)
    sort_order = IntegerField(null=False, default=0)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'change_assessment': {'from_model': 'ChangeAssessment', 'from_field': 'metric_id', 'referenced_field': 'id', 'related_name': 'change_assessment', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "change_metric"
    _db_schema = "seo"
    _entity_token = "seo_change_metric"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class CompetitorObservation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    competitor_id = ForeignKey(to_model=Competitor, to_column='id', to_schema='seo', null=False)
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    location_code = IntegerField()
    language_code = TextField()
    organic_keywords = IntegerField()
    paid_keywords = IntegerField()
    keyword_intersections = IntegerField()
    estimated_traffic = DecimalField()
    average_position = DecimalField()
    median_position = DecimalField()
    serp_visibility = DecimalField()
    rank_score = DecimalField()
    metrics = JSONBField(null=False, default={})
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    observed_at = DateTimeField(null=False)
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "competitor_observation"
    _db_schema = "seo"
    _entity_token = "seo_competitor_observation"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class CompetitorOpportunity(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    competitor_id = ForeignKey(to_model=Competitor, to_column='id', to_schema='seo', )
    target_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    opportunity_key = TextField(null=False)
    title = TextField(null=False)
    opportunity_type = TextField(null=False)
    competitor_domain = TextField(null=False)
    competitor_url = TextField()
    target_page_url = TextField()
    primary_keyword = TextField()
    supporting_keywords = JSONBField(null=False, default=[])
    verdict = TextField(null=False)
    why_competitor_wins = TextField(null=False)
    current_advantage = TextField(null=False)
    recommended_action = TextField(null=False)
    priority = SmallIntegerField(null=False)
    impact = TextField(null=False)
    effort = TextField(null=False)
    confidence = SmallIntegerField(null=False)
    evidence = JSONBField(null=False, default=[])
    dependencies = JSONBField(null=False, default=[])
    status = TextField(null=False, default='open')
    human_notes = TextField()
    accepted_at = DateTimeField()
    completed_at = DateTimeField()
    dismissed_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'link_gap_match': {'from_model': 'LinkGapMatch', 'from_field': 'competitor_opportunity_id', 'referenced_field': 'id', 'related_name': 'link_gap_match', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "competitor_opportunity"
    _db_schema = "seo"
    _entity_token = "seo_competitor_opportunity"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KeywordFacet(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    source = TextField(null=False, default='classifier')
    confidence = SmallIntegerField()
    classifier_version = TextField()
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    category_id = ForeignKey(to_model='Categories', to_column='id', to_schema='platform', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    matcher_id = ForeignKey(to_model=DimensionValueMatcher, to_column='id', to_schema='seo', )
    as_of = DateTimeField()
    pinned = BooleanField(null=False, default=False)
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_facet"
    _db_schema = "seo"
    _entity_token = "seo_keyword_facet"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class KeywordMarketObservation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    location_code = ForeignKey(to_model=Location, to_column='location_code', to_schema='seo', null=False)
    observed_at = DateTimeField(null=False)
    search_volume = IntegerField()
    competition = TextField()
    competition_index = IntegerField()
    cpc = DecimalField()
    low_top_of_page_bid = DecimalField()
    high_top_of_page_bid = DecimalField()
    monthly_searches = JSONBField(null=False, default=[])
    metrics_task_id = TextField()
    raw = JSONBField()
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'keyword_market': {'from_model': 'KeywordMarket', 'from_field': 'source_observation_id', 'referenced_field': 'id', 'related_name': 'keyword_market', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "keyword_market_observation"
    _db_schema = "seo"
    _entity_token = "seo_keyword_market_observation"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class PageIntentQueue(MatrxEntity):
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', primary_key=True, null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', primary_key=True, null=False)
    topic_id = ForeignKey(to_model=MapTopic, to_column='id', to_schema='seo', null=False)
    status = TextField(null=False, default='pending')
    intent_source = TextField()
    intent_disposition = TextField()
    intent_state = TextField()
    priority_clicks = BigIntegerField(null=False, default=0)
    priority_impressions = BigIntegerField(null=False, default=0)
    demand_window_days = IntegerField(null=False)
    demand_as_of = DateField(null=False)
    attempts = IntegerField(null=False, default=0)
    last_error = TextField()
    claimed_at = DateTimeField()
    completed_at = DateTimeField()
    enqueued_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "page_intent_queue"
    _db_schema = "seo"
    _entity_token = "page_intent_queue"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "entity"

class PagePerformance(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    strategy = TextField(null=False)
    performance_score = DecimalField()
    accessibility_score = DecimalField()
    best_practices_score = DecimalField()
    seo_score = DecimalField()
    lighthouse = JSONBField(null=False, default={})
    crux = JSONBField(null=False, default={})
    diagnostics = JSONBField(null=False, default={})
    observed_at = DateTimeField(null=False)
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "page_performance"
    _db_schema = "seo"
    _entity_token = "seo_page_performance"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class RankObservation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    rank_target_id = ForeignKey(to_model=RankTarget, to_column='id', to_schema='seo', null=False)
    location_id = ForeignKey(to_model=Location, to_column='id', to_schema='seo', )
    engine = TextField(null=False)
    language = TextField(null=False, default='en')
    device = TextField(null=False, default='desktop')
    search_type = TextField(null=False, default='organic')
    matched_domain = TextField()
    matched_url = TextField()
    organic_rank = IntegerField()
    absolute_rank = IntegerField()
    result_type = TextField(null=False, default='organic')
    match_rule = TextField(null=False, default='domain')
    observed_at = DateTimeField(null=False)
    query_settings = JSONBField(null=False, default={})
    serp_features = JSONBField(null=False, default={})
    title = TextField()
    snippet = TextField()
    extras = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "rank_observation"
    _db_schema = "seo"
    _entity_token = "seo_rank_observation"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class ReputationCase(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    backlink_id = ForeignKey(to_model=Backlink, to_column='id', to_schema='seo', )
    referring_domain_profile_id = ForeignKey(to_model=ReferringDomainProfile, to_column='id', to_schema='seo', )
    case_key = TextField(null=False)
    primary_source_kind = TextField(null=False)
    primary_source_id = TextField()
    source_url = TextField()
    source_domain = TextField()
    source_title = TextField()
    case_type = TextField(null=False)
    sentiment = TextField(null=False)
    verdict = TextField(null=False)
    controllability = TextField(null=False)
    headline = TextField(null=False)
    summary = TextField(null=False)
    priority = SmallIntegerField(null=False)
    confidence = SmallIntegerField(null=False)
    evidence_quality = SmallIntegerField(null=False)
    risk_score = SmallIntegerField(null=False)
    opportunity_score = SmallIntegerField(null=False)
    recommended_action = TextField(null=False)
    action_reason = TextField(null=False)
    pitch_angle = TextField()
    facts = JSONBField(null=False, default=[])
    inferences = JSONBField(null=False, default=[])
    evidence_refs = JSONBField(null=False, default=[])
    contradictions = JSONBField(null=False, default=[])
    missing_evidence = JSONBField(null=False, default=[])
    analysis = JSONBField(null=False, default={})
    human_ruling = JSONBField(null=False, default={})
    resolved_assessment = JSONBField(null=False, default={})
    evidence_fingerprint = TextField(null=False)
    analysis_version = TextField(null=False)
    requires_human_review = BooleanField(null=False, default=False)
    status = TextField(null=False, default='open')
    first_observed_at = DateTimeField()
    last_observed_at = DateTimeField()
    analyzed_at = DateTimeField(null=False)
    human_reviewed_at = DateTimeField()
    accepted_at = DateTimeField()
    completed_at = DateTimeField()
    dismissed_at = DateTimeField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "reputation_case"
    _db_schema = "seo"
    _entity_token = "seo_reputation_case"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class SearchPerformanceDaily(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', )
    date = DateField(null=False)
    query = TextField()
    country = TextField()
    device = TextField()
    dimension_profile = TextField(null=False, default='default')
    search_appearance = TextField()
    clicks = IntegerField(null=False, default=0)
    impressions = IntegerField(null=False, default=0)
    ctr = DecimalField()
    average_position = DecimalField()
    extras = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "search_performance_daily"
    _db_schema = "seo"
    _entity_token = "seo_search_performance_daily"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class SerpMention(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    serp_opportunity_id = ForeignKey(to_model=SerpOpportunity, to_column='id', to_schema='seo', null=False)
    query = TextField(null=False)
    variant = TextField(null=False)
    seed_keyword = TextField()
    url = TextField(null=False)
    title = TextField()
    snippet = TextField()
    rank = IntegerField()
    result_type = TextField(null=False, default='organic')
    observed_at = DateTimeField(null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', )
    extras = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "serp_mention"
    _db_schema = "seo"
    _entity_token = "seo_serp_mention"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SerpSnapshot(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    rank_target_id = ForeignKey(to_model=RankTarget, to_column='id', to_schema='seo', )
    location_id = ForeignKey(to_model=Location, to_column='id', to_schema='seo', )
    engine = TextField(null=False)
    language = TextField(null=False, default='en')
    device = TextField(null=False, default='desktop')
    search_type = TextField(null=False, default='organic')
    observed_at = DateTimeField(null=False)
    query_settings = JSONBField(null=False, default={})
    serp_features = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'serp_result': {'from_model': 'SerpResult', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'serp_result', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "serp_snapshot"
    _db_schema = "seo"
    _entity_token = "seo_serp_snapshot"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class SiteKeywordValue(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    offering_match = TextField()
    lead_quality = TextField()
    audience_fit = TextField()
    capacity_appetite = TextField()
    brand_fit = TextField()
    competitive_position = TextField()
    content_role = TextField()
    workflow_status = TextField(null=False, default='candidate')
    suppression_reason = TextField()
    priority_score = DecimalField()
    priority_computed_at = DateTimeField()
    traffic_class = TextField()
    notes = TextField()
    value_tier = TextField()
    value_score = DecimalField()
    value_reasons = JSONBField()
    value_computed_at = DateTimeField()
    topic_id = ForeignKey(to_model=MapTopic, to_column='id', to_schema='seo', )
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_keyword_value"
    _db_schema = "seo"
    _entity_token = "seo_site_keyword_value"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteOfferingValue(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    brand_offering_id = ForeignKey(to_model='BrandOffering', to_column='id', to_schema='web', null=False)
    offering_match = TextField()
    lead_quality = TextField()
    audience_fit = TextField()
    capacity_appetite = TextField()
    brand_fit = TextField()
    worth_points = DecimalField(null=False)
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    topic_id = ForeignKey(to_model=MapTopic, to_column='id', to_schema='seo', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site_offering_value"
    _db_schema = "seo"
    _entity_token = "seo_site_offering_value"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class WebAnalyticsDaily(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    date = DateField(null=False)
    source = TextField()
    medium = TextField()
    channel = TextField()
    campaign = TextField()
    device = TextField()
    landing_page = TextField()
    currency_code = TextField()
    property_timezone = TextField()
    sessions = IntegerField(null=False, default=0)
    users = IntegerField(null=False, default=0)
    engaged_sessions = IntegerField(null=False, default=0)
    views = IntegerField(null=False, default=0)
    engagement_rate = DecimalField()
    key_events = DecimalField(null=False, default=0)
    conversions = DecimalField(null=False, default=0)
    revenue = DecimalField()
    extras = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "web_analytics_daily"
    _db_schema = "seo"
    _entity_token = "seo_web_analytics_daily"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class BacklinkDimensionSnapshot(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    snapshot_id = ForeignKey(to_model=BacklinkSnapshot, to_column='id', to_schema='seo', null=False)
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    dimension_kind = TextField(null=False)
    dimension_key = TextField(null=False)
    label = TextField()
    url = TextField()
    backlinks = BigIntegerField()
    referring_domains = BigIntegerField()
    rank_score = DecimalField()
    spam_score = DecimalField()
    first_seen_at = DateTimeField()
    last_seen_at = DateTimeField()
    extras = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "backlink_dimension_snapshot"
    _db_schema = "seo"
    _entity_token = "seo_backlink_dimension_snapshot"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class BacklinkObservation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    run_id = ForeignKey(to_model=CollectionRun, to_column='id', to_schema='seo', null=False)
    raw_payload_id = ForeignKey(to_model=RawPayload, to_column='id', to_schema='seo', )
    snapshot_id = ForeignKey(to_model=BacklinkSnapshot, to_column='id', to_schema='seo', null=False)
    provider = TextField(null=False)
    dedup_key = TextField(null=False, unique=True)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    source_url = TextField(null=False)
    source_domain = TextField()
    target_url = TextField(null=False)
    anchor_text = TextField()
    link_type = TextField()
    is_dofollow = BooleanField()
    first_seen_at = DateTimeField()
    last_seen_at = DateTimeField()
    lost_at = DateTimeField()
    state = TextField(null=False, default='active')
    source_rank = DecimalField()
    domain_rank = DecimalField()
    spam_score = DecimalField()
    extras = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    backlink_id = ForeignKey(to_model=Backlink, to_column='id', to_schema='seo', )
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'backlink_change_event': {'from_model': 'BacklinkChangeEvent', 'from_field': 'previous_observation_id', 'referenced_field': 'id', 'related_name': 'backlink_change_event', 'from_schema': 'seo'}}
    _database = "matrx_seo"
    _table_name = "backlink_observation"
    _db_schema = "seo"
    _entity_token = "seo_backlink_observation"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class ChangeAssessment(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    change_set_id = ForeignKey(to_model=ChangeSet, to_column='id', to_schema='seo', null=False)
    theory_id = ForeignKey(to_model=ChangeTheory, to_column='id', to_schema='seo', null=False)
    metric_id = ForeignKey(to_model=ChangeMetric, to_column='id', to_schema='seo', )
    verdict = TextField(null=False)
    baseline_start = DateField(null=False)
    baseline_end = DateField(null=False)
    observation_start = DateField(null=False)
    observation_end = DateField(null=False)
    baseline_value = DecimalField()
    observed_value = DecimalField()
    delta = DecimalField()
    delta_pct = DecimalField()
    evidence_note = TextField(null=False)
    source = TextField(null=False, default='system')
    assessed_at = DateTimeField(null=False)
    assessed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "change_assessment"
    _db_schema = "seo"
    _entity_token = "seo_change_assessment"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ShownTo(str, Enum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class KeywordMarket(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    keyword_id = ForeignKey(to_model=Keyword, to_column='id', to_schema='seo', null=False)
    location_code = ForeignKey(to_model=Location, to_column='location_code', to_schema='seo', null=False, default=2840)
    search_volume = IntegerField()
    competition = TextField()
    competition_index = IntegerField()
    cpc = DecimalField()
    low_top_of_page_bid = DecimalField()
    high_top_of_page_bid = DecimalField()
    monthly_searches = JSONBField(null=False, default=[])
    demand_trajectory = TextField()
    growth_rate = DecimalField()
    seasonality_index = DecimalField()
    data_months = SmallIntegerField()
    metrics_fetched_at = DateTimeField()
    metrics_task_id = TextField()
    raw = JSONBField()
    source_provider = TextField()
    source_observation_id = ForeignKey(to_model=KeywordMarketObservation, to_column='id', to_schema='seo', )
    last_observed_at = DateTimeField()
    shown_to = EnumField(enum_class=ShownTo, )
    difficulty = SmallIntegerField()
    difficulty_source = TextField()
    difficulty_observed_at = DateTimeField()
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "keyword_market"
    _db_schema = "seo"
    _entity_token = "seo_keyword_market"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class LinkGapMatch(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    link_gap_domain_id = ForeignKey(to_model=LinkGapDomain, to_column='id', to_schema='seo', null=False)
    competitor_id = ForeignKey(to_model=Competitor, to_column='id', to_schema='seo', null=False)
    competitor_domain = TextField(null=False)
    source_url = TextField()
    target_url = TextField()
    backlinks = BigIntegerField()
    domain_rank = DecimalField()
    spam_score = DecimalField()
    is_dofollow = BooleanField()
    first_seen_at = DateTimeField()
    last_seen_at = DateTimeField()
    provider_metrics = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    competitor_opportunity_id = ForeignKey(to_model=CompetitorOpportunity, to_column='id', to_schema='seo', )
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "link_gap_match"
    _db_schema = "seo"
    _entity_token = "seo_link_gap_match"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SerpResult(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    snapshot_id = ForeignKey(to_model=SerpSnapshot, to_column='id', to_schema='seo', null=False)
    result_type = TextField(null=False, default='organic')
    organic_rank = IntegerField()
    absolute_rank = IntegerField(null=False)
    url = TextField()
    domain = TextField()
    title = TextField()
    snippet = TextField()
    extras = JSONBField(null=False, default={})
    metadata = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "serp_result"
    _db_schema = "seo"
    _entity_token = "seo_serp_result"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = True
    _rls_variant = "component"

class BacklinkChangeEvent(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    backlink_id = ForeignKey(to_model=Backlink, to_column='id', to_schema='seo', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    change_kind = TextField(null=False)
    severity = SmallIntegerField(null=False)
    source_domain = TextField(null=False)
    source_url = TextField(null=False)
    target_url = TextField()
    previous_value = JSONBField(null=False, default={})
    current_value = JSONBField(null=False, default={})
    previous_observation_id = ForeignKey(to_model=BacklinkObservation, to_column='id', to_schema='seo', )
    current_observation_id = ForeignKey(to_model=BacklinkObservation, to_column='id', to_schema='seo', )
    observed_at = DateTimeField(null=False)
    detected_at = DateTimeField(null=False)
    dedupe_key = TextField(null=False)
    alerted_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    deleted_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "backlink_change_event"
    _db_schema = "seo"
    _entity_token = "seo_backlink_change_event"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

# Read-only model for the seo.keyword_universal_facet VIEW (auto-generated — views are not writable).
class KeywordUniversalFacet(Model):
    keyword_id = UUIDField()
    intent_class = TextField()
    fulfillment_mode = TextField()
    audience_type = TextField()
    funnel_stage = TextField()
    transaction_direction = TextField()
    local_intent = TextField()
    urgency = TextField()
    comparison_intent = TextField()
    price_sensitivity = TextField()
    query_form = TextField()
    specificity = TextField()
    brand_presence = TextField()
    compliance_framing = TextField()
    _read_only = True
    _primary_keys = ['keyword_id']
    _table_name = "keyword_universal_facet"
    _db_schema = "seo"
    _database = "matrx_seo"

# Read-only model for the seo.v_change_set_summary VIEW (auto-generated — views are not writable).
class VChangeSetSummary(Model):
    id = UUIDField()
    organization_id = UUIDField()
    site_id = UUIDField()
    primary_page_id = UUIDField()
    primary_page_url = TextField()
    primary_page_path = TextField()
    title = TextField()
    summary = TextField()
    rationale = TextField()
    business_outcome = TextField()
    change_kind = TextField()
    status = TextField()
    confidence = SmallIntegerField()
    planned_for = DateTimeField()
    deployed_at = DateTimeField()
    verification_due_at = DateTimeField()
    completed_at = DateTimeField()
    source = TextField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    created_by = UUIDField()
    updated_by = UUIDField()
    version = IntegerField()
    theory_count = IntegerField()
    supported_theory_count = IntegerField()
    refuted_theory_count = IntegerField()
    item_count = IntegerField()
    verified_item_count = IntegerField()
    mismatched_item_count = IntegerField()
    last_assessed_at = DateTimeField()
    _read_only = True
    _primary_keys = ['id']
    _table_name = "v_change_set_summary"
    _db_schema = "seo"
    _database = "matrx_seo"

# Read-only model for the seo.v_map_topic_stats VIEW (auto-generated — views are not writable).
class VMapTopicStats(Model):
    topic_id = UUIDField()
    map_id = UUIDField()
    site_id = UUIDField()
    page_count = IntegerField()
    planned_count = IntegerField()
    keyword_count = IntegerField()
    _read_only = True
    _primary_keys = ['topic_id']
    _table_name = "v_map_topic_stats"
    _db_schema = "seo"
    _database = "matrx_seo"

# Read-only model for the seo.v_site_keyword_performance VIEW (auto-generated — views are not writable).
class VSiteKeywordPerformance(Model):
    site_id = UUIDField()
    organization_id = UUIDField()
    provider = TextField()
    keyword_id = UUIDField()
    query = TextField()
    first_date = DateField()
    last_date = DateField()
    clicks = BigIntegerField()
    impressions = BigIntegerField()
    ctr = DecimalField()
    average_position = DecimalField()
    top_page_id = UUIDField()
    top_page_url = TextField()
    top_page_path = TextField()
    top_page_clicks = BigIntegerField()
    top_page_impressions = BigIntegerField()
    search_volume = IntegerField()
    cpc = DecimalField()
    competition = TextField()
    competition_index = IntegerField()
    demand_trajectory = TextField()
    market_fetched_at = DateTimeField()
    workflow_status = TextField()
    content_role = TextField()
    competitive_position = TextField()
    priority_score = DecimalField()
    _read_only = True
    _primary_keys = ['site_id', 'provider', 'query']
    _table_name = "v_site_keyword_performance"
    _db_schema = "seo"
    _database = "matrx_seo"

# Read-only model for the seo.v_untracked_snapshot_change VIEW (auto-generated — views are not writable).
class VUntrackedSnapshotChange(Model):
    id = UUIDField()
    snapshot_id = UUIDField()
    previous_snapshot_id = UUIDField()
    organization_id = UUIDField()
    site_id = UUIDField()
    page_id = UUIDField()
    page_url = TextField()
    page_path = TextField()
    crawl_session_id = UUIDField()
    captured_at = DateTimeField()
    changed_fields = TextArrayField()
    _read_only = True
    _primary_keys = ['snapshot_id']
    _table_name = "v_untracked_snapshot_change"
    _db_schema = "seo"
    _database = "matrx_seo"

__all__ = [
    "AiCapability",
    "ChangeSet",
    "ClassifierRevisionLedger",
    "CollectionRun",
    "CoverageTracker",
    "EngineOwnerTask",
    "EngineSchedule",
    "GeoPlace",
    "GscDigRule",
    "Keyword",
    "KeywordSavedView",
    "LandscapeBrief",
    "Location",
    "MapFacet",
    "PageMappingQueue",
    "PageMeasurementHealth",
    "PrMoment",
    "ReferringDomainProfile",
    "SiteGeoArea",
    "SiteValueCombo",
    "SiteValueWorth",
    "SiteVocabulary",
    "StarterPack",
    "StoryAngle",
    "Topic",
    "TopicalMap",
    "AiVisibilityPanel",
    "AiVisibilityResponse",
    "Backlink",
    "ChangeItem",
    "ChangeTheory",
    "Competitor",
    "CoverageMention",
    "DimensionValueMatcher",
    "KeywordClassRule",
    "KeywordClassificationQueue",
    "KeywordEdge",
    "KeywordPlace",
    "KeywordTopic",
    "LinkGapDomain",
    "MapFacetValue",
    "MapTopic",
    "ProviderCall",
    "ProviderTask",
    "RankTarget",
    "RawPayload",
    "SerpOpportunity",
    "SiteKeywordOffering",
    "SiteTopicValue",
    "SourceRequest",
    "StarterPackItem",
    "TopicPlacementQueue",
    "TrackerStory",
    "AiVisibilityCitation",
    "AiVisibilityClaim",
    "AiVisibilitySignal",
    "BacklinkSnapshot",
    "ChangeEvent",
    "ChangeMetric",
    "CompetitorObservation",
    "CompetitorOpportunity",
    "KeywordFacet",
    "KeywordMarketObservation",
    "PageIntentQueue",
    "PagePerformance",
    "RankObservation",
    "ReputationCase",
    "SearchPerformanceDaily",
    "SerpMention",
    "SerpSnapshot",
    "SiteKeywordValue",
    "SiteOfferingValue",
    "WebAnalyticsDaily",
    "BacklinkDimensionSnapshot",
    "BacklinkObservation",
    "ChangeAssessment",
    "KeywordMarket",
    "LinkGapMatch",
    "SerpResult",
    "BacklinkChangeEvent",
    "Visibility",
    "ShownTo",
    "KeywordUniversalFacet",
    "VChangeSetSummary",
    "VMapTopicStats",
    "VSiteKeywordPerformance",
    "VUntrackedSnapshotChange",
]


model_registry.register_all(
[
        AiCapability,
        ChangeSet,
        ClassifierRevisionLedger,
        CollectionRun,
        CoverageTracker,
        EngineOwnerTask,
        EngineSchedule,
        GeoPlace,
        GscDigRule,
        Keyword,
        KeywordSavedView,
        LandscapeBrief,
        Location,
        MapFacet,
        PageMappingQueue,
        PageMeasurementHealth,
        PrMoment,
        ReferringDomainProfile,
        SiteGeoArea,
        SiteValueCombo,
        SiteValueWorth,
        SiteVocabulary,
        StarterPack,
        StoryAngle,
        Topic,
        TopicalMap,
        AiVisibilityPanel,
        AiVisibilityResponse,
        Backlink,
        ChangeItem,
        ChangeTheory,
        Competitor,
        CoverageMention,
        DimensionValueMatcher,
        KeywordClassRule,
        KeywordClassificationQueue,
        KeywordEdge,
        KeywordPlace,
        KeywordTopic,
        LinkGapDomain,
        MapFacetValue,
        MapTopic,
        ProviderCall,
        ProviderTask,
        RankTarget,
        RawPayload,
        SerpOpportunity,
        SiteKeywordOffering,
        SiteTopicValue,
        SourceRequest,
        StarterPackItem,
        TopicPlacementQueue,
        TrackerStory,
        AiVisibilityCitation,
        AiVisibilityClaim,
        AiVisibilitySignal,
        BacklinkSnapshot,
        ChangeEvent,
        ChangeMetric,
        CompetitorObservation,
        CompetitorOpportunity,
        KeywordFacet,
        KeywordMarketObservation,
        PageIntentQueue,
        PagePerformance,
        RankObservation,
        ReputationCase,
        SearchPerformanceDaily,
        SerpMention,
        SerpSnapshot,
        SiteKeywordValue,
        SiteOfferingValue,
        WebAnalyticsDaily,
        BacklinkDimensionSnapshot,
        BacklinkObservation,
        ChangeAssessment,
        KeywordMarket,
        LinkGapMatch,
        SerpResult,
        BacklinkChangeEvent,
        KeywordUniversalFacet,
        VChangeSetSummary,
        VMapTopicStats,
        VSiteKeywordPerformance,
        VUntrackedSnapshotChange
    ],
    skip_existing=True
)