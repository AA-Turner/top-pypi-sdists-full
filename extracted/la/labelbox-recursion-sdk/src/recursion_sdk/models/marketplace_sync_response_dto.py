from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="MarketplaceSyncResponseDto")



@_attrs_define
class MarketplaceSyncResponseDto:
    """ Summary of a marketplace sync run against the upstream container registry.

        Attributes:
            upserted (float): Number of marketplace images created or updated during the sync. Example: 12.
            deleted (float): Number of marketplace images removed because they no longer exist upstream. Example: 1.
            errors (list[str]): Human-readable error messages for any images that failed to sync.
     """

    upserted: float
    deleted: float
    errors: list[str]





    def to_dict(self) -> dict[str, Any]:
        upserted = self.upserted

        deleted = self.deleted

        errors = self.errors




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "upserted": upserted,
            "deleted": deleted,
            "errors": errors,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        upserted = d.pop("upserted")

        deleted = d.pop("deleted")

        errors = cast(list[str], d.pop("errors"))


        marketplace_sync_response_dto = cls(
            upserted=upserted,
            deleted=deleted,
            errors=errors,
        )

        return marketplace_sync_response_dto

