from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_run_execution_evidence_dto_handoff_clone_from_run_id_status import ProblemRunExecutionEvidenceDtoHandoffCloneFromRunIdStatus
from ..models.problem_run_execution_evidence_dto_handoff_episode_artifact_ref_status import ProblemRunExecutionEvidenceDtoHandoffEpisodeArtifactRefStatus
from typing import cast






T = TypeVar("T", bound="ProblemRunExecutionEvidenceDtoHandoff")



@_attrs_define
class ProblemRunExecutionEvidenceDtoHandoff:
    """ Evidence about the solver-to-grader state handoff. It does not claim live restore verification.

        Attributes:
            clone_from_run_id (None | str): Solver run ID supplied as clone_from_run_id when grading is dispatched; null
                before solver submission.
            clone_from_run_id_status (ProblemRunExecutionEvidenceDtoHandoffCloneFromRunIdStatus): Whether an execution
                handoff fact is verified by persisted evidence.
            episode_artifact_ref_status (ProblemRunExecutionEvidenceDtoHandoffEpisodeArtifactRefStatus): Whether an
                execution handoff fact is verified by persisted evidence.
     """

    clone_from_run_id: None | str
    clone_from_run_id_status: ProblemRunExecutionEvidenceDtoHandoffCloneFromRunIdStatus
    episode_artifact_ref_status: ProblemRunExecutionEvidenceDtoHandoffEpisodeArtifactRefStatus





    def to_dict(self) -> dict[str, Any]:
        clone_from_run_id: None | str
        clone_from_run_id = self.clone_from_run_id

        clone_from_run_id_status = self.clone_from_run_id_status.value

        episode_artifact_ref_status = self.episode_artifact_ref_status.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cloneFromRunId": clone_from_run_id,
            "cloneFromRunIdStatus": clone_from_run_id_status,
            "episodeArtifactRefStatus": episode_artifact_ref_status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_clone_from_run_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        clone_from_run_id = _parse_clone_from_run_id(d.pop("cloneFromRunId"))


        clone_from_run_id_status = ProblemRunExecutionEvidenceDtoHandoffCloneFromRunIdStatus(d.pop("cloneFromRunIdStatus"))




        episode_artifact_ref_status = ProblemRunExecutionEvidenceDtoHandoffEpisodeArtifactRefStatus(d.pop("episodeArtifactRefStatus"))




        problem_run_execution_evidence_dto_handoff = cls(
            clone_from_run_id=clone_from_run_id,
            clone_from_run_id_status=clone_from_run_id_status,
            episode_artifact_ref_status=episode_artifact_ref_status,
        )

        return problem_run_execution_evidence_dto_handoff

