from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedRancherClusterRequest")


@_attrs_define
class PatchedRancherClusterRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        ssh_public_key (Union[Unset, str]):
        install_longhorn (Union[Unset, bool]): Longhorn is a distributed block storage deployed on top of Kubernetes
            cluster Default: False.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    ssh_public_key: Union[Unset, str] = UNSET
    install_longhorn: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        ssh_public_key = self.ssh_public_key

        install_longhorn = self.install_longhorn

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if ssh_public_key is not UNSET:
            field_dict["ssh_public_key"] = ssh_public_key
        if install_longhorn is not UNSET:
            field_dict["install_longhorn"] = install_longhorn

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        ssh_public_key = d.pop("ssh_public_key", UNSET)

        install_longhorn = d.pop("install_longhorn", UNSET)

        patched_rancher_cluster_request = cls(
            name=name,
            description=description,
            ssh_public_key=ssh_public_key,
            install_longhorn=install_longhorn,
        )

        patched_rancher_cluster_request.additional_properties = d
        return patched_rancher_cluster_request

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
