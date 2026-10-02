"""Paid end-to-end certification for every DataForSEO catalog example.

This runner uses the local standalone REST API so each case exercises the same
Supabase auth, secrets battery, provider client, and ORM persistence path as the
frontend lab. It never prints credentials or bearer tokens.
"""

from __future__ import annotations

import argparse
import asyncio
import os
from collections import Counter
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum
from uuid import uuid4

import httpx
from pydantic import BaseModel, ConfigDict


class Workflow(StrEnum):
    LIVE = "live"
    STANDARD = "standard"


class EndpointExample(BaseModel):
    model_config = ConfigDict(extra="ignore")

    endpoint: str
    workflow: Workflow
    task: dict[str, object]


class CatalogOperation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    endpoint_examples: list[EndpointExample]


class Catalog(BaseModel):
    operations: list[CatalogOperation]


class CertificationCase(BaseModel):
    operation: str
    example: EndpointExample


class CaseResult(BaseModel):
    operation: str
    endpoint: str
    workflow: Workflow
    passed: bool
    run_id: str | None = None
    request_count: int = 0
    reported_cost: Decimal | None = None
    elapsed_seconds: float
    error: object | None = None


class CertificationReport(BaseModel):
    started_at: datetime
    completed_at: datetime
    server_url: str
    results: list[CaseResult]

    @property
    def passed(self) -> int:
        return sum(result.passed for result in self.results)

    @property
    def failed(self) -> int:
        return len(self.results) - self.passed

    @property
    def reported_cost(self) -> Decimal:
        return sum(
            (result.reported_cost or Decimal("0") for result in self.results),
            start=Decimal("0"),
        )


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--confirm-paid", action="store_true")
    parser.add_argument(
        "--workflow",
        choices=("live", "standard", "all"),
        default="live",
    )
    parser.add_argument("--operation", action="append", default=[])
    parser.add_argument("--server-url", default="http://127.0.0.1:8081")
    parser.add_argument("--concurrency", type=int, default=4)
    return parser.parse_args()


def _require_environment() -> tuple[str, str]:
    email = os.environ.get("AI_ADMIN_USERNAME", "").strip()
    password = os.environ.get("AI_ADMIN_PASSWORD", "").strip()
    if not email or not password:
        raise RuntimeError(
            "AI_ADMIN_USERNAME and AI_ADMIN_PASSWORD must be loaded from aidream/.env"
        )
    return email, password


async def _json(response: httpx.Response) -> object:
    try:
        return response.json()
    except ValueError:
        return {"http_status": response.status_code, "body": response.text[:2_000]}


def _failure_detail(payload: object) -> object:
    if not isinstance(payload, dict):
        return payload
    detail = payload.get("detail")
    return detail if detail is not None else payload


def _assert_evidence(
    status: dict[str, object],
    evidence: dict[str, object],
    case: CertificationCase,
) -> None:
    if status.get("status") != "completed":
        raise AssertionError(f"run status is {status.get('status')!r}")
    if status.get("error") is not None:
        raise AssertionError("completed run retained an error")
    receipt = status.get("receipt")
    if not isinstance(receipt, dict) or not receipt.get("raw_payload_id"):
        raise AssertionError("completed run has no raw-payload receipt")
    raw_payloads = evidence.get("raw_payloads")
    if not isinstance(raw_payloads, list) or not raw_payloads:
        raise AssertionError("run has no persisted raw provider payload")
    for raw in raw_payloads:
        if not isinstance(raw, dict) or not raw.get("checksum") or not raw.get("size_bytes"):
            raise AssertionError("raw provider payload lacks checksum or byte size")
        if raw.get("payload") is None and not raw.get("cloud_file_id"):
            raise AssertionError("raw provider payload has neither inline JSON nor a cloud file")
    provider_calls = evidence.get("provider_calls")
    if not isinstance(provider_calls, list) or not provider_calls:
        raise AssertionError("run has no persisted provider-call evidence")
    requests = [
        request
        for call in provider_calls
        if isinstance(call, dict)
        for request in (
            call.get("metadata", {}).get("requests", [])
            if isinstance(call.get("metadata"), dict)
            else []
        )
        if isinstance(request, dict)
    ]
    matching = [
        request
        for request in requests
        if str(request.get("url", "")).endswith(case.example.endpoint)
    ]
    if not matching:
        raise AssertionError("provider-call evidence omits the selected outbound endpoint")
    for request in requests:
        headers = request.get("headers")
        if not isinstance(headers, dict):
            continue
        for key, value in headers.items():
            if key.casefold() == "authorization" and value != "<redacted>":
                raise AssertionError("provider Authorization evidence is not redacted")
    if case.example.workflow is Workflow.STANDARD:
        tasks = evidence.get("provider_tasks")
        if not isinstance(tasks, list) or len(tasks) < 2:
            raise AssertionError("standard run lacks task and submission checkpoints")
        statuses = Counter(str(task.get("status")) for task in tasks if isinstance(task, dict))
        if set(statuses) != {"completed"}:
            raise AssertionError(f"standard task checkpoints are not all completed: {statuses}")


async def _run_case(
    client: httpx.AsyncClient,
    headers: dict[str, str],
    organization_id: str,
    case: CertificationCase,
    semaphore: asyncio.Semaphore,
) -> CaseResult:
    started = asyncio.get_running_loop().time()
    request_id = str(uuid4())
    body = {
        "provider": "dataforseo",
        "organization_id": organization_id,
        "capability": "raw_provider",
        "operation": case.operation,
        "target_ref": f"dataforseo-certification:{case.example.workflow}:{request_id}",
        "observation_period": date.today().isoformat(),
        "settings": {
            "tasks": [case.example.task],
            "workflow": case.example.workflow.value,
            "endpoint": case.example.endpoint,
        },
        "request_id": request_id,
        "force_refresh": True,
    }
    run_id: str | None = None
    try:
        async with semaphore:
            response = await client.post("/collections", headers=headers, json=body)
        payload = await _json(response)
        if isinstance(payload, dict):
            candidate = payload.get("run_id")
            if isinstance(candidate, str):
                run_id = candidate
            detail = payload.get("detail")
            if run_id is None and isinstance(detail, dict):
                candidate = detail.get("run_id")
                if isinstance(candidate, str):
                    run_id = candidate
        if response.status_code != 200:
            raise RuntimeError(f"HTTP {response.status_code}: {_failure_detail(payload)}")
        if run_id is None:
            raise AssertionError("collection receipt omitted run_id")
        status_response, evidence_response = await asyncio.gather(
            client.get(f"/collections/{run_id}", headers=headers),
            client.get(f"/collections/{run_id}/evidence", headers=headers),
        )
        status_response.raise_for_status()
        evidence_response.raise_for_status()
        status = status_response.json()
        evidence = evidence_response.json()
        _assert_evidence(status, evidence, case)
        elapsed = asyncio.get_running_loop().time() - started
        return CaseResult(
            operation=case.operation,
            endpoint=case.example.endpoint,
            workflow=case.example.workflow,
            passed=True,
            run_id=run_id,
            request_count=int(status.get("request_count") or 0),
            reported_cost=status.get("reported_cost"),
            elapsed_seconds=elapsed,
        )
    except Exception as exc:
        status: dict[str, object] = {}
        if run_id is not None:
            persisted = await client.get(f"/collections/{run_id}", headers=headers)
            if persisted.status_code == 200 and isinstance(persisted.json(), dict):
                status = persisted.json()
        elapsed = asyncio.get_running_loop().time() - started
        return CaseResult(
            operation=case.operation,
            endpoint=case.example.endpoint,
            workflow=case.example.workflow,
            passed=False,
            run_id=run_id,
            request_count=int(status.get("request_count") or 0),
            reported_cost=status.get("reported_cost"),
            elapsed_seconds=elapsed,
            error=status.get("error") or {"type": type(exc).__name__, "message": str(exc)},
        )


async def _main(args: argparse.Namespace) -> int:
    if not args.confirm_paid:
        raise RuntimeError("refusing paid calls without --confirm-paid")
    if args.concurrency < 1 or args.concurrency > 10:
        raise ValueError("--concurrency must be between 1 and 10")
    email, password = _require_environment()
    started_at = datetime.now(UTC)
    timeout = httpx.Timeout(connect=20, read=18_000, write=60, pool=20)
    async with httpx.AsyncClient(
        base_url=args.server_url.rstrip("/"),
        timeout=timeout,
    ) as client:
        login = await client.post("/auth/login", json={"email": email, "password": password})
        login.raise_for_status()
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        me_response, catalog_response = await asyncio.gather(
            client.get("/me", headers=headers),
            client.get("/providers/dataforseo/operations", headers=headers),
        )
        me_response.raise_for_status()
        catalog_response.raise_for_status()
        organization_id = me_response.json()["organization_id"]
        catalog = Catalog.model_validate(catalog_response.json())
        selected_workflows = (
            {Workflow.LIVE, Workflow.STANDARD}
            if args.workflow == "all"
            else {Workflow(args.workflow)}
        )
        selected_operations = set(args.operation)
        cases = [
            CertificationCase(operation=operation.name, example=example)
            for operation in catalog.operations
            for example in operation.endpoint_examples
            if example.workflow in selected_workflows
            and (not selected_operations or operation.name in selected_operations)
        ]
        if not cases:
            raise RuntimeError("the selected catalog slice contains no certification cases")
        print(
            f"Running {len(cases)} paid DataForSEO cases through {args.server_url} "
            f"with concurrency={args.concurrency}",
            flush=True,
        )
        semaphore = asyncio.Semaphore(args.concurrency)

        async def run_and_report(case: CertificationCase) -> CaseResult:
            result = await _run_case(client, headers, organization_id, case, semaphore)
            label = "PASS" if result.passed else "FAIL"
            print(
                f"{label} {result.workflow.value:8} {result.endpoint} "
                f"run={result.run_id or '-'} cost={result.reported_cost or 0} "
                f"requests={result.request_count} seconds={result.elapsed_seconds:.1f}",
                flush=True,
            )
            if result.error is not None:
                print(f"  error={result.error}", flush=True)
            return result

        results = await asyncio.gather(*(run_and_report(case) for case in cases))
    report = CertificationReport(
        started_at=started_at,
        completed_at=datetime.now(UTC),
        server_url=args.server_url,
        results=results,
    )
    print(
        f"SUMMARY passed={report.passed} failed={report.failed} "
        f"reported_cost_usd={report.reported_cost}",
        flush=True,
    )
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(_main(_arguments())))
