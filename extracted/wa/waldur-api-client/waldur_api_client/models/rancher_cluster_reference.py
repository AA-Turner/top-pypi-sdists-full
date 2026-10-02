from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RancherClusterReference")


@_attrs_define
class RancherClusterReference:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        marketplace_uuid (Union[None, Unset, str]):
    """

    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    marketplace_uuid: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        marketplace_uuid: Union[None, Unset, str]
        if isinstance(self.marketplace_uuid, Unset):
            marketplace_uuid = UNSET
        else:
            marketplace_uuid = self.marketplace_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if marketplace_uuid is not UNSET:
            field_dict["marketplace_uuid"] = marketplace_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        def _parse_marketplace_uuid(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        marketplace_uuid = _parse_marketplace_uuid(d.pop("marketplace_uuid", UNSET))

        rancher_cluster_reference = cls(
            uuid=uuid,
            name=name,
            marketplace_uuid=marketplace_uuid,
        )

        rancher_cluster_reference.additional_properties = d
        return rancher_cluster_reference

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
