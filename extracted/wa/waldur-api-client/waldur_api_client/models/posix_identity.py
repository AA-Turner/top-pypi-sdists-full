import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PosixIdentity")


@_attrs_define
class PosixIdentity:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        pool_uuid (UUID):
        offering_uuid (UUID):
        offering_name (str):
        consumer_type (Union[None, str]):
        consumer_name (Union[None, str]):
        uid (Union[None, Unset, int]):
        gid (Union[None, Unset, int]):
        released_at (Union[None, Unset, datetime.datetime]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    pool_uuid: UUID
    offering_uuid: UUID
    offering_name: str
    consumer_type: Union[None, str]
    consumer_name: Union[None, str]
    uid: Union[None, Unset, int] = UNSET
    gid: Union[None, Unset, int] = UNSET
    released_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        pool_uuid = str(self.pool_uuid)

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        consumer_type: Union[None, str]
        consumer_type = self.consumer_type

        consumer_name: Union[None, str]
        consumer_name = self.consumer_name

        uid: Union[None, Unset, int]
        if isinstance(self.uid, Unset):
            uid = UNSET
        else:
            uid = self.uid

        gid: Union[None, Unset, int]
        if isinstance(self.gid, Unset):
            gid = UNSET
        else:
            gid = self.gid

        released_at: Union[None, Unset, str]
        if isinstance(self.released_at, Unset):
            released_at = UNSET
        elif isinstance(self.released_at, datetime.datetime):
            released_at = self.released_at.isoformat()
        else:
            released_at = self.released_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "pool_uuid": pool_uuid,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "consumer_type": consumer_type,
                "consumer_name": consumer_name,
            }
        )
        if uid is not UNSET:
            field_dict["uid"] = uid
        if gid is not UNSET:
            field_dict["gid"] = gid
        if released_at is not UNSET:
            field_dict["released_at"] = released_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        pool_uuid = UUID(d.pop("pool_uuid"))

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        def _parse_consumer_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        consumer_type = _parse_consumer_type(d.pop("consumer_type"))

        def _parse_consumer_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        consumer_name = _parse_consumer_name(d.pop("consumer_name"))

        def _parse_uid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        uid = _parse_uid(d.pop("uid", UNSET))

        def _parse_gid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        gid = _parse_gid(d.pop("gid", UNSET))

        def _parse_released_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                released_at_type_0 = isoparse(data)

                return released_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        released_at = _parse_released_at(d.pop("released_at", UNSET))

        posix_identity = cls(
            url=url,
            uuid=uuid,
            created=created,
            pool_uuid=pool_uuid,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            consumer_type=consumer_type,
            consumer_name=consumer_name,
            uid=uid,
            gid=gid,
            released_at=released_at,
        )

        posix_identity.additional_properties = d
        return posix_identity

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
