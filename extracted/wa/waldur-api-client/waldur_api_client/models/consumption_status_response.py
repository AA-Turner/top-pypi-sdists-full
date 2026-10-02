import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ConsumptionStatusResponse")


@_attrs_define
class ConsumptionStatusResponse:
    """
    Attributes:
        global_sync_enabled (bool):
        settings_sync_enabled (bool):
        settings_uuid (Union[None, UUID]):
        last_sync_run (Union[None, datetime.datetime]):
    """

    global_sync_enabled: bool
    settings_sync_enabled: bool
    settings_uuid: Union[None, UUID]
    last_sync_run: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        global_sync_enabled = self.global_sync_enabled

        settings_sync_enabled = self.settings_sync_enabled

        settings_uuid: Union[None, str]
        if isinstance(self.settings_uuid, UUID):
            settings_uuid = str(self.settings_uuid)
        else:
            settings_uuid = self.settings_uuid

        last_sync_run: Union[None, str]
        if isinstance(self.last_sync_run, datetime.datetime):
            last_sync_run = self.last_sync_run.isoformat()
        else:
            last_sync_run = self.last_sync_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "global_sync_enabled": global_sync_enabled,
                "settings_sync_enabled": settings_sync_enabled,
                "settings_uuid": settings_uuid,
                "last_sync_run": last_sync_run,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        global_sync_enabled = d.pop("global_sync_enabled")

        settings_sync_enabled = d.pop("settings_sync_enabled")

        def _parse_settings_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                settings_uuid_type_0 = UUID(data)

                return settings_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        settings_uuid = _parse_settings_uuid(d.pop("settings_uuid"))

        def _parse_last_sync_run(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sync_run_type_0 = isoparse(data)

                return last_sync_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_sync_run = _parse_last_sync_run(d.pop("last_sync_run"))

        consumption_status_response = cls(
            global_sync_enabled=global_sync_enabled,
            settings_sync_enabled=settings_sync_enabled,
            settings_uuid=settings_uuid,
            last_sync_run=last_sync_run,
        )

        consumption_status_response.additional_properties = d
        return consumption_status_response

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
