from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_unsigned_custom_event_source_verification_type import ManagedAgentsUnsignedCustomEventSourceVerificationType






T = TypeVar("T", bound="ManagedAgentsUnsignedCustomEventSourceVerification")



@_attrs_define
class ManagedAgentsUnsignedCustomEventSourceVerification:
    """ Explicit unsigned-delivery policy for a custom webhook.

        Example:
            {'type': 'none'}

        Attributes:
            type_ (ManagedAgentsUnsignedCustomEventSourceVerificationType): Accept deliveries without a cryptographic
                signature.
     """

    type_: ManagedAgentsUnsignedCustomEventSourceVerificationType





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = ManagedAgentsUnsignedCustomEventSourceVerificationType(d.pop("type"))




        managed_agents_unsigned_custom_event_source_verification = cls(
            type_=type_,
        )

        return managed_agents_unsigned_custom_event_source_verification

