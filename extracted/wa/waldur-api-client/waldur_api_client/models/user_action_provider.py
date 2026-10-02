import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserActionProvider")


@_attrs_define
class UserActionProvider:
    """
    Attributes:
        id (int):
        app_name (str):
        provider_class (str):
        action_type (str):
        last_execution (Union[None, datetime.datetime]):
        last_execution_status (str):
        is_enabled (Union[Unset, bool]):
        schedule (Union[Unset, str]):
    """

    id: int
    app_name: str
    provider_class: str
    action_type: str
    last_execution: Union[None, datetime.datetime]
    last_execution_status: str
    is_enabled: Union[Unset, bool] = UNSET
    schedule: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        app_name = self.app_name

        provider_class = self.provider_class

        action_type = self.action_type

        last_execution: Union[None, str]
        if isinstance(self.last_execution, datetime.datetime):
            last_execution = self.last_execution.isoformat()
        else:
            last_execution = self.last_execution

        last_execution_status = self.last_execution_status

        is_enabled = self.is_enabled

        schedule = self.schedule

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "app_name": app_name,
                "provider_class": provider_class,
                "action_type": action_type,
                "last_execution": last_execution,
                "last_execution_status": last_execution_status,
            }
        )
        if is_enabled is not UNSET:
            field_dict["is_enabled"] = is_enabled
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        app_name = d.pop("app_name")

        provider_class = d.pop("provider_class")

        action_type = d.pop("action_type")

        def _parse_last_execution(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_execution_type_0 = isoparse(data)

                return last_execution_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_execution = _parse_last_execution(d.pop("last_execution"))

        last_execution_status = d.pop("last_execution_status")

        is_enabled = d.pop("is_enabled", UNSET)

        schedule = d.pop("schedule", UNSET)

        user_action_provider = cls(
            id=id,
            app_name=app_name,
            provider_class=provider_class,
            action_type=action_type,
            last_execution=last_execution,
            last_execution_status=last_execution_status,
            is_enabled=is_enabled,
            schedule=schedule,
        )

        user_action_provider.additional_properties = d
        return user_action_provider

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
