from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ComputeAccessSessionDto")



@_attrs_define
class ComputeAccessSessionDto:
    """ Short-lived access session for connecting to a running compute via the agent-service gateway.

        Example:
            {'redemptionUrl':
                'https://c-9f3a2c7b-1d4e-4a5b-8c6d-7e8f9a0b1c2d.compute.example.com/__redeem?t=eyJhbGciOiJIUzI1NiJ9',
                'redemptionUrlExpiresAt': '2026-01-15T10:00:00.000Z'}

        Attributes:
            redemption_url (str): Single-use URL the client redeems to open an interactive session against the compute.
                Served on the compute's own origin, not a shared gateway, so the host identifies the compute the session is for.
            redemption_url_expires_at (str): Timestamp when the redemption URL expires (ISO-8601, UTC).
     """

    redemption_url: str
    redemption_url_expires_at: str





    def to_dict(self) -> dict[str, Any]:
        redemption_url = self.redemption_url

        redemption_url_expires_at = self.redemption_url_expires_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "redemptionUrl": redemption_url,
            "redemptionUrlExpiresAt": redemption_url_expires_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        redemption_url = d.pop("redemptionUrl")

        redemption_url_expires_at = d.pop("redemptionUrlExpiresAt")

        compute_access_session_dto = cls(
            redemption_url=redemption_url,
            redemption_url_expires_at=redemption_url_expires_at,
        )

        return compute_access_session_dto

