from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.compute_access_readiness_dto_status import ComputeAccessReadinessDtoStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="ComputeAccessReadinessDto")



@_attrs_define
class ComputeAccessReadinessDto:
    """ Application readiness for opening browser access to a compute.

        Example:
            {'status': 'pending'}

        Attributes:
            status (ComputeAccessReadinessDtoStatus): Current application readiness state.
            reason (str | Unset): Reason the application readiness probe failed, when status is failed.
     """

    status: ComputeAccessReadinessDtoStatus
    reason: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        reason = self.reason


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = ComputeAccessReadinessDtoStatus(d.pop("status"))




        reason = d.pop("reason", UNSET)

        compute_access_readiness_dto = cls(
            status=status,
            reason=reason,
        )

        return compute_access_readiness_dto

