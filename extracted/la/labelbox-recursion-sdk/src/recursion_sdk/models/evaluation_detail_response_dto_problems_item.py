from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="EvaluationDetailResponseDtoProblemsItem")



@_attrs_define
class EvaluationDetailResponseDtoProblemsItem:
    """ One problem included in an evaluation, pinned to a specific version with rollup metadata.

        Attributes:
            id (UUID): Stable evaluation-problem identifier (UUID). Refers to one problem included in an evaluation.
            evaluation_id (UUID): Stable evaluation identifier (UUID). An evaluation is a multi-problem comparison run.
            problem_id (UUID): Stable problem identifier (UUID).
            problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have many versions; this
                points at one specific version.
            environment_id (UUID): Stable environment identifier (UUID).
            problem_title (None | str): Title of the referenced problem at the time it was added. Null when untitled.
            environment_name (str): Display name of the environment that owns the problem.
            version_label (str): Human-readable label of the pinned problem version (e.g., the version number).
            sort_order (int): Position of this problem in evaluation results, top-to-bottom. Example: 0.
     """

    id: UUID
    evaluation_id: UUID
    problem_id: UUID
    problem_version_id: UUID
    environment_id: UUID
    problem_title: None | str
    environment_name: str
    version_label: str
    sort_order: int





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        evaluation_id = str(self.evaluation_id)

        problem_id = str(self.problem_id)

        problem_version_id = str(self.problem_version_id)

        environment_id = str(self.environment_id)

        problem_title: None | str
        problem_title = self.problem_title

        environment_name = self.environment_name

        version_label = self.version_label

        sort_order = self.sort_order


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "evaluationId": evaluation_id,
            "problemId": problem_id,
            "problemVersionId": problem_version_id,
            "environmentId": environment_id,
            "problemTitle": problem_title,
            "environmentName": environment_name,
            "versionLabel": version_label,
            "sortOrder": sort_order,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        evaluation_id = UUID(d.pop("evaluationId"))




        problem_id = UUID(d.pop("problemId"))




        problem_version_id = UUID(d.pop("problemVersionId"))




        environment_id = UUID(d.pop("environmentId"))




        def _parse_problem_title(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        problem_title = _parse_problem_title(d.pop("problemTitle"))


        environment_name = d.pop("environmentName")

        version_label = d.pop("versionLabel")

        sort_order = d.pop("sortOrder")

        evaluation_detail_response_dto_problems_item = cls(
            id=id,
            evaluation_id=evaluation_id,
            problem_id=problem_id,
            problem_version_id=problem_version_id,
            environment_id=environment_id,
            problem_title=problem_title,
            environment_name=environment_name,
            version_label=version_label,
            sort_order=sort_order,
        )

        return evaluation_detail_response_dto_problems_item

