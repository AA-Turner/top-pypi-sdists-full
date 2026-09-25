from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alert_filters import AlertFilters


T = TypeVar("T", bound="AlertUpsertRequest")


@_attrs_define
class AlertUpsertRequest:
    """
    Attributes:
        filters (AlertFilters | Unset): Filters applied to this alert
    """

    filters: AlertFilters | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        filters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.alert_filters import AlertFilters

        d = dict(src_dict)
        _filters = d.pop("filters", UNSET)
        filters: AlertFilters | Unset
        if isinstance(_filters, Unset):
            filters = UNSET
        else:
            filters = AlertFilters.from_dict(_filters)

        alert_upsert_request = cls(
            filters=filters,
        )

        alert_upsert_request.additional_properties = d
        return alert_upsert_request

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
