from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.evaluation_detail_response_dto_metadata_schema_version import EvaluationDetailResponseDtoMetadataSchemaVersion
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.evaluation_detail_response_dto_metadata_retry_policy import EvaluationDetailResponseDtoMetadataRetryPolicy





T = TypeVar("T", bound="EvaluationDetailResponseDtoMetadata")



@_attrs_define
class EvaluationDetailResponseDtoMetadata:
    """ Orchestration metadata persisted on the evaluation (attempts per problem, success threshold).

        Attributes:
            schema_version (EvaluationDetailResponseDtoMetadataSchemaVersion): Version discriminant of the metadata shape.
                Always 1 today.
            attempts_per_problem (int): Number of attempts each solver makes against each problem (1-25).
            success_threshold (float | Unset): Score at or above which an attempt counts as a pass in aggregated results.
                Omitted means the platform default (0.5) applies at read time.
            retry_policy (EvaluationDetailResponseDtoMetadataRetryPolicy | Unset): Infra-retry policy override applied to
                every problem run in this evaluation, taking precedence over the run-config-level override when both are set.
                Omit to use the run-config value (or the platform default if neither is set).
     """

    schema_version: EvaluationDetailResponseDtoMetadataSchemaVersion
    attempts_per_problem: int
    success_threshold: float | Unset = UNSET
    retry_policy: EvaluationDetailResponseDtoMetadataRetryPolicy | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.evaluation_detail_response_dto_metadata_retry_policy import EvaluationDetailResponseDtoMetadataRetryPolicy # noqa: PLC0415
        schema_version = self.schema_version.value

        attempts_per_problem = self.attempts_per_problem

        success_threshold = self.success_threshold

        retry_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retry_policy, Unset):
            retry_policy = self.retry_policy.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schemaVersion": schema_version,
            "attemptsPerProblem": attempts_per_problem,
        })
        if success_threshold is not UNSET:
            field_dict["successThreshold"] = success_threshold
        if retry_policy is not UNSET:
            field_dict["retryPolicy"] = retry_policy

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.evaluation_detail_response_dto_metadata_retry_policy import EvaluationDetailResponseDtoMetadataRetryPolicy # noqa: PLC0415
        d = dict(src_dict)
        schema_version = EvaluationDetailResponseDtoMetadataSchemaVersion(d.pop("schemaVersion"))




        attempts_per_problem = d.pop("attemptsPerProblem")

        success_threshold = d.pop("successThreshold", UNSET)

        _retry_policy = d.pop("retryPolicy", UNSET)
        retry_policy: EvaluationDetailResponseDtoMetadataRetryPolicy | Unset
        if isinstance(_retry_policy,  Unset):
            retry_policy = UNSET
        else:
            retry_policy = EvaluationDetailResponseDtoMetadataRetryPolicy.from_dict(_retry_policy)




        evaluation_detail_response_dto_metadata = cls(
            schema_version=schema_version,
            attempts_per_problem=attempts_per_problem,
            success_threshold=success_threshold,
            retry_policy=retry_policy,
        )

        return evaluation_detail_response_dto_metadata

