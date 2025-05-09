# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from .order_line_item_discount_type import OrderLineItemDiscountType
from .money import Money
from .order_line_item_discount_scope import OrderLineItemDiscountScope
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class OrderReturnDiscount(UncheckedBaseModel):
    """
    Represents a discount being returned that applies to one or more return line items in an
    order.

    Fixed-amount, order-scoped discounts are distributed across all non-zero return line item totals.
    The amount distributed to each return line item is relative to that item’s contribution to the
    order subtotal.
    """

    uid: typing.Optional[str] = pydantic.Field(default=None)
    """
    A unique ID that identifies the returned discount only within this order.
    """

    source_discount_uid: typing.Optional[str] = pydantic.Field(default=None)
    """
    The discount `uid` from the order that contains the original application of this discount.
    """

    catalog_object_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    The catalog object ID referencing [CatalogDiscount](entity:CatalogDiscount).
    """

    catalog_version: typing.Optional[int] = pydantic.Field(default=None)
    """
    The version of the catalog object that this discount references.
    """

    name: typing.Optional[str] = pydantic.Field(default=None)
    """
    The discount's name.
    """

    type: typing.Optional[OrderLineItemDiscountType] = pydantic.Field(default=None)
    """
    The type of the discount. If it is created by the API, it is `FIXED_PERCENTAGE` or `FIXED_AMOUNT`.
    
    Discounts that do not reference a catalog object ID must have a type of
    `FIXED_PERCENTAGE` or `FIXED_AMOUNT`.
    See [OrderLineItemDiscountType](#type-orderlineitemdiscounttype) for possible values
    """

    percentage: typing.Optional[str] = pydantic.Field(default=None)
    """
    The percentage of the tax, as a string representation of a decimal number.
    A value of `"7.25"` corresponds to a percentage of 7.25%.
    
    `percentage` is not set for amount-based discounts.
    """

    amount_money: typing.Optional[Money] = pydantic.Field(default=None)
    """
    The total declared monetary amount of the discount.
    
    `amount_money` is not set for percentage-based discounts.
    """

    applied_money: typing.Optional[Money] = pydantic.Field(default=None)
    """
    The amount of discount actually applied to this line item. When an amount-based
    discount is at the order level, this value is different from `amount_money` because the discount
    is distributed across the line items.
    """

    scope: typing.Optional[OrderLineItemDiscountScope] = pydantic.Field(default=None)
    """
    Indicates the level at which the `OrderReturnDiscount` applies. For `ORDER` scoped
    discounts, the server generates references in `applied_discounts` on all
    `OrderReturnLineItem`s. For `LINE_ITEM` scoped discounts, the discount is only applied to
    `OrderReturnLineItem`s with references in their `applied_discounts` field.
    See [OrderLineItemDiscountScope](#type-orderlineitemdiscountscope) for possible values
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
