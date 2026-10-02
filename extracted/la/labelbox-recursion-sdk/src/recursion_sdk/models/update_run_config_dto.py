from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateRunConfigDto")



@_attrs_define
class UpdateRunConfigDto:
    """ Patch-style update body for run-config identity-level metadata. Omitted fields are left unchanged.

        Example:
            {'name': 'claude-sonnet-baseline', 'description': 'Baseline Claude Sonnet solver harness for the vision-agent-
                eval environment.'}

        Attributes:
            name (str | Unset): New display name. Omit to leave unchanged.
            description (None | str | Unset): New description. Send null to clear; omit to leave unchanged.
            tags (list[str] | Unset): New full tag list (replaces the existing tags). Omit to leave unchanged.
     """

    name: str | Unset = UNSET
    description: None | str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        tags = cast(list[str], d.pop("tags", UNSET))


        update_run_config_dto = cls(
            name=name,
            description=description,
            tags=tags,
        )


        update_run_config_dto.additional_properties = d
        return update_run_config_dto

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
