import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PosixIdPool")


@_attrs_define
class PosixIdPool:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        description (Union[Unset, str]):
        service_provider (Union[None, UUID, Unset]):
        offering (Union[None, UUID, Unset]):
        min_uid (Union[None, Unset, int]):
        max_uid (Union[None, Unset, int]):
        next_uid (Union[None, Unset, int]):
        min_gid (Union[None, Unset, int]):
        max_gid (Union[None, Unset, int]):
        next_gid (Union[None, Unset, int]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        scope (Union[Unset, str]):
        uid_used (Union[Unset, int]):
        gid_used (Union[Unset, int]):
        uid_utilization (Union[None, Unset, float]):
        gid_utilization (Union[None, Unset, float]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    description: Union[Unset, str] = UNSET
    service_provider: Union[None, UUID, Unset] = UNSET
    offering: Union[None, UUID, Unset] = UNSET
    min_uid: Union[None, Unset, int] = UNSET
    max_uid: Union[None, Unset, int] = UNSET
    next_uid: Union[None, Unset, int] = UNSET
    min_gid: Union[None, Unset, int] = UNSET
    max_gid: Union[None, Unset, int] = UNSET
    next_gid: Union[None, Unset, int] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    scope: Union[Unset, str] = UNSET
    uid_used: Union[Unset, int] = UNSET
    gid_used: Union[Unset, int] = UNSET
    uid_utilization: Union[None, Unset, float] = UNSET
    gid_utilization: Union[None, Unset, float] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        description = self.description

        service_provider: Union[None, Unset, str]
        if isinstance(self.service_provider, Unset):
            service_provider = UNSET
        elif isinstance(self.service_provider, UUID):
            service_provider = str(self.service_provider)
        else:
            service_provider = self.service_provider

        offering: Union[None, Unset, str]
        if isinstance(self.offering, Unset):
            offering = UNSET
        elif isinstance(self.offering, UUID):
            offering = str(self.offering)
        else:
            offering = self.offering

        min_uid: Union[None, Unset, int]
        if isinstance(self.min_uid, Unset):
            min_uid = UNSET
        else:
            min_uid = self.min_uid

        max_uid: Union[None, Unset, int]
        if isinstance(self.max_uid, Unset):
            max_uid = UNSET
        else:
            max_uid = self.max_uid

        next_uid: Union[None, Unset, int]
        if isinstance(self.next_uid, Unset):
            next_uid = UNSET
        else:
            next_uid = self.next_uid

        min_gid: Union[None, Unset, int]
        if isinstance(self.min_gid, Unset):
            min_gid = UNSET
        else:
            min_gid = self.min_gid

        max_gid: Union[None, Unset, int]
        if isinstance(self.max_gid, Unset):
            max_gid = UNSET
        else:
            max_gid = self.max_gid

        next_gid: Union[None, Unset, int]
        if isinstance(self.next_gid, Unset):
            next_gid = UNSET
        else:
            next_gid = self.next_gid

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        scope = self.scope

        uid_used = self.uid_used

        gid_used = self.gid_used

        uid_utilization: Union[None, Unset, float]
        if isinstance(self.uid_utilization, Unset):
            uid_utilization = UNSET
        else:
            uid_utilization = self.uid_utilization

        gid_utilization: Union[None, Unset, float]
        if isinstance(self.gid_utilization, Unset):
            gid_utilization = UNSET
        else:
            gid_utilization = self.gid_utilization

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if description is not UNSET:
            field_dict["description"] = description
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider
        if offering is not UNSET:
            field_dict["offering"] = offering
        if min_uid is not UNSET:
            field_dict["min_uid"] = min_uid
        if max_uid is not UNSET:
            field_dict["max_uid"] = max_uid
        if next_uid is not UNSET:
            field_dict["next_uid"] = next_uid
        if min_gid is not UNSET:
            field_dict["min_gid"] = min_gid
        if max_gid is not UNSET:
            field_dict["max_gid"] = max_gid
        if next_gid is not UNSET:
            field_dict["next_gid"] = next_gid
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if scope is not UNSET:
            field_dict["scope"] = scope
        if uid_used is not UNSET:
            field_dict["uid_used"] = uid_used
        if gid_used is not UNSET:
            field_dict["gid_used"] = gid_used
        if uid_utilization is not UNSET:
            field_dict["uid_utilization"] = uid_utilization
        if gid_utilization is not UNSET:
            field_dict["gid_utilization"] = gid_utilization

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

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        description = d.pop("description", UNSET)

        def _parse_service_provider(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                service_provider_type_0 = UUID(data)

                return service_provider_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        service_provider = _parse_service_provider(d.pop("service_provider", UNSET))

        def _parse_offering(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offering_type_0 = UUID(data)

                return offering_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        offering = _parse_offering(d.pop("offering", UNSET))

        def _parse_min_uid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_uid = _parse_min_uid(d.pop("min_uid", UNSET))

        def _parse_max_uid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_uid = _parse_max_uid(d.pop("max_uid", UNSET))

        def _parse_next_uid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_uid = _parse_next_uid(d.pop("next_uid", UNSET))

        def _parse_min_gid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        min_gid = _parse_min_gid(d.pop("min_gid", UNSET))

        def _parse_max_gid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        max_gid = _parse_max_gid(d.pop("max_gid", UNSET))

        def _parse_next_gid(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        next_gid = _parse_next_gid(d.pop("next_gid", UNSET))

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        scope = d.pop("scope", UNSET)

        uid_used = d.pop("uid_used", UNSET)

        gid_used = d.pop("gid_used", UNSET)

        def _parse_uid_utilization(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        uid_utilization = _parse_uid_utilization(d.pop("uid_utilization", UNSET))

        def _parse_gid_utilization(data: object) -> Union[None, Unset, float]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, float], data)

        gid_utilization = _parse_gid_utilization(d.pop("gid_utilization", UNSET))

        posix_id_pool = cls(
            url=url,
            uuid=uuid,
            created=created,
            description=description,
            service_provider=service_provider,
            offering=offering,
            min_uid=min_uid,
            max_uid=max_uid,
            next_uid=next_uid,
            min_gid=min_gid,
            max_gid=max_gid,
            next_gid=next_gid,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            scope=scope,
            uid_used=uid_used,
            gid_used=gid_used,
            uid_utilization=uid_utilization,
            gid_utilization=gid_utilization,
        )

        posix_id_pool.additional_properties = d
        return posix_id_pool

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
