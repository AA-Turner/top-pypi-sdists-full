from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_checkpoint_request_kind import CreateCheckpointRequestKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCheckpointRequest")


@_attrs_define
class CreateCheckpointRequest:
    """Checkpoint creation request.

    Attributes:
        kind (CreateCheckpointRequestKind | Unset): live (also accepted: full) stores the disk, guest memory, and
            running processes, so restore keeps CPU and memory fixed. cold stores only the disk of a shut-down runtime, so
            restore can rechoose CPU and memory. Default: CreateCheckpointRequestKind.FULL.
        name (None | str | Unset): Human-readable checkpoint name.
    """

    kind: CreateCheckpointRequestKind | Unset = CreateCheckpointRequestKind.FULL
    name: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        name: None | str | Unset
        if isinstance(self.name, Unset):
            name = UNSET
        else:
            name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if kind is not UNSET:
            field_dict["kind"] = kind
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _kind = d.pop("kind", UNSET)
        kind: CreateCheckpointRequestKind | Unset
        if isinstance(_kind, Unset):
            kind = UNSET
        else:
            kind = CreateCheckpointRequestKind(_kind)

        def _parse_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        name = _parse_name(d.pop("name", UNSET))

        create_checkpoint_request = cls(
            kind=kind,
            name=name,
        )

        create_checkpoint_request.additional_properties = d
        return create_checkpoint_request

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
