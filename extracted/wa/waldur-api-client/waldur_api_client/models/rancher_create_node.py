from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.rancher_node_role_enum import RancherNodeRoleEnum

T = TypeVar("T", bound="RancherCreateNode")


@_attrs_define
class RancherCreateNode:
    """
    Attributes:
        cluster (str):
        role (RancherNodeRoleEnum):
        uuid (UUID):
    """

    cluster: str
    role: RancherNodeRoleEnum
    uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster = self.cluster

        role = self.role.value

        uuid = str(self.uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster": cluster,
                "role": role,
                "uuid": uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cluster = d.pop("cluster")

        role = RancherNodeRoleEnum(d.pop("role"))

        uuid = UUID(d.pop("uuid"))

        rancher_create_node = cls(
            cluster=cluster,
            role=role,
            uuid=uuid,
        )

        rancher_create_node.additional_properties = d
        return rancher_create_node

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
