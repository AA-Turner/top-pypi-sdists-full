import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.accessor_type_enum import AccessorTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.accessor_user import AccessorUser
    from ..models.user_data_access_log_context import UserDataAccessLogContext


T = TypeVar("T", bound="UserDataAccessLog")


@_attrs_define
class UserDataAccessLog:
    """
    Attributes:
        uuid (UUID):
        timestamp (datetime.datetime):
        accessor_type (AccessorTypeEnum):
        accessed_fields (list[str]):
        accessor_category (Union[Unset, str]):
        accessor (Union[Unset, AccessorUser]):
        ip_address (Union[None, Unset, str]): An IPv4 or IPv6 address.
        context (Union[Unset, UserDataAccessLogContext]):
    """

    uuid: UUID
    timestamp: datetime.datetime
    accessor_type: AccessorTypeEnum
    accessed_fields: list[str]
    accessor_category: Union[Unset, str] = UNSET
    accessor: Union[Unset, "AccessorUser"] = UNSET
    ip_address: Union[None, Unset, str] = UNSET
    context: Union[Unset, "UserDataAccessLogContext"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        timestamp = self.timestamp.isoformat()

        accessor_type = self.accessor_type.value

        accessed_fields = self.accessed_fields

        accessor_category = self.accessor_category

        accessor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.accessor, Unset):
            accessor = self.accessor.to_dict()

        ip_address: Union[None, Unset, str]
        if isinstance(self.ip_address, Unset):
            ip_address = UNSET
        else:
            ip_address = self.ip_address

        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "timestamp": timestamp,
                "accessor_type": accessor_type,
                "accessed_fields": accessed_fields,
            }
        )
        if accessor_category is not UNSET:
            field_dict["accessor_category"] = accessor_category
        if accessor is not UNSET:
            field_dict["accessor"] = accessor
        if ip_address is not UNSET:
            field_dict["ip_address"] = ip_address
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.accessor_user import AccessorUser
        from ..models.user_data_access_log_context import UserDataAccessLogContext

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        timestamp = isoparse(d.pop("timestamp"))

        accessor_type = AccessorTypeEnum(d.pop("accessor_type"))

        accessed_fields = cast(list[str], d.pop("accessed_fields"))

        accessor_category = d.pop("accessor_category", UNSET)

        _accessor = d.pop("accessor", UNSET)
        accessor: Union[Unset, AccessorUser]
        if isinstance(_accessor, Unset):
            accessor = UNSET
        else:
            accessor = AccessorUser.from_dict(_accessor)

        def _parse_ip_address(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ip_address = _parse_ip_address(d.pop("ip_address", UNSET))

        _context = d.pop("context", UNSET)
        context: Union[Unset, UserDataAccessLogContext]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = UserDataAccessLogContext.from_dict(_context)

        user_data_access_log = cls(
            uuid=uuid,
            timestamp=timestamp,
            accessor_type=accessor_type,
            accessed_fields=accessed_fields,
            accessor_category=accessor_category,
            accessor=accessor,
            ip_address=ip_address,
            context=context,
        )

        user_data_access_log.additional_properties = d
        return user_data_access_log

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
