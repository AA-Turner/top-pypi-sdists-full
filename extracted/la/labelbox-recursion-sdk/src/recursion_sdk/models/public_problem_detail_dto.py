from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.public_problem_detail_dto_problem import PublicProblemDetailDtoProblem
  from ..models.public_problem_detail_dto_rubrics_by_version_id import PublicProblemDetailDtoRubricsByVersionId
  from ..models.public_problem_detail_dto_runs import PublicProblemDetailDtoRuns
  from ..models.public_problem_detail_dto_versions_item import PublicProblemDetailDtoVersionsItem





T = TypeVar("T", bound="PublicProblemDetailDto")



@_attrs_define
class PublicProblemDetailDto:
    """ Read-only problem detail exposed to unauthenticated public-catalogue visitors.

        Attributes:
            problem (PublicProblemDetailDtoProblem): The problem, confirmed to belong to the public environment.
            versions (list[PublicProblemDetailDtoVersionsItem]): Locked versions of the problem, ordered oldest-first by
                version number. Draft (unlocked) versions are excluded.
            rubrics_by_version_id (PublicProblemDetailDtoRubricsByVersionId): Rubric criteria for each returned version,
                keyed by problem-version id.
            runs (PublicProblemDetailDtoRuns): Execution summaries for the returned locked versions.
     """

    problem: PublicProblemDetailDtoProblem
    versions: list[PublicProblemDetailDtoVersionsItem]
    rubrics_by_version_id: PublicProblemDetailDtoRubricsByVersionId
    runs: PublicProblemDetailDtoRuns





    def to_dict(self) -> dict[str, Any]:
        from ..models.public_problem_detail_dto_problem import PublicProblemDetailDtoProblem # noqa: PLC0415
        from ..models.public_problem_detail_dto_rubrics_by_version_id import PublicProblemDetailDtoRubricsByVersionId # noqa: PLC0415
        from ..models.public_problem_detail_dto_runs import PublicProblemDetailDtoRuns # noqa: PLC0415
        from ..models.public_problem_detail_dto_versions_item import PublicProblemDetailDtoVersionsItem # noqa: PLC0415
        problem = self.problem.to_dict()

        versions = []
        for versions_item_data in self.versions:
            versions_item = versions_item_data.to_dict()
            versions.append(versions_item)



        rubrics_by_version_id = self.rubrics_by_version_id.to_dict()

        runs = self.runs.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problem": problem,
            "versions": versions,
            "rubricsByVersionId": rubrics_by_version_id,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.public_problem_detail_dto_problem import PublicProblemDetailDtoProblem # noqa: PLC0415
        from ..models.public_problem_detail_dto_rubrics_by_version_id import PublicProblemDetailDtoRubricsByVersionId # noqa: PLC0415
        from ..models.public_problem_detail_dto_runs import PublicProblemDetailDtoRuns # noqa: PLC0415
        from ..models.public_problem_detail_dto_versions_item import PublicProblemDetailDtoVersionsItem # noqa: PLC0415
        d = dict(src_dict)
        problem = PublicProblemDetailDtoProblem.from_dict(d.pop("problem"))




        versions = []
        _versions = d.pop("versions")
        for versions_item_data in (_versions):
            versions_item = PublicProblemDetailDtoVersionsItem.from_dict(versions_item_data)



            versions.append(versions_item)


        rubrics_by_version_id = PublicProblemDetailDtoRubricsByVersionId.from_dict(d.pop("rubricsByVersionId"))




        runs = PublicProblemDetailDtoRuns.from_dict(d.pop("runs"))




        public_problem_detail_dto = cls(
            problem=problem,
            versions=versions,
            rubrics_by_version_id=rubrics_by_version_id,
            runs=runs,
        )

        return public_problem_detail_dto

