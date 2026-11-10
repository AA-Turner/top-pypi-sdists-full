import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.chart_spec import ChartSpec
    from ..models.hpc_component_usage import HpcComponentUsage


T = TypeVar("T", bound="HpcAllocationUsage")


@_attrs_define
class HpcAllocationUsage:
    """
    Attributes:
        as_of (datetime.date):
        components (list['HpcComponentUsage']):
        charts (list['ChartSpec']):
    """

    as_of: datetime.date
    components: list["HpcComponentUsage"]
    charts: list["ChartSpec"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        as_of = self.as_of.isoformat()

        components = []
        for components_item_data in self.components:
            components_item = components_item_data.to_dict()
            components.append(components_item)

        charts = []
        for charts_item_data in self.charts:
            charts_item = charts_item_data.to_dict()
            charts.append(charts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "as_of": as_of,
                "components": components,
                "charts": charts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chart_spec import ChartSpec
        from ..models.hpc_component_usage import HpcComponentUsage

        d = dict(src_dict)
        as_of = isoparse(d.pop("as_of")).date()

        components = []
        _components = d.pop("components")
        for components_item_data in _components:
            components_item = HpcComponentUsage.from_dict(components_item_data)

            components.append(components_item)

        charts = []
        _charts = d.pop("charts")
        for charts_item_data in _charts:
            charts_item = ChartSpec.from_dict(charts_item_data)

            charts.append(charts_item)

        hpc_allocation_usage = cls(
            as_of=as_of,
            components=components,
            charts=charts,
        )

        hpc_allocation_usage.additional_properties = d
        return hpc_allocation_usage

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
