from datetime import datetime
from typing import ClassVar, List, Optional
from urllib.parse import urlencode
from pydantic import BaseModel, Field, ConfigDict
import json
from functools import cached_property
from channel_advisor_api.models.channel_advisor_attributes import (
    BaseOptimizeAttributes,
    ChildOptimizeAttributes,
    ParentOptimizeAttributes,
)
from channel_advisor_api.models.channel_advisor_dc import ChannelAdvisorDC
from channel_advisor_api.models.channel_advisor_client import ChannelAdvisorClient
from abc import ABC

from channel_advisor_api.utils.logger import get_logger

logger = get_logger(__name__)


class BaseProduct(BaseModel, ABC):
    model_config = ConfigDict(populate_by_name=True)

    @cached_property
    def client(self) -> ChannelAdvisorClient:
        return ChannelAdvisorClient()

    @classmethod
    def get_client(cls) -> ChannelAdvisorClient:
        return ChannelAdvisorClient()

    @classmethod
    def get_property_names(cls, as_param: bool = False) -> List[str] | dict:
        # Get the Alias names for all of the properties in the model
        fields = [field.alias for field in cls.model_fields.values()]
        if as_param:
            return {"$select": ",".join(fields)}
        return fields

    @classmethod
    def by_id(cls, id: int):
        client = cls.get_client()
        uri = f"{cls._base_uri}({id})"
        params = cls.get_property_names(as_param=True)
        uri = f"{uri}?{urlencode(params, doseq=True)}"
        response = client.request("get", uri)
        if not response:
            raise ValueError(f"Product with ID {id} not found")
        product = json.loads(response.content)
        if not product:
            raise ValueError(f"Product with ID {id} not found")
        return cls.model_validate(product)

    @classmethod
    def all(cls, limit: int = None, filter: str = None, order_by: str = "Sku") -> List["MinProduct"]:
        params = {
            "$orderby": order_by,
            **cls.get_property_names(as_param=True),
        }
        if filter:
            params["$filter"] = filter
        uri = f"{cls._base_uri}?{urlencode(params, doseq=True)}"
        items = cls.get_client().get_all_pages(uri, limit=limit)
        return [cls.model_validate(item) for item in items]

    @classmethod
    def by_sku(cls, sku: str) -> "MinProduct":
        escaped_sku = cls.escape_filter_value(sku)
        products = cls.all(filter=f"Sku eq '{escaped_sku}'")
        if not products:
            raise ValueError(f"Product with SKU {sku} not found")
        return products[0]

    @classmethod
    def escape_filter_value(cls, value: str) -> str:
        """Escapes special characters in filter values for the ChannelAdvisor API."""
        return value.replace("'", "''")

    @classmethod
    def search_by_sku(cls, sku: str, limit: int = None, include_children: bool = False) -> List["MinProduct"]:
        """We have to check each page for the sku because the API doesn't support fuzzy search"""
        logger.info(f"Searching for product with sku: {sku} and include_children: {include_children}")
        products: List[cls] = []
        params = {
            "$orderby": "Sku",
            "$filter": f"Sku ge '{sku}'",
            **cls.get_property_names(as_param=True),
        }
        if not include_children:
            params["$filter"] += " and (IsParent eq true or IsInRelationship eq false)"
        if limit:
            params["$top"] = [limit]
        next_link = f"{cls._base_uri}?{urlencode(params, doseq=True)}"
        client = cls.get_client()
        while next_link:
            response = client.request("get", next_link)
            content = json.loads(response.content)
            next_link = content.get("@odata.nextLink", None)
            for item in content.get("value"):
                product = cls.model_validate(item)
                if product.sku.lower().startswith(sku.lower()):
                    products.append(product)
                else:
                    logger.debug(f"Ending search with '{product.sku}' because it doesn't start with '{sku}'")
                    next_link = None
                    break
        logger.info(f"Found {len(products)} products with sku starting with {sku} include_children: {include_children}")
        return products

    def _exluded_save_fields(self) -> List[str]:
        exclude_fields = {
            field_name
            for field_name in self.model_fields
            if (
                "quantity" in field_name.lower()
                or field_name.lower().endswith("id")
                or field_name.lower().endswith("utc")
            )
        }
        return exclude_fields

    def save(self) -> None:
        """
        Save the product to the Channel Advisor API.
        :param copy_to_children: Whether to copy the product to children # THIS DOES NOT WORK
        :param include_fields: A list of fields to include in the save.
            If not provided, all fields except for quantity fields, ids, and utc fields will be included.
        """
        # Get all the fields from the model that we can update
        exclude_fields = self._exluded_save_fields()
        model_data = self.model_dump(by_alias=True, exclude_none=True, exclude=exclude_fields)
        logger.info(f"Saving product {self.id}", model_data=model_data)
        self.client.request("put", f"Products({self.id})", data=model_data)

    def save_to_children(self, include_fields: List[str] = None):
        """
        Save the product to its children.
        :param include_fields: A list of fields to include in the save.
            Field names must be model parameters, not aliases.
            If not provided, all fields except for quantity fields, ids, and utc fields will be included.
        """
        if include_fields:
            model_data = self.model_dump(by_alias=True, exclude_none=True, include=include_fields)
        else:
            model_data = self.model_dump(by_alias=True, exclude_none=True, exclude=self._exluded_save_fields())
        if not model_data:
            raise ValueError("No data to save")
        for child_id in self.child_ids:
            logger.info(
                f"Saving child {child_id} of {self.id} with include_fields: {include_fields}",
                model_data=model_data,
            )
            self.client.request("put", f"Products({child_id})", data=model_data)

    @classmethod
    def get_products_with_label(cls, label: str, limit: int = None) -> List["MinProduct"]:
        # https://api.channeladvisor.com/v1/ProductLabels ?
        # $filter=Name eq 'Shopify' & $select=ProductID
        items = cls.get_client().get_all_pages(f"ProductLabels?$filter=Name eq '{label}'", limit=limit)
        return [cls.model_validate(cls.by_id(item.get("ProductID"))) for item in items]

    @classmethod
    def get_shopify_products(cls, limit: int = None) -> List["MinProduct"]:
        return cls.get_products_with_label("Shopify", limit)

    @property
    def is_shopify(self) -> bool:
        return "Shopify" in self.labels

    @property
    def labels(self) -> List[str]:
        if not self._labels:
            self._labels = []
            labels = MinProduct.get_client().get_all_pages("get", f"Products({self.id})/Labels")
            for label in labels:
                label = label.get("Name")
                self._labels.append(label)
        return self._labels

    @property
    def dc_qtys(self) -> List[dict]:
        if self.total_available_quantity == 0:
            return []
        dc_qtys = self.get_client().get_all_pages(f"Products({self.id})/DCQuantities")
        dc_qtys = filter(lambda x: x.get("AvailableQuantity") > 0, dc_qtys)
        return [
            {
                "dc": ChannelAdvisorDC.by_id(dc_qty.get("DistributionCenterID")).name,
                "qty": dc_qty.get("AvailableQuantity"),
            }
            for dc_qty in dc_qtys
        ]

    @cached_property
    def attributes(self) -> BaseOptimizeAttributes:
        if self.is_parent:
            return ParentOptimizeAttributes.get_attributes_by_id(self.id)
        return ChildOptimizeAttributes.get_attributes_by_id(self.id)

    @property
    def images(self) -> List[str]:
        images = self.get_client().get_all_pages(f"Products({self.id})/Images")
        return [image.get("Url") for image in images]

    @classmethod
    def get_first_image_url(cls, id: str) -> str | None:
        images = cls.get_client().get_all_pages(f"Products({id})/Images", limit=1)
        return images[0].get("Url") if images else None

    @property
    def children(self) -> List["MinProduct"]:
        return self.all(filter=f"ParentProductID eq {self.id} and IsParent ne true")

    @property
    def child_ids(self) -> List[int]:
        # GET https://api.channeladvisor.com/v1/Products(12345678)/Children
        # "value": [ { "ParentProductID": 15623577, "ProfileID": 12345678, "ChildProductID": 25398133 },
        items = self.get_client().get_all_pages(f"{self._base_uri}({self.id})/Children")
        return [item.get("ChildProductID") for item in items]


def get_current_year() -> int:
    # If it is after October, use the next year
    return datetime.now().year if datetime.now().month < 10 else datetime.now().year + 1


class MinProduct(BaseProduct):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="ID", frozen=True, description="Channel Advisor Id")
    sku: Optional[str] = Field(None, alias="Sku", frozen=True)
    title: str = Field(
        alias="Title",
        description="Product title formatting rules: "
        "1) Include apostrophe in Men's/Women's, "
        "2) If Status contains 'NC' (non-current) remove the model year from title , "
        f"3) If Status contains 'CR' (current year) include the current year {get_current_year()} in the title, "
        "4) For Child products use numeric prefix for sizes (2X-Large, 3X-Large, 4X-Large), "
        "5) For Child products inlcude the color in the title if known ",
    )
    subtitle: str = Field(alias="Subtitle", description="Catchy subtitle for SEO")
    brand: Optional[str] = Field(None, alias="Brand", description="Manufacturer. If already provided, do not change.")
    description: Optional[str] = Field(
        None,
        alias="Description",
        # max_length=2000,  # This causes issues with importing existing products
        description="HTML product description: "
        "1) Remove ™, © and ® symbols, "
        "2) Use <br> for line breaks and new lines. Break up long paragraphs into smaller chunks, "
        "3) Preserve formatting like <strong>, <em>, <ul>, <li>, "
        "4) Keep URLs intact, "
        "5) Maintain brand/model name consistency with title"
        "6) Keep length under 2000 characters",
    )
    short_description: Optional[str] = Field(
        None,
        alias="ShortDescription",
        description="Short text only description for SEO."
        "1) Remove ™, © and ® symbols, "
        "2) Do not use any html markup, "
        "3) Do not use any urls, "
        "4) Maintain brand/model name consistency with title"
        "5) Keep length under 150 characters",
        # max_length=300,  # This causes issues with importing existing products
    )
    asin: Optional[str] = Field(
        None,
        alias="ASIN",
        frozen=True,
        description="Amazon Standard Identification Number. If provided, do not change.",
    )
    # TODO create an object for this
    product_type: Optional[str] = Field(
        None, alias="ProductType", frozen=True, description="Parent, Child or Standalone"
    )
    is_parent: Optional[bool] = Field(
        None, alias="IsParent", description="Whether the product is a parent or a child", frozen=True
    )
    is_in_relationship: Optional[bool] = Field(
        None,
        alias="IsInRelationship",
        description="Whether the product is in a parent/child relationship",
        frozen=True,
    )
    parent_product_id: Optional[int] = Field(
        None,
        alias="ParentProductID",
        description="The id of the parent product",
        frozen=True,
    )
    parent_sku: Optional[str] = Field(None, alias="ParentSku", description="The sku of the parent product", frozen=True)
    relationship_name: Optional[str] = Field(None, alias="RelationshipName", frozen=True)
    vary_by: Optional[str] = Field(None, alias="VaryBy", frozen=True)

    _labels: ClassVar[str] = None
    _base_uri: ClassVar[str] = "Products"


class FullProduct(MinProduct):
    retail_price: Optional[float] = Field(None, alias="RetailPrice")
    estimated_shipping_cost: Optional[float] = Field(None, alias="EstimatedShippingCost")
    supplier_po: Optional[str] = Field(None, alias="SupplierPO")
    alias_type: str = Field(alias="AliasType")
    classification: Optional[str] = Field(None, alias="Classification")
    warehouse_location: Optional[str] = Field(None, alias="WarehouseLocation")
    condition: Optional[str] = Field(alias="Condition", description="The condition of the product", frozen=True)
    supplier_name: Optional[str] = Field(None, alias="SupplierName", frozen=True)
    supplier_code: Optional[str] = Field(None, alias="SupplierCode", frozen=True)
    bundle_type: str = Field(alias="BundleType", frozen=True, description="Bundle Type")
    total_available_quantity: int = Field(
        alias="TotalAvailableQuantity", frozen=True, description="The total available quantity of the product"
    )
    total_quantity: int = Field(alias="TotalQuantity", frozen=True, description="The total quantity of the product")
    total_quantity_pooled: int = Field(
        alias="TotalQuantityPooled", frozen=True, description="The total quantity of the product pooled"
    )
    reference_sku: Optional[str] = Field(None, alias="ReferenceSku", frozen=True)
    reference_product_id: Optional[int] = Field(None, alias="ReferenceProductID", frozen=True)
    height: Optional[float] = Field(None, alias="Height")
    length: Optional[float] = Field(None, alias="Length")
    width: Optional[float] = Field(None, alias="Width")
    cost: Optional[float] = Field(None, alias="Cost")
    margin: Optional[float] = Field(None, alias="Margin")
    warranty: Optional[str] = Field(None, alias="Warranty")
    upc: Optional[str] = Field(None, alias="UPC")
    multipack_quantity: Optional[int] = Field(None, alias="MultipackQuantity")
    tax_product_code: Optional[str] = Field(None, alias="TaxProductCode")
    copy_to_children: Optional[bool] = Field(None, alias="CopyToChildren")
    copy_to_aliases: Optional[bool] = Field(None, alias="CopyToAliases")
    manufacturer: Optional[str] = Field(None, alias="Manufacturer")
    mpn: Optional[str] = Field(alias="MPN")
    ean: Optional[str] = Field(None, alias="EAN", description="European Article Number")
    flag_description: Optional[str] = Field(None, alias="FlagDescription")
    flag: str = Field(alias="Flag")
    harmonized_code: Optional[str] = Field(alias="HarmonizedCode")
    isbn: Optional[str] = Field(alias="ISBN")
    profile_id: int = Field(alias="ProfileID")
    is_external_quantity_blocked: bool = Field(alias="IsExternalQuantityBlocked")
    infinite_quantity: bool = Field(alias="InfiniteQuantity")
    block_comment: Optional[str] = Field(None, alias="BlockComment")
    starting_price: Optional[float] = Field(None, alias="StartingPrice")
    reserve_price: Optional[float] = Field(None, alias="ReservePrice")
    buy_it_now_price: Optional[float] = Field(None, alias="BuyItNowPrice")
    store_price: Optional[float] = Field(None, alias="StorePrice")
    weight: Optional[float] = Field(None, alias="Weight")
    second_chance_price: Optional[float] = Field(None, alias="SecondChancePrice")
    min_price: Optional[float] = Field(None, alias="MinPrice")
    max_price: Optional[float] = Field(None, alias="MaxPrice")
    is_display_in_store: bool = Field(alias="IsDisplayInStore")
    store_title: Optional[str] = Field(None, alias="StoreTitle")
    store_description: Optional[str] = Field(None, alias="StoreDescription")
    open_allocated_quantity: int = Field(alias="OpenAllocatedQuantity")
    open_allocated_quantity_pooled: int = Field(alias="OpenAllocatedQuantityPooled")
    pending_checkout_quantity: int = Field(alias="PendingCheckoutQuantity")
    pending_checkout_quantity_pooled: int = Field(alias="PendingCheckoutQuantityPooled")
    pending_payment_quantity: int = Field(alias="PendingPaymentQuantity")
    pending_payment_quantity_pooled: int = Field(alias="PendingPaymentQuantityPooled")
    pending_shipment_quantity: int = Field(alias="PendingShipmentQuantity")
    pending_shipment_quantity_pooled: int = Field(alias="PendingShipmentQuantityPooled")
    create_date_utc: datetime = Field(
        alias="CreateDateUtc", frozen=True, description="The date the product was created"
    )
    update_date_utc: datetime = Field(
        alias="UpdateDateUtc", frozen=True, description="The date the product was last updated"
    )
    quantity_update_date_utc: datetime = Field(
        alias="QuantityUpdateDateUtc", frozen=True, description="The date the product quantity was last updated"
    )
    is_available_in_store: bool = Field(
        alias="IsAvailableInStore", description="Whether the product is available in store"
    )
    is_blocked: bool = Field(alias="IsBlocked", description="Whether the product is blocked")
    is_blocked_from_advertising: bool = Field(
        alias="IsBlockedFromAdvertising", description="Whether the product is blocked from advertising"
    )
    quantity_sold_last_7_days: Optional[int] = Field(
        None, alias="QuantitySoldLast7Days", frozen=True, description="The quantity sold in the last 7 days"
    )
    quantity_sold_last_14_days: Optional[int] = Field(
        None, alias="QuantitySoldLast14Days", frozen=True, description="The quantity sold in the last 14 days"
    )
    quantity_sold_last_30_days: Optional[int] = Field(
        None, alias="QuantitySoldLast30Days", frozen=True, description="The quantity sold in the last 30 days"
    )
    quantity_sold_last_60_days: Optional[int] = Field(
        None, alias="QuantitySoldLast60Days", frozen=True, description="The quantity sold in the last 60 days"
    )
    quantity_sold_last_90_days: Optional[int] = Field(
        None, alias="QuantitySoldLast90Days", frozen=True, description="The quantity sold in the last 90 days"
    )
    blocked_date_utc: Optional[datetime] = Field(
        None, alias="BlockedDateUtc", frozen=True, description="The date the product was blocked"
    )
    blocked_from_advertising_date_utc: Optional[datetime] = Field(
        None,
        alias="BlockedFromAdvertisingDateUtc",
        frozen=True,
        description="The date the product was blocked from advertising",
    )
    received_date_utc: Optional[datetime] = Field(
        None, alias="ReceivedDateUtc", frozen=True, description="The date the product was received"
    )
    last_sale_date_utc: Optional[datetime] = Field(
        None, alias="LastSaleDateUtc", frozen=True, description="The date the product was last sold"
    )

    @classmethod
    def get_property_names(cls, as_param: bool = False) -> List[str] | dict:
        # Get the Alias names for all of the properties in the model
        fields = [field.alias for field in cls.model_fields.values()]
        if as_param:
            return {}  # forces all fields to be returned. Api errors if all fields are requesed in select
        return fields
