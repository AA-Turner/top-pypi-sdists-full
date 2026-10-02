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
  from ..models.create_evaluation_body_dto_metadata import CreateEvaluationBodyDtoMetadata
  from ..models.create_evaluation_body_dto_problems_item import CreateEvaluationBodyDtoProblemsItem
  from ..models.create_evaluation_body_dto_solvers_item import CreateEvaluationBodyDtoSolversItem





T = TypeVar("T", bound="CreateEvaluationBodyDto")



@_attrs_define
class CreateEvaluationBodyDto:
    """ Input for creating a multi-problem comparison evaluation across one or more solvers.

        Example:
            {'name': 'claude-sonnet-baseline', 'description': 'Baseline run of Claude Sonnet against the surface-defect
                detection problem.', 'metadata': {'schemaVersion': 1, 'attemptsPerProblem': 3}, 'solvers': [{'displayName':
                'claude-sonnet-baseline', 'runConfigVersionId': 'e9d0f1c2-3e4a-4b6c-8d7e-9f0a1b2c3d4e'}], 'problems':
                [{'problemId': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'problemVersionId':
                '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'environmentId': '784e2386-e297-4f9d-a886-838422383b65'}]}

        Attributes:
            name (str): Human-readable display name for the evaluation.
            metadata (CreateEvaluationBodyDtoMetadata): Versioned orchestration metadata persisted on an evaluation.
            solvers (list[CreateEvaluationBodyDtoSolversItem]): Solvers to compare in the evaluation (1-20 entries).
            problems (list[CreateEvaluationBodyDtoProblemsItem]): Problems to include in the evaluation (one or more).
            description (str | Unset): Free-form description of the evaluation. Omit to leave empty.
            grader_run_config_version_id (UUID | Unset): Locked run-config version (kind "grader") to pin as the grader for
                every run in this evaluation. Omit to fall back to the problem-version / environment grader default.
            tags (list[str] | Unset): Free-form tags for list filtering. Omit to leave the evaluation untagged.
     """

    name: str
    metadata: CreateEvaluationBodyDtoMetadata
    solvers: list[CreateEvaluationBodyDtoSolversItem]
    problems: list[CreateEvaluationBodyDtoProblemsItem]
    description: str | Unset = UNSET
    grader_run_config_version_id: UUID | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_evaluation_body_dto_metadata import CreateEvaluationBodyDtoMetadata # noqa: PLC0415
        from ..models.create_evaluation_body_dto_problems_item import CreateEvaluationBodyDtoProblemsItem # noqa: PLC0415
        from ..models.create_evaluation_body_dto_solvers_item import CreateEvaluationBodyDtoSolversItem # noqa: PLC0415
        name = self.name

        metadata = self.metadata.to_dict()

        solvers = []
        for solvers_item_data in self.solvers:
            solvers_item = solvers_item_data.to_dict()
            solvers.append(solvers_item)



        problems = []
        for problems_item_data in self.problems:
            problems_item = problems_item_data.to_dict()
            problems.append(problems_item)



        description = self.description

        grader_run_config_version_id: str | Unset = UNSET
        if not isinstance(self.grader_run_config_version_id, Unset):
            grader_run_config_version_id = str(self.grader_run_config_version_id)

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "metadata": metadata,
            "solvers": solvers,
            "problems": problems,
        })
        if description is not UNSET:
            field_dict["description"] = description
        if grader_run_config_version_id is not UNSET:
            field_dict["graderRunConfigVersionId"] = grader_run_config_version_id
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_evaluation_body_dto_metadata import CreateEvaluationBodyDtoMetadata # noqa: PLC0415
        from ..models.create_evaluation_body_dto_problems_item import CreateEvaluationBodyDtoProblemsItem # noqa: PLC0415
        from ..models.create_evaluation_body_dto_solvers_item import CreateEvaluationBodyDtoSolversItem # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        metadata = CreateEvaluationBodyDtoMetadata.from_dict(d.pop("metadata"))




        solvers = []
        _solvers = d.pop("solvers")
        for solvers_item_data in (_solvers):
            solvers_item = CreateEvaluationBodyDtoSolversItem.from_dict(solvers_item_data)



            solvers.append(solvers_item)


        problems = []
        _problems = d.pop("problems")
        for problems_item_data in (_problems):
            problems_item = CreateEvaluationBodyDtoProblemsItem.from_dict(problems_item_data)



            problems.append(problems_item)


        description = d.pop("description", UNSET)

        _grader_run_config_version_id = d.pop("graderRunConfigVersionId", UNSET)
        grader_run_config_version_id: UUID | Unset
        if isinstance(_grader_run_config_version_id,  Unset):
            grader_run_config_version_id = UNSET
        else:
            grader_run_config_version_id = UUID(_grader_run_config_version_id)




        tags = cast(list[str], d.pop("tags", UNSET))


        create_evaluation_body_dto = cls(
            name=name,
            metadata=metadata,
            solvers=solvers,
            problems=problems,
            description=description,
            grader_run_config_version_id=grader_run_config_version_id,
            tags=tags,
        )


        create_evaluation_body_dto.additional_properties = d
        return create_evaluation_body_dto

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
