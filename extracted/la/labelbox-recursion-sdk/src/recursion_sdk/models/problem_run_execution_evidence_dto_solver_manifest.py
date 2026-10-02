from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_run_execution_evidence_dto_solver_manifest_availability import ProblemRunExecutionEvidenceDtoSolverManifestAvailability
from typing import cast






T = TypeVar("T", bound="ProblemRunExecutionEvidenceDtoSolverManifest")



@_attrs_define
class ProblemRunExecutionEvidenceDtoSolverManifest:
    """ Sanitized evidence extracted from the solver manifest.

        Attributes:
            availability (ProblemRunExecutionEvidenceDtoSolverManifestAvailability): Whether the solver manifest could be
                read and parsed.
            status (None | str): Status recorded by the solver manifest, if present.
            episode_id (None | str): Episode identifier recorded by the manifest.
            episode_artifact_ref (None | str): Episode artifact reference recorded by the manifest.
     """

    availability: ProblemRunExecutionEvidenceDtoSolverManifestAvailability
    status: None | str
    episode_id: None | str
    episode_artifact_ref: None | str





    def to_dict(self) -> dict[str, Any]:
        availability = self.availability.value

        status: None | str
        status = self.status

        episode_id: None | str
        episode_id = self.episode_id

        episode_artifact_ref: None | str
        episode_artifact_ref = self.episode_artifact_ref


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "availability": availability,
            "status": status,
            "episodeId": episode_id,
            "episodeArtifactRef": episode_artifact_ref,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        availability = ProblemRunExecutionEvidenceDtoSolverManifestAvailability(d.pop("availability"))




        def _parse_status(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        status = _parse_status(d.pop("status"))


        def _parse_episode_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        episode_id = _parse_episode_id(d.pop("episodeId"))


        def _parse_episode_artifact_ref(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        episode_artifact_ref = _parse_episode_artifact_ref(d.pop("episodeArtifactRef"))


        problem_run_execution_evidence_dto_solver_manifest = cls(
            availability=availability,
            status=status,
            episode_id=episode_id,
            episode_artifact_ref=episode_artifact_ref,
        )

        return problem_run_execution_evidence_dto_solver_manifest

