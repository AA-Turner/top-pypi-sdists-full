from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Literal, TypedDict, cast
from urllib.parse import quote, urlencode

from bitfab.assertion_categories import AssertionCategorySummary
from bitfab.http import HttpClient

EXPERIMENTS_PATH = "/api/sdk/experiments"

ExperimentStatus = Literal["pending", "completed", "failed", "interrupted"]


class ExperimentCodeChangeTotals(TypedDict):
    files: int
    added: int
    removed: int


class ExperimentRunBy(TypedDict):
    id: str
    fullName: str | None
    email: str | None
    imageUrl: str | None


class Experiment(TypedDict):
    """One replay run. ``metadata`` holds the caller-owned tags passed at replay start and is ``{}`` when none were set."""

    id: str
    name: str | None
    notes: str | None
    status: ExperimentStatus
    traceFunctionKey: str | None
    createdAt: str
    completedAt: str | None
    codeChangeDescription: str | None
    codeChangeTotals: ExperimentCodeChangeTotals | None
    experimentGroupId: str | None
    experimentGroupName: str | None
    datasetId: str | None
    datasetName: str | None
    datasetIds: list[str]
    datasetNames: list[str]
    attempts: int
    plannedTraceCount: int | None
    runBy: ExperimentRunBy | None
    githubEmail: str | None
    gitBranch: str | None
    commitSha: str | None
    baseSha: str | None
    experimentSha: str | None
    metadata: dict[str, str]


class ExperimentPage(TypedDict):
    """One page of runs, newest first. Pass ``nextCursor`` back as ``cursor`` while ``hasMore`` is true."""

    experiments: list[Experiment]
    nextCursor: str | None
    hasMore: bool


class ExperimentTotals(TypedDict):
    """How the run's replays ended. ``total`` counts one replay per trace per attempt and the rest split it by outcome. ``traces`` counts distinct traces."""

    total: int
    traces: int
    succeeded: int
    failed: int
    pending: int
    awaitingLabels: int
    errored: int
    withErrors: int
    ungradable: int
    skipped: int


class ExperimentTally(TypedDict):
    """Verdicts compared against the original. Something passes when at least 75 percent of its attempts passed. ``passing`` and ``failing`` count every verdict, compared or not, so ``passing / (passing + failing)`` is the pass rate."""

    fixed: int
    stillPassing: int
    regressed: int
    stillFailing: int
    originalUnlabeled: int
    unpaired: int
    classified: int
    passing: int
    failing: int


class ExperimentCategoryTally(TypedDict):
    """The assertions in one category, tallied the same way as ``labels``."""

    category: AssertionCategorySummary
    labels: ExperimentTally


class ExperimentJitter(TypedDict):
    """Attempts whose own verdict disagreed with their trace's verdict, and how many traces that touched."""

    disagreeing: int
    attempts: int
    traces: int


class ExperimentRollup(TypedDict):
    """``traces`` tallies replayed traces, ``labels`` tallies scored assertions and graders, ``checks`` tallies raw checks before the pass threshold, and ``categories`` tallies the assertions in each category."""

    traces: ExperimentTally
    skippedTraces: int
    labels: ExperimentTally
    checks: ExperimentTally
    categories: list[ExperimentCategoryTally]
    jitter: ExperimentJitter


class ExperimentRollupResult(TypedDict):
    experimentId: str
    totals: ExperimentTotals
    rollup: ExperimentRollup


def _iso_with_offset(value: datetime | str) -> str:
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


class ExperimentsClient:
    """Read the organization's replay runs and their scored results."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list(
        self,
        *,
        dataset_id: str | None = None,
        trace_function_key: str | None = None,
        git_branch: str | None = None,
        experiment_group_id: str | None = None,
        status: ExperimentStatus | None = None,
        metadata: dict[str, str] | None = None,
        created_after: datetime | str | None = None,
        created_before: datetime | str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> ExperimentPage:
        """List runs newest first, narrowed by every filter given.

        ``metadata`` matches runs carrying every pair given (1 to 10 pairs).
        ``created_after`` is inclusive and ``created_before`` exclusive; a naive
        datetime is treated as UTC. An unfiltered call pages the whole
        organization, so ``limit=1`` fetches the latest run. Pass ``nextCursor``
        from the result as ``cursor`` to fetch another page.
        """
        params: dict[str, str] = {}
        if dataset_id is not None:
            params["datasetId"] = dataset_id
        if trace_function_key is not None:
            params["traceFunctionKey"] = trace_function_key
        if git_branch is not None:
            params["gitBranch"] = git_branch
        if experiment_group_id is not None:
            params["experimentGroupId"] = experiment_group_id
        if status is not None:
            params["status"] = status
        if metadata is not None:
            params["metadata"] = json.dumps(metadata, separators=(",", ":"))
        if created_after is not None:
            params["createdAfter"] = _iso_with_offset(created_after)
        if created_before is not None:
            params["createdBefore"] = _iso_with_offset(created_before)
        if cursor is not None:
            params["cursor"] = cursor
        if limit is not None:
            params["limit"] = str(limit)
        query = f"?{urlencode(params)}" if params else ""
        return cast(ExperimentPage, self._http_client.get(f"{EXPERIMENTS_PATH}{query}"))

    def get(self, id: str) -> Experiment:
        """Read one run in the API key's organization."""
        return self._http_client.get(f"{EXPERIMENTS_PATH}/{quote(id, safe='')}")[
            "experiment"
        ]

    def get_rollup(self, id: str) -> ExperimentRollupResult:
        """Read one run's totals and verdict tallies."""
        return cast(
            ExperimentRollupResult,
            self._http_client.get(f"{EXPERIMENTS_PATH}/{quote(id, safe='')}/rollup"),
        )

    def get_rollup_all(self, ids: list[str]) -> list[ExperimentRollupResult]:
        """Read several runs' rollups in one request, returned in the order given. An id outside the organization fails the whole call."""
        if not ids:
            return []
        query = urlencode({"experimentIds": ",".join(ids)}, safe=",")
        return self._http_client.get(f"{EXPERIMENTS_PATH}/rollups?{query}")["rollups"]
