from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.product_limits import ProductLimits
    from ..models.product_plans import ProductPlans


T = TypeVar("T", bound="Product")


@_attrs_define
class Product:
    """A smplkit product, with its plans, metered limits, and marketing copy.

    Attributes:
        display_name (str): Human-readable product name.
        description (str): Long-form product description.
        limits (ProductLimits): Map of limit key to limit definition for this product.
        plans (ProductPlans): Map of plan key to plan definition for this product.
        tagline (None | str | Unset): Short marketing tagline shown on plan-selection surfaces.
        features (list[str] | Unset): Bullet-list feature highlights for the product.
        coming_soon (bool | Unset): When `true`, the product is listed but not yet available for subscription. Default:
            False.
    """

    display_name: str
    description: str
    limits: ProductLimits
    plans: ProductPlans
    tagline: None | str | Unset = UNSET
    features: list[str] | Unset = UNSET
    coming_soon: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        description = self.description

        limits = self.limits.to_dict()

        plans = self.plans.to_dict()

        tagline: None | str | Unset
        if isinstance(self.tagline, Unset):
            tagline = UNSET
        else:
            tagline = self.tagline

        features: list[str] | Unset = UNSET
        if not isinstance(self.features, Unset):
            features = self.features

        coming_soon = self.coming_soon

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_name": display_name,
                "description": description,
                "limits": limits,
                "plans": plans,
            }
        )
        if tagline is not UNSET:
            field_dict["tagline"] = tagline
        if features is not UNSET:
            field_dict["features"] = features
        if coming_soon is not UNSET:
            field_dict["coming_soon"] = coming_soon

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.product_limits import ProductLimits
        from ..models.product_plans import ProductPlans

        d = dict(src_dict)
        display_name = d.pop("display_name")

        description = d.pop("description")

        limits = ProductLimits.from_dict(d.pop("limits"))

        plans = ProductPlans.from_dict(d.pop("plans"))

        def _parse_tagline(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        tagline = _parse_tagline(d.pop("tagline", UNSET))

        features = cast(list[str], d.pop("features", UNSET))

        coming_soon = d.pop("coming_soon", UNSET)

        product = cls(
            display_name=display_name,
            description=description,
            limits=limits,
            plans=plans,
            tagline=tagline,
            features=features,
            coming_soon=coming_soon,
        )

        product.additional_properties = d
        return product

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
