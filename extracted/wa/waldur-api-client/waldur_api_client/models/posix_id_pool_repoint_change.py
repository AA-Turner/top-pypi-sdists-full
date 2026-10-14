from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PosixIdPoolRepointChange")


@_attrs_define
class PosixIdPoolRepointChange:
    """
    Attributes:
        offering_user_uuid (str):
        offering_uuid (str):
        offering_name (str):
        user_uuid (str):
        username (str):
        namespace (str):
        old_value (Union[None, int]):
        new_value (int):
    """

    offering_user_uuid: str
    offering_uuid: str
    offering_name: str
    user_uuid: str
    username: str
    namespace: str
    old_value: Union[None, int]
    new_value: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering_user_uuid = self.offering_user_uuid

        offering_uuid = self.offering_uuid

        offering_name = self.offering_name

        user_uuid = self.user_uuid

        username = self.username

        namespace = self.namespace

        old_value: Union[None, int]
        old_value = self.old_value

        new_value = self.new_value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering_user_uuid": offering_user_uuid,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "user_uuid": user_uuid,
                "username": username,
                "namespace": namespace,
                "old_value": old_value,
                "new_value": new_value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering_user_uuid = d.pop("offering_user_uuid")

        offering_uuid = d.pop("offering_uuid")

        offering_name = d.pop("offering_name")

        user_uuid = d.pop("user_uuid")

        username = d.pop("username")

        namespace = d.pop("namespace")

        def _parse_old_value(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        old_value = _parse_old_value(d.pop("old_value"))

        new_value = d.pop("new_value")

        posix_id_pool_repoint_change = cls(
            offering_user_uuid=offering_user_uuid,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            user_uuid=user_uuid,
            username=username,
            namespace=namespace,
            old_value=old_value,
            new_value=new_value,
        )

        posix_id_pool_repoint_change.additional_properties = d
        return posix_id_pool_repoint_change

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
