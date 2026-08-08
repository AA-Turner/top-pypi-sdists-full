from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.variable_upsert import VariableUpsert


T = TypeVar("T", bound="VariablesChange")


@_attrs_define
class VariablesChange:
    """
    Attributes:
        profile (None | str): Scope to change; `null` targets the workspace-wide scope
        deletes (list[str] | Unset): Variable names to remove
        upserts (list[VariableUpsert] | Unset): Variables to create or update
    """

    profile: None | str
    deletes: list[str] | Unset = UNSET
    upserts: list[VariableUpsert] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        profile: None | str
        profile = self.profile

        deletes: list[str] | Unset = UNSET
        if not isinstance(self.deletes, Unset):
            deletes = self.deletes

        upserts: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.upserts, Unset):
            upserts = []
            for upserts_item_data in self.upserts:
                upserts_item = upserts_item_data.to_dict()
                upserts.append(upserts_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
            }
        )
        if deletes is not UNSET:
            field_dict["deletes"] = deletes
        if upserts is not UNSET:
            field_dict["upserts"] = upserts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.variable_upsert import VariableUpsert

        d = dict(src_dict)

        def _parse_profile(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profile = _parse_profile(d.pop("profile"))

        deletes = cast(list[str], d.pop("deletes", UNSET))

        _upserts = d.pop("upserts", UNSET)
        upserts: list[VariableUpsert] | Unset = UNSET
        if _upserts is not UNSET:
            upserts = []
            for upserts_item_data in _upserts:
                upserts_item = VariableUpsert.from_dict(upserts_item_data)

                upserts.append(upserts_item)

        variables_change = cls(
            profile=profile,
            deletes=deletes,
            upserts=upserts,
        )

        variables_change.additional_properties = d
        return variables_change

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
