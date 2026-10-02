"""Dataset operations for the authenticated organization, reached as
``client.datasets``. A dataset is a named bucket of traces scoped to one trace
function. Experiments replay against it and its graders score its members."""

from __future__ import annotations

import asyncio
import time
from typing import Any, Literal, TypedDict
from urllib.parse import quote, urlencode

from bitfab.http import HttpClient


class DatasetGraderRef(TypedDict):
    id: str
    name: str | None


class Dataset(TypedDict):
    id: str
    traceFunctionKey: str
    name: str
    description: str | None
    traceCount: int
    graders: list[DatasetGraderRef]
    createdAt: str
    updatedAt: str


class SaveDatasetResult(TypedDict):
    dataset: Dataset
    created: bool


class DatasetTraceIds(TypedDict):
    datasetId: str
    traceIds: list[str]


class AddDatasetTracesResult(TypedDict):
    dataset: Dataset
    addedTraceIds: list[str]
    alreadyPresentTraceIds: list[str]
    skippedTraceIds: list[str]


class RemoveDatasetTracesResult(TypedDict):
    dataset: Dataset
    removedTraceIds: list[str]
    notPresentTraceIds: list[str]


class AddDatasetGradersResult(TypedDict):
    dataset: Dataset
    addedGraderIds: list[str]
    alreadyAssignedGraderIds: list[str]
    skippedGraderIds: list[str]


class RemoveDatasetGradersResult(TypedDict):
    dataset: Dataset
    removedGraderIds: list[str]
    notAssignedGraderIds: list[str]


GraderRerunStatus = Literal["pending", "running", "completed", "errored"]


class GraderRerunProgress(TypedDict):
    completedTraces: int
    totalTraces: int
    graderCount: int


class GraderRerunResult(TypedDict):
    tracesGraded: int
    gradersRun: int


class GraderRerun(TypedDict):
    id: str
    status: GraderRerunStatus
    graderIds: list[str]
    progress: GraderRerunProgress | None
    result: GraderRerunResult | None
    error: str | None
    createdAt: str
    updatedAt: str


class RerunGradersResult(TypedDict):
    run: GraderRerun
    joinedExisting: bool


DEFAULT_RERUN_TIMEOUT_SECONDS = 90.0
RERUN_POLL_INTERVAL_SECONDS = 1.0
_TERMINAL_RERUN_STATUSES = frozenset({"completed", "errored"})


class GraderRerunError(RuntimeError):
    def __init__(self, message: str, run: GraderRerun) -> None:
        super().__init__(message)
        self.run = run


class GraderRerunTimeoutError(GraderRerunError, TimeoutError):
    pass


def _rerun_payload(grader_ids: list[str] | None) -> dict[str, Any]:
    return {} if grader_ids is None else {"graderIds": grader_ids}


def _finished_rerun(
    dataset_id: str, run: GraderRerun, started: RerunGradersResult
) -> RerunGradersResult | None:
    if run["status"] not in _TERMINAL_RERUN_STATUSES:
        return None
    if run["status"] == "errored":
        raise GraderRerunError(
            f"Grader re-run {run['id']} on dataset {dataset_id} errored: "
            f"{run['error'] or 'no reason recorded'}",
            run,
        )
    return {"run": run, "joinedExisting": started["joinedExisting"]}


def _rerun_timed_out(
    dataset_id: str, run: GraderRerun, timeout: float
) -> GraderRerunTimeoutError:
    return GraderRerunTimeoutError(
        f"Grader re-run {run['id']} on dataset {dataset_id} was still {run['status']} "
        f"after {timeout:g} seconds. It keeps running on Bitfab; read it later with "
        "get_grader_rerun.",
        run,
    )


def _dataset_path(dataset_id: str, suffix: str = "") -> str:
    return f"/api/sdk/datasets/{quote(dataset_id, safe='')}{suffix}"


class DatasetsClient:
    """Create, read, and modify datasets, the same operations the Bitfab MCP
    dataset tools expose to a coding agent."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def save(
        self,
        trace_function_key: str,
        name: str,
        description: str | None = None,
    ) -> SaveDatasetResult:
        """Create a dataset, or update the one already named this way under the
        same trace function. ``created`` reports which happened. ``None`` for
        ``description`` leaves an existing description untouched."""
        payload: dict[str, Any] = {
            "traceFunctionKey": trace_function_key,
            "name": name,
        }
        if description is not None:
            payload["description"] = description
        result = self._http_client.request("/api/sdk/datasets", payload)
        return result  # type: ignore[return-value]

    def list(self, trace_function_key: str | None = None) -> list[Dataset]:
        """List datasets, scoped to one trace function when given and
        organization-wide otherwise. Fetches all pages automatically."""
        datasets: list[Dataset] = []
        query = {"limit": "100"}
        if trace_function_key is not None:
            query["traceFunctionKey"] = trace_function_key
        while True:
            result = self._http_client.get(f"/api/sdk/datasets?{urlencode(query)}")
            datasets.extend(result["datasets"])
            cursor = result.get("nextCursor")
            if cursor is None:
                return datasets
            query["cursor"] = cursor

    def get(self, dataset_id: str) -> Dataset:
        """Fetch one dataset by id. A dataset outside this organization raises
        ``requests.HTTPError`` with a 404."""
        result = self._http_client.get(_dataset_path(dataset_id))
        return result["dataset"]

    def list_traces(self, dataset_id: str) -> DatasetTraceIds:
        """The ids of every trace in the dataset, the same membership a replay
        with ``dataset_id`` selects. Fetches all pages automatically."""
        trace_ids: list[str] = []
        query = {"limit": "100"}
        while True:
            page = self._http_client.get(
                f"{_dataset_path(dataset_id, '/traces')}?{urlencode(query)}"
            )
            trace_ids.extend(page["traceIds"])
            cursor = page.get("nextCursor")
            if cursor is None:
                return {"datasetId": page["datasetId"], "traceIds": trace_ids}
            query["cursor"] = cursor

    def add_traces(
        self, dataset_id: str, trace_ids: list[str]
    ) -> AddDatasetTracesResult:
        """Add traces to the dataset (1 to 100 ids per call). Traces outside the
        organization or under another trace function are reported in
        ``skippedTraceIds`` rather than failing the call."""
        result = self._http_client.request(
            _dataset_path(dataset_id, "/traces"), {"traceIds": trace_ids}
        )
        return result  # type: ignore[return-value]

    def remove_traces(
        self, dataset_id: str, trace_ids: list[str]
    ) -> RemoveDatasetTracesResult:
        """Remove traces from the dataset. The traces themselves are never
        deleted."""
        result = self._http_client.request(
            _dataset_path(dataset_id, "/removeTraces"), {"traceIds": trace_ids}
        )
        return result  # type: ignore[return-value]

    def add_graders(
        self, dataset_id: str, grader_ids: list[str]
    ) -> AddDatasetGradersResult:
        """Assign graders to the dataset (1 to 100 ids per call). Graders
        outside the organization or under another trace function are reported
        in ``skippedGraderIds`` rather than failing the call."""
        result = self._http_client.request(
            _dataset_path(dataset_id, "/graders"), {"graderIds": grader_ids}
        )
        return result  # type: ignore[return-value]

    def remove_graders(
        self, dataset_id: str, grader_ids: list[str]
    ) -> RemoveDatasetGradersResult:
        """Unassign graders from the dataset."""
        result = self._http_client.request(
            _dataset_path(dataset_id, "/removeGraders"), {"graderIds": grader_ids}
        )
        return result  # type: ignore[return-value]

    def rerun_graders(
        self,
        dataset_id: str,
        grader_ids: list[str] | None = None,
        *,
        timeout: float = DEFAULT_RERUN_TIMEOUT_SECONDS,
    ) -> RerunGradersResult:
        started: RerunGradersResult = self._http_client.request(  # type: ignore[assignment]
            _dataset_path(dataset_id, "/rerunGraders"), _rerun_payload(grader_ids)
        )
        run = started["run"]
        deadline = time.monotonic() + timeout
        while True:
            finished = _finished_rerun(dataset_id, run, started)
            if finished is not None:
                return finished
            if time.monotonic() >= deadline:
                raise _rerun_timed_out(dataset_id, run, timeout)
            time.sleep(RERUN_POLL_INTERVAL_SECONDS)
            run = self.get_grader_rerun(dataset_id, run["id"]) or run

    async def rerun_graders_async(
        self,
        dataset_id: str,
        grader_ids: list[str] | None = None,
        *,
        timeout: float = DEFAULT_RERUN_TIMEOUT_SECONDS,
    ) -> RerunGradersResult:
        started: RerunGradersResult = await asyncio.to_thread(
            self._http_client.request,
            _dataset_path(dataset_id, "/rerunGraders"),
            _rerun_payload(grader_ids),
        )
        run = started["run"]
        deadline = time.monotonic() + timeout
        while True:
            finished = _finished_rerun(dataset_id, run, started)
            if finished is not None:
                return finished
            if time.monotonic() >= deadline:
                raise _rerun_timed_out(dataset_id, run, timeout)
            await asyncio.sleep(RERUN_POLL_INTERVAL_SECONDS)
            run = (
                await asyncio.to_thread(self.get_grader_rerun, dataset_id, run["id"])
                or run
            )

    def get_grader_rerun(
        self, dataset_id: str, run_id: str | None = None
    ) -> GraderRerun | None:
        """The dataset's active grader re-run, or the run named by ``run_id``.
        ``None`` when nothing is active or the run is not this dataset's."""
        query = "" if run_id is None else f"?{urlencode({'runId': run_id})}"
        result = self._http_client.get(
            _dataset_path(dataset_id, f"/rerunGraders{query}")
        )
        return result.get("run")
