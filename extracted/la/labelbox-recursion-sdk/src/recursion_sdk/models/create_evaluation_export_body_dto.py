from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_evaluation_export_body_dto_format import CreateEvaluationExportBodyDtoFormat
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="CreateEvaluationExportBodyDto")



@_attrs_define
class CreateEvaluationExportBodyDto:
    """ Request body for creating an evaluation-results export. The evaluation id comes from the URL and the user from auth
    context.

        Example:
            {'format': 'csv', 'includeCosts': True, 'includeTimestamps': True, 'includeErrors': True,
                'includeGradingRationale': False, 'includeTranscripts': False}

        Attributes:
            format_ (CreateEvaluationExportBodyDtoFormat): Output format for the export artifact.
            include_costs (bool): When true, include per-run cost columns in the output.
            include_timestamps (bool): When true, include start/end timestamp columns in the output.
            include_errors (bool): When true, include error-message columns for failed runs.
            include_grading_rationale (bool): When true, include the grader rationale text alongside the score.
            include_transcripts (bool): When true, emit a tar.gz archive with the data file plus each available run
                transcript in the transcripts directory, named <problem_run_id>.txt and keyed by the full stable problem-run
                UUID.
            solver_ids (list[UUID] | Unset): Optional filter restricting the export to specific evaluation solvers. Omit to
                include all solvers. Empty arrays are rejected.
            problem_version_ids (list[UUID] | Unset): Optional filter restricting the export to specific problem versions.
                Omit to include all problem versions. Empty arrays are rejected.
     """

    format_: CreateEvaluationExportBodyDtoFormat
    include_costs: bool
    include_timestamps: bool
    include_errors: bool
    include_grading_rationale: bool
    include_transcripts: bool
    solver_ids: list[UUID] | Unset = UNSET
    problem_version_ids: list[UUID] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        format_ = self.format_.value

        include_costs = self.include_costs

        include_timestamps = self.include_timestamps

        include_errors = self.include_errors

        include_grading_rationale = self.include_grading_rationale

        include_transcripts = self.include_transcripts

        solver_ids: list[str] | Unset = UNSET
        if not isinstance(self.solver_ids, Unset):
            solver_ids = []
            for solver_ids_item_data in self.solver_ids:
                solver_ids_item = str(solver_ids_item_data)
                solver_ids.append(solver_ids_item)



        problem_version_ids: list[str] | Unset = UNSET
        if not isinstance(self.problem_version_ids, Unset):
            problem_version_ids = []
            for problem_version_ids_item_data in self.problem_version_ids:
                problem_version_ids_item = str(problem_version_ids_item_data)
                problem_version_ids.append(problem_version_ids_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "format": format_,
            "includeCosts": include_costs,
            "includeTimestamps": include_timestamps,
            "includeErrors": include_errors,
            "includeGradingRationale": include_grading_rationale,
            "includeTranscripts": include_transcripts,
        })
        if solver_ids is not UNSET:
            field_dict["solverIds"] = solver_ids
        if problem_version_ids is not UNSET:
            field_dict["problemVersionIds"] = problem_version_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        format_ = CreateEvaluationExportBodyDtoFormat(d.pop("format"))




        include_costs = d.pop("includeCosts")

        include_timestamps = d.pop("includeTimestamps")

        include_errors = d.pop("includeErrors")

        include_grading_rationale = d.pop("includeGradingRationale")

        include_transcripts = d.pop("includeTranscripts")

        _solver_ids = d.pop("solverIds", UNSET)
        solver_ids: list[UUID] | Unset = UNSET
        if _solver_ids is not UNSET:
            solver_ids = []
            for solver_ids_item_data in _solver_ids:
                solver_ids_item = UUID(solver_ids_item_data)



                solver_ids.append(solver_ids_item)


        _problem_version_ids = d.pop("problemVersionIds", UNSET)
        problem_version_ids: list[UUID] | Unset = UNSET
        if _problem_version_ids is not UNSET:
            problem_version_ids = []
            for problem_version_ids_item_data in _problem_version_ids:
                problem_version_ids_item = UUID(problem_version_ids_item_data)



                problem_version_ids.append(problem_version_ids_item)


        create_evaluation_export_body_dto = cls(
            format_=format_,
            include_costs=include_costs,
            include_timestamps=include_timestamps,
            include_errors=include_errors,
            include_grading_rationale=include_grading_rationale,
            include_transcripts=include_transcripts,
            solver_ids=solver_ids,
            problem_version_ids=problem_version_ids,
        )


        create_evaluation_export_body_dto.additional_properties = d
        return create_evaluation_export_body_dto

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
