from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.demo_preset_user import DemoPresetUser


T = TypeVar("T", bound="DemoPresetLoadResponse")


@_attrs_define
class DemoPresetLoadResponse:
    """
    Attributes:
        success (bool):
        message (str):
        output (Union[Unset, str]):
        users (Union[Unset, list['DemoPresetUser']]):
    """

    success: bool
    message: str
    output: Union[Unset, str] = UNSET
    users: Union[Unset, list["DemoPresetUser"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        success = self.success

        message = self.message

        output = self.output

        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "message": message,
            }
        )
        if output is not UNSET:
            field_dict["output"] = output
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.demo_preset_user import DemoPresetUser

        d = dict(src_dict)
        success = d.pop("success")

        message = d.pop("message")

        output = d.pop("output", UNSET)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = DemoPresetUser.from_dict(users_item_data)

            users.append(users_item)

        demo_preset_load_response = cls(
            success=success,
            message=message,
            output=output,
            users=users,
        )

        demo_preset_load_response.additional_properties = d
        return demo_preset_load_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
