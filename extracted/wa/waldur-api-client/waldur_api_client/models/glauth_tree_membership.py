from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.glauth_group_kind import GlauthGroupKind

T = TypeVar("T", bound="GlauthTreeMembership")


@_attrs_define
class GlauthTreeMembership:
    """
    Attributes:
        gid (int):
        group_name (str):
        kind (GlauthGroupKind):
        role (Union[None, str]):
    """

    gid: int
    group_name: str
    kind: GlauthGroupKind
    role: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gid = self.gid

        group_name = self.group_name

        kind = self.kind.value

        role: Union[None, str]
        role = self.role

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gid": gid,
                "group_name": group_name,
                "kind": kind,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        gid = d.pop("gid")

        group_name = d.pop("group_name")

        kind = GlauthGroupKind(d.pop("kind"))

        def _parse_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role = _parse_role(d.pop("role"))

        glauth_tree_membership = cls(
            gid=gid,
            group_name=group_name,
            kind=kind,
            role=role,
        )

        glauth_tree_membership.additional_properties = d
        return glauth_tree_membership

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
