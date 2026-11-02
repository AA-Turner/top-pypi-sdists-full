from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from channel_advisor_api.utils.logger import get_logger

logger = get_logger(__name__)


class ChannelAdvisorDC(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="ID")
    name: str = Field(alias="Name")
    code: str = Field(alias="Code")
    fulfillment_partner_name: str = Field(alias="FulfillmentPartnerName")
    contact_name: Optional[str] = Field(None, alias="ContactName")
    contact_email: Optional[str] = Field(None, alias="ContactEmail")
    contact_phone: Optional[str] = Field(None, alias="ContactPhone")
    address1: Optional[str] = Field(alias="Address1")
    address2: Optional[str] = Field(None, alias="Address2")
    city: Optional[str] = Field(alias="City")
    state_or_province: Optional[str] = Field(alias="StateOrProvince")
    country: Optional[str] = Field(alias="Country")
    postal_code: Optional[str] = Field(alias="PostalCode")
    pickup_location: bool = Field(alias="PickupLocation")
    ship_location: bool = Field(alias="ShipLocation")
    type: str = Field(alias="Type")
    is_externally_managed: bool = Field(alias="IsExternallyManaged")
    is_deleted: bool = Field(alias="IsDeleted")
    deleted_date_utc: Optional[str] = Field(None, alias="DeletedDateUtc")
    county: Optional[str] = Field(None, alias="County")
    district: Optional[str] = Field(None, alias="District")
    time_zone: Optional[str] = Field(None, alias="TimeZone")
    handling_time_minutes: Optional[int] = Field(None, alias="HandlingTimeMinutes")
    delivery_available: bool = Field(alias="DeliveryAvailable")
    pickup_order_hold_minutes: Optional[int] = Field(None, alias="PickupOrderHoldMinutes")
    throughput_limit_number: Optional[int] = Field(None, alias="ThroughputLimitNumber")
    throughput_limit_units: Optional[str] = Field(alias="ThroughputLimitUnits")
    main_phone: Optional[str] = Field(None, alias="MainPhone")
    alt_phone: Optional[str] = Field(None, alias="AltPhone")
    fax: Optional[str] = Field(None, alias="Fax")
    home_page: Optional[str] = Field(None, alias="HomePage")
    email: Optional[str] = Field(None, alias="Email")
    business_description: Optional[str] = Field(None, alias="BusinessDescription")
    latitude: Optional[float] = Field(None, alias="Latitude")
    longitude: Optional[float] = Field(None, alias="Longitude")
    store_categories: Optional[str] = Field(None, alias="StoreCategories")
    courier_pickup_instructions: Optional[str] = Field(None, alias="CourierPickupInstructions")
    customer_pickup_instructions: Optional[str] = Field(None, alias="CustomerPickupInstructions")
    pickup_instructions: Optional[str] = Field(None, alias="PickupInstructions")

    @staticmethod
    def all(limit: int = None):
        dcs = ChannelAdvisorDC.get_client().get_all_pages("DistributionCenters", limit=limit)
        return [ChannelAdvisorDC.model_validate(dc) for dc in dcs]

    def by_id(id: int):
        dcs = ChannelAdvisorDC.get_client().get_all_pages(f"DistributionCenters({id})", limit=1)
        if not dcs:
            raise ValueError(f"Failed to retrieve DC with ID {id}.")
        return ChannelAdvisorDC.model_validate(dcs[0])
