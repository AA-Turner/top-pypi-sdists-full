from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OffboardWorkspaceUserJsonBody")


@_attrs_define
class OffboardWorkspaceUserJsonBody:
    """
    Attributes:
        reassign_to (str): Target for reassignment: 'u/{username}' or 'f/{folder}'
        new_on_behalf_of_user (Union[Unset, str]): Required when reassign_to is a folder. The username whose identity
            will be used as permissioned_as for schedules and triggers.
        delete_user (Union[Unset, bool]): Whether to also remove the user from the workspace Default: True.
    """

    reassign_to: str
    new_on_behalf_of_user: Union[Unset, str] = UNSET
    delete_user: Union[Unset, bool] = True
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reassign_to = self.reassign_to
        new_on_behalf_of_user = self.new_on_behalf_of_user
        delete_user = self.delete_user

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reassign_to": reassign_to,
            }
        )
        if new_on_behalf_of_user is not UNSET:
            field_dict["new_on_behalf_of_user"] = new_on_behalf_of_user
        if delete_user is not UNSET:
            field_dict["delete_user"] = delete_user

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reassign_to = d.pop("reassign_to")

        new_on_behalf_of_user = d.pop("new_on_behalf_of_user", UNSET)

        delete_user = d.pop("delete_user", UNSET)

        offboard_workspace_user_json_body = cls(
            reassign_to=reassign_to,
            new_on_behalf_of_user=new_on_behalf_of_user,
            delete_user=delete_user,
        )

        offboard_workspace_user_json_body.additional_properties = d
        return offboard_workspace_user_json_body

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
