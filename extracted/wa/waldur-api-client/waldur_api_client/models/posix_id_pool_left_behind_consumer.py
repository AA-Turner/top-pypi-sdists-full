from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PosixIdPoolLeftBehindConsumer")


@_attrs_define
class PosixIdPoolLeftBehindConsumer:
    """
    Attributes:
        kind (str):
        uid (Union[None, int]):
        gid (Union[None, int]):
        identity_uuid (str):
    """

    kind: str
    uid: Union[None, int]
    gid: Union[None, int]
    identity_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind

        uid: Union[None, int]
        uid = self.uid

        gid: Union[None, int]
        gid = self.gid

        identity_uuid = self.identity_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "uid": uid,
                "gid": gid,
                "identity_uuid": identity_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = d.pop("kind")

        def _parse_uid(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        uid = _parse_uid(d.pop("uid"))

        def _parse_gid(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        gid = _parse_gid(d.pop("gid"))

        identity_uuid = d.pop("identity_uuid")

        posix_id_pool_left_behind_consumer = cls(
            kind=kind,
            uid=uid,
            gid=gid,
            identity_uuid=identity_uuid,
        )

        posix_id_pool_left_behind_consumer.additional_properties = d
        return posix_id_pool_left_behind_consumer

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
