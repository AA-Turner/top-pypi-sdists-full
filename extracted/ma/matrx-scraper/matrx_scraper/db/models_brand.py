# File: matrx_scraper/db/models_brand.py
from matrx_orm import BooleanField, DateTimeField, DecimalField, EnumField, ForeignKey, IntegerField, JSONBField, MatrxEntity, TextArrayField, TextField, UUIDField, model_registry, BaseDTO, BaseManager
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

class Brand(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
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
    integrations = JSONBField(null=False, default={})
    custom_fields = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    kind = TextField(null=False, default='company')
    person_party_id = ForeignKey(to_model='Party', to_column='id', to_schema='crm', )
    person_user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    focus = TextField(null=False, default='market')
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'brand_asset': {'from_model': 'BrandAsset', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_asset', 'from_schema': 'brand'}, 'brand_case_finding': {'from_model': 'BrandCaseFinding', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_case_finding', 'from_schema': 'brand'}, 'brand_choice': {'from_model': 'BrandChoice', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_choice', 'from_schema': 'brand'}, 'brand_exclusion': {'from_model': 'BrandExclusion', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_exclusion', 'from_schema': 'brand'}, 'brand_look_token': {'from_model': 'BrandLookToken', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_look_token', 'from_schema': 'brand'}, 'brand_offering': {'from_model': 'BrandOffering', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_offering', 'from_schema': 'brand'}, 'brand_persona': {'from_model': 'BrandPersona', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_persona', 'from_schema': 'brand'}, 'brand_review': {'from_model': 'BrandReview', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_review', 'from_schema': 'brand'}, 'brand_testimony': {'from_model': 'BrandTestimony', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_testimony', 'from_schema': 'brand'}, 'brand_fact': {'from_model': 'BrandFact', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_fact', 'from_schema': 'brand'}, 'brand_voice_fingerprint': {'from_model': 'BrandVoiceFingerprint', 'from_field': 'brand_id', 'referenced_field': 'id', 'related_name': 'brand_voice_fingerprint', 'from_schema': 'brand'}}
    _database = "matrx_web"
    _table_name = "brand"
    _db_schema = "brand"
    _entity_token = "brand"
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

class BrandOfferingTemplate(MatrxEntity):
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
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    parent_id = ForeignKey(to_model='BrandOfferingTemplate', to_column='id', to_schema='brand', )
    shown_to = EnumField(enum_class=ShownTo, )
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {'brand_offering': {'from_model': 'BrandOffering', 'from_field': 'template_id', 'referenced_field': 'id', 'related_name': 'brand_offering', 'from_schema': 'brand'}}
    _database = "matrx_web"
    _table_name = "brand_offering_template"
    _db_schema = "brand"
    _entity_token = "brand_offering_template"
    _is_versioned = True
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

class BrandRelationKind(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    key = TextField(null=False)
    label = TextField(null=False)
    routes_to = TextField()
    is_known = BooleanField(null=False, default=False)
    sort = IntegerField(null=False, default=0)
    status = TextField(null=False, default='active')
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
    stance = TextField(null=False, default='associated')
    description = TextField()
    has_sentiment = BooleanField(null=False, default=False)
    usage = TextField(null=False, default='use')
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_relation_kind"
    _db_schema = "brand"
    _entity_token = "brand_relation_kind"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "system"

class BrandAsset(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    kind = TextField(null=False)
    file_id = ForeignKey(to_model='Files', to_column='id', to_schema='files', )
    source_url = TextField()
    title = TextField()
    notes = TextField()
    source = TextField(null=False, default='manual')
    is_primary = BooleanField(null=False, default=False)
    sort_order = IntegerField(null=False, default=0)
    data = JSONBField(null=False, default={})
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    confirmed_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_asset"
    _db_schema = "brand"
    _entity_token = "brand_asset"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BrandCaseFinding(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    run_id = UUIDField()
    topic = TextField(null=False)
    pile = TextField(null=False)
    statement = TextField(null=False)
    other_side = TextField()
    explanation = TextField()
    element_codes = TextArrayField(null=False, default=[])
    rooms = TextArrayField(null=False, default=[])
    status = TextField(null=False, default='open')
    question_id = ForeignKey(to_model='DecisionQuestion', to_column='id', to_schema='interview', )
    settled_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    settled_at = DateTimeField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_case_finding"
    _db_schema = "brand"
    _entity_token = "brand_case_finding"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BrandChoice(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    element_id = ForeignKey(to_model='Categories', to_column='id', to_schema='platform', null=False)
    value = JSONBField(null=False)
    origin = TextField(null=False)
    recommended_placement = TextField()
    opinion_reason = TextField()
    decision = TextField(null=False, default='open')
    decided_by = UUIDField()
    decided_at = DateTimeField()
    decided_via = TextField()
    decision_reason = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    placement = TextField()
    word_signals = JSONBField(null=False, default=[])
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_choice"
    _db_schema = "brand"
    _entity_token = "brand_choice"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class ShownTo(StrEnum):
    ONLY_ME = "only_me"
    MY_TEAM = "my_team"
    EVERYONE = "everyone"
    EVERYONE_ON_AI_MATRX = "everyone_on_ai_matrx"

class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class BrandExclusion(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    match_kind = TextField(null=False)
    match_value = TextField(null=False)
    url = TextField()
    label = TextField()
    relation_key = TextField(null=False, default='not_us')
    source = TextField(null=False, default='smart_add')
    context = JSONBField(null=False, default={})
    shown_to = EnumField(enum_class=ShownTo, )
    custom_fields = JSONBField(null=False, default={})
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_exclusion"
    _db_schema = "brand"
    _entity_token = "brand_exclusion"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class BrandFact(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    kind = TextField(null=False)
    label = TextField()
    value = JSONBField(null=False)
    source = TextField(null=False, default='manual')
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    confirmed_at = DateTimeField()
    custom_fields = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    origin = TextField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_fact"
    _db_schema = "brand"
    _entity_token = "brand_fact"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BrandLookToken(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    chapter = TextField(null=False)
    token_key = TextField(null=False)
    role = TextField()
    light_value = JSONBField(null=False)
    dark_value = JSONBField()
    usage_note = TextField()
    status = TextField(null=False, default='suggested')
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    confirmed_at = DateTimeField()
    origin = TextField(null=False)
    source_url = TextField()
    found_by = TextField()
    sort_order = IntegerField(null=False, default=0)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_look_token"
    _db_schema = "brand"
    _entity_token = "brand_look_token"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BrandOffering(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    template_id = ForeignKey(to_model=BrandOfferingTemplate, to_column='id', to_schema='brand', )
    name = TextField(null=False)
    slug = TextField(null=False)
    kind = TextField(null=False)
    description = TextField()
    status = TextField(null=False, default='active')
    adopted_at = DateTimeField()
    sort = IntegerField(null=False, default=0)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    parent_id = ForeignKey(to_model='BrandOffering', to_column='id', to_schema='brand', )
    custom_fields = JSONBField(null=False, default={})
    price_amount = DecimalField()
    price_currency = TextField()
    price_unit = TextField()
    price_note = TextField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    revenue_share_pct = DecimalField()
    profit_share_pct = DecimalField()
    numbers_period = TextField()
    numbers_entered_by = UUIDField()
    numbers_entered_at = DateTimeField()
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    confirmed_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_offering"
    _db_schema = "brand"
    _entity_token = "brand_offering"
    _is_versioned = True
    _has_soft_delete = True
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

class BrandPersona(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    name = TextField(null=False)
    summary = TextField()
    demographics = JSONBField(null=False, default={})
    goals = TextArrayField(null=False, default=[])
    pain_points = TextArrayField(null=False, default=[])
    objections = TextArrayField(null=False, default=[])
    channels = TextArrayField(null=False, default=[])
    is_primary = BooleanField(null=False, default=False)
    sort = IntegerField(null=False, default=0)
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
    _database = "matrx_web"
    _table_name = "brand_persona"
    _db_schema = "brand"
    _entity_token = "brand_persona"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

class BrandReview(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    source = TextField(null=False)
    place_id = TextField()
    external_review_id = TextField(null=False)
    author_name = TextField()
    rating = DecimalField()
    review_text = TextField()
    published_at = DateTimeField()
    owner_response = TextField()
    raw = JSONBField(null=False, default={})
    fetched_at = DateTimeField(null=False)
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_review"
    _db_schema = "brand"
    _entity_token = "brand_review"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"

class BrandTestimony(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', null=False)
    room_id = ForeignKey(to_model='Categories', to_column='id', to_schema='platform', null=False)
    topic = TextField(null=False)
    statement = TextField(null=False)
    quote = TextField()
    source_url = TextField()
    source_value = TextField()
    firsthand = BooleanField()
    checkable = BooleanField()
    how_to_check = TextField()
    conferred = BooleanField()
    respondent_key = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_testimony"
    _db_schema = "brand"
    _entity_token = "brand_testimony"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "component"



class Visibility(StrEnum):
    PERSONAL = "personal"
    INTERNAL = "internal"
    LINK = "link"
    PUBLIC = "public"

class BrandVoiceFingerprint(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    label = TextField(null=False)
    profile_scope = TextField(null=False)
    person_user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    brand_id = ForeignKey(to_model=Brand, to_column='id', to_schema='brand', )
    status = TextField(null=False, default='draft')
    confidence = TextField(null=False)
    register_label = TextField()
    sample_count = IntegerField(null=False)
    sample_word_count = IntegerField(null=False)
    last_extracted_at = DateTimeField(null=False)
    refresh_due_at = DateTimeField(null=False)
    fingerprint = JSONBField(null=False)
    confirmed_at = DateTimeField()
    confirmed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    visibility = EnumField(enum_class=Visibility, null=False)
    published_to_web = BooleanField(null=False)
    published_to_web_at = DateTimeField()
    published_to_web_by = UUIDField()
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "brand_voice_fingerprint"
    _db_schema = "brand"
    _entity_token = "brand_voice_fingerprint"
    _is_versioned = True
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

__all__ = [
    "Brand",
    "BrandOfferingTemplate",
    "BrandRelationKind",
    "BrandAsset",
    "BrandCaseFinding",
    "BrandChoice",
    "BrandExclusion",
    "BrandFact",
    "BrandLookToken",
    "BrandOffering",
    "BrandPersona",
    "BrandReview",
    "BrandTestimony",
    "BrandVoiceFingerprint",
    "Visibility",
    "ShownTo",
]


model_registry.register_all(
[
        Brand,
        BrandOfferingTemplate,
        BrandRelationKind,
        BrandAsset,
        BrandCaseFinding,
        BrandChoice,
        BrandExclusion,
        BrandFact,
        BrandLookToken,
        BrandOffering,
        BrandPersona,
        BrandReview,
        BrandTestimony,
        BrandVoiceFingerprint
    ],
    skip_existing=True
)