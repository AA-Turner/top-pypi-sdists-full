from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AlertFilters")


@_attrs_define
class AlertFilters:
    """Filters applied to this alert

    Attributes:
        script_ids (list[UUID] | None | Unset): Optional list of script/pipeline IDs to filter this alert to. If null or
            empty, fires for all scripts in the workspace.
    """

    script_ids: list[UUID] | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        script_ids: list[str] | None | Unset
        if isinstance(self.script_ids, Unset):
            script_ids = UNSET
        elif isinstance(self.script_ids, list):
            script_ids = []
            for script_ids_type_0_item_data in self.script_ids:
                script_ids_type_0_item = str(script_ids_type_0_item_data)
                script_ids.append(script_ids_type_0_item)

        else:
            script_ids = self.script_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if script_ids is not UNSET:
            field_dict["script_ids"] = script_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_script_ids(data: object) -> list[UUID] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                script_ids_type_0 = []
                _script_ids_type_0 = data
                for script_ids_type_0_item_data in _script_ids_type_0:
                    script_ids_type_0_item = UUID(script_ids_type_0_item_data)

                    script_ids_type_0.append(script_ids_type_0_item)

                return script_ids_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[UUID] | None | Unset, data)

        script_ids = _parse_script_ids(d.pop("script_ids", UNSET))

        alert_filters = cls(
            script_ids=script_ids,
        )

        alert_filters.additional_properties = d
        return alert_filters

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
