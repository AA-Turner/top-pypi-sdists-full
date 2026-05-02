from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_copilot_settings_state_response_200_instance_ai_summary import (
        GetCopilotSettingsStateResponse200InstanceAiSummary,
    )


T = TypeVar("T", bound="GetCopilotSettingsStateResponse200")


@_attrs_define
class GetCopilotSettingsStateResponse200:
    """
    Attributes:
        has_instance_ai_config (bool):
        uses_instance_ai_config (bool):
        instance_ai_summary (Union[Unset, GetCopilotSettingsStateResponse200InstanceAiSummary]):
    """

    has_instance_ai_config: bool
    uses_instance_ai_config: bool
    instance_ai_summary: Union[Unset, "GetCopilotSettingsStateResponse200InstanceAiSummary"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        has_instance_ai_config = self.has_instance_ai_config
        uses_instance_ai_config = self.uses_instance_ai_config
        instance_ai_summary: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.instance_ai_summary, Unset):
            instance_ai_summary = self.instance_ai_summary.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "has_instance_ai_config": has_instance_ai_config,
                "uses_instance_ai_config": uses_instance_ai_config,
            }
        )
        if instance_ai_summary is not UNSET:
            field_dict["instance_ai_summary"] = instance_ai_summary

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_copilot_settings_state_response_200_instance_ai_summary import (
            GetCopilotSettingsStateResponse200InstanceAiSummary,
        )

        d = src_dict.copy()
        has_instance_ai_config = d.pop("has_instance_ai_config")

        uses_instance_ai_config = d.pop("uses_instance_ai_config")

        _instance_ai_summary = d.pop("instance_ai_summary", UNSET)
        instance_ai_summary: Union[Unset, GetCopilotSettingsStateResponse200InstanceAiSummary]
        if isinstance(_instance_ai_summary, Unset):
            instance_ai_summary = UNSET
        else:
            instance_ai_summary = GetCopilotSettingsStateResponse200InstanceAiSummary.from_dict(_instance_ai_summary)

        get_copilot_settings_state_response_200 = cls(
            has_instance_ai_config=has_instance_ai_config,
            uses_instance_ai_config=uses_instance_ai_config,
            instance_ai_summary=instance_ai_summary,
        )

        get_copilot_settings_state_response_200.additional_properties = d
        return get_copilot_settings_state_response_200

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
