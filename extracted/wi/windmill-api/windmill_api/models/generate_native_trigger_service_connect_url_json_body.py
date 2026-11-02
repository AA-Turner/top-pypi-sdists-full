from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GenerateNativeTriggerServiceConnectUrlJsonBody")


@_attrs_define
class GenerateNativeTriggerServiceConnectUrlJsonBody:
    """
    Attributes:
        redirect_uri (str):
        resource_path (Union[Unset, str]):
    """

    redirect_uri: str
    resource_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        redirect_uri = self.redirect_uri
        resource_path = self.resource_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "redirect_uri": redirect_uri,
            }
        )
        if resource_path is not UNSET:
            field_dict["resource_path"] = resource_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        redirect_uri = d.pop("redirect_uri")

        resource_path = d.pop("resource_path", UNSET)

        generate_native_trigger_service_connect_url_json_body = cls(
            redirect_uri=redirect_uri,
            resource_path=resource_path,
        )

        generate_native_trigger_service_connect_url_json_body.additional_properties = d
        return generate_native_trigger_service_connect_url_json_body

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
