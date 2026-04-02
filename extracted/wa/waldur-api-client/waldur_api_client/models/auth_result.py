from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_result_state_enum import AuthResultStateEnum

T = TypeVar("T", bound="AuthResult")


@_attrs_define
class AuthResult:
    """
    Attributes:
        uuid (UUID):
        token (str):
        phone (str):
        message (str): This message will be shown to user.
        state (AuthResultStateEnum):
        error_message (str):
        details (str): Cancellation details.
    """

    uuid: UUID
    token: str
    phone: str
    message: str
    state: AuthResultStateEnum
    error_message: str
    details: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        token = self.token

        phone = self.phone

        message = self.message

        state = self.state.value

        error_message = self.error_message

        details = self.details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "token": token,
                "phone": phone,
                "message": message,
                "state": state,
                "error_message": error_message,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        token = d.pop("token")

        phone = d.pop("phone")

        message = d.pop("message")

        state = AuthResultStateEnum(d.pop("state"))

        error_message = d.pop("error_message")

        details = d.pop("details")

        auth_result = cls(
            uuid=uuid,
            token=token,
            phone=phone,
            message=message,
            state=state,
            error_message=error_message,
            details=details,
        )

        auth_result.additional_properties = d
        return auth_result

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
