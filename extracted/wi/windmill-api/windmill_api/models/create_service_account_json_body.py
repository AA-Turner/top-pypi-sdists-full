from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateServiceAccountJsonBody")


@_attrs_define
class CreateServiceAccountJsonBody:
    """
    Attributes:
        username (str):
        is_admin (Union[Unset, bool]): Grant the service account workspace admin. Defaults to false. Cannot be combined
            with operator=true.
        operator (Union[Unset, bool]): Make the service account an operator. Defaults to true for backward
            compatibility. Set to false to count as a developer (1 seat) instead of 0.5 seat.
        add_to_deployers (Union[Unset, bool]): Add the service account to the workspace `wm_deployers` group on
            creation. Recommended when the account will be used as a CLI sync / CI deploy identity so it can deploy on
            behalf of other users.
    """

    username: str
    is_admin: Union[Unset, bool] = UNSET
    operator: Union[Unset, bool] = UNSET
    add_to_deployers: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        is_admin = self.is_admin
        operator = self.operator
        add_to_deployers = self.add_to_deployers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
            }
        )
        if is_admin is not UNSET:
            field_dict["is_admin"] = is_admin
        if operator is not UNSET:
            field_dict["operator"] = operator
        if add_to_deployers is not UNSET:
            field_dict["add_to_deployers"] = add_to_deployers

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username")

        is_admin = d.pop("is_admin", UNSET)

        operator = d.pop("operator", UNSET)

        add_to_deployers = d.pop("add_to_deployers", UNSET)

        create_service_account_json_body = cls(
            username=username,
            is_admin=is_admin,
            operator=operator,
            add_to_deployers=add_to_deployers,
        )

        create_service_account_json_body.additional_properties = d
        return create_service_account_json_body

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
