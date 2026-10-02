from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsDeletedResponse")



@_attrs_define
class ManagedAgentsDeletedResponse:
    """ Shared response body of every soft-delete endpoint, on agents, environments, tags, vaults, vault credentials,
    webhook bindings, and sessions. Soft delete is a tombstone, not an erase: the row stops appearing in list and get
    responses but is retained, and there is no undelete endpoint to bring it back. Irreversible erasure is the separate,
    confirmation-gated purge path.

        Example:
            {'deleted': True}

        Attributes:
            deleted (bool): Always true. The record was soft deleted and is now excluded from reads; a delete that did not
                happen is an HTTP error instead, so this field never reports false.
     """

    deleted: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        deleted = self.deleted


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "deleted": deleted,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        deleted = d.pop("deleted")

        managed_agents_deleted_response = cls(
            deleted=deleted,
        )


        managed_agents_deleted_response.additional_properties = d
        return managed_agents_deleted_response

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
