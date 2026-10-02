from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_evaluation_body_dto_metadata_schema_version import CreateEvaluationBodyDtoMetadataSchemaVersion
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_evaluation_body_dto_metadata_retry_policy import CreateEvaluationBodyDtoMetadataRetryPolicy





T = TypeVar("T", bound="CreateEvaluationBodyDtoMetadata")



@_attrs_define
class CreateEvaluationBodyDtoMetadata:
    """ Versioned orchestration metadata persisted on an evaluation.

        Attributes:
            schema_version (CreateEvaluationBodyDtoMetadataSchemaVersion): Version discriminant of the metadata shape.
                Always 1 today.
            attempts_per_problem (int): Number of attempts each solver makes against each problem (1-25).
            success_threshold (float | Unset): Score at or above which an attempt counts as a pass in aggregated results.
                Omitted means the platform default (0.5) applies at read time.
            retry_policy (CreateEvaluationBodyDtoMetadataRetryPolicy | Unset): Infra-retry policy override applied to every
                problem run in this evaluation, taking precedence over the run-config-level override when both are set. Omit to
                use the run-config value (or the platform default if neither is set).
     """

    schema_version: CreateEvaluationBodyDtoMetadataSchemaVersion
    attempts_per_problem: int
    success_threshold: float | Unset = UNSET
    retry_policy: CreateEvaluationBodyDtoMetadataRetryPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_evaluation_body_dto_metadata_retry_policy import CreateEvaluationBodyDtoMetadataRetryPolicy # noqa: PLC0415
        schema_version = self.schema_version.value

        attempts_per_problem = self.attempts_per_problem

        success_threshold = self.success_threshold

        retry_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retry_policy, Unset):
            retry_policy = self.retry_policy.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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
        from ..models.create_evaluation_body_dto_metadata_retry_policy import CreateEvaluationBodyDtoMetadataRetryPolicy # noqa: PLC0415
        d = dict(src_dict)
        schema_version = CreateEvaluationBodyDtoMetadataSchemaVersion(d.pop("schemaVersion"))




        attempts_per_problem = d.pop("attemptsPerProblem")

        success_threshold = d.pop("successThreshold", UNSET)

        _retry_policy = d.pop("retryPolicy", UNSET)
        retry_policy: CreateEvaluationBodyDtoMetadataRetryPolicy | Unset
        if isinstance(_retry_policy,  Unset):
            retry_policy = UNSET
        else:
            retry_policy = CreateEvaluationBodyDtoMetadataRetryPolicy.from_dict(_retry_policy)




        create_evaluation_body_dto_metadata = cls(
            schema_version=schema_version,
            attempts_per_problem=attempts_per_problem,
            success_threshold=success_threshold,
            retry_policy=retry_policy,
        )


        create_evaluation_body_dto_metadata.additional_properties = d
        return create_evaluation_body_dto_metadata

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
