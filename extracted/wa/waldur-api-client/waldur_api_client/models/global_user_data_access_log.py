import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.accessor_type_enum import AccessorTypeEnum

if TYPE_CHECKING:
    from ..models.accessor_user import AccessorUser
    from ..models.global_user_data_access_log_context import GlobalUserDataAccessLogContext
    from ..models.target_user import TargetUser


T = TypeVar("T", bound="GlobalUserDataAccessLog")


@_attrs_define
class GlobalUserDataAccessLog:
    """
    Attributes:
        uuid (UUID):
        timestamp (datetime.datetime):
        accessor_type (AccessorTypeEnum):
        accessed_fields (list[str]):
        user (TargetUser):
        accessor (AccessorUser):
        ip_address (Union[None, str]): An IPv4 or IPv6 address.
        context (GlobalUserDataAccessLogContext):
    """

    uuid: UUID
    timestamp: datetime.datetime
    accessor_type: AccessorTypeEnum
    accessed_fields: list[str]
    user: "TargetUser"
    accessor: "AccessorUser"
    ip_address: Union[None, str]
    context: "GlobalUserDataAccessLogContext"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        timestamp = self.timestamp.isoformat()

        accessor_type = self.accessor_type.value

        accessed_fields = self.accessed_fields

        user = self.user.to_dict()

        accessor = self.accessor.to_dict()

        ip_address: Union[None, str]
        ip_address = self.ip_address

        context = self.context.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "timestamp": timestamp,
                "accessor_type": accessor_type,
                "accessed_fields": accessed_fields,
                "user": user,
                "accessor": accessor,
                "ip_address": ip_address,
                "context": context,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.accessor_user import AccessorUser
        from ..models.global_user_data_access_log_context import GlobalUserDataAccessLogContext
        from ..models.target_user import TargetUser

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        timestamp = isoparse(d.pop("timestamp"))

        accessor_type = AccessorTypeEnum(d.pop("accessor_type"))

        accessed_fields = cast(list[str], d.pop("accessed_fields"))

        user = TargetUser.from_dict(d.pop("user"))

        accessor = AccessorUser.from_dict(d.pop("accessor"))

        def _parse_ip_address(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        ip_address = _parse_ip_address(d.pop("ip_address"))

        context = GlobalUserDataAccessLogContext.from_dict(d.pop("context"))

        global_user_data_access_log = cls(
            uuid=uuid,
            timestamp=timestamp,
            accessor_type=accessor_type,
            accessed_fields=accessed_fields,
            user=user,
            accessor=accessor,
            ip_address=ip_address,
            context=context,
        )

        global_user_data_access_log.additional_properties = d
        return global_user_data_access_log

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
