from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.create_problem_with_version_response_dto_problem import CreateProblemWithVersionResponseDtoProblem
  from ..models.create_problem_with_version_response_dto_version import CreateProblemWithVersionResponseDtoVersion





T = TypeVar("T", bound="CreateProblemWithVersionResponseDto")



@_attrs_define
class CreateProblemWithVersionResponseDto:
    """ Response bundling a problem and its initial version, with a created flag distinguishing fresh from idempotent
    results.

        Example:
            {'problem': {'id': '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'environmentId':
                '784e2386-e297-4f9d-a886-838422383b65', 'externalId': 'detect-surface-defects', 'title': 'Detect surface defects
                on machined parts', 'isTemplate': False, 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt':
                '2026-01-16T14:20:00.000Z'}, 'version': {'id': '0c3ac467-57e1-4074-b57d-b6a7be392f71', 'problemId':
                '2d3fe029-a7d1-4747-9d09-81b976087bbb', 'environmentId': '784e2386-e297-4f9d-a886-838422383b65', 'version':
                'v3', 'prompt': 'You are a manufacturing QA agent. Inspect the metal panel image at /workspace/panel.png and
                identify every surface defect (scratch, dent, corrosion). Write a JSON report to /workspace/report.json with one
                entry per defect: { "type", "bbox": [x, y, w, h], "severity": "low" | "medium" | "high" }.', 'tools': ['Read',
                'Write', 'Bash'], 'installedPackageManagers': ['pip'], 'containerImage': 'python:3.12', 'containerSize':
                'medium', 'gpuType': None, 'timeoutSeconds': 7200, 'toolTimeouts': {'Bash': 300}, 'maxTurns': 50,
                'gradingConfig': {'type': 'rubric'}, 'singleAgentRubric': True, 'privileged': False, 'issueTemplate': None,
                'solverRunConfigVersionId': '39088cb6-ca62-4544-a074-fc66e10807ad', 'graderRunConfigVersionId': None,
                'qaRunConfigVersionId': None, 'synthesizerRunConfigVersionId': None, 'worldsimConfig': None, 'lockedAt':
                '2026-01-16T14:20:00.000Z', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T14:20:00.000Z'},
                'created': True}

        Attributes:
            problem (CreateProblemWithVersionResponseDtoProblem): The created or existing problem.
            version (CreateProblemWithVersionResponseDtoVersion): The initial version associated with the problem.
            created (bool): True when a new problem was created (201); false when an existing one was returned (200).
     """

    problem: CreateProblemWithVersionResponseDtoProblem
    version: CreateProblemWithVersionResponseDtoVersion
    created: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_problem_with_version_response_dto_problem import CreateProblemWithVersionResponseDtoProblem # noqa: PLC0415
        from ..models.create_problem_with_version_response_dto_version import CreateProblemWithVersionResponseDtoVersion # noqa: PLC0415
        problem = self.problem.to_dict()

        version = self.version.to_dict()

        created = self.created


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problem": problem,
            "version": version,
            "created": created,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_problem_with_version_response_dto_problem import CreateProblemWithVersionResponseDtoProblem # noqa: PLC0415
        from ..models.create_problem_with_version_response_dto_version import CreateProblemWithVersionResponseDtoVersion # noqa: PLC0415
        d = dict(src_dict)
        problem = CreateProblemWithVersionResponseDtoProblem.from_dict(d.pop("problem"))




        version = CreateProblemWithVersionResponseDtoVersion.from_dict(d.pop("version"))




        created = d.pop("created")

        create_problem_with_version_response_dto = cls(
            problem=problem,
            version=version,
            created=created,
        )

        return create_problem_with_version_response_dto

