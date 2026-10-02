from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_grade_only_evaluation_body_dto_metadata_schema_version import CreateGradeOnlyEvaluationBodyDtoMetadataSchemaVersion
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_grade_only_evaluation_body_dto_metadata_retry_policy import CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy





T = TypeVar("T", bound="CreateGradeOnlyEvaluationBodyDtoMetadata")



@_attrs_define
class CreateGradeOnlyEvaluationBodyDtoMetadata:
    """ Optional orchestration metadata (success threshold, grader retry policy). Omit to accept platform defaults.

        Attributes:
            schema_version (CreateGradeOnlyEvaluationBodyDtoMetadataSchemaVersion): Version discriminant of the metadata
                shape. Always 1 today.
            success_threshold (float | Unset): Score at or above which a grade counts as a pass in the comparison view.
                Omitted means the platform default (0.5) applies at read time.
            retry_policy (CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy | Unset): Infra-retry policy override applied
                to every grader container in this evaluation. Omit to use the grader run-config value (or the platform default
                if neither is set).
     """

    schema_version: CreateGradeOnlyEvaluationBodyDtoMetadataSchemaVersion
    success_threshold: float | Unset = UNSET
    retry_policy: CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_grade_only_evaluation_body_dto_metadata_retry_policy import CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy # noqa: PLC0415
        schema_version = self.schema_version.value

        success_threshold = self.success_threshold

        retry_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.retry_policy, Unset):
            retry_policy = self.retry_policy.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "schemaVersion": schema_version,
        })
        if success_threshold is not UNSET:
            field_dict["successThreshold"] = success_threshold
        if retry_policy is not UNSET:
            field_dict["retryPolicy"] = retry_policy

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_grade_only_evaluation_body_dto_metadata_retry_policy import CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy # noqa: PLC0415
        d = dict(src_dict)
        schema_version = CreateGradeOnlyEvaluationBodyDtoMetadataSchemaVersion(d.pop("schemaVersion"))




        success_threshold = d.pop("successThreshold", UNSET)

        _retry_policy = d.pop("retryPolicy", UNSET)
        retry_policy: CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy | Unset
        if isinstance(_retry_policy,  Unset):
            retry_policy = UNSET
        else:
            retry_policy = CreateGradeOnlyEvaluationBodyDtoMetadataRetryPolicy.from_dict(_retry_policy)




        create_grade_only_evaluation_body_dto_metadata = cls(
            schema_version=schema_version,
            success_threshold=success_threshold,
            retry_policy=retry_policy,
        )


        create_grade_only_evaluation_body_dto_metadata.additional_properties = d
        return create_grade_only_evaluation_body_dto_metadata

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
