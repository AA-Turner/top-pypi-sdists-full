from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.passkey_assertion_finish_request_credential import PasskeyAssertionFinishRequestCredential


T = TypeVar("T", bound="PasskeyAssertionFinishRequest")


@_attrs_define
class PasskeyAssertionFinishRequest:
    """
    Attributes:
        ceremony (UUID):
        credential (PasskeyAssertionFinishRequestCredential):
    """

    ceremony: UUID
    credential: "PasskeyAssertionFinishRequestCredential"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ceremony = str(self.ceremony)

        credential = self.credential.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ceremony": ceremony,
                "credential": credential,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.passkey_assertion_finish_request_credential import PasskeyAssertionFinishRequestCredential

        d = dict(src_dict)
        ceremony = UUID(d.pop("ceremony"))

        credential = PasskeyAssertionFinishRequestCredential.from_dict(d.pop("credential"))

        passkey_assertion_finish_request = cls(
            ceremony=ceremony,
            credential=credential,
        )

        passkey_assertion_finish_request.additional_properties = d
        return passkey_assertion_finish_request

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
