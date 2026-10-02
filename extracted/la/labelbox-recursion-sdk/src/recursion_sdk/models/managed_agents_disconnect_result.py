from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsDisconnectResult")



@_attrs_define
class ManagedAgentsDisconnectResult:
    """ Summary of what removing an integration connection retired. Returned when a connection is disconnected, so a caller
    can see how many vault grants it invalidated.

        Example:
            {'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'deleted': True, 'grants_revoked': 1}

        Attributes:
            connection_id (str): Connection that was disconnected (UUID). Adding the same GitHub installation later creates
                a new connection; saved agent references remain on this retired ID.
            deleted (bool): Always true on success: the connection row was soft-deleted and this service will no longer mint
                tokens for it. The app itself is deliberately left installed at the provider.
            grants_revoked (int): Number of vault grants that referenced this connection and have stopped working. They are
                not restored by reconnecting and must be recreated.
     """

    connection_id: str
    deleted: bool
    grants_revoked: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        connection_id = self.connection_id

        deleted = self.deleted

        grants_revoked = self.grants_revoked


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "connection_id": connection_id,
            "deleted": deleted,
            "grants_revoked": grants_revoked,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        connection_id = d.pop("connection_id")

        deleted = d.pop("deleted")

        grants_revoked = d.pop("grants_revoked")

        managed_agents_disconnect_result = cls(
            connection_id=connection_id,
            deleted=deleted,
            grants_revoked=grants_revoked,
        )


        managed_agents_disconnect_result.additional_properties = d
        return managed_agents_disconnect_result

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
