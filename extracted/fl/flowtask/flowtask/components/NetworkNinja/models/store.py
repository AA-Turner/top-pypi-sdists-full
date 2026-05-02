from typing import List, Optional, Union, Dict, Any
from datetime import datetime
from datamodel import BaseModel, Field
from slugify import slugify
from .abstract import AbstractPayload
from .organization import Organization
from .client import Client
from .region import Region
from .market import Market
from .district import District


class StoreGeography(AbstractPayload):
    """
    Store Geography Model.

    Represents a store's geographical information.

    Example:
        {
            "geoid": 479,
            "region": "Assembly - Region",
            "district": "Assembly - District",
            "market": "136",
            "company_id": 61,
            "orgid": 71,
            "client_id": 61,
            "client_name": "ASSEMBLY"
        }
    """
    geoid: int = Field(primary_key=True, required=True)
    region: str
    region_id: int
    district_id: int
    district: str
    market_id: int
    market: str
    company_id: int
    orgid: Organization
    client_id: Client
    client_name: str

    class Meta:
        strict = True
        as_objects = True
        name = 'stores_geographies'
        schema: str = 'networkninja'

    def __post_init__(self):
        super().__post_init__()
        self.client_id.client_name = self.client_name

class StoreType(AbstractPayload):
    """
    Store Type Model.

    Represents a store type in the system.

    Example:
        {
            "store_type_id": 1,
            "store_type_name": "Retail",
            "store_type_description": "Retail Store"
        }
    """
    store_type_id: int = Field(primary_key=True, required=True)
    store_type: str = Field(alias="store_type_name")
    description: str
    client_id: Client
    client_name: str
    status: bool = Field(default=True)

    class Meta:
        strict = True
        as_objects = True
        name = 'stores_types'
        schema: str = 'networkninja'


class CustomStoreField(BaseModel):
    """
    Custom Field Model for Store.

    Represents a custom field for a store.

    Example:
        {
        "custom_id": 33,
        "custom_name": "Store Name",
        "custom_value": "Best Buy 4350",
        "custom_orgid": null,
        "custom_client_id": 1
    }
    """
    store_id: int
    custom_id: int = Field(primary_key=True, required=True)
    name: str = Field(alias="custom_name")
    column_name: Union[str, int]
    value: Union[str, None] = Field(alias="custom_value")
    obj_type: str = Field(alias="custom_type", default="Text")
    orgid: int = Field(alias="custom_orgid")
    client_id: str = Field(alias="custom_client_id")

    class Meta:
        name = 'stores_attributes'
        schema: str = 'networkninja'

    def __post_init__(self):
        self.column_name = slugify(self.name, separator="_")
        return super().__post_init__()

    def get_field(self):
        return {
            self.column_name: self.value
        }

def default_timezone(*args, **kwargs):
    return "America/New_York"


class Store(AbstractPayload):
    """
    Store Model.

    Represents a store in the system.

    Example:
        {
            "store_name": "KILMARNOCK-4350",
            "store_address": "200 Old Fair Grounds Way",
            "city": "Kilmarnock",
            "zipcode": "22482",
            "phone_number": "804-435-6149",
        }
    """
    store_number: int = Field(primary_key=True, required=True, alias='store_id')
    store_id: Optional[str]
    store_name: str
    store_address: str
    city: str
    zipcode: str
    phone_number: Optional[str]
    email_address: str = Field(alias="emailAddress")
    store_status: bool = Field(required=False, default=True)
    latitude: float
    longitude: float
    location_code: str
    timezone: str = Field(default=default_timezone)
    account_id: int
    account_name: str
    client_id: int
    client_name: str
    country: str = Field(alias='country_id')
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now)
    store_type_id: StoreType
    store_type: str = Field(alias="store_type_name")
    visit_rule: List[str]
    visit_category: List[str]
    orgid: List[int] = Field(alias='orgids', default_factory=list)
    custom_fields: List[CustomStoreField] = Field(default_factory=list)
    client_id: List[int] = Field(alias='client_ids', default_factory=list)
    client_name: List[str] = Field(alias='client_names', default_factory=list)
    market_name: Optional[Dict[str, str]] = Field(required=False, alias='markets')
    region_name: Optional[Dict[str, str]] = Field(required=False, alias='regions')
    district_name: Optional[Dict[str, str]] = Field(required=False, alias='districts')
    is_active: bool = Field(required=False, alias='store_is_active', default=True)
    is_deleted: bool = Field(default=False)

    class Meta:
        strict = True
        as_objects = True
        name = 'stores'
        schema: str = 'networkninja'

    def __post_init__(self):
        super().__post_init__()
        # geography
        if self.market_name and isinstance(self.market_name, dict):
            self.market_name = str(list(self.market_name.values())[0])
        if self.region_name and isinstance(self.region_name, dict):
            self.region_name = str(list(self.region_name.values())[0])
        if self.district_name and isinstance(self.district_name, dict):
            self.district_name = str(list(self.district_name.values())[0])
        # client
        if self.client_id and isinstance(self.client_id, list):
            self.client_id = self.client_id[0]
        if self.client_name and isinstance(self.client_name, list):
            self.client_name = self.client_name[0]
        # orgid:
        if self.orgid and isinstance(self.orgid, list):
            self.orgid = self.orgid[0]

    async def _sync_object(self, conn):
        """
        Sync the organization with the Database.
        """
        query = f"""
        select store_id, location_code FROM networkninja.stores where store_number = {self.store_number}
        """
        result = await conn.fetch_one(query)
        if result:
            self.store_id = result['store_id']
            self.location_code = result['location_code']
