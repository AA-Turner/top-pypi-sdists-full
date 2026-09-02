from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateWorkspaceJsonBody")


@_attrs_define
class CreateWorkspaceJsonBody:
    """
    Attributes:
        id (str):
        name (str):
        username (Union[Unset, str]):
        color (Union[Unset, str]):
        error_handler_fallback_to_instance_alerts (Union[Unset, bool]): Report failed jobs to the instance critical
            alert channels when no workspace error handler is set. Not available on cloud or on fork workspaces.
    """

    id: str
    name: str
    username: Union[Unset, str] = UNSET
    color: Union[Unset, str] = UNSET
    error_handler_fallback_to_instance_alerts: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        username = self.username
        color = self.color
        error_handler_fallback_to_instance_alerts = self.error_handler_fallback_to_instance_alerts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if color is not UNSET:
            field_dict["color"] = color
        if error_handler_fallback_to_instance_alerts is not UNSET:
            field_dict["error_handler_fallback_to_instance_alerts"] = error_handler_fallback_to_instance_alerts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        username = d.pop("username", UNSET)

        color = d.pop("color", UNSET)

        error_handler_fallback_to_instance_alerts = d.pop("error_handler_fallback_to_instance_alerts", UNSET)

        create_workspace_json_body = cls(
            id=id,
            name=name,
            username=username,
            color=color,
            error_handler_fallback_to_instance_alerts=error_handler_fallback_to_instance_alerts,
        )

        create_workspace_json_body.additional_properties = d
        return create_workspace_json_body

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
