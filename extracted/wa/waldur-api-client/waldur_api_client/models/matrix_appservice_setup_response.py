from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixAppserviceSetupResponse")


@_attrs_define
class MatrixAppserviceSetupResponse:
    """
    Attributes:
        registration_yaml (str):
        as_token (str):
        hs_token (str):
        sender_localpart (str):
        webhook_url (str):
        bot_provision_status (str):
    """

    registration_yaml: str
    as_token: str
    hs_token: str
    sender_localpart: str
    webhook_url: str
    bot_provision_status: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        registration_yaml = self.registration_yaml

        as_token = self.as_token

        hs_token = self.hs_token

        sender_localpart = self.sender_localpart

        webhook_url = self.webhook_url

        bot_provision_status = self.bot_provision_status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "registration_yaml": registration_yaml,
                "as_token": as_token,
                "hs_token": hs_token,
                "sender_localpart": sender_localpart,
                "webhook_url": webhook_url,
                "bot_provision_status": bot_provision_status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        registration_yaml = d.pop("registration_yaml")

        as_token = d.pop("as_token")

        hs_token = d.pop("hs_token")

        sender_localpart = d.pop("sender_localpart")

        webhook_url = d.pop("webhook_url")

        bot_provision_status = d.pop("bot_provision_status")

        matrix_appservice_setup_response = cls(
            registration_yaml=registration_yaml,
            as_token=as_token,
            hs_token=hs_token,
            sender_localpart=sender_localpart,
            webhook_url=webhook_url,
            bot_provision_status=bot_provision_status,
        )

        matrix_appservice_setup_response.additional_properties = d
        return matrix_appservice_setup_response

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
