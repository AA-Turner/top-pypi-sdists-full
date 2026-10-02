from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsConnectionProbe")



@_attrs_define
class ManagedAgentsConnectionProbe:
    """ Result of a live health check against one integration connection: its refreshed state at the provider, whether a
    token could be minted, and what is missing if not. A failed check is reported here rather than as an HTTP error.

        Example:
            {'activated': True, 'failure': 'example', 'missing_permissions': ['example'], 'ok': True, 'resource_count': 1,
                'state': 'example', 'token_minted': True}

        Attributes:
            ok (bool): True only when the connection is active at the provider and a scoped token was successfully minted
                during this probe. False means the connection cannot currently be used; read failure for why. A probe that fails
                this way is still an HTTP 200.
            resource_count (int): Number of provider resources the connection can authorize, for example selected GitHub
                repositories. The live probe credential may be narrower when the provider cannot represent the entire connection
                scope in one token. Zero when no token could be minted.
            state (str): Lifecycle of the connection as of this probe: pending (registered, waiting for the customer to
                grant trust), active (usable), suspended (paused at the provider), or revoked (uninstalled or deleted).
                Refreshed here, so it can differ from the previously stored value: a pending connection whose trust proved
                usable is reported active.
            token_minted (bool): Whether a scoped credential could actually be issued during this probe. This is the check
                that predicts whether a session using the connection will work.
            activated (bool | Unset): True when this probe moved a pending connection to active by proving its trust with a
                successful mint. Omitted (false) on every later probe of the same connection.
            failure (str | Unset): Human-readable reason the probe did not succeed, such as a suspended install or a
                rejected mint. Empty when ok is true.
            missing_permissions (list[str] | Unset): Permissions this service requires that the install has not granted at
                the required level. Reported, not enforced: accept the provider's pending permission request to clear them.
     """

    ok: bool
    resource_count: int
    state: str
    token_minted: bool
    activated: bool | Unset = UNSET
    failure: str | Unset = UNSET
    missing_permissions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        ok = self.ok

        resource_count = self.resource_count

        state = self.state

        token_minted = self.token_minted

        activated = self.activated

        failure = self.failure

        missing_permissions: list[str] | Unset = UNSET
        if not isinstance(self.missing_permissions, Unset):
            missing_permissions = self.missing_permissions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "ok": ok,
            "resource_count": resource_count,
            "state": state,
            "token_minted": token_minted,
        })
        if activated is not UNSET:
            field_dict["activated"] = activated
        if failure is not UNSET:
            field_dict["failure"] = failure
        if missing_permissions is not UNSET:
            field_dict["missing_permissions"] = missing_permissions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ok = d.pop("ok")

        resource_count = d.pop("resource_count")

        state = d.pop("state")

        token_minted = d.pop("token_minted")

        activated = d.pop("activated", UNSET)

        failure = d.pop("failure", UNSET)

        missing_permissions = cast(list[str], d.pop("missing_permissions", UNSET))


        managed_agents_connection_probe = cls(
            ok=ok,
            resource_count=resource_count,
            state=state,
            token_minted=token_minted,
            activated=activated,
            failure=failure,
            missing_permissions=missing_permissions,
        )


        managed_agents_connection_probe.additional_properties = d
        return managed_agents_connection_probe

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
