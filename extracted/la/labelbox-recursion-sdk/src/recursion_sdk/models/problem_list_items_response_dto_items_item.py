from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.problem_list_items_response_dto_items_item_avg_score_type_0 import ProblemListItemsResponseDtoItemsItemAvgScoreType0
  from ..models.problem_list_items_response_dto_items_item_latest_run_type_0 import ProblemListItemsResponseDtoItemsItemLatestRunType0
  from ..models.problem_list_items_response_dto_items_item_recent_runs_item import ProblemListItemsResponseDtoItemsItemRecentRunsItem





T = TypeVar("T", bound="ProblemListItemsResponseDtoItemsItem")



@_attrs_define
class ProblemListItemsResponseDtoItemsItem:
    """ A problem augmented with aggregate stats and latest-run information used by the environment-overview list.

        Attributes:
            id (UUID): Stable problem identifier (UUID).
            environment_id (UUID): Environment this problem belongs to.
            external_id (None | str): Caller-provided external identifier for this problem. Null when no external system
                tracks it.
            is_template (bool): True for environment-scoped seed problems used as templates; false for regular problems.
                Templates are hidden from public lists and rejected by mutation routes.
            created_at (datetime.datetime): Timestamp when the problem was created (ISO-8601, UTC).
            updated_at (datetime.datetime): Timestamp when the problem was last updated (ISO-8601, UTC).
            latest_version_created_at (datetime.datetime | None): Timestamp when the most recent problem version was created
                (ISO-8601, UTC). Null when the problem has no versions.
            has_locked_version (bool): True when the problem has at least one locked (immutable) version.
            is_draft (bool): True when the most recent problem version is unlocked (or the problem has no versions yet),
                meaning it is still editable.
            total_cost_usd (float | None): Total USD spend across all runs of this problem. Null when no run costs are
                recorded.
            runs_count (int): Total number of problem runs recorded for this problem.
            models (list[str]): Distinct models that have produced at least one run for this problem.
            avg_score (None | ProblemListItemsResponseDtoItemsItemAvgScoreType0): Average / min / max problem-run score for
                this problem. Null when no graded runs exist.
            best_score (float | None): Best problem-run grader score for this problem. Null when no graded runs exist. May
                be negative. Example: 0.95.
            latest_run (None | ProblemListItemsResponseDtoItemsItemLatestRunType0): Summary of the latest run for this
                problem. Null when no runs exist.
            recent_runs (list[ProblemListItemsResponseDtoItemsItemRecentRunsItem]): Up to RECENT_RUNS_LIMIT most-recent runs
                for the sparkline, newest first.
            preview_file_url (None | str): Signed URL for the most recent completed run's output file matching the
                environment's previewFilename, or null when no preview is available.
            title (None | str | Unset): Human-readable problem title shown in lists and detail views.
            description (None | str | Unset): Free-text description of the problem. Null when unset.
            domain (None | str | Unset): Problem domain (e.g. the subject area the task belongs to). Null when unset.
     """

    id: UUID
    environment_id: UUID
    external_id: None | str
    is_template: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    latest_version_created_at: datetime.datetime | None
    has_locked_version: bool
    is_draft: bool
    total_cost_usd: float | None
    runs_count: int
    models: list[str]
    avg_score: None | ProblemListItemsResponseDtoItemsItemAvgScoreType0
    best_score: float | None
    latest_run: None | ProblemListItemsResponseDtoItemsItemLatestRunType0
    recent_runs: list[ProblemListItemsResponseDtoItemsItemRecentRunsItem]
    preview_file_url: None | str
    title: None | str | Unset = UNSET
    description: None | str | Unset = UNSET
    domain: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.problem_list_items_response_dto_items_item_avg_score_type_0 import ProblemListItemsResponseDtoItemsItemAvgScoreType0 # noqa: PLC0415
        from ..models.problem_list_items_response_dto_items_item_latest_run_type_0 import ProblemListItemsResponseDtoItemsItemLatestRunType0 # noqa: PLC0415
        from ..models.problem_list_items_response_dto_items_item_recent_runs_item import ProblemListItemsResponseDtoItemsItemRecentRunsItem # noqa: PLC0415
        id = str(self.id)

        environment_id = str(self.environment_id)

        external_id: None | str
        external_id = self.external_id

        is_template = self.is_template

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        latest_version_created_at: None | str
        if isinstance(self.latest_version_created_at, datetime.datetime):
            latest_version_created_at = self.latest_version_created_at.isoformat()
        else:
            latest_version_created_at = self.latest_version_created_at

        has_locked_version = self.has_locked_version

        is_draft = self.is_draft

        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd

        runs_count = self.runs_count

        models = self.models



        avg_score: dict[str, Any] | None
        if isinstance(self.avg_score, ProblemListItemsResponseDtoItemsItemAvgScoreType0):
            avg_score = self.avg_score.to_dict()
        else:
            avg_score = self.avg_score

        best_score: float | None
        best_score = self.best_score

        latest_run: dict[str, Any] | None
        if isinstance(self.latest_run, ProblemListItemsResponseDtoItemsItemLatestRunType0):
            latest_run = self.latest_run.to_dict()
        else:
            latest_run = self.latest_run

        recent_runs = []
        for recent_runs_item_data in self.recent_runs:
            recent_runs_item = recent_runs_item_data.to_dict()
            recent_runs.append(recent_runs_item)



        preview_file_url: None | str
        preview_file_url = self.preview_file_url

        title: None | str | Unset
        if isinstance(self.title, Unset):
            title = UNSET
        else:
            title = self.title

        description: None | str | Unset
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        domain: None | str | Unset
        if isinstance(self.domain, Unset):
            domain = UNSET
        else:
            domain = self.domain


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "environmentId": environment_id,
            "externalId": external_id,
            "isTemplate": is_template,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "latestVersionCreatedAt": latest_version_created_at,
            "hasLockedVersion": has_locked_version,
            "isDraft": is_draft,
            "totalCostUsd": total_cost_usd,
            "runsCount": runs_count,
            "models": models,
            "avgScore": avg_score,
            "bestScore": best_score,
            "latestRun": latest_run,
            "recentRuns": recent_runs,
            "previewFileUrl": preview_file_url,
        })
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if domain is not UNSET:
            field_dict["domain"] = domain

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.problem_list_items_response_dto_items_item_avg_score_type_0 import ProblemListItemsResponseDtoItemsItemAvgScoreType0 # noqa: PLC0415
        from ..models.problem_list_items_response_dto_items_item_latest_run_type_0 import ProblemListItemsResponseDtoItemsItemLatestRunType0 # noqa: PLC0415
        from ..models.problem_list_items_response_dto_items_item_recent_runs_item import ProblemListItemsResponseDtoItemsItemRecentRunsItem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        environment_id = UUID(d.pop("environmentId"))




        def _parse_external_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        external_id = _parse_external_id(d.pop("externalId"))


        is_template = d.pop("isTemplate")

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        def _parse_latest_version_created_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                latest_version_created_at_type_0 = datetime.datetime.fromisoformat(data)



                return latest_version_created_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        latest_version_created_at = _parse_latest_version_created_at(d.pop("latestVersionCreatedAt"))


        has_locked_version = d.pop("hasLockedVersion")

        is_draft = d.pop("isDraft")

        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        runs_count = d.pop("runsCount")

        models = cast(list[str], d.pop("models"))


        def _parse_avg_score(data: object) -> None | ProblemListItemsResponseDtoItemsItemAvgScoreType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                avg_score_type_0 = ProblemListItemsResponseDtoItemsItemAvgScoreType0.from_dict(data)



                return avg_score_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemListItemsResponseDtoItemsItemAvgScoreType0, data)

        avg_score = _parse_avg_score(d.pop("avgScore"))


        def _parse_best_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        best_score = _parse_best_score(d.pop("bestScore"))


        def _parse_latest_run(data: object) -> None | ProblemListItemsResponseDtoItemsItemLatestRunType0:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                latest_run_type_0 = ProblemListItemsResponseDtoItemsItemLatestRunType0.from_dict(data)



                return latest_run_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | ProblemListItemsResponseDtoItemsItemLatestRunType0, data)

        latest_run = _parse_latest_run(d.pop("latestRun"))


        recent_runs = []
        _recent_runs = d.pop("recentRuns")
        for recent_runs_item_data in (_recent_runs):
            recent_runs_item = ProblemListItemsResponseDtoItemsItemRecentRunsItem.from_dict(recent_runs_item_data)



            recent_runs.append(recent_runs_item)


        def _parse_preview_file_url(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        preview_file_url = _parse_preview_file_url(d.pop("previewFileUrl"))


        def _parse_title(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        title = _parse_title(d.pop("title", UNSET))


        def _parse_description(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        description = _parse_description(d.pop("description", UNSET))


        def _parse_domain(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        domain = _parse_domain(d.pop("domain", UNSET))


        problem_list_items_response_dto_items_item = cls(
            id=id,
            environment_id=environment_id,
            external_id=external_id,
            is_template=is_template,
            created_at=created_at,
            updated_at=updated_at,
            latest_version_created_at=latest_version_created_at,
            has_locked_version=has_locked_version,
            is_draft=is_draft,
            total_cost_usd=total_cost_usd,
            runs_count=runs_count,
            models=models,
            avg_score=avg_score,
            best_score=best_score,
            latest_run=latest_run,
            recent_runs=recent_runs,
            preview_file_url=preview_file_url,
            title=title,
            description=description,
            domain=domain,
        )

        return problem_list_items_response_dto_items_item

