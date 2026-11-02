from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.set_azure_trigger_mode_json_body_mode import SetAzureTriggerModeJsonBodyMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="SetAzureTriggerModeJsonBody")


@_attrs_define
class SetAzureTriggerModeJsonBody:
    """
    Attributes:
        mode (SetAzureTriggerModeJsonBodyMode): job trigger mode
        force (Union[Unset, bool]): Bypass the parent-state conflict warning when enabling a trigger in a fork whose
            parent has the same path enabled.
    """

    mode: SetAzureTriggerModeJsonBodyMode
    force: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        mode = self.mode.value

        force = self.force

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
            }
        )
        if force is not UNSET:
            field_dict["force"] = force

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        mode = SetAzureTriggerModeJsonBodyMode(d.pop("mode"))

        force = d.pop("force", UNSET)

        set_azure_trigger_mode_json_body = cls(
            mode=mode,
            force=force,
        )

        set_azure_trigger_mode_json_body.additional_properties = d
        return set_azure_trigger_mode_json_body

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
