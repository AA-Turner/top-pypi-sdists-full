from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.create_grade_only_evaluation_body_dto_graders_item import CreateGradeOnlyEvaluationBodyDtoGradersItem
  from ..models.create_grade_only_evaluation_body_dto_metadata import CreateGradeOnlyEvaluationBodyDtoMetadata





T = TypeVar("T", bound="CreateGradeOnlyEvaluationBodyDto")



@_attrs_define
class CreateGradeOnlyEvaluationBodyDto:
    """ Input for running selected grader configurations over existing solver trajectories.

        Example:
            {'name': 'Compare grader candidates', 'graders': [{'displayName': 'candidate-grader', 'runConfigVersionId':
                'f9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e'}], 'sourceProblemRunIds': ['e8f7a6b5-4c3d-4e2f-9a1b-0c8d7e6f5a4b']}

        Attributes:
            name (str): Human-readable display name for the evaluation.
            graders (list[CreateGradeOnlyEvaluationBodyDtoGradersItem]): Grader configs to compare — the columns of the
                comparison matrix (1-20 entries).
            source_problem_run_ids (list[UUID]): Existing trajectories (solver problem runs) to grade — the rows of the
                comparison matrix. Every id is individually authorized against the caller's scope; mixed-environment selections
                are rejected.
            description (str | Unset): Free-form description of the evaluation. Omit to leave empty.
            metadata (CreateGradeOnlyEvaluationBodyDtoMetadata | Unset): Optional orchestration metadata (success threshold,
                grader retry policy). Omit to accept platform defaults.
            tags (list[str] | Unset): Free-form tags for list filtering. Omit to leave the evaluation untagged.
     """

    name: str
    graders: list[CreateGradeOnlyEvaluationBodyDtoGradersItem]
    source_problem_run_ids: list[UUID]
    description: str | Unset = UNSET
    metadata: CreateGradeOnlyEvaluationBodyDtoMetadata | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_grade_only_evaluation_body_dto_graders_item import CreateGradeOnlyEvaluationBodyDtoGradersItem # noqa: PLC0415
        from ..models.create_grade_only_evaluation_body_dto_metadata import CreateGradeOnlyEvaluationBodyDtoMetadata # noqa: PLC0415
        name = self.name

        graders = []
        for graders_item_data in self.graders:
            graders_item = graders_item_data.to_dict()
            graders.append(graders_item)



        source_problem_run_ids = []
        for source_problem_run_ids_item_data in self.source_problem_run_ids:
            source_problem_run_ids_item = str(source_problem_run_ids_item_data)
            source_problem_run_ids.append(source_problem_run_ids_item)



        description = self.description

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "graders": graders,
            "sourceProblemRunIds": source_problem_run_ids,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_grade_only_evaluation_body_dto_graders_item import CreateGradeOnlyEvaluationBodyDtoGradersItem # noqa: PLC0415
        from ..models.create_grade_only_evaluation_body_dto_metadata import CreateGradeOnlyEvaluationBodyDtoMetadata # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        graders = []
        _graders = d.pop("graders")
        for graders_item_data in (_graders):
            graders_item = CreateGradeOnlyEvaluationBodyDtoGradersItem.from_dict(graders_item_data)



            graders.append(graders_item)


        source_problem_run_ids = []
        _source_problem_run_ids = d.pop("sourceProblemRunIds")
        for source_problem_run_ids_item_data in (_source_problem_run_ids):
            source_problem_run_ids_item = UUID(source_problem_run_ids_item_data)



            source_problem_run_ids.append(source_problem_run_ids_item)


        description = d.pop("description", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: CreateGradeOnlyEvaluationBodyDtoMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = CreateGradeOnlyEvaluationBodyDtoMetadata.from_dict(_metadata)




        tags = cast(list[str], d.pop("tags", UNSET))


        create_grade_only_evaluation_body_dto = cls(
            name=name,
            graders=graders,
            source_problem_run_ids=source_problem_run_ids,
            description=description,
            metadata=metadata,
            tags=tags,
        )


        create_grade_only_evaluation_body_dto.additional_properties = d
        return create_grade_only_evaluation_body_dto

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
