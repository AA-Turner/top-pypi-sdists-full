from typing import Literal, cast

ProductResourceType = Literal["product"]

PRODUCT_RESOURCE_TYPE_VALUES: set[ProductResourceType] = {
    "product",
}


def check_product_resource_type(value: str) -> ProductResourceType:
    if value in PRODUCT_RESOURCE_TYPE_VALUES:
        return cast(ProductResourceType, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {PRODUCT_RESOURCE_TYPE_VALUES!r}")
