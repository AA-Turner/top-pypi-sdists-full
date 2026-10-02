from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsHandoffAccessResponse")



@_attrs_define
class ManagedAgentsHandoffAccessResponse:
    """ Response body of POST /v1/sessions/{session_id}/handoff/access. The URL is an ephemeral credential, is never
    persisted by Managed Agents, and the response is always Cache-Control: no-store.

        Example:
            {'redemption_url': 'https://example.com', 'redemption_url_expires_at': '2026-02-18T09:30:00Z'}

        Attributes:
            redemption_url (str): One-time or short-lived URL that establishes access to the session's existing noVNC
                display. Treat it as a credential.
            redemption_url_expires_at (datetime.datetime): RFC 3339 time after which this redemption URL can no longer
                establish a browser session, capped by the handoff deadline. An already redeemed browser session remains usable
                until hand-back, deadline, or revoke.
     """

    redemption_url: str
    redemption_url_expires_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        redemption_url = self.redemption_url

        redemption_url_expires_at = self.redemption_url_expires_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "redemption_url": redemption_url,
            "redemption_url_expires_at": redemption_url_expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        redemption_url = d.pop("redemption_url")

        redemption_url_expires_at = datetime.datetime.fromisoformat(d.pop("redemption_url_expires_at"))




        managed_agents_handoff_access_response = cls(
            redemption_url=redemption_url,
            redemption_url_expires_at=redemption_url_expires_at,
        )


        managed_agents_handoff_access_response.additional_properties = d
        return managed_agents_handoff_access_response

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
