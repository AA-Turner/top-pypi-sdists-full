from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="HasCompletedRunResponseDto")



@_attrs_define
class HasCompletedRunResponseDto:
    """ Response payload indicating whether a problem has any completed runs.

        Example:
            {'hasCompletedRun': True}

        Attributes:
            has_completed_run (bool): True when the problem has at least one run that reached a terminal status.
     """

    has_completed_run: bool





    def to_dict(self) -> dict[str, Any]:
        has_completed_run = self.has_completed_run


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "hasCompletedRun": has_completed_run,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        has_completed_run = d.pop("hasCompletedRun")

        has_completed_run_response_dto = cls(
            has_completed_run=has_completed_run,
        )

        return has_completed_run_response_dto

