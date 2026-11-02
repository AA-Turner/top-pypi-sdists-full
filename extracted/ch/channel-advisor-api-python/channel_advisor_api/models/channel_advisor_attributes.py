from abc import ABC
from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
from functools import cached_property
from enum import StrEnum

from channel_advisor_api.models.channel_advisor_client import ChannelAdvisorClient
from channel_advisor_api.utils.logger import get_logger

logger = get_logger(__name__)


class BaseAttr(StrEnum):
    @property
    def description(self) -> str:
        """Returns the description if set, otherwise returns the value."""
        return getattr(self, "_description_", self.value)

    def __new__(cls, value: str, description: str = None):
        obj = str.__new__(cls, value)
        obj._value_ = value
        if description:
            obj._description_ = description
        return obj


class ProductTypes(BaseAttr):
    PROTECTIVE_GEAR = ("ProtectiveGear", "This is the default for most product. Anything wearable for a rider.")
    AUTO_ACCESSORY_MISC = ("AutoAccessoryMisc", "Anything that is not a motorcycle part or a powersports part.")
    POWERSPORTS_PART = ("PowersportsPart", "Anything that is a part for a powersports vehicle.")
    MOTORCYCLE_PART = ("Motorcyclepart", "Anything that is a part for a motorcycle.")


class ColorMaps(BaseAttr):
    AQUA = "Aqua"
    BEIGE = "Beige"
    BLACK = "Black"
    BLUE = "Blue"
    BRONZE = "Bronze"
    FUCHSIA = "Fuchsia"
    GOLD = "Gold"
    GRAY = "Gray"
    GREEN = "Green"
    LIME = "Lime"
    MAROON = "Maroon"
    MULTICOLORED = "Multicolored"
    NAVY = "Navy"
    BROWN = "Brown"
    NUDE = "Nude"
    OLIVE = "Olive"
    ORANGE = "Orange"
    PINK = "Pink"
    PURPLE = "Purple"
    RED = "Red"
    ROSE = "Rose"
    SILVER = "Silver"
    TEAL = "Teal"
    TRANSPARENT = "Transparent"
    VIOLET = "Violet"
    WHITE = "White"
    YELLOW = "Yellow"
    UNPAINTED = "Unpainted"


class Departments(BaseAttr):
    UNISEX_ADULT = "unisex-adult"
    MENS = "mens"
    WOMENS = "womens"
    UNISEX_CHILD = "unisex-child"


class ItemTypes(BaseAttr):
    PROTECTIVE_JACKETS = "powersports-protective-jackets"
    PROTECTIVE_PANTS = "powersports-protective-pants"
    PROTECTIVE_GEAR = "powersports-protective-gear"
    BASE_LAYER_TOPS = "powersports-base-layer-tops"
    BASE_LAYER_BOTTOMS = "powersports-base-layer-bottoms"
    HELMETS = "powersports-helmets"
    GOGGLES = "powersports-goggles"
    JERSEYS = "powersports-jerseys"
    GLOVES = "powersports-gloves"
    BOOTS = "powersports-boots"
    SOCKS = "powersports-socks"
    HELMET_COMM_DEVICES = "powersports-helmet-communication-devices"
    HELMET_FACE_SHIELDS = "powersports-helmet-face-shields"
    RACING_SUITS = "powersports-racing-suits"
    BACKPACKS = "powersports-backpacks"
    GEAR_BAGS = "powersports-gear-bags"
    PROTECTIVE_FACE_MASKS = "powersports-protective-face-masks"
    HELMET_BAGS = "powersports-helmet-bags"


class Sizes(BaseAttr):
    ONE_SIZE = "One Size"
    XXXXX_SMALL = "XXXXX-Small"
    XXXX_SMALL = "XXXX-Small"
    XXX_SMALL = "XXX-Small"
    XX_SMALL = "XX-Small"
    X_SMALL = "X-Small"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    X_LARGE = "X-Large"
    XX_LARGE = "XX-Large"
    XXX_LARGE = "XXX-Large"
    XXXX_LARGE = "XXXX-Large"
    XXXXX_LARGE = "XXXXX-Large"


class SizesAbbreviations(BaseAttr):
    OS = ("OS", "One Size")
    MDSH = ("MDSH", "Medium Short")
    LGSH = ("LGSH", "Large Short")
    XLSH = ("XLSH", "Xtra Large Short")
    TWO_XSH = ("2XSH", "2X Short")
    THREE_XSH = ("3XSH", "3X Short")
    FOUR_XSH = ("4XSH", "4X Short")
    FIVE_XSH = ("5XSH", "5X Short")
    FIVE_XS = ("5XS", "5X Small")
    FOUR_XS = ("4XS", "4X Small")
    THREE_XS = ("3XS", "3X Small")
    TWO_XS = ("2XS", "2X Small")
    XS = ("XS", "X Small")
    SM = ("SM", "Small")
    MD = ("MD", "Medium")
    LG = ("LG", "Large")
    XL = ("XL", "Xtra Large")
    TWO_X = ("2X", "2X")
    THREE_X = ("3X", "3X")
    FOUR_X = ("4X", "4X")
    FIVE_X = ("5X", "5X")
    MDTL = ("MDTL", "Medium Tall")
    LGTL = ("LGTL", "Large Tall")
    XLTL = ("XLTL", "Xtra Large Tall")
    TWO_XTL = ("2XTL", "2X Tall")
    THREE_XTL = ("3XTL", "3X Tall")
    FOUR_XTL = ("4XTL", "4X Tall")
    FIVE_XTL = ("5XTL", "5X Tall")


class SizeMaps(BaseAttr):
    XXXXX_SMALL = "XXXXX-Small"
    XXXX_SMALL = "XXXX-Small"
    XXX_SMALL = "XXX-Small"
    XX_SMALL = "XX-Small"
    X_SMALL = "X-Small"
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    X_LARGE = "X-Large"
    XX_LARGE = "XX-Large"
    XXX_LARGE = "XXX-Large"
    XXXX_LARGE = "XXXX-Large"
    XXXXX_LARGE = "XXXXX-Large"
    XXXXXX_LARGE = "XXXXXX-Large"


class StyleKeywords(BaseAttr):
    ALL_WEATHER = "all-weather"


class OptimizedProductStatus(BaseAttr):
    MIN_LOADED = "1 - Min Loaded"
    PARENT_CHILD = "2 - Parent Child"
    BASICS = "3 - Basics"
    OPTIMIZED = "4 - Optimized"
    PUSHED = "5 - Pushed"
    LISTED = "6 - Listed"


class OptimizedPicturesStatus(BaseAttr):
    YES = ("Yes", "Product images have been optimized for Amazon")
    NO = ("No", "Product images have not been optimized for Amazon")


class BaseAttributes(ABC, BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        # extra="allow",  # if this is "allow" we'll allow any attribute. If not, we will only work with the below attrs
    )
    product_id: int = Field(
        # exclude=True,  # We dont want to try and save this field back to Channel Advisor
        frozen=True,
        description="The product id of the product to which thses attribute belong",
    )

    @classmethod
    def _get_client(cls) -> ChannelAdvisorClient:
        """Get a client instance for class methods."""
        return ChannelAdvisorClient()

    @cached_property
    def client(self) -> ChannelAdvisorClient:
        """Get a cached client instance for instance methods."""
        return self._get_client()

    @classmethod
    def get_attributes_by_id(cls, product_id: int) -> "BaseAttributes":
        value_dict = {}
        values = cls._get_client().get_all_pages(f"Products({product_id})/Attributes")
        for value in values:
            value_dict[value.get("Name")] = value.get("Value")
        return cls.model_validate({**value_dict, "product_id": product_id})

    @classmethod
    def update_attributes(cls, product_id: int, data: dict) -> None:
        client = cls._get_client()  # Use the class method to get client
        logger.info(
            f"update_attributes() updating {len(data['Value']['Attributes'])} attrs for product {product_id}",
            extra={"attributes": data["Value"]["Attributes"]},
        )
        client.request("POST", f"Products({product_id})/UpdateAttributes", data=data)

    @classmethod
    def delete_attributes(cls, product_id: int, attrs: list[str]) -> None:
        client = cls._get_client()  # Use the class method to get client
        for attr in attrs:
            logger.info(
                f"update_attributes() received None value for '{attr}' product {product_id}. Deleting attribute."
            )
            client.request("DELETE", f"Products({product_id})/Attributes('{attr}')")

    @classmethod
    def save_to_id(
        cls, attributes: "BaseOptimizeAttributes", product_id: int, include_fields: list[str] = None
    ) -> None:
        # Build the data to send to the API and the delete list without regard to include_fields
        post_data = {"Value": {"Attributes": []}}
        delete_fields = []
        if include_fields:
            model_data = attributes.model_dump(by_alias=True, include=include_fields)
        else:
            model_data = attributes.model_dump(by_alias=True, exclude="product_id")
        for key, value in model_data.items():
            if value is None or value == "":
                delete_fields.append(key)
            else:
                post_data["Value"]["Attributes"].append({"Name": key, "Value": str(value)})

        # Save the attributes
        cls.delete_attributes(product_id, delete_fields)
        cls.update_attributes(product_id, post_data)

    def save(self) -> None:
        self.save_to_id(self, self.product_id)

    def save_to_children(self, include_fields: list[str] = None) -> None:
        items = self.client.get_all_pages(f"Products({self.product_id})/Children")
        child_ids = [item.get("ChildProductID") for item in items]
        for child_id in child_ids:
            self.save_to_id(self, child_id, include_fields=include_fields)


class AllAttributes(BaseAttributes):
    """Wide open attributes list"""

    model_config = ConfigDict(
        extra="allow",  # if this is "allow" we'll allow any attribute. If not, we will only work with the below attrs
    )


class BaseOptimizeAttributes(BaseAttributes):
    product_id: int = Field(
        # exclude=True,  # We dont want to try and save this field back to Channel Advisor
        frozen=True,
        description="The product id of the product to which thses attribute belong",
    )
    AMZ_Category: Optional[str] = Field(
        default="Automotive",
        description="The Amazon category for the product. Shoudld ALWAYS be 'Automotive'",
        examples=["Automotive"],
        frozen=True,
    )
    AmzProductType: Optional[str | ProductTypes] = Field(
        default=None,
        description="The Amazon product type for the product",
    )
    Bullet_01: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Point  for listing.",
    )
    Bullet_02: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Point 2 for listing.",
    )
    Bullet_03: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Point 3 for listing.",
    )
    Bullet_04: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Point 4 for listing.",
    )
    Bullet_05: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Point 5 for listing.",
    )
    Department: Optional[str | Departments] = Field(default=None, description="The department of the product")
    ItemType: Optional[str | ItemTypes] = Field(
        default=None,
        max_length=50,
        description="Item type of the product",
    )
    Model: Optional[str] = Field(default=None, max_length=50, description="Model of the product")
    Search_1: Optional[str] = Field(default=None, max_length=50, description="search term 1")
    Search_2: Optional[str] = Field(default=None, max_length=50, description="search term 2")
    Search_3: Optional[str] = Field(default=None, max_length=50, description="search term 3")
    Search_4: Optional[str] = Field(default=None, max_length=50, description="search term 4")
    Search_5: Optional[str] = Field(
        default=None, max_length=50, description="search term 5. Should always be the product sku"
    )
    Inner_Material_Type: Optional[str] = Field(
        default=None,
        description="The inner material type of the product",
        examples=["Nylon", "Polyester"],
    )
    Material_Composition: Optional[str] = Field(
        default=None,
        description="The material composition of the product",
        examples=["Nylon", "Polyester"],
    )
    Outer_Material_Type: Optional[str] = Field(
        default=None,
        description="The outer material type of the product",
        examples=["Nylon", "Polyester"],
    )
    eBay_Condition: Optional[str | Literal["New", "Used"]] = Field(
        default=None,
        description="The eBay condition of the product",
        alias="eBay Condition",
        examples=["New", "Used"],
    )
    shopify_category: Optional[str] = Field(
        default=None,
        description="The Shopify category of the product",
        examples=["Automotive"],
    )
    shopify_tag: Optional[str] = Field(
        default=None,
        description="The Shopify tag of the product. Should be a comman separated string like",
        examples=["Riding Gear,Helmets"],
    )
    Optimized_Process: Optional[str | OptimizedProductStatus] = Field(
        default=None,
        description="Status of the optimized process. Always set to `4 - Optimized`",
        alias="Optimized Process",
    )
    Optimized_Pictures: Optional[str | OptimizedPicturesStatus] = Field(
        default=None, description="Status of the optimized pictures", alias="Optimized Pictures"
    )
    Optimized_Attributes: Optional[str | Literal["Yes", "No"]] = Field(
        default=None, description="Status of the optimized attributes", alias="Optimized Attributes"
    )
    Status: Optional[str] = Field(default=None, description="Status of the product")


class ParentOptimizeAttributes(BaseOptimizeAttributes):
    """Attributes that should only be set on parent products"""


class ChildOptimizeAttributes(BaseOptimizeAttributes):
    """Attributes that should only be set on child products"""

    Color: Optional[str] = Field(default=None, max_length=50, description="Product color. Dont guess")
    Colormap: Optional[str | ColorMaps] = Field(
        default=None,
        description="Colormap of product. Dont guess. Parent products should not have a colormap.",
    )
    Size: Optional[str | Sizes] = Field(
        default=None, description="Product size. May be a integer or a size abbreviation of type Sizes. "
    )
    Size_Abbreviation: Optional[str | SizesAbbreviations] = Field(
        default=None,
        description="The size abbreviation of the product. Parent products should not have a size abbreviation.",
        alias="Size Abbreviation",
    )
    Sizemap: Optional[str | SizeMaps] = Field(
        default=None, description="The sizemap of the product. Parent products should not have a sizemap."
    )
    Style_Keywords: Optional[str | StyleKeywords] = Field(
        default=None,
        description="The style keywords of the product",
        alias="Style Keywords",
        examples=["all-weather"],
    )
