from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="FilterState")



@_attrs_define
class FilterState:
    """ The dashboard/Insights filter bar's own saved shape (and the
    Branches page's status, forge, advisories and search, in a `branches` group) —
    whatever the frontend's `$lib/filters` `loadState`/`saveState` already produce
    client-side (shared forge/repo/label/author/title/created/
    updated/groupBy, plus the two board-owned extras with no
    equivalent on the other entity type). `shared.label`,
    `shared.repo` (forge-qualified, `forge:owner/name`) and
    `shared.author` are each one lowercase value, or several separated
    by a newline: the filter matches an item with any of them, and a
    single value saved before they took several still reads as a list
    of one. At most 20 values and 1000 characters in each, with no
    control character other than the separator; a save over either is
    refused. This server stores and
    returns it verbatim, byte for byte, and apart from those limits never parses or
    validates its shape — the same "opaque blob, not this layer's
    concern" treatment WebAuthnCeremonyOptions above gets, so a
    client-side shape change here never needs a matching spec change.

     """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        filter_state = cls(
        )


        filter_state.additional_properties = d
        return filter_state

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
