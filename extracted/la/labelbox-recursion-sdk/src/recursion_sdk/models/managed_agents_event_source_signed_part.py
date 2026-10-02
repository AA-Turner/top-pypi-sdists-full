from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_source_signed_part_kind import ManagedAgentsEventSourceSignedPartKind






T = TypeVar("T", bound="ManagedAgentsEventSourceSignedPart")



@_attrs_define
class ManagedAgentsEventSourceSignedPart:
    """ One ordered component of the HMAC signature input.

        Example:
            {'kind': 'body'}

        Attributes:
            kind (ManagedAgentsEventSourceSignedPartKind): Delivery component included in the signature input; currently the
                exact request body.
     """

    kind: ManagedAgentsEventSourceSignedPartKind





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ManagedAgentsEventSourceSignedPartKind(d.pop("kind"))




        managed_agents_event_source_signed_part = cls(
            kind=kind,
        )

        return managed_agents_event_source_signed_part

