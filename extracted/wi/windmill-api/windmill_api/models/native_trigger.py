from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.native_trigger_service_name import NativeTriggerServiceName
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.native_trigger_service_config import NativeTriggerServiceConfig


T = TypeVar("T", bound="NativeTrigger")


@_attrs_define
class NativeTrigger:
    """A native trigger stored in Windmill

    Attributes:
        external_id (str): The unique identifier from the external service
        workspace_id (str): The workspace this trigger belongs to
        service_name (NativeTriggerServiceName):
        script_path (str): The path to the script or flow that will be triggered
        is_flow (bool): Whether the trigger targets a flow (true) or a script (false)
        service_config (NativeTriggerServiceConfig): Configuration for the trigger including event_type and
            service_config
        error (Union[Unset, None, str]): Error message if the trigger is in an error state
    """

    external_id: str
    workspace_id: str
    service_name: NativeTriggerServiceName
    script_path: str
    is_flow: bool
    service_config: "NativeTriggerServiceConfig"
    error: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        external_id = self.external_id
        workspace_id = self.workspace_id
        service_name = self.service_name.value

        script_path = self.script_path
        is_flow = self.is_flow
        service_config = self.service_config.to_dict()

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "external_id": external_id,
                "workspace_id": workspace_id,
                "service_name": service_name,
                "script_path": script_path,
                "is_flow": is_flow,
                "service_config": service_config,
            }
        )
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.native_trigger_service_config import NativeTriggerServiceConfig

        d = src_dict.copy()
        external_id = d.pop("external_id")

        workspace_id = d.pop("workspace_id")

        service_name = NativeTriggerServiceName(d.pop("service_name"))

        script_path = d.pop("script_path")

        is_flow = d.pop("is_flow")

        service_config = NativeTriggerServiceConfig.from_dict(d.pop("service_config"))

        error = d.pop("error", UNSET)

        native_trigger = cls(
            external_id=external_id,
            workspace_id=workspace_id,
            service_name=service_name,
            script_path=script_path,
            is_flow=is_flow,
            service_config=service_config,
            error=error,
        )

        native_trigger.additional_properties = d
        return native_trigger

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
