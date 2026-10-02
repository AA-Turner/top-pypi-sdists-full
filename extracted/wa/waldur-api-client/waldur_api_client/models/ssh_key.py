from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SshKey")


@_attrs_define
class SshKey:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        name (Union[Unset, str]):
        public_key (Union[Unset, str]):
        fingerprint_md5 (Union[Unset, str]):
        fingerprint_sha256 (Union[Unset, str]):
        fingerprint_sha512 (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        is_shared (Union[Unset, bool]):
        type_ (Union[Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    public_key: Union[Unset, str] = UNSET
    fingerprint_md5: Union[Unset, str] = UNSET
    fingerprint_sha256: Union[Unset, str] = UNSET
    fingerprint_sha512: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        name = self.name

        public_key = self.public_key

        fingerprint_md5 = self.fingerprint_md5

        fingerprint_sha256 = self.fingerprint_sha256

        fingerprint_sha512 = self.fingerprint_sha512

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        is_shared = self.is_shared

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if public_key is not UNSET:
            field_dict["public_key"] = public_key
        if fingerprint_md5 is not UNSET:
            field_dict["fingerprint_md5"] = fingerprint_md5
        if fingerprint_sha256 is not UNSET:
            field_dict["fingerprint_sha256"] = fingerprint_sha256
        if fingerprint_sha512 is not UNSET:
            field_dict["fingerprint_sha512"] = fingerprint_sha512
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        name = d.pop("name", UNSET)

        public_key = d.pop("public_key", UNSET)

        fingerprint_md5 = d.pop("fingerprint_md5", UNSET)

        fingerprint_sha256 = d.pop("fingerprint_sha256", UNSET)

        fingerprint_sha512 = d.pop("fingerprint_sha512", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        is_shared = d.pop("is_shared", UNSET)

        type_ = d.pop("type", UNSET)

        ssh_key = cls(
            url=url,
            uuid=uuid,
            name=name,
            public_key=public_key,
            fingerprint_md5=fingerprint_md5,
            fingerprint_sha256=fingerprint_sha256,
            fingerprint_sha512=fingerprint_sha512,
            user_uuid=user_uuid,
            is_shared=is_shared,
            type_=type_,
        )

        ssh_key.additional_properties = d
        return ssh_key

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
