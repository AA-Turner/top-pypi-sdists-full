from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.set_capture_config_json_body_trigger_kind import SetCaptureConfigJsonBodyTriggerKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.set_capture_config_json_body_trigger_config import SetCaptureConfigJsonBodyTriggerConfig


T = TypeVar("T", bound="SetCaptureConfigJsonBody")


@_attrs_define
class SetCaptureConfigJsonBody:
    """
    Attributes:
        trigger_kind (SetCaptureConfigJsonBodyTriggerKind):
        path (str):
        is_flow (bool):
        trigger_config (Union[Unset, SetCaptureConfigJsonBodyTriggerConfig]):
    """

    trigger_kind: SetCaptureConfigJsonBodyTriggerKind
    path: str
    is_flow: bool
    trigger_config: Union[Unset, "SetCaptureConfigJsonBodyTriggerConfig"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        trigger_kind = self.trigger_kind.value

        path = self.path
        is_flow = self.is_flow
        trigger_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.trigger_config, Unset):
            trigger_config = self.trigger_config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "trigger_kind": trigger_kind,
                "path": path,
                "is_flow": is_flow,
            }
        )
        if trigger_config is not UNSET:
            field_dict["trigger_config"] = trigger_config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.set_capture_config_json_body_trigger_config import SetCaptureConfigJsonBodyTriggerConfig

        d = src_dict.copy()
        trigger_kind = SetCaptureConfigJsonBodyTriggerKind(d.pop("trigger_kind"))

        path = d.pop("path")

        is_flow = d.pop("is_flow")

        _trigger_config = d.pop("trigger_config", UNSET)
        trigger_config: Union[Unset, SetCaptureConfigJsonBodyTriggerConfig]
        if isinstance(_trigger_config, Unset):
            trigger_config = UNSET
        else:
            trigger_config = SetCaptureConfigJsonBodyTriggerConfig.from_dict(_trigger_config)

        set_capture_config_json_body = cls(
            trigger_kind=trigger_kind,
            path=path,
            is_flow=is_flow,
            trigger_config=trigger_config,
        )

        set_capture_config_json_body.additional_properties = d
        return set_capture_config_json_body

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
