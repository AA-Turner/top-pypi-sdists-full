from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TriggerConsumptionSyncRequestRequest")


@_attrs_define
class TriggerConsumptionSyncRequestRequest:
    """
    Attributes:
        year (int):
        month (int):
        settings_uuid (Union[Unset, UUID]):
        resource_uuid (Union[Unset, UUID]): Sync specific resource only
    """

    year: int
    month: int
    settings_uuid: Union[Unset, UUID] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        year = self.year

        month = self.month

        settings_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.settings_uuid, Unset):
            settings_uuid = str(self.settings_uuid)

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "year": year,
                "month": month,
            }
        )
        if settings_uuid is not UNSET:
            field_dict["settings_uuid"] = settings_uuid
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        year = d.pop("year")

        month = d.pop("month")

        _settings_uuid = d.pop("settings_uuid", UNSET)
        settings_uuid: Union[Unset, UUID]
        if isinstance(_settings_uuid, Unset):
            settings_uuid = UNSET
        else:
            settings_uuid = UUID(_settings_uuid)

        _resource_uuid = d.pop("resource_uuid", UNSET)
        resource_uuid: Union[Unset, UUID]
        if isinstance(_resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = UUID(_resource_uuid)

        trigger_consumption_sync_request_request = cls(
            year=year,
            month=month,
            settings_uuid=settings_uuid,
            resource_uuid=resource_uuid,
        )

        trigger_consumption_sync_request_request.additional_properties = d
        return trigger_consumption_sync_request_request

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
