from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PosixIdPoolRequest")


@_attrs_define
class PosixIdPoolRequest:
    """
    Attributes:
        description (Union[Unset, str]):
        service_provider (Union[None, UUID, Unset]):
        offering (Union[None, UUID, Unset]):
        min_uid (Union[None, Unset, int]):
        max_uid (Union[None, Unset, int]):
        min_gid (Union[None, Unset, int]):
        max_gid (Union[None, Unset, int]):
    """

    description: Union[Unset, str] = UNSET
    service_provider: Union[None, UUID, Unset] = UNSET
    offering: Union[None, UUID, Unset] = UNSET
    min_uid: Union[None, Unset, int] = UNSET
    max_uid: Union[None, Unset, int] = UNSET
    min_gid: Union[None, Unset, int] = UNSET
    max_gid: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
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
        if min_gid is not UNSET:
            field_dict["min_gid"] = min_gid
        if max_gid is not UNSET:
            field_dict["max_gid"] = max_gid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
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

        posix_id_pool_request = cls(
            description=description,
            service_provider=service_provider,
            offering=offering,
            min_uid=min_uid,
            max_uid=max_uid,
            min_gid=min_gid,
            max_gid=max_gid,
        )

        posix_id_pool_request.additional_properties = d
        return posix_id_pool_request

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
