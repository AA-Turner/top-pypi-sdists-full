from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RancherUserClusterLink")


@_attrs_define
class RancherUserClusterLink:
    """
    Attributes:
        cluster (str):
        role (str):
        cluster_name (str):
        cluster_uuid (UUID):
    """

    cluster: str
    role: str
    cluster_name: str
    cluster_uuid: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        cluster = self.cluster

        role = self.role

        cluster_name = self.cluster_name

        cluster_uuid = str(self.cluster_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "cluster": cluster,
                "role": role,
                "cluster_name": cluster_name,
                "cluster_uuid": cluster_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cluster = d.pop("cluster")

        role = d.pop("role")

        cluster_name = d.pop("cluster_name")

        cluster_uuid = UUID(d.pop("cluster_uuid"))

        rancher_user_cluster_link = cls(
            cluster=cluster,
            role=role,
            cluster_name=cluster_name,
            cluster_uuid=cluster_uuid,
        )

        rancher_user_cluster_link.additional_properties = d
        return rancher_user_cluster_link

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
