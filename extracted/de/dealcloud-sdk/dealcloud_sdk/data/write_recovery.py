"""Per-payload row-error recovery for DealCloud Rows writes.

DealCloud POST/PUT batches are all-or-none: if any row in a payload returns
``Errors``, nothing in that payload is committed. The SDK splits indexed
failures, retries clean rows once, and if the retry batch still has errors,
reports every row in the retry batch as failed (no further splits).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Callable, Optional

from intapp_rest_client.models import ErrorHandling

from ..utils.process_response_errors import (
    map_row_errors_to_indices,
    split_row_results,
)
@dataclass
class PayloadRecoveryResult:
    """Outcome of row-error recovery for one HTTP payload."""

    ok_rows: list[dict] = field(default_factory=list)
    row_errors: list[dict] = field(default_factory=list)
    failed_inputs: list[dict] = field(default_factory=list)


@dataclass
class AggregatedRecoveryResult:
    """Combined recovery outcome across multiple HTTP payloads."""

    ok_rows: list[dict] = field(default_factory=list)
    row_errors: list[dict] = field(default_factory=list)
    failed_inputs: list[dict] = field(default_factory=list)
    transport_errors: list = field(default_factory=list)


def assign_insert_entry_ids(payload: list[dict]) -> None:
    """Assign per-payload negative EntryIds for insert correlation."""
    for idx, row in enumerate(payload):
        row["EntryId"] = -(idx + 1)


def _normalize_rows_response(response: object) -> list[dict]:
    if isinstance(response, list):
        return [r for r in response if isinstance(r, dict)]
    if isinstance(response, dict):
        return [response]
    return []


def _error_row_for_index(
    row_errors: list[dict],
    batch_index: int,
    batch: list[dict],
    *,
    is_insert: bool,
) -> dict | None:
    target_id = -(batch_index + 1) if is_insert else batch[batch_index].get("EntryId")
    if target_id is None:
        return None
    for err_row in row_errors:
        entry_id = err_row.get("EntryId")
        if entry_id is not None and int(entry_id) == int(target_id):
            return err_row
    return None


def _synthetic_error_row(row: dict, description: str) -> dict:
    return {
        "EntryId": row.get("EntryId"),
        "Errors": [{"field": "", "code": 0, "description": description}],
    }


_UNCOMMITTED_DESC = "entry not committed (batch all-or-none)"


def _filter_row_errors_for_batch(
    batch: list[dict],
    row_errors: list[dict],
    *,
    is_insert: bool,
) -> list[dict]:
    batch_ids: set[int] = set()
    for idx, row in enumerate(batch):
        entry_id = row.get("EntryId")
        if entry_id is None:
            continue
        batch_ids.add(-(idx + 1) if is_insert else int(entry_id))
    return [
        err
        for err in row_errors
        if err.get("EntryId") is not None and int(err["EntryId"]) in batch_ids
    ]


def _primary_row_errors(row_errors: list[dict]) -> list[dict]:
    """Errors that caused the row to fail validation (not batch all-or-none collateral)."""
    primary: list[dict] = []
    for err_row in row_errors:
        errors = [
            err
            for err in (err_row.get("Errors") or [])
            if err.get("description") != _UNCOMMITTED_DESC
        ]
        if errors:
            primary.append({"EntryId": err_row.get("EntryId"), "Errors": errors})
    return primary


def recover_payload_write(
    payload: list[dict],
    send_once: Callable[[list[dict]], object],
    *,
    is_insert: bool,
    assign_entry_ids: Callable[[list[dict]], None] | None = None,
    split_results: Callable[[list], tuple[list[dict], list[dict]]] | None = None,
) -> PayloadRecoveryResult:
    """Split indexed row errors once and retry clean rows (at most two HTTP calls)."""
    split = split_results or split_row_results
    if not payload:
        return PayloadRecoveryResult()

    attempt_rows = [deepcopy(row) for row in payload]
    if assign_entry_ids:
        assign_entry_ids(attempt_rows)

    response = _normalize_rows_response(send_once(attempt_rows))
    ok_rows, row_errors = split(response)
    row_errors = _filter_row_errors_for_batch(attempt_rows, row_errors, is_insert=is_insert)

    if not row_errors:
        return PayloadRecoveryResult(ok_rows=ok_rows)

    primary_errors = _primary_row_errors(row_errors)
    bad_indices = map_row_errors_to_indices(
        attempt_rows, primary_errors or row_errors, is_insert=is_insert
    )
    permanent_errors: list[dict] = []
    failed_inputs: list[dict] = []

    def record_index_failures(indices: set[int], errors: list[dict]) -> None:
        for idx in sorted(indices):
            failed_inputs.append(deepcopy(payload[idx]))
            err_row = _error_row_for_index(errors, idx, attempt_rows, is_insert=is_insert)
            permanent_errors.append(
                err_row
                if err_row is not None
                else _synthetic_error_row(payload[idx], "validation failed")
            )

    if not bad_indices:
        return PayloadRecoveryResult(ok_rows=ok_rows)

    if len(bad_indices) >= len(attempt_rows):
        record_index_failures(bad_indices, primary_errors or row_errors)
        return PayloadRecoveryResult(row_errors=permanent_errors, failed_inputs=failed_inputs)

    record_index_failures(bad_indices, primary_errors or row_errors)

    retry_rows = [deepcopy(row) for idx, row in enumerate(payload) if idx not in bad_indices]
    if not retry_rows:
        return PayloadRecoveryResult(row_errors=permanent_errors, failed_inputs=failed_inputs)

    retry_attempt = [deepcopy(row) for row in retry_rows]
    if assign_entry_ids:
        assign_entry_ids(retry_attempt)

    retry_response = _normalize_rows_response(send_once(retry_attempt))
    retry_ok, retry_row_errors = split(retry_response)

    if not retry_row_errors:
        return PayloadRecoveryResult(
            ok_rows=retry_ok,
            row_errors=permanent_errors,
            failed_inputs=failed_inputs,
        )

    for idx, row in enumerate(retry_rows):
        failed_inputs.append(deepcopy(row))
        err_row = _error_row_for_index(
            retry_row_errors,
            idx,
            retry_attempt,
            is_insert=is_insert,
        )
        permanent_errors.append(
            err_row
            if err_row is not None
            else _synthetic_error_row(
                row,
                "retry batch rejected (all-or-none; no further split)",
            )
        )

    return PayloadRecoveryResult(row_errors=permanent_errors, failed_inputs=failed_inputs)


def recover_payloads(
    payloads: list[list[dict]],
    send_once: Callable[[list[dict]], object],
    *,
    is_insert: bool,
    assign_entry_ids: Callable[[list[dict]], None] | None = None,
    max_workers: int = 1,
    error_handling: ErrorHandling = ErrorHandling.FAIL_FAST,
    split_results: Callable[[list], tuple[list[dict], list[dict]]] | None = None,
) -> AggregatedRecoveryResult:
    """Run per-payload recovery, optionally in parallel across payloads."""
    if not payloads:
        return AggregatedRecoveryResult()

    aggregated = AggregatedRecoveryResult()

    def run_one(payload: list[dict]) -> PayloadRecoveryResult:
        return recover_payload_write(
            payload,
            send_once,
            is_insert=is_insert,
            assign_entry_ids=assign_entry_ids,
            split_results=split_results,
        )

    if max_workers <= 1 or len(payloads) == 1:
        for payload in payloads:
            try:
                outcome = run_one(payload)
            except Exception as exc:
                if error_handling == ErrorHandling.FAIL_FAST:
                    raise
                aggregated.transport_errors.append(exc)
                continue
            aggregated.ok_rows.extend(outcome.ok_rows)
            aggregated.row_errors.extend(outcome.row_errors)
            aggregated.failed_inputs.extend(outcome.failed_inputs)
        return aggregated

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_one, payload): idx for idx, payload in enumerate(payloads)}
        for future in as_completed(futures):
            try:
                outcome = future.result()
            except Exception as exc:
                if error_handling == ErrorHandling.FAIL_FAST:
                    raise
                aggregated.transport_errors.append({"payload_index": futures[future], "error": exc})
                continue
            aggregated.ok_rows.extend(outcome.ok_rows)
            aggregated.row_errors.extend(outcome.row_errors)
            aggregated.failed_inputs.extend(outcome.failed_inputs)

    return aggregated
