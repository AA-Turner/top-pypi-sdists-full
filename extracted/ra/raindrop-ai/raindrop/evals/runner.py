"""One replay protocol for local callbacks, hosted judges and saved UI runs."""

from __future__ import annotations

import asyncio
import time
from typing import Any
from urllib.parse import quote, urlencode
from uuid import uuid4

from .agents import AgentExecution, invoke
from .capture import capture_row, record_output, upload_capture
from .client import EvalClient, replay_ingest_endpoint
from .datasets import publish_eval_suite, read_eval_dataset
from .models import (
    DatasetManifest,
    Destination,
    EvalProgram,
    EvalSuite,
    LocalEvaluator,
    LocalEvaluatorContext,
    ReplayRow,
    RowResult,
    Selection,
    SuiteResult,
    assess_verdict,
    evaluator_name,
    parse_verdict,
)


def select_rows(
    dataset: DatasetManifest, row_ids: list[str] | None = None
) -> list[str]:
    ids = row_ids if row_ids is not None else [r.id for r in dataset.rows]
    if not ids or len(set(ids)) != len(ids):
        raise ValueError("Selected rows must be nonempty and unique")
    available = {r.id for r in dataset.rows}
    if set(ids) - available:
        raise ValueError("Selection contains an unknown row")
    return [r.id for r in dataset.rows if r.id in ids]


async def read_details(
    client: EvalClient, run_id: str, **options: Any
) -> dict[str, Any]:
    result = await client.request(
        "GET", f"/v1/replays/{quote(run_id, safe='')}", **options
    )
    if result["replay"]["id"] != run_id:
        raise ValueError("Raindrop returned a different run")
    return result


async def read_eval_run(
    client: EvalClient, run_id: str, *, query_url: str | None = None
) -> dict[str, Any]:
    detail = await read_details(client, run_id, query_url=query_url)
    if len(detail["eval_runs"]) >= 200:
        raise ValueError("Run evaluation history exceeds the read limit")
    evaluators = []
    for entry in detail["eval_runs"]:
        data = await read_evaluation(client, entry["id"], query_url=query_url)
        evaluators.append(
            {
                **data,
                "evaluator": data["evalSlug"],
                "evaluatorId": entry["eval_id"],
                "programVersion": entry["program_version"],
                "executedBy": entry["executed_by"],
            }
        )
    replay = detail["replay"]
    return {
        "runId": replay["id"],
        "datasetId": replay["dataset_id"],
        "datasetVersionId": replay["dataset_version_id"],
        "status": replay["status"],
        "counts": replay["counts"],
        "tracesExpireAt": replay["traces_expire_at"],
        "tracesExpired": replay["traces_expired"],
        "evaluators": evaluators,
        "rows": [
            {
                "rowId": r["row_id"],
                "attempt": r["attempt"],
                "status": r["status"],
                "traceId": r["trace_id"],
                "error": r["error"],
            }
            for r in detail["rows"]
        ],
    }


async def read_evaluation(
    client: EvalClient, run_id: str, **options: Any
) -> dict[str, Any]:
    data = (
        await client.request(
            "GET",
            f"/v1/eval-runs/{quote(run_id, safe='')}?include=traces",
            retries=2,
            **options,
        )
    )["data"]
    if data["id"] != run_id:
        raise ValueError("Raindrop returned a different evaluation")
    return data


async def compare_eval_runs(
    client: EvalClient,
    *,
    before_run_id: str,
    after_run_id: str,
    evaluator: str | None = None,
    query_url: str | None = None,
) -> dict[str, Any]:
    first, second = await asyncio.gather(
        read_eval_run(client, before_run_id, query_url=query_url),
        read_eval_run(client, after_run_id, query_url=query_url),
    )
    candidates = [
        e
        for e in first["evaluators"]
        if (not evaluator or e["evaluator"] == evaluator)
        and any(
            other["evaluatorId"] == e["evaluatorId"] for other in second["evaluators"]
        )
    ]
    if len(candidates) != 1:
        raise ValueError(
            "Comparison requires one shared evaluator; specify evaluator for a suite"
        )
    selected = candidates[0]
    matches = [
        e for e in second["evaluators"] if e["evaluatorId"] == selected["evaluatorId"]
    ]
    if len(matches) != 1:
        raise ValueError(
            "Comparison is ambiguous; evaluator graded the run more than once"
        )
    counterpart = matches[0]
    if "running" in (selected["status"], counterpart["status"]):
        raise ValueError("Wait for both evaluations to finish")
    data = (
        await client.request(
            "GET",
            f"/v1/eval-runs/{selected['id']}/compare/{counterpart['id']}",
            query_url=query_url,
        )
    )["data"]
    if (
        data["first"]["id"] != selected["id"]
        or data["second"]["id"] != counterpart["id"]
    ):
        raise ValueError("Raindrop returned a different comparison pair")
    return {
        **data,
        "beforeRunId": before_run_id,
        "afterRunId": after_run_id,
        "evaluator": selected["evaluator"],
        "sameEvaluatorVersion": data["first"]["programVersion"]
        == data["second"]["programVersion"],
    }


async def evaluate_eval_run(
    client: EvalClient,
    run_id: str,
    *,
    evaluators: list[str],
    evaluator_pins: dict[str, dict[str, Any]] | None = None,
    wait_ms: float = 600000,
    poll_interval_ms: float = 2000,
    query_url: str | None = None,
    trace_evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if (
        not evaluators
        or len(set(evaluators)) != len(evaluators)
        or any(not e.strip() for e in evaluators)
    ):
        raise ValueError("Evaluator references must be nonempty and unique")
    if wait_ms < 0 or poll_interval_ms <= 0:
        raise ValueError("Invalid evaluator polling settings")
    pins = evaluator_pins or {}
    if set(pins) - set(evaluators):
        raise ValueError("Evaluator pins contain an unselected evaluator")
    starts = []
    causes = []
    for slug in evaluators:
        body = {"source": {"replay": run_id}, **pins.get(slug, {})}
        if trace_evidence is not None:
            body["source"]["traceEvidence"] = trace_evidence
        try:
            data = (
                await client.request(
                    "POST",
                    f"/v1/evals/{quote(slug, safe='')}/runs",
                    body=body,
                    query_url=query_url,
                )
            )["data"]
            pin = pins.get(slug)
            if pin and (
                data.get("evalId") != pin["expectedEvalId"]
                or data.get("programVersion") != pin["expectedProgramVersion"]
            ):
                raise ValueError("Hosted evaluator did not honor its version pin")
            starts.append((slug, data))
        except Exception as error:
            causes.append(error)
    if causes:
        error = RuntimeError("Could not start every evaluator")
        error.started_runs, error.causes = starts, causes
        raise error
    deadline = time.monotonic() + wait_ms / 1000

    async def wait(slug: str, start: dict[str, Any]) -> dict[str, Any]:
        while True:
            data = await read_evaluation(
                client, start["runId"], query_url=query_url, deadline=deadline
            )
            if data["status"] != "running":
                if data["evalSlug"] != slug:
                    raise ValueError("Hosted evaluator returned the wrong slug")
                return {
                    "evaluator": slug,
                    "runId": data["id"],
                    "status": data["status"],
                    "url": start["url"],
                    "summary": data["summary"],
                    "error": data["error"],
                    "outcomes": data["traces"],
                }
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    f"Evaluator {slug} did not finish within {wait_ms}ms"
                )
            await asyncio.sleep(
                min(poll_interval_ms / 1000, max(0, deadline - time.monotonic()))
            )

    return {
        "runId": run_id,
        "evaluators": await asyncio.gather(
            *(wait(slug, start) for slug, start in starts)
        ),
    }


class EvalSuiteRunSession:
    def __init__(
        self,
        client: EvalClient,
        suite: EvalSuite,
        dataset: DatasetManifest,
        row_ids: list[str],
        destination: Destination,
        *,
        parameters: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> None:
        self.client, self.suite, self.dataset, self.row_ids, self.destination = (
            client,
            suite,
            dataset,
            row_ids,
            destination,
        )
        self.id = str(uuid4())
        self.queued_run_id = run_id
        self.execution: AgentExecution | None = (
            suite.agent.start(parameters or {}) if suite.agent else None
        )
        self.ready: asyncio.Task[None] | None = None
        self.finishing: asyncio.Task[SuiteResult] | None = None
        self.active: set[asyncio.Future[None]] = set()
        self.permits = asyncio.Semaphore(suite.concurrency)
        self.attempts: set[tuple[str, int]] = set()
        self.completed: list[RowResult] = []
        self.parents: dict[str, dict[str, Any]] = {}
        self.evidence: dict[tuple[str, int], dict[str, Any]] = {}
        self.plan: dict[str, Any] = {}
        self.ingest_url = ""

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        return await self.client.request(
            method, path, query_url=self.destination.query_url, **kwargs
        )

    async def _report(self, body: dict[str, Any]) -> Any:
        return await self._request(
            "POST", f"/v1/replays/{self.id}/report", body=body, retries=2
        )

    async def _prepare(self) -> None:
        for entry in self.suite.evaluators:
            evaluator = entry.evaluator
            if isinstance(evaluator, LocalEvaluator) and evaluator.requires_reference:
                if any(
                    not (r.reference_trace_sha256 or r.reference_capture)
                    for r in self.dataset.rows
                    if r.id in self.row_ids
                ):
                    raise ValueError(
                        f"Evaluator {evaluator.slug} requires recorded reference traces before replay"
                    )
        git_fields = await self.client.git_fields()
        if self.queued_run_id:
            detail = await read_details(
                self.client, self.queued_run_id, query_url=self.destination.query_url
            )
            if detail["replay"]["status"] != "queued":
                raise ValueError("Run is already claimed or finished")
            if detail["replay"]["dataset_id"] != str(self.dataset.dataset.id) or detail[
                "replay"
            ]["dataset_version_id"] != str(self.dataset.version.id):
                raise ValueError("Queued run uses a different dataset version")
            self.plan = await self._request(
                "POST", f"/v1/replays/{self.queued_run_id}/claim", body=git_fields
            )
            self.id = self.queued_run_id
        else:
            self.plan = await self._request(
                "POST",
                "/v1/replays",
                body={
                    "dataset_slug": self.dataset.dataset.slug,
                    "dataset_version_id": str(self.dataset.version.id),
                    "dataset_fingerprint": self.dataset.version.fingerprint,
                    "request_key": self.id,
                    "row_ids": self.row_ids,
                    **git_fields,
                },
                retries=2,
            )
            self.id = self.plan["replay"]["id"]
        if (
            self.plan["replay"]["id"] != self.id
            or [r["row_id"] for r in self.plan["rows"]] != self.row_ids
        ):
            raise ValueError("Replay plan does not match selected rows")
        if not self.plan["ingest_url"]:
            raise ValueError("Run is already claimed")
        self.ingest_url = replay_ingest_endpoint(
            self.plan["ingest_url"],
            self.destination.replay_ingest_url or self.client.replay_ingest_url,
        )
        await self._report({"type": "started", **git_fields})
        for entry in self.suite.evaluators:
            evaluator = entry.evaluator
            if not isinstance(evaluator, LocalEvaluator):
                continue
            registered = (
                await self._request(
                    "PUT",
                    f"/v1/evals/{evaluator.slug}/local",
                    body={"name": evaluator.name, "output": evaluator.output},
                )
            )["data"]
            if (
                registered["slug"] != evaluator.slug
                or registered["output"] != evaluator.output
            ):
                raise ValueError(
                    "Local evaluator registration returned a different identity"
                )
            run_id = str(uuid4())
            started = (
                await self._request(
                    "POST",
                    f"/v1/evals/{evaluator.slug}/runs/local",
                    body={
                        "type": "started",
                        "runId": run_id,
                        "expectedEvalId": registered["id"],
                        "expectedProgramVersion": registered["programVersion"],
                        "source": {"replay": self.id},
                    },
                    retries=2,
                )
            )["data"]
            if started["id"] != run_id:
                raise ValueError("Local evaluator returned the wrong run id")
            self.parents[evaluator.slug] = started

    async def _ensure_ready(self) -> None:
        if self.ready is None:
            self.ready = asyncio.create_task(self._prepare())
        await asyncio.shield(self.ready)

    async def run(
        self, *, selection: Selection | dict[str, Any], attempt: int = 0
    ) -> SuiteResult:
        if self.finishing is not None:
            raise RuntimeError("Run is already finishing")
        selected = (
            selection
            if isinstance(selection, Selection)
            else Selection.model_validate(selection)
        )
        if (
            selected.dataset.version.id != self.dataset.version.id
            or selected.dataset.version.fingerprint != self.dataset.version.fingerprint
        ):
            raise ValueError("Selected dataset version does not match the run")
        if len(selected.row_ids) != 1 or selected.row_ids[0] not in self.row_ids:
            raise ValueError("Row-scoped execution requires exactly one planned row")
        if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 0:
            raise ValueError("Attempt must be a nonnegative integer")
        key = (selected.row_ids[0], attempt)
        if key in self.attempts:
            raise ValueError("This row attempt already ran")
        self.attempts.add(key)
        completion = asyncio.get_running_loop().create_future()
        self.active.add(completion)
        try:
            async with self.permits:
                await self._ensure_ready()
                result = await self._run_row(key[0], attempt)
                self.completed.append(result)
                return self._result(
                    "running",
                    [result],
                    {
                        "total": 1,
                        "pending": 0,
                        "done": int(result.status == "done"),
                        "missing": int(result.status == "missing"),
                    },
                    [
                        {
                            "evaluator": verdict.evaluator,
                            "runId": verdict.verdict.get("runId"),
                            "status": "completed",
                            "url": verdict.verdict.get("url"),
                            "summary": None,
                            "error": None,
                        }
                        for verdict in result.verdicts
                    ],
                )
        finally:
            self.active.discard(completion)
            if not completion.done():
                completion.set_result(None)

    async def run_selected(self, *, attempt: int = 0) -> SuiteResult:
        """Always finalize claimed work, including failed and cancelled callbacks."""
        failure = None
        try:
            outcomes = await asyncio.gather(
                *(
                    self.run(
                        selection=Selection(dataset=self.dataset, row_ids=[row]),
                        attempt=attempt,
                    )
                    for row in self.row_ids
                ),
                return_exceptions=True,
            )
            failure = next(
                (item for item in outcomes if isinstance(item, BaseException)), None
            )
        except BaseException as error:
            failure = error
        try:
            result = await self.finish()
        except BaseException:
            if failure is not None:
                raise failure
            raise
        if failure is not None:
            raise failure
        return result

    async def _run_row(self, row_id: str, attempt: int) -> RowResult:
        plan = next(row for row in self.plan["rows"] if row["row_id"] == row_id)
        row = ReplayRow(
            id=row_id,
            name=plan["name"],
            input=plan["input"],
            output=plan["output"],
            properties=plan["properties"],
        )
        correlation = plan["correlation_id"]
        if attempt:
            receipt = await self._report(
                {
                    "type": "attempt_started",
                    "row_id": row_id,
                    "attempt": attempt,
                    "request_key": str(uuid4()),
                }
            )
            if (
                receipt["row"]["row_id"] != row_id
                or receipt["row"]["attempt"] != attempt
            ):
                raise ValueError("Retry receipt does not match the row attempt")
            correlation = receipt["row"]["correlation_id"]
        capture = None
        failure = None
        try:
            with capture_row(
                correlation,
                row,
                attributes=dict(self.client.app_git_snapshot.properties),
            ) as capture:
                result = (
                    await self.execution.run(row)
                    if self.execution
                    else await invoke(self.suite.run, row, wait_on_cancel=True)
                )
                record_output(result)
        except Exception as error:
            failure = str(error) or type(error).__name__
        evidence = None
        try:
            if capture:
                evidence = {
                    "rowId": row_id,
                    **await upload_capture(
                        self.client, capture, self.id, self.ingest_url
                    ),
                }
            if evidence:
                self.evidence[(row_id, attempt)] = evidence
            if not evidence:
                raise RuntimeError("No replay trace captured")
            if not failure:
                pair = await self._read_pair(row_id, attempt, evidence)
        except Exception as error:
            failure = failure or str(error)
        if failure:
            await self._report(
                {
                    "type": "row_missing",
                    "row_id": row_id,
                    "attempt": attempt,
                    "error": failure,
                }
            )
            return RowResult(
                **row.model_dump(),
                attempt=attempt,
                status="missing",
                error=failure,
                trace_id=evidence["traceId"] if evidence else None,
            )
        verdicts = []
        for entry in self.suite.evaluators:
            evaluator = entry.evaluator
            if not isinstance(evaluator, LocalEvaluator):
                continue
            parent = self.parents[evaluator.slug]
            started = time.monotonic()
            try:
                verdict = parse_verdict(
                    evaluator.output,
                    await invoke(
                        evaluator.judge,
                        LocalEvaluatorContext(
                            trace=pair["candidate"]["trace"],
                            reference=pair.get("reference"),
                            row=row,
                            result=result,
                        ),
                    ),
                )
            except Exception as error:
                verdict = {"error": (str(error) or type(error).__name__)[:600]}
            request_id = str(uuid4())
            data = (
                await self._request(
                    "POST",
                    f"/v1/evals/{evaluator.slug}/runs/local",
                    body={
                        "type": "attempt",
                        "runId": parent["id"],
                        "requestId": request_id,
                        "source": {
                            "replay": self.id,
                            "rowId": row_id,
                            "attempt": attempt,
                            "traceEvidence": [evidence],
                        },
                        "verdict": verdict,
                        "durationMs": int((time.monotonic() - started) * 1000),
                    },
                    retries=2,
                )
            )["data"]
            if (
                data["runId"],
                data["requestId"],
                data["rowId"],
                data["attempt"],
                data["traceId"],
            ) != (parent["id"], request_id, row_id, attempt, evidence["traceId"]):
                raise ValueError(
                    "Local evaluator returned a mismatched attempt receipt"
                )
            wire = {
                "evaluator": evaluator.slug,
                "runId": parent["id"],
                "url": parent["url"],
                **data["outcome"],
            }
            verdicts.append(assess_verdict(entry, wire, evaluator.output))
        return RowResult(
            **row.model_dump(),
            attempt=attempt,
            status="done",
            trace_id=evidence["traceId"],
            verdicts=verdicts,
        )

    async def _read_pair(
        self, row_id: str, attempt: int, evidence: dict[str, Any]
    ) -> dict[str, Any]:
        deadline = time.monotonic() + self.suite.trace_wait_ms / 1000
        query = urlencode(
            [
                ("row_id", row_id),
                ("attempt", str(attempt)),
                ("expected_trace_id", evidence["traceId"]),
            ]
            + [("expected_span_id", span) for span in evidence["spanIds"]]
        )
        while True:
            pair = await self._request(
                "GET",
                f"/v1/replays/{self.id}/trace?{query}",
                retries=2,
                deadline=deadline,
            )
            if pair["state"] == "ready":
                if (
                    pair["caseId"],
                    pair["attempt"],
                    pair["datasetVersion"]["id"],
                    pair["datasetVersion"]["fingerprint"],
                ) != (
                    row_id,
                    attempt,
                    str(self.dataset.version.id),
                    self.dataset.version.fingerprint,
                ):
                    raise ValueError(
                        "Trace pair belongs to a different row, attempt or dataset version"
                    )
                if pair["candidate"]["trace"]["event"]["id"] != evidence["traceId"]:
                    raise ValueError("Trace pair returned a different trace")
                return pair
            if pair["state"] != "pending" or time.monotonic() >= deadline:
                raise RuntimeError(f"Trace pair unavailable: {pair['state']}")
            await asyncio.sleep(min(0.5, max(0, deadline - time.monotonic())))

    def _result(
        self,
        status: str,
        rows: list[RowResult],
        counts: dict[str, Any],
        evaluators: list[dict[str, Any]],
        **kwargs: Any,
    ) -> SuiteResult:
        return SuiteResult(
            run_id=self.id,
            name=self.suite.name,
            status=status,
            rows=rows,
            counts=counts,
            evaluators=evaluators,
            traces_expired=kwargs.get("traces_expired", False),
            traces_expire_at=kwargs.get("traces_expire_at"),
        )

    async def finish(self) -> SuiteResult:
        if self.finishing is None:
            self.finishing = asyncio.create_task(self._finish())
        return await asyncio.shield(self.finishing)

    async def _finish_local(self) -> list[dict[str, Any]]:
        summaries = []
        failure = None
        for slug, parent in self.parents.items():
            try:
                data = (
                    await self._request(
                        "POST",
                        f"/v1/evals/{slug}/runs/local",
                        body={
                            "type": "finished",
                            "runId": parent["id"],
                            "source": {"replay": self.id},
                        },
                        retries=2,
                    )
                )["data"]
                if data["id"] != parent["id"]:
                    raise ValueError(
                        "Local evaluator finalization returned a different run"
                    )
                summaries.append(
                    {
                        "evaluator": slug,
                        "runId": data["id"],
                        "status": data["status"],
                        "url": data["url"],
                        "summary": data["summary"],
                        "error": data["error"],
                    }
                )
            except Exception as error:
                if failure is None:
                    failure = error
        if failure is not None:
            raise failure
        return summaries

    async def _finish(self) -> SuiteResult:
        await asyncio.gather(*self.active, return_exceptions=True)
        try:
            failure = None
            try:
                await self._ensure_ready()
            except BaseException as error:
                failure = error
            if failure is None or self.ingest_url:
                # Finalize independent resources even after partial preparation or API failure.
                try:
                    await self._report({"type": "finished"})
                except Exception as error:
                    if failure is None:
                        failure = error
                try:
                    summaries = await self._finish_local()
                except Exception as error:
                    if failure is None:
                        failure = error
            if failure is not None:
                raise failure
            hosted = [
                e
                for e in self.suite.evaluators
                if not isinstance(e.evaluator, LocalEvaluator)
            ]
            if hosted:
                evidence = [
                    self.evidence[(row.id, row.attempt)]
                    for row in self.completed
                    if row.status == "done"
                ]
                pins = {}
                for entry in hosted:
                    e = entry.evaluator
                    identity = e.expected if isinstance(e, EvalProgram) else None
                    if identity:
                        pins[e.slug] = {
                            "expectedEvalId": str(identity.eval_id),
                            "expectedProgramVersion": identity.program_version,
                        }
                    elif getattr(e, "kind", None) == "portable":
                        pins[e.slug] = {
                            "expectedEvalId": e.artifact["evaluator"]["id"],
                            "expectedProgramVersion": e.artifact["evaluator"][
                                "programVersion"
                            ],
                        }
                evaluation = await evaluate_eval_run(
                    self.client,
                    self.id,
                    evaluators=[evaluator_name(e) for e in hosted],
                    evaluator_pins=pins,
                    trace_evidence=evidence,
                    query_url=self.destination.query_url,
                    wait_ms=self.suite.eval_wait_ms,
                    poll_interval_ms=self.suite.eval_poll_interval_ms,
                )
                for result in evaluation["evaluators"]:
                    entry = next(
                        e for e in hosted if evaluator_name(e) == result["evaluator"]
                    )
                    output = entry.evaluator.output
                    returned = {
                        outcome["traceId"]: outcome
                        for outcome in result.pop("outcomes")
                    }
                    for row in self.completed:
                        outcome = returned.get(
                            row.trace_id,
                            {
                                "state": "ungraded",
                                "reason": "trace unavailable",
                                "traceId": row.trace_id or "",
                            },
                        )
                        row.verdicts.append(
                            assess_verdict(
                                entry,
                                {
                                    "evaluator": result["evaluator"],
                                    "runId": result["runId"],
                                    "url": result["url"],
                                    **outcome,
                                },
                                output,
                            )
                        )
                    summaries.append(result)
            detail = await read_details(
                self.client, self.id, query_url=self.destination.query_url
            )
            replay = detail["replay"]
            order = {row: i for i, row in enumerate(self.row_ids)}
            result = self._result(
                replay["status"],
                sorted(self.completed, key=lambda r: (order[r.id], r.attempt)),
                replay["counts"],
                summaries,
                traces_expire_at=replay["traces_expire_at"],
                traces_expired=replay["traces_expired"],
            )
        except BaseException:
            if self.execution:
                try:
                    await self.execution.finish()
                except Exception:
                    pass
            raise
        if self.execution:
            await self.execution.finish()
        return result


async def create_eval_suite_run(
    client: EvalClient,
    definition: EvalSuite,
    *,
    selection: Selection | dict[str, Any],
    destination: Destination | dict[str, Any] | None = None,
    parameters: dict[str, Any] | None = None,
) -> EvalSuiteRunSession:
    selected = (
        selection
        if isinstance(selection, Selection)
        else Selection.model_validate(selection)
    )
    dest = (
        destination
        if isinstance(destination, Destination)
        else Destination.model_validate(destination or {})
    )
    if not isinstance(definition.dataset, str) or definition.dataset not in (
        selected.dataset.dataset.slug,
        str(selected.dataset.dataset.id),
    ):
        raise ValueError("Selected dataset does not match the suite")
    if (
        definition.dataset_version_id
        and selected.dataset.version.id != definition.dataset_version_id
    ):
        raise ValueError("Selected dataset version does not match the suite")
    if not all(isinstance(e.evaluator, LocalEvaluator) for e in definition.evaluators):
        raise ValueError("Row-scoped sessions support local evaluators only")
    return EvalSuiteRunSession(
        client,
        definition,
        selected.dataset,
        select_rows(selected.dataset, selected.row_ids),
        dest,
        parameters=parameters,
    )


async def run_eval_suite(
    client: EvalClient,
    definition: EvalSuite,
    *,
    destination: Destination | dict[str, Any] | None = None,
    parameters: dict[str, Any] | None = None,
    run_id: str | None = None,
    selection: Selection | dict[str, Any] | None = None,
    attempt: int = 0,
    expected_current_dataset_version_id: str | None = None,
) -> SuiteResult:
    dest = (
        destination
        if isinstance(destination, Destination)
        else Destination.model_validate(destination or {})
    )
    selected = (
        selection
        if isinstance(selection, Selection)
        else Selection.model_validate(selection)
        if selection
        else None
    )
    if (
        selected
        and definition.dataset_version_id
        and definition.dataset_version_id != selected.dataset.version.id
    ):
        raise ValueError("Selected dataset version does not match the suite")
    if selected:
        if not isinstance(definition.dataset, str) or definition.dataset not in (
            selected.dataset.dataset.slug,
            str(selected.dataset.dataset.id),
        ):
            raise ValueError("Selected dataset does not match the suite")
        definition = definition.model_copy(
            update={"dataset_version_id": selected.dataset.version.id}
        )
    if definition.agent is not None:
        definition.agent.start(
            parameters
        )  # Validate before publication or claiming a run.
    suite = await publish_eval_suite(
        client,
        definition,
        query_url=dest.query_url,
        expected_current_dataset_version_id=expected_current_dataset_version_id,
    )
    dataset = await read_eval_dataset(
        client,
        suite.dataset,
        version_id=suite.dataset_version_id,
        query_url=dest.query_url,
    )
    if selected and selected.dataset.version.fingerprint != dataset.version.fingerprint:
        raise ValueError("Selected dataset fingerprint does not match")
    row_ids = selected.row_ids if selected else None
    if run_id:
        queued = await read_details(client, run_id, query_url=dest.query_url)
        planned = [row["row_id"] for row in queued["rows"]]
        if row_ids is not None and row_ids != planned:
            raise ValueError("Selected rows do not match the queued run")
        row_ids = planned
    rows = select_rows(dataset, row_ids)
    session = EvalSuiteRunSession(
        client, suite, dataset, rows, dest, parameters=parameters, run_id=run_id
    )
    return await session.run_selected(attempt=attempt)
