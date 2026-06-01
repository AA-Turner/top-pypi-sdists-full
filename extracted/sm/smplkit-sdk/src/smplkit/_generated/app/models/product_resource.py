from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.product_resource_type import check_product_resource_type
from ..models.product_resource_type import ProductResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.product import Product


T = TypeVar("T", bound="ProductResource")


@_attrs_define
class ProductResource:
    """JSON:API resource envelope for a product catalog entry.

    Example:
        {'attributes': {'coming_soon': False, 'description': 'Feature flag management', 'display_name': 'Smpl Flags',
            'features': ['Targeted rollouts', 'Experiment toggles', 'Environment controls'], 'limits': {'flags':
            {'description': 'Maximum number of feature flags', 'display_name': 'Feature Flags', 'unit': 'flags'}}, 'plans':
            {'free': {'limits': {'flags': 10}, 'price_monthly_cents': 0}, 'pro': {'limits': {'flags': -1},
            'price_monthly_cents': 2900}}, 'tagline': 'Feature flag delivery for safer rollouts and controlled
            experiments.'}, 'id': 'flags', 'type': 'product'}

    Attributes:
        type_ (ProductResourceType):
        attributes (Product): A smplkit product, with its plans, metered limits, and marketing copy.
        id (None | str | Unset):
    """

    type_: ProductResourceType
    attributes: Product
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product import Product

        d = dict(src_dict)
        type_ = check_product_resource_type(d.pop("type"))

        attributes = Product.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        product_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        product_resource.additional_properties = d
        return product_resource

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
