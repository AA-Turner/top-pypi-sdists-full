import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_capture_configs_response_200_item_trigger_kind import GetCaptureConfigsResponse200ItemTriggerKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetCaptureConfigsResponse200Item")


@_attrs_define
class GetCaptureConfigsResponse200Item:
    """
    Attributes:
        trigger_kind (GetCaptureConfigsResponse200ItemTriggerKind):
        trigger_config (Union[Unset, Any]):
        error (Union[Unset, str]):
        last_server_ping (Union[Unset, datetime.datetime]):
    """

    trigger_kind: GetCaptureConfigsResponse200ItemTriggerKind
    trigger_config: Union[Unset, Any] = UNSET
    error: Union[Unset, str] = UNSET
    last_server_ping: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trigger_kind = self.trigger_kind.value

        trigger_config = self.trigger_config
        error = self.error
        last_server_ping: Union[Unset, str] = UNSET
        if not isinstance(self.last_server_ping, Unset):
            last_server_ping = self.last_server_ping.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger_kind": trigger_kind,
            }
        )
        if trigger_config is not UNSET:
            field_dict["trigger_config"] = trigger_config
        if error is not UNSET:
            field_dict["error"] = error
        if last_server_ping is not UNSET:
            field_dict["last_server_ping"] = last_server_ping

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        trigger_kind = GetCaptureConfigsResponse200ItemTriggerKind(d.pop("trigger_kind"))

        trigger_config = d.pop("trigger_config", UNSET)

        error = d.pop("error", UNSET)

        _last_server_ping = d.pop("last_server_ping", UNSET)
        last_server_ping: Union[Unset, datetime.datetime]
        if isinstance(_last_server_ping, Unset):
            last_server_ping = UNSET
        else:
            last_server_ping = isoparse(_last_server_ping)

        get_capture_configs_response_200_item = cls(
            trigger_kind=trigger_kind,
            trigger_config=trigger_config,
            error=error,
            last_server_ping=last_server_ping,
        )

        get_capture_configs_response_200_item.additional_properties = d
        return get_capture_configs_response_200_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
