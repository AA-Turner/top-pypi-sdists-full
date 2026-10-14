from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.plan_billing_mode import PlanBillingMode
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.export_plan_component_data import ExportPlanComponentData


T = TypeVar("T", bound="ExportPlanData")


@_attrs_define
class ExportPlanData:
    """
    Attributes:
        name (str):
        description (str):
        unit_price (float):
        unit (str):
        archived (bool):
        max_amount (Union[None, int]):
        article_code (str):
        backend_id (str):
        components (list['ExportPlanComponentData']):
        billing_mode (Union[Unset, PlanBillingMode]):  Default: PlanBillingMode.INHERIT.
    """

    name: str
    description: str
    unit_price: float
    unit: str
    archived: bool
    max_amount: Union[None, int]
    article_code: str
    backend_id: str
    components: list["ExportPlanComponentData"]
    billing_mode: Union[Unset, PlanBillingMode] = PlanBillingMode.INHERIT
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        unit_price = self.unit_price

        unit = self.unit

        archived = self.archived

        max_amount: Union[None, int]
        max_amount = self.max_amount

        article_code = self.article_code

        backend_id = self.backend_id

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        billing_mode: Union[Unset, str] = UNSET
        if not isinstance(self.billing_mode, Unset):
            billing_mode = self.billing_mode.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "unit_price": unit_price,
                "unit": unit,
                "archived": archived,
                "max_amount": max_amount,
                "article_code": article_code,
                "backend_id": backend_id,
                "components": components,
            }
        )
        if billing_mode is not UNSET:
            field_dict["billing_mode"] = billing_mode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.export_plan_component_data import ExportPlanComponentData

        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        unit_price = d.pop("unit_price")

        unit = d.pop("unit")

        archived = d.pop("archived")

        def _parse_max_amount(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        max_amount = _parse_max_amount(d.pop("max_amount"))

        article_code = d.pop("article_code")

        backend_id = d.pop("backend_id")

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = ExportPlanComponentData.from_dict(components_item_data)

            components.append(components_item)

        _billing_mode = d.pop("billing_mode", UNSET)
        billing_mode: Union[Unset, PlanBillingMode]
        if isinstance(_billing_mode, Unset):
            billing_mode = UNSET
        else:
            billing_mode = PlanBillingMode(_billing_mode)

        export_plan_data = cls(
            name=name,
            description=description,
            unit_price=unit_price,
            unit=unit,
            archived=archived,
            max_amount=max_amount,
            article_code=article_code,
            backend_id=backend_id,
            components=components,
            billing_mode=billing_mode,
        )

        export_plan_data.additional_properties = d
        return export_plan_data

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
