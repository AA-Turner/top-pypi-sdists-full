# File: matrx_scraper/db/models_local.py
from matrx_orm import BooleanField, DateTimeField, FloatField, ForeignKey, IntegerField, JSONBField, MatrxEntity, SmallIntegerField, TextArrayField, TextField, UUIDField, model_registry, BaseDTO, BaseManager
from dataclasses import dataclass
from typing import ClassVar

class BusinessLocation(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model='Brand', to_column='id', to_schema='brand', null=False)
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
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'location_listing': {'from_model': 'LocationListing', 'from_field': 'location_id', 'referenced_field': 'id', 'related_name': 'location_listing', 'from_schema': 'local'}}
    _database = "matrx_web"
    _table_name = "business_location"
    _db_schema = "local"
    _entity_token = "local_business_location"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class LocationListing(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    location_id = ForeignKey(to_model=BusinessLocation, to_column='id', to_schema='local', null=False)
    publisher_id = UUIDField(null=False)
    status = TextField(null=False, default='unknown')
    listing_url = TextField()
    observed = JSONBField(null=False, default={})
    nap_match = JSONBField()
    match_score = SmallIntegerField()
    last_checked_at = DateTimeField()
    source = TextField(null=False, default='manual')
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
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "location_listing"
    _db_schema = "local"
    _entity_token = "local_location_listing"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

__all__ = [
    "BusinessLocation",
    "LocationListing",
]


model_registry.register_all(
[
        BusinessLocation,
        LocationListing
    ],
    skip_existing=True
)