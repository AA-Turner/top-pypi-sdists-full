from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.glauth_group_kind import GlauthGroupKind

if TYPE_CHECKING:
    from ..models.glauth_tree_scope import GlauthTreeScope


T = TypeVar("T", bound="GlauthTreeGroup")


@_attrs_define
class GlauthTreeGroup:
    """
    Attributes:
        gid (int):
        name (str):
        kind (GlauthGroupKind):
        scope (GlauthTreeScope):
        role (Union[None, str]):
        members (list[str]):
    """

    gid: int
    name: str
    kind: GlauthGroupKind
    scope: "GlauthTreeScope"
    role: Union[None, str]
    members: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        gid = self.gid

        name = self.name

        kind = self.kind.value

        scope = self.scope.to_dict()

        role: Union[None, str]
        role = self.role

        members = self.members

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "gid": gid,
                "name": name,
                "kind": kind,
                "scope": scope,
                "role": role,
                "members": members,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.glauth_tree_scope import GlauthTreeScope

        d = dict(src_dict)
        gid = d.pop("gid")

        name = d.pop("name")

        kind = GlauthGroupKind(d.pop("kind"))

        scope = GlauthTreeScope.from_dict(d.pop("scope"))

        def _parse_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role = _parse_role(d.pop("role"))

        members = cast(list[str], d.pop("members"))

        glauth_tree_group = cls(
            gid=gid,
            name=name,
            kind=kind,
            scope=scope,
            role=role,
            members=members,
        )

        glauth_tree_group.additional_properties = d
        return glauth_tree_group

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
