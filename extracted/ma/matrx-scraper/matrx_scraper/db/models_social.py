# File: matrx_scraper/db/models_social.py
from matrx_orm import BooleanField, DateTimeField, EnumField, ForeignKey, IntegerField, JSONBField, MatrxEntity, SmallIntegerField, TextArrayField, TextField, UUIDField, model_registry, BaseDTO, BaseManager
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
    _database = "matrx_web"
    _table_name = "listing_publisher"
    _db_schema = "social"
    _entity_token = "social_listing_publisher"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class Property(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='brand', null=False)
    kind = TextField(null=False)
    url = TextField()
    handle = TextField()
    display_name = TextField()
    status = TextField(null=False, default='active')
    site_id = ForeignKey(to_model='Site', to_column='id', to_schema='web', )
    connection = JSONBField(null=False, default={})
    settings = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    owner_kind = TextField(null=False, default='company')
    owner_party_id = ForeignKey(to_model='Party', to_column='id', to_schema='crm', )
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'tracked_account': {'from_model': 'TrackedAccount', 'from_field': 'property_id', 'referenced_field': 'id', 'related_name': 'tracked_account', 'from_schema': 'social'}}
    _database = "matrx_web"
    _table_name = "property"
    _db_schema = "social"
    _entity_token = "social_property"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

__all__ = [
    "ListingPublisher",
    "Property",
    "Visibility",
    "ShownTo",
]


model_registry.register_all(
[
        ListingPublisher,
        Property
    ],
    skip_existing=True
)