from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.native_trigger_data_service_config import NativeTriggerDataServiceConfig


T = TypeVar("T", bound="NativeTriggerData")


@_attrs_define
class NativeTriggerData:
    """Data for creating or updating a native trigger

    Attributes:
        script_path (str): The path to the script or flow that will be triggered
        is_flow (bool): Whether the trigger targets a flow (true) or a script (false)
        service_config (NativeTriggerDataServiceConfig): Service-specific configuration (e.g., event types, filters)
    """

    script_path: str
    is_flow: bool
    service_config: "NativeTriggerDataServiceConfig"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        script_path = self.script_path
        is_flow = self.is_flow
        service_config = self.service_config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "script_path": script_path,
                "is_flow": is_flow,
                "service_config": service_config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.native_trigger_data_service_config import NativeTriggerDataServiceConfig

        d = src_dict.copy()
        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        service_config = NativeTriggerDataServiceConfig.from_dict(d.pop("service_config"))

        native_trigger_data = cls(
            script_path=script_path,
            is_flow=is_flow,
            service_config=service_config,
        )

        native_trigger_data.additional_properties = d
        return native_trigger_data

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
