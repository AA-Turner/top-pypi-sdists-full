from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ResolvedRunConfigDtoConfigRetryPolicy")



@_attrs_define
class ResolvedRunConfigDtoConfigRetryPolicy:
    """ Infra-retry policy override for runs launched from this run-config. Omit to use the platform default; an eval-level
    override (EvaluationMetadataSchema.retryPolicy) takes precedence over this when both are set.

        Attributes:
            max_infra_retries (int | Unset): Additional attempts allowed after a failure classified as infra (container
                eviction, image pull error, queue orphan) before the run terminates as failed. Omit to use the platform default
                (2).
     """

    max_infra_retries: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        max_infra_retries = self.max_infra_retries


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if max_infra_retries is not UNSET:
            field_dict["maxInfraRetries"] = max_infra_retries

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        max_infra_retries = d.pop("maxInfraRetries", UNSET)

        resolved_run_config_dto_config_retry_policy = cls(
            max_infra_retries=max_infra_retries,
        )

        return resolved_run_config_dto_config_retry_policy

