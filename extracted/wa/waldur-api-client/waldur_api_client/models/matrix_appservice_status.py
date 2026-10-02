from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MatrixAppserviceStatus")


@_attrs_define
class MatrixAppserviceStatus:
    """
    Attributes:
        enabled (bool):
        as_token_configured (bool):
        hs_token_configured (bool):
        sender_localpart (str):
        bot_user_id (str):
        webhook_path (str):
        homeserver_url (str):
        homeserver_domain (str):
        transaction_count (int):
    """

    enabled: bool
    as_token_configured: bool
    hs_token_configured: bool
    sender_localpart: str
    bot_user_id: str
    webhook_path: str
    homeserver_url: str
    homeserver_domain: str
    transaction_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        as_token_configured = self.as_token_configured

        hs_token_configured = self.hs_token_configured

        sender_localpart = self.sender_localpart

        bot_user_id = self.bot_user_id

        webhook_path = self.webhook_path

        homeserver_url = self.homeserver_url

        homeserver_domain = self.homeserver_domain

        transaction_count = self.transaction_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "as_token_configured": as_token_configured,
                "hs_token_configured": hs_token_configured,
                "sender_localpart": sender_localpart,
                "bot_user_id": bot_user_id,
                "webhook_path": webhook_path,
                "homeserver_url": homeserver_url,
                "homeserver_domain": homeserver_domain,
                "transaction_count": transaction_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        as_token_configured = d.pop("as_token_configured")

        hs_token_configured = d.pop("hs_token_configured")

        sender_localpart = d.pop("sender_localpart")

        bot_user_id = d.pop("bot_user_id")

        webhook_path = d.pop("webhook_path")

        homeserver_url = d.pop("homeserver_url")

        homeserver_domain = d.pop("homeserver_domain")

        transaction_count = d.pop("transaction_count")

        matrix_appservice_status = cls(
            enabled=enabled,
            as_token_configured=as_token_configured,
            hs_token_configured=hs_token_configured,
            sender_localpart=sender_localpart,
            bot_user_id=bot_user_id,
            webhook_path=webhook_path,
            homeserver_url=homeserver_url,
            homeserver_domain=homeserver_domain,
            transaction_count=transaction_count,
        )

        matrix_appservice_status.additional_properties = d
        return matrix_appservice_status

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
