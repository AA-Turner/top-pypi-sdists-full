from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ComputeOwnershipDto")



@_attrs_define
class ComputeOwnershipDto:
    """ Confirmation that the caller owns a compute.

        Example:
            {'ownsCompute': True}

        Attributes:
            owns_compute (bool): Whether the caller holds the reservation for this compute.
     """

    owns_compute: bool





    def to_dict(self) -> dict[str, Any]:
        owns_compute = self.owns_compute


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "ownsCompute": owns_compute,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        owns_compute = d.pop("ownsCompute")

        compute_ownership_dto = cls(
            owns_compute=owns_compute,
        )

        return compute_ownership_dto

