from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NativeTriggerServiceCallbackJsonBody")


@_attrs_define
class NativeTriggerServiceCallbackJsonBody:
    """
    Attributes:
        code (str):
        state (str):
        redirect_uri (str):
        resource_path (Union[Unset, str]):
    """

    code: str
    state: str
    redirect_uri: str
    resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        state = self.state
        redirect_uri = self.redirect_uri
        resource_path = self.resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "code": code,
                "state": state,
                "redirect_uri": redirect_uri,
            }
        )
        if resource_path is not UNSET:
            field_dict["resource_path"] = resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code")

        state = d.pop("state")

        redirect_uri = d.pop("redirect_uri")

        resource_path = d.pop("resource_path", UNSET)

        native_trigger_service_callback_json_body = cls(
            code=code,
            state=state,
            redirect_uri=redirect_uri,
            resource_path=resource_path,
        )

        native_trigger_service_callback_json_body.additional_properties = d
        return native_trigger_service_callback_json_body

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
