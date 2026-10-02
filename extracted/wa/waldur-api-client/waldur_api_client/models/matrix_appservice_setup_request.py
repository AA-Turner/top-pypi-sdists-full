from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MatrixAppserviceSetupRequest")


@_attrs_define
class MatrixAppserviceSetupRequest:
    """
    Attributes:
        url (Union[Unset, str]): Waldur URL reachable by the Matrix homeserver (for webhook callbacks)
        sender_localpart (Union[Unset, str]): Localpart for the appservice bot user, e.g. 'waldur-bot'
        homeserver_url (Union[Unset, str]): Matrix homeserver base URL. Only persisted if MATRIX_HOMESERVER_URL is not
            already configured.
        homeserver_public_url (Union[Unset, str]): Optional. Matrix homeserver URL used by browser clients. Leave blank
            when the homeserver URL above is reachable from both servers and browsers. Set this for deployments where the
            two differ (e.g. Docker-internal vs. Caddy-proxied). Only persisted if MATRIX_HOMESERVER_PUBLIC_URL is not
            already configured.
        homeserver_domain (Union[Unset, str]): Matrix homeserver server_name domain. Only persisted if
            MATRIX_HOMESERVER_DOMAIN is not already configured.
        user_registration_secret (Union[Unset, str]): Shared secret configured in the homeserver for user registration.
            Only persisted if MATRIX_USER_REGISTRATION_SECRET is not already configured.
    """

    url: Union[Unset, str] = UNSET
    sender_localpart: Union[Unset, str] = UNSET
    homeserver_url: Union[Unset, str] = UNSET
    homeserver_public_url: Union[Unset, str] = UNSET
    homeserver_domain: Union[Unset, str] = UNSET
    user_registration_secret: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        sender_localpart = self.sender_localpart

        homeserver_url = self.homeserver_url

        homeserver_public_url = self.homeserver_public_url

        homeserver_domain = self.homeserver_domain

        user_registration_secret = self.user_registration_secret

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if sender_localpart is not UNSET:
            field_dict["sender_localpart"] = sender_localpart
        if homeserver_url is not UNSET:
            field_dict["homeserver_url"] = homeserver_url
        if homeserver_public_url is not UNSET:
            field_dict["homeserver_public_url"] = homeserver_public_url
        if homeserver_domain is not UNSET:
            field_dict["homeserver_domain"] = homeserver_domain
        if user_registration_secret is not UNSET:
            field_dict["user_registration_secret"] = user_registration_secret

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        sender_localpart = d.pop("sender_localpart", UNSET)

        homeserver_url = d.pop("homeserver_url", UNSET)

        homeserver_public_url = d.pop("homeserver_public_url", UNSET)

        homeserver_domain = d.pop("homeserver_domain", UNSET)

        user_registration_secret = d.pop("user_registration_secret", UNSET)

        matrix_appservice_setup_request = cls(
            url=url,
            sender_localpart=sender_localpart,
            homeserver_url=homeserver_url,
            homeserver_public_url=homeserver_public_url,
            homeserver_domain=homeserver_domain,
            user_registration_secret=user_registration_secret,
        )

        matrix_appservice_setup_request.additional_properties = d
        return matrix_appservice_setup_request

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
