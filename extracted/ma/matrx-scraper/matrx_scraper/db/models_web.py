# File: matrx_scraper/db/models_web.py
from matrx_orm import BigIntegerField, BooleanField, CharField, DateField, DateTimeField, DecimalField, EnumField, FloatField, ForeignKey, IntegerField, JSONBField, MatrxEntity, Model, SmallIntegerField, TextArrayField, TextField, UUIDField, model_registry, BaseDTO, BaseManager
from enum import Enum
from dataclasses import dataclass
from typing import ClassVar



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class Brand(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    name = TextField(null=False)
    description = TextField()
    website_url = TextField()
    logo_url = TextField()
    favicon_url = TextField()
    og_image_url = TextField()
    industry = TextField()
    notes = TextField()
    status = TextField(null=False, default='active')
    visibility = EnumField(enum_class=Visibility, null=False)
    settings = JSONBField(null=False, default={})
    profile = JSONBField(null=False, default={})
    slug = TextField()
    previous_slugs = TextArrayField(null=False, default=[])
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'brand_asset': {'from_model': 'BrandAsset', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_asset', 'from_schema': 'web'}, 'brand_offering': {'from_model': 'BrandOffering', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_offering', 'from_schema': 'web'}, 'business_fact': {'from_model': 'BusinessFact', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'business_fact', 'from_schema': 'web'}, 'business_location': {'from_model': 'BusinessLocation', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'business_location', 'from_schema': 'web'}, 'discovered_item': {'from_model': 'DiscoveredItem', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'discovered_item', 'from_schema': 'web'}, 'property': {'from_model': 'Property', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'property', 'from_schema': 'web'}, 'site': {'from_model': 'Site', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'site', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "brand"
    _db_schema = "web"
    _entity_token = "web_brand"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class ListingPublisher(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    slug = TextField(null=False)
    name = TextField(null=False)
    domain = TextField()
    tier = TextField(null=False)
    is_aggregator = BooleanField(null=False, default=False)
    api_access = TextField(null=False, default='none')
    api_notes = TextField()
    manage_url = TextField()
    categories = TextArrayField(null=False, default=[])
    citation_weight = SmallIntegerField(null=False, default=50)
    sort_rank = IntegerField(null=False, default=1000)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False, default='public')
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'location_listing': {'from_model': 'LocationListing', 'from_field': 'publisher_id', 'referenced_field': 'id', 'related_name': 'location_listing', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "listing_publisher"
    _db_schema = "web"
    _entity_token = "web_listing_publisher"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class OfferingTemplate(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    name = TextField(null=False)
    slug = TextField(null=False)
    kind = TextField(null=False)
    description = TextField()
    aliases = JSONBField(null=False, default=[])
    industry_id = ForeignKey(to_model='Industries', to_column='id', to_schema='iam', )
    status = TextField(null=False, default='active')
    sort = IntegerField(null=False, default=0)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False, default='public')
    parent_id = ForeignKey(to_model='OfferingTemplate', to_column='id', to_schema='web', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'brand_offering': {'from_model': 'BrandOffering', 'from_field': 'template_id', 'referenced_field': 'id', 'related_name': 'brand_offering', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "offering_template"
    _db_schema = "web"
    _entity_token = "web_offering_template"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class Provider(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False, default='public')
    key = TextField(null=False)
    label = TextField(null=False)
    kind = TextField(null=False)
    config = JSONBField(null=False, default={})
    is_builtin = BooleanField(null=False, default=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'analysis_item': {'from_model': 'AnalysisItem', 'from_field': 'default_provider_id', 'referenced_field': 'id', 'related_name': 'analysis_item', 'from_schema': 'web'}, 'analysis_result': {'from_model': 'AnalysisResult', 'from_field': 'provider_id', 'referenced_field': 'id', 'related_name': 'analysis_result', 'from_schema': 'web'}, 'site_item_config': {'from_model': 'SiteItemConfig', 'from_field': 'provider_id', 'referenced_field': 'id', 'related_name': 'site_item_config', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "provider"
    _db_schema = "web"
    _entity_token = "web_provider"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class AnalysisItem(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False, default='public')
    key = TextField(null=False)
    label = TextField(null=False)
    description = TextField()
    category = TextField(null=False)
    subcategory = TextField(null=False)
    kind_definition_id = ForeignKey(to_model='KindDefinition', to_column='id', to_schema='content_ir', null=False)
    weight = DecimalField(null=False, default=1)
    score_contract = JSONBField(null=False, default={})
    severity_map = JSONBField(null=False, default={})
    is_builtin = BooleanField(null=False, default=False)
    default_provider_id = ForeignKey(to_model=Provider, to_column='id', to_schema='web', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'analysis_result': {'from_model': 'AnalysisResult', 'from_field': 'item_id', 'referenced_field': 'id', 'related_name': 'analysis_result', 'from_schema': 'web'}, 'finding': {'from_model': 'Finding', 'from_field': 'item_id', 'referenced_field': 'id', 'related_name': 'finding', 'from_schema': 'web'}, 'site_item_config': {'from_model': 'SiteItemConfig', 'from_field': 'item_id', 'referenced_field': 'id', 'related_name': 'site_item_config', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "analysis_item"
    _db_schema = "web"
    _entity_token = "web_analysis_item"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class BrandAsset(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Files', to_column='organization_id', to_schema='files', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', null=False)
    kind = TextField(null=False)
    file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    source_url = TextField()
    title = TextField()
    notes = TextField()
    source = TextField(null=False, default='manual')
    is_primary = BooleanField(null=False, default=False)
    sort_order = IntegerField(null=False, default=0)
    data = JSONBField(null=False, default={})
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    confirmed_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'discovered_item': {'from_model': 'DiscoveredItem', 'from_field': 'resolved_asset_id', 'referenced_field': 'id', 'related_name': 'discovered_item', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "brand_asset"
    _db_schema = "web"
    _entity_token = "web_brand_asset"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BrandOffering(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', null=False)
    template_id = ForeignKey(to_model=OfferingTemplate, to_column='id', to_schema='web', )
    name = TextField(null=False)
    slug = TextField(null=False)
    kind = TextField(null=False)
    description = TextField()
    status = TextField(null=False, default='active')
    adopted_at = DateTimeField()
    sort = IntegerField(null=False, default=0)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    parent_id = ForeignKey(to_model='BrandOffering', to_column='id', to_schema='web', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'site_offering': {'from_model': 'SiteOffering', 'from_field': 'brand_offering_id', 'referenced_field': 'id', 'related_name': 'site_offering', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "brand_offering"
    _db_schema = "web"
    _entity_token = "web_brand_offering"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BusinessFact(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', null=False)
    kind = TextField(null=False)
    label = TextField()
    value = JSONBField(null=False)
    source = TextField(null=False, default='manual')
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    confirmed_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'discovered_item': {'from_model': 'DiscoveredItem', 'from_field': 'resolved_fact_id', 'referenced_field': 'id', 'related_name': 'discovered_item', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "business_fact"
    _db_schema = "web"
    _entity_token = "web_business_fact"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BusinessLocation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', null=False)
    name = TextField(null=False)
    status = TextField(null=False, default='active')
    is_primary = BooleanField(null=False, default=False)
    street_address = TextField()
    address_line2 = TextField()
    locality = TextField()
    region = TextField()
    postal_code = TextField()
    country_code = TextField()
    phone = TextField()
    email = TextField()
    website_url = TextField()
    latitude = FloatField()
    longitude = FloatField()
    business_type = TextField()
    categories = TextArrayField(null=False, default=[])
    opening_hours = JSONBField(null=False, default=[])
    special_hours = JSONBField(null=False, default=[])
    attributes = JSONBField(null=False, default={})
    identifiers = JSONBField(null=False, default={})
    description = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'location_listing': {'from_model': 'LocationListing', 'from_field': 'location_id', 'referenced_field': 'id', 'related_name': 'location_listing', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "business_location"
    _db_schema = "web"
    _entity_token = "web_business_location"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class LocationListing(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    location_id = ForeignKey(to_model=BusinessLocation, to_column='id', to_schema='web', null=False)
    publisher_id = ForeignKey(to_model=ListingPublisher, to_column='id', to_schema='web', null=False)
    status = TextField(null=False, default='unknown')
    listing_url = TextField()
    observed = JSONBField(null=False, default={})
    nap_match = JSONBField()
    match_score = SmallIntegerField()
    last_checked_at = DateTimeField()
    source = TextField(null=False, default='manual')
    notes = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "location_listing"
    _db_schema = "web"
    _entity_token = "web_location_listing"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class AnalysisResult(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    subject_type = TextField(null=False)
    subject_id = UUIDField(null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    item_id = ForeignKey(to_model=AnalysisItem, to_column='id', to_schema='web', null=False)
    item_key = TextField(null=False)
    category = TextField(null=False)
    subcategory = TextField(null=False)
    provider_id = ForeignKey(to_model=Provider, to_column='id', to_schema='web', null=False)
    provider_version = TextField()
    run_id = UUIDField()
    batch_id = ForeignKey(to_model='ProviderBatch', to_column='id', to_schema='batch', )
    computed_at = DateTimeField(null=False)
    status = TextField(null=False)
    score = SmallIntegerField()
    severity = TextField(null=False, default='info')
    issue_count = IntegerField(null=False, default=0)
    confidence = DecimalField(null=False, default=1)
    payload_instance_id = ForeignKey(to_model='KindInstance', to_column='id', to_schema='content_ir', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'finding': {'from_model': 'Finding', 'from_field': 'last_result_id', 'referenced_field': 'id', 'related_name': 'finding', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "analysis_result"
    _db_schema = "web"
    _entity_token = "web_result"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class CrawlEvent(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    session_id = ForeignKey(to_model='CrawlSession', to_column='id', to_schema='web', null=False)
    sequence = BigIntegerField(null=False)
    event_type = TextField(null=False)
    phase = TextField()
    level = TextField(null=False, default='info')
    message = TextField()
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    crawl_url_id = ForeignKey(to_model='CrawlUrl', to_column='id', to_schema='web', )
    payload = JSONBField(null=False, default={})
    occurred_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "crawl_event"
    _db_schema = "web"
    _entity_token = "web_crawl_event"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class CrawlPreset(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    name = TextField(null=False)
    description = TextField()
    config = JSONBField(null=False, default={})
    last_used_at = DateTimeField()
    use_count = IntegerField(null=False, default=0)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'crawl_schedule': {'from_model': 'CrawlSchedule', 'from_field': 'preset_id', 'referenced_field': 'id', 'related_name': 'crawl_schedule', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "crawl_preset"
    _db_schema = "web"
    _entity_token = "web_crawl_preset"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class CrawlSchedule(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    name = TextField(null=False)
    enabled = BooleanField(null=False, default=True)
    cadence = JSONBField(null=False)
    timezone = TextField(null=False, default='UTC')
    next_run_at = DateTimeField()
    last_run_at = DateTimeField()
    last_session_id = ForeignKey(to_model='CrawlSession', to_column='id', to_schema='web', )
    preset_id = ForeignKey(to_model=CrawlPreset, to_column='id', to_schema='web', )
    claim_token = UUIDField()
    claim_expires_at = DateTimeField()
    last_outcome = TextField()
    last_error = TextField()
    consecutive_failures = IntegerField(null=False, default=0)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "crawl_schedule"
    _db_schema = "web"
    _entity_token = "web_crawl_schedule"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class CrawlSession(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    status = TextField(null=False, default='queued')
    trigger = TextField(null=False, default='manual')
    scope = JSONBField(null=False, default={})
    stats = JSONBField(null=False, default={})
    started_at = DateTimeField()
    finished_at = DateTimeField()
    error = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'crawl_event': {'from_model': 'CrawlEvent', 'from_field': 'session_id', 'referenced_field': 'id', 'related_name': 'crawl_event', 'from_schema': 'web'}, 'crawl_schedule': {'from_model': 'CrawlSchedule', 'from_field': 'last_session_id', 'referenced_field': 'id', 'related_name': 'crawl_schedule', 'from_schema': 'web'}, 'crawl_url': {'from_model': 'CrawlUrl', 'from_field': 'session_id', 'referenced_field': 'id', 'related_name': 'crawl_url', 'from_schema': 'web'}, 'snapshot': {'from_model': 'Snapshot', 'from_field': 'session_id', 'referenced_field': 'id', 'related_name': 'snapshot', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "crawl_session"
    _db_schema = "web"
    _entity_token = "web_crawl_session"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class CrawlUrl(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    session_id = ForeignKey(to_model=CrawlSession, to_column='id', to_schema='web', null=False)
    sequence = BigIntegerField(null=False)
    raw_url = TextField(null=False)
    normalized_url = TextField()
    url_hash = TextField(null=False)
    discovery_source = TextField(null=False, default='link')
    discovered_from_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    classification = TextField(null=False)
    outcome = TextField(null=False)
    is_in_scope = BooleanField(null=False, default=True)
    depth = IntegerField(null=False, default=0)
    http_status = IntegerField()
    final_url = TextField()
    reason_code = TextField()
    reason = TextField()
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    snapshot_id = ForeignKey(to_model='Snapshot', to_column='id', to_schema='web', )
    discovered_at = DateTimeField(null=False)
    completed_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'crawl_event': {'from_model': 'CrawlEvent', 'from_field': 'crawl_url_id', 'referenced_field': 'id', 'related_name': 'crawl_event', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "crawl_url"
    _db_schema = "web"
    _entity_token = "web_crawl_url"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class DiscoveredItem(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    snapshot_id = ForeignKey(to_model='Snapshot', to_column='id', to_schema='web', )
    source = TextField(null=False)
    category = TextField(null=False)
    guessed_kind = TextField()
    url = TextField()
    value = JSONBField(null=False, default={})
    context = JSONBField(null=False, default={})
    confidence = DecimalField()
    status = TextField(null=False, default='pending')
    resolved_asset_id = ForeignKey(to_model=BrandAsset, to_column='id', to_schema='web', )
    resolved_fact_id = ForeignKey(to_model=BusinessFact, to_column='id', to_schema='web', )
    reviewed_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    reviewed_at = DateTimeField()
    value_hash = TextField()
    resolved_property_id = ForeignKey(to_model='Property', to_column='id', to_schema='web', )
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "discovered_item"
    _db_schema = "web"
    _entity_token = "web_discovered_item"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class EndpointFamilySweepState(Model):
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', primary_key=True, null=False)
    last_sweep_at = DateTimeField()
    page_watermark = DateTimeField()
    sweeps_total = IntegerField(null=False, default=0)
    families_proposed_total = IntegerField(null=False, default=0)
    next_eligible_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "endpoint_family_sweep_state"
    _db_schema = "web"

class Finding(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    subject_type = TextField(null=False)
    subject_id = UUIDField(null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    item_id = ForeignKey(to_model=AnalysisItem, to_column='id', to_schema='web', null=False)
    item_key = TextField(null=False)
    category = TextField(null=False)
    subcategory = TextField(null=False)
    severity = TextField(null=False, default='info')
    status = TextField(null=False, default='open')
    suppressed = BooleanField(null=False, default=False)
    suppressed_reason = TextField()
    first_result_id = ForeignKey(to_model=AnalysisResult, to_column='id', to_schema='web', )
    last_result_id = ForeignKey(to_model=AnalysisResult, to_column='id', to_schema='web', )
    first_detected_at = DateTimeField(null=False)
    last_detected_at = DateTimeField(null=False)
    resolved_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "finding"
    _db_schema = "web"
    _entity_token = "web_finding"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class GscPageStat(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', null=False)
    date = DateField(null=False)
    clicks = IntegerField(null=False, default=0)
    impressions = IntegerField(null=False, default=0)
    ctr = DecimalField()
    position = DecimalField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "gsc_page_stat"
    _db_schema = "web"
    _entity_token = "web_gsc_page_stat"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class LinkEdge(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    snapshot_id = ForeignKey(to_model='Snapshot', to_column='id', to_schema='web', null=False)
    source_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', null=False)
    target_url = TextField(null=False)
    target_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', )
    is_internal = BooleanField(null=False)
    rel = TextField()
    anchor_text = TextField()
    http_status = IntegerField()
    position = IntegerField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "link_edge"
    _db_schema = "web"
    _entity_token = "web_link_edge"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Page(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    url = TextField(null=False)
    url_hash = TextField(null=False)
    path = TextField()
    provenance = TextField(null=False)
    status = TextField(null=False, default='active')
    first_seen = DateTimeField(null=False)
    last_seen = DateTimeField(null=False)
    http_status_last = IntegerField()
    target_keyword = TextField()
    meta_title_desired = TextField()
    meta_description_desired = TextField()
    latest_snapshot_id = UUIDField()
    seo_metrics_desired = JSONBField()
    content_type_last = TextField()
    desired_values = JSONBField(null=False, default={})
    canonical_page_id = ForeignKey(to_model='Page', to_column='id', to_schema='web', null=False)
    launch_tracking = JSONBField()
    link_score = DecimalField()
    link_score_computed_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'analysis_result': {'from_model': 'AnalysisResult', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'analysis_result', 'from_schema': 'web'}, 'crawl_event': {'from_model': 'CrawlEvent', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'crawl_event', 'from_schema': 'web'}, 'crawl_url': {'from_model': 'CrawlUrl', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'crawl_url', 'from_schema': 'web'}, 'finding': {'from_model': 'Finding', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'finding', 'from_schema': 'web'}, 'gsc_page_stat': {'from_model': 'GscPageStat', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'gsc_page_stat', 'from_schema': 'web'}, 'link_edge': {'from_model': 'LinkEdge', 'from_field': 'target_page_id', 'referenced_field': 'id', 'related_name': 'link_edge', 'from_schema': 'web'}, 'page_content': {'from_model': 'PageContent', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'page_content', 'from_schema': 'web'}, 'page_evidence': {'from_model': 'PageEvidence', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'page_evidence', 'from_schema': 'web'}, 'page_sitemap': {'from_model': 'PageSitemap', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'page_sitemap', 'from_schema': 'web'}, 'screenshot': {'from_model': 'Screenshot', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'screenshot', 'from_schema': 'web'}, 'snapshot': {'from_model': 'Snapshot', 'from_field': 'page_id', 'referenced_field': 'id', 'related_name': 'snapshot', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "page"
    _db_schema = "web"
    _entity_token = "web_page"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class PageContent(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model=Page, to_column='id', to_schema='web', null=False, unique=True)
    content = TextField(null=False)
    metadata = JSONBField(null=False, default={})
    version = IntegerField(null=False, default=1)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "page_content"
    _db_schema = "web"
    _entity_token = "web_page_content"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class PageEvidence(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model=Page, to_column='id', to_schema='web', null=False)
    source_type = TextField(null=False)
    source_binding_id = UUIDField()
    external_key = TextField()
    is_present = BooleanField(null=False, default=True)
    first_seen_at = DateTimeField(null=False)
    last_seen_at = DateTimeField(null=False)
    last_checked_at = DateTimeField()
    evidence = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "page_evidence"
    _db_schema = "web"
    _entity_token = "web_page_evidence"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class PageSitemap(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model=Page, to_column='id', to_schema='web', null=False)
    sitemap_id = ForeignKey(to_model='Sitemap', to_column='id', to_schema='web', null=False)
    lastmod = DateTimeField()
    changefreq = TextField()
    priority = DecimalField()
    first_seen = DateTimeField(null=False)
    last_seen = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "page_sitemap"
    _db_schema = "web"
    _entity_token = "web_page_sitemap"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Property(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', null=False)
    kind = TextField(null=False)
    url = TextField()
    handle = TextField()
    display_name = TextField()
    status = TextField(null=False, default='active')
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    connection = JSONBField(null=False, default={})
    settings = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'discovered_item': {'from_model': 'DiscoveredItem', 'from_field': 'resolved_property_id', 'referenced_field': 'id', 'related_name': 'discovered_item', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "property"
    _db_schema = "web"
    _entity_token = "web_property"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Screenshot(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Files', to_column='organization_id', to_schema='files', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model=Page, to_column='id', to_schema='web', )
    snapshot_id = ForeignKey(to_model='Snapshot', to_column='id', to_schema='web', )
    kind = TextField(null=False, default='page')
    width = IntegerField()
    height = IntegerField()
    captured_at = DateTimeField(null=False)
    file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'site': {'from_model': 'Site', 'from_field': 'homepage_screenshot_id', 'referenced_field': 'id', 'related_name': 'site', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "screenshot"
    _db_schema = "web"
    _entity_token = "web_screenshot"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(str, Enum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class Site(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    name = TextField(null=False)
    root_url = TextField(null=False)
    domain = TextField(null=False)
    status = TextField(null=False, default='active')
    visibility = EnumField(enum_class=Visibility, null=False)
    integrations = JSONBField(null=False, default={})
    homepage_screenshot_id = ForeignKey(to_model=Screenshot, to_column='id', to_schema='web', )
    settings = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='web', )
    description = TextField()
    favicon_url = TextField()
    logo_url = TextField()
    og_image_url = TextField()
    initialized_at = DateTimeField()
    initialization = JSONBField(null=False, default={})
    gsc_synced_at = DateTimeField()
    gsc_sync = JSONBField(null=False, default={})
    plan_profile_id = ForeignKey(to_model='Profile', to_column='id', to_schema='plan', )
    slug = TextField()
    previous_slugs = TextArrayField(null=False, default=[])
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'analysis_result': {'from_model': 'AnalysisResult', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'analysis_result', 'from_schema': 'web'}, 'crawl_event': {'from_model': 'CrawlEvent', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'crawl_event', 'from_schema': 'web'}, 'crawl_preset': {'from_model': 'CrawlPreset', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'crawl_preset', 'from_schema': 'web'}, 'crawl_schedule': {'from_model': 'CrawlSchedule', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'crawl_schedule', 'from_schema': 'web'}, 'crawl_session': {'from_model': 'CrawlSession', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'crawl_session', 'from_schema': 'web'}, 'crawl_url': {'from_model': 'CrawlUrl', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'crawl_url', 'from_schema': 'web'}, 'discovered_item': {'from_model': 'DiscoveredItem', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'discovered_item', 'from_schema': 'web'}, 'endpoint_family_sweep_state': {'from_model': 'EndpointFamilySweepState', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'endpoint_family_sweep_state', 'from_schema': 'web'}, 'finding': {'from_model': 'Finding', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'finding', 'from_schema': 'web'}, 'gsc_page_stat': {'from_model': 'GscPageStat', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'gsc_page_stat', 'from_schema': 'web'}, 'link_edge': {'from_model': 'LinkEdge', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'link_edge', 'from_schema': 'web'}, 'page_content': {'from_model': 'PageContent', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'page_content', 'from_schema': 'web'}, 'page_evidence': {'from_model': 'PageEvidence', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'page_evidence', 'from_schema': 'web'}, 'page': {'from_model': 'Page', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'page', 'from_schema': 'web'}, 'page_sitemap': {'from_model': 'PageSitemap', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'page_sitemap', 'from_schema': 'web'}, 'property': {'from_model': 'Property', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'property', 'from_schema': 'web'}, 'screenshot': {'from_model': 'Screenshot', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'screenshot', 'from_schema': 'web'}, 'site_endpoint_rule': {'from_model': 'SiteEndpointRule', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'site_endpoint_rule', 'from_schema': 'web'}, 'site_item_config': {'from_model': 'SiteItemConfig', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'site_item_config', 'from_schema': 'web'}, 'site_offering': {'from_model': 'SiteOffering', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'site_offering', 'from_schema': 'web'}, 'sitemap': {'from_model': 'Sitemap', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'sitemap', 'from_schema': 'web'}, 'snapshot': {'from_model': 'Snapshot', 'from_field': 'site_id', 'referenced_field': 'id', 'related_name': 'snapshot', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "site"
    _db_schema = "web"
    _entity_token = "web_site"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class SiteEndpointRule(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    site_id = ForeignKey(to_model=Site, to_column='id', to_schema='web', null=False)
    path_prefix = TextField(null=False)
    query_param = TextField()
    reason = TextField(null=False)
    source = TextField(null=False, default='sweep')
    detector = TextField()
    confidence = FloatField()
    is_active = BooleanField(null=False, default=True)
    pages_matched_at_apply = IntegerField()
    assist_id = UUIDField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "site_endpoint_rule"
    _db_schema = "web"
    _entity_token = "web_site_endpoint_rule"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteItemConfig(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model=Site, to_column='id', to_schema='web', null=False)
    item_id = ForeignKey(to_model=AnalysisItem, to_column='id', to_schema='web', null=False)
    provider_id = ForeignKey(to_model=Provider, to_column='id', to_schema='web', null=False)
    enabled = BooleanField(null=False, default=True)
    cadence = JSONBField(null=False, default={})
    config = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "site_item_config"
    _db_schema = "web"
    _entity_token = "web_site_item_config"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class SiteOffering(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    site_id = ForeignKey(to_model=Site, to_column='id', to_schema='web', null=False)
    brand_offering_id = ForeignKey(to_model=BrandOffering, to_column='id', to_schema='web', null=False)
    status = TextField(null=False, default='active')
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "site_offering"
    _db_schema = "web"
    _entity_token = "web_site_offering"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Sitemap(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model=Site, to_column='id', to_schema='web', null=False)
    url = TextField(null=False)
    kind = TextField(null=False, default='unknown')
    parent_sitemap_id = ForeignKey(to_model='Sitemap', to_column='id', to_schema='web', )
    status_code = IntegerField()
    url_count = IntegerField()
    child_count = IntegerField()
    is_active = BooleanField(null=False, default=True)
    first_seen = DateTimeField(null=False)
    last_seen = DateTimeField()
    last_fetched_at = DateTimeField()
    fetch_error = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'page_sitemap': {'from_model': 'PageSitemap', 'from_field': 'sitemap_id', 'referenced_field': 'id', 'related_name': 'page_sitemap', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "sitemap"
    _db_schema = "web"
    _entity_token = "web_sitemap"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class Snapshot(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Files', to_column='organization_id', to_schema='files', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='auth', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    site_id = ForeignKey(to_model=Site, to_column='id', to_schema='web', null=False)
    page_id = ForeignKey(to_model=Page, to_column='id', to_schema='web', null=False)
    session_id = ForeignKey(to_model=CrawlSession, to_column='id', to_schema='web', null=False)
    captured_at = DateTimeField(null=False)
    final_url = TextField()
    http_status = IntegerField()
    content_hash = TextField()
    word_count = IntegerField()
    head_tags = JSONBField(null=False, default={})
    headings = JSONBField(null=False, default={})
    links_summary = JSONBField(null=False, default={})
    images = JSONBField(null=False, default={})
    structured_data = JSONBField(null=False, default={})
    perf = JSONBField(null=False, default={})
    extracted = JSONBField(null=False, default={})
    body_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', null=False)
    markdown_file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    seo_metrics = JSONBField()
    audit_metrics = JSONBField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'crawl_url': {'from_model': 'CrawlUrl', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'crawl_url', 'from_schema': 'web'}, 'discovered_item': {'from_model': 'DiscoveredItem', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'discovered_item', 'from_schema': 'web'}, 'link_edge': {'from_model': 'LinkEdge', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'link_edge', 'from_schema': 'web'}, 'screenshot': {'from_model': 'Screenshot', 'from_field': 'snapshot_id', 'referenced_field': 'id', 'related_name': 'screenshot', 'from_schema': 'web'}}
    _database = "matrx_web"
    _table_name = "snapshot"
    _db_schema = "web"
    _entity_token = "web_snapshot"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

# Read-only model for the web.v_latest_result VIEW (auto-generated — views are not writable).
class VLatestResult(Model):
    id = UUIDField()
    organization_id = UUIDField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    created_by = UUIDField()
    updated_by = UUIDField()
    deleted_at = DateTimeField()
    version = IntegerField()
    metadata = JSONBField()
    site_id = UUIDField()
    subject_type = TextField()
    subject_id = UUIDField()
    page_id = UUIDField()
    item_id = UUIDField()
    item_key = TextField()
    category = TextField()
    subcategory = TextField()
    provider_id = UUIDField()
    provider_version = TextField()
    run_id = UUIDField()
    batch_id = UUIDField()
    computed_at = DateTimeField()
    status = TextField()
    score = SmallIntegerField()
    severity = TextField()
    issue_count = IntegerField()
    confidence = DecimalField()
    payload_instance_id = UUIDField()
    _read_only = True
    _primary_keys = ['id']
    _table_name = "v_latest_result"
    _db_schema = "web"
    _database = "matrx_web"

# Read-only model for the web.v_page_list VIEW (auto-generated — views are not writable).
class VPageList(Model):
    page_id = UUIDField()
    site_id = UUIDField()
    url = TextField()
    path = TextField()
    status = TextField()
    provenance = TextField()
    http_status_last = IntegerField()
    content_type_last = TextField()
    is_resource = BooleanField()
    target_keyword = TextField()
    first_seen = DateTimeField()
    last_seen = DateTimeField()
    latest_snapshot_id = UUIDField()
    sitemap_count = BigIntegerField()
    in_gsc = BooleanField()
    observed_title = TextField()
    word_count = IntegerField()
    serp_ok = BooleanField()
    social_ok = BooleanField()
    indexability_verdict = TextField()
    gsc_clicks_28d = BigIntegerField()
    gsc_impressions_28d = BigIntegerField()
    gsc_position_28d = DecimalField()
    backlink_count = BigIntegerField()
    backlink_referring_domains = BigIntegerField()
    health_score = IntegerField()
    is_canonical = BooleanField()
    has_page_evidence = BooleanField()
    _read_only = True
    _primary_keys = ['page_id']
    _table_name = "v_page_list"
    _db_schema = "web"
    _database = "matrx_web"

# Read-only model for the web.v_page_score VIEW (auto-generated — views are not writable).
class VPageScore(Model):
    site_id = UUIDField()
    page_id = UUIDField()
    page_score = DecimalField()
    fail_count = BigIntegerField()
    _read_only = True
    _primary_keys = ['site_id', 'page_id']
    _table_name = "v_page_score"
    _db_schema = "web"
    _database = "matrx_web"

# Read-only model for the web.v_priority_queue VIEW (auto-generated — views are not writable).
class VPriorityQueue(Model):
    site_id = UUIDField()
    page_id = UUIDField()
    item_id = UUIDField()
    item_key = TextField()
    category = TextField()
    subcategory = TextField()
    severity = TextField()
    priority = DecimalField()
    _read_only = True
    _primary_keys = ['site_id', 'page_id', 'item_id']
    _table_name = "v_priority_queue"
    _db_schema = "web"
    _database = "matrx_web"

# Read-only model for the web.v_site_kpis VIEW (auto-generated — views are not writable).
class VSiteKpis(Model):
    site_id = UUIDField()
    page_count = BigIntegerField()
    pages_in_gsc = BigIntegerField()
    gsc_clicks_28d = BigIntegerField()
    gsc_impressions_28d = BigIntegerField()
    gsc_position_28d = DecimalField()
    gsc_clicks_prev_28d = BigIntegerField()
    gsc_impressions_prev_28d = BigIntegerField()
    gsc_cur_days = BigIntegerField()
    gsc_prev_days = BigIntegerField()
    gsc_latest_date = DateField()
    resource_count = BigIntegerField()
    _read_only = True
    _primary_keys = ['site_id']
    _table_name = "v_site_kpis"
    _db_schema = "web"
    _database = "matrx_web"

# Read-only model for the web.v_site_score VIEW (auto-generated — views are not writable).
class VSiteScore(Model):
    site_id = UUIDField()
    site_score = DecimalField()
    scored_pages = BigIntegerField()
    _read_only = True
    _primary_keys = ['site_id']
    _table_name = "v_site_score"
    _db_schema = "web"
    _database = "matrx_web"

__all__ = [
    "Brand",
    "ListingPublisher",
    "OfferingTemplate",
    "Provider",
    "AnalysisItem",
    "BrandAsset",
    "BrandOffering",
    "BusinessFact",
    "BusinessLocation",
    "LocationListing",
    "AnalysisResult",
    "CrawlEvent",
    "CrawlPreset",
    "CrawlSchedule",
    "CrawlSession",
    "CrawlUrl",
    "DiscoveredItem",
    "EndpointFamilySweepState",
    "Finding",
    "GscPageStat",
    "LinkEdge",
    "Page",
    "PageContent",
    "PageEvidence",
    "PageSitemap",
    "Property",
    "Screenshot",
    "Site",
    "SiteEndpointRule",
    "SiteItemConfig",
    "SiteOffering",
    "Sitemap",
    "Snapshot",
    "Visibility",
    "VLatestResult",
    "VPageList",
    "VPageScore",
    "VPriorityQueue",
    "VSiteKpis",
    "VSiteScore",
]


model_registry.register_all(
[
        Brand,
        ListingPublisher,
        OfferingTemplate,
        Provider,
        AnalysisItem,
        BrandAsset,
        BrandOffering,
        BusinessFact,
        BusinessLocation,
        LocationListing,
        AnalysisResult,
        CrawlEvent,
        CrawlPreset,
        CrawlSchedule,
        CrawlSession,
        CrawlUrl,
        DiscoveredItem,
        EndpointFamilySweepState,
        Finding,
        GscPageStat,
        LinkEdge,
        Page,
        PageContent,
        PageEvidence,
        PageSitemap,
        Property,
        Screenshot,
        Site,
        SiteEndpointRule,
        SiteItemConfig,
        SiteOffering,
        Sitemap,
        Snapshot,
        VLatestResult,
        VPageList,
        VPageScore,
        VPriorityQueue,
        VSiteKpis,
        VSiteScore
    ],
    skip_existing=True
)