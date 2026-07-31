"""Structured-output protocol + jsonschema validation for workflow agent calls.

Every ``agent()`` call gets a RESULT PROTOCOL footer appended to its prompt
instructing the agent to write its final answer to a well-known file on the
rsync-back results mount:

* with ``schema=`` — JSON to ``/workflow-results/<call_id>/result.json``
* without a schema — free text/markdown to ``/workflow-results/<call_id>/result.md``

Validation (jsonschema Draft 2020-12) is SDK-resident and shared by BOTH retry
paths so their semantics never diverge:

* ``build_schema_exit_condition`` / ``build_schema_continuation_instruction`` feed
  ``AgentTask.with_continuation`` — used for every call whose primary mount is NOT
  a git+sync mount (i.e. no ``workspace=`` and ``publish_ref`` calls). The review
  gate would be silently dropped for those (execution.py:117-120, :250-261), so
  retries MUST ride the continuation loop.
* ``build_schema_review_fn`` builds a ``review_fn`` for ``sync="merge_to_main"``
  calls ONLY, where the primary mount is git and the review gate actually attaches.
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import best_match

from plato.agents.review_models import ReviewGateResult

__all__ = [
    "build_result_protocol_block",
    "read_and_validate_result",
    "build_schema_exit_condition",
    "build_schema_continuation_instruction",
    "build_schema_review_fn",
]

DEFAULT_RESULTS_MOUNT_PATH = "/workflow-results"
_MAX_RENDERED_ERRORS = 5


def _result_path(results_dir: Path, call_id: str, schema: dict | None) -> Path:
    filename = "result.json" if schema is not None else "result.md"
    return results_dir / call_id / filename


def _render_errors(schema: dict, instance: Any) -> str:
    """Render the top validation errors as ``at $.<path>: <message>`` lines."""
    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance),
        # Deepest/most-specific first, then stable by path + message.
        key=lambda e: (-len(e.absolute_path), e.json_path, e.message),
    )
    if not errors:
        return ""
    lines = [f"at {err.json_path}: {err.message}" for err in errors[:_MAX_RENDERED_ERRORS]]
    remaining = len(errors) - len(lines)
    if remaining > 0:
        lines.append(f"... and {remaining} more validation error(s)")
    return "\n".join(lines)


def read_and_validate_result(
    results_dir: Path,
    call_id: str,
    schema: dict | None,
) -> tuple[bool, Any, str]:
    """Read + validate the agent's result file.

    Returns ``(ok, value, error)``:

    * schema given — ``value`` is the parsed & validated JSON on success.
    * no schema — ``value`` is the ``result.md`` text on success.
    * ``ok`` is ``False`` with a human-readable ``error`` when the file is
      missing/empty, not valid JSON, or fails schema validation.
    """
    path = _result_path(results_dir, call_id, schema)
    if not path.exists():
        return False, None, f"result file {path.name} not found for call {call_id}"

    try:
        raw = path.read_text()
    except OSError as exc:
        return False, None, f"could not read {path.name}: {exc}"

    if schema is None:
        if not raw.strip():
            return False, None, f"{path.name} is empty for call {call_id}"
        return True, raw, ""

    try:
        instance = json.loads(raw)
    except json.JSONDecodeError as exc:
        return False, None, f"result.json is not valid JSON: {exc}"

    best = best_match(Draft202012Validator(schema).iter_errors(instance))
    if best is not None:
        return False, None, _render_errors(schema, instance)

    return True, instance, ""


def build_result_protocol_block(
    call_id: str,
    schema: dict | None,
    results_mount_path: str = DEFAULT_RESULTS_MOUNT_PATH,
) -> str:
    """Build the RESULT PROTOCOL footer appended to an agent-call prompt."""
    base = results_mount_path.rstrip("/")
    if schema is not None:
        target = f"{base}/{call_id}/result.json"
        schema_json = json.dumps(schema, indent=2, sort_keys=True)
        return (
            "\n\n---\n"
            "## RESULT PROTOCOL (required)\n"
            f"When you are done, write your FINAL answer as a single JSON document to:\n"
            f"    {target}\n"
            "That directory ALREADY EXISTS — copy the path above exactly (do not retype "
            "it, and do not create a new directory: if the target directory seems "
            "missing, your path is mistyped). The JSON MUST validate "
            "against this JSON Schema (Draft 2020-12):\n"
            "```json\n"
            f"{schema_json}\n"
            "```\n"
            "Write ONLY the JSON to that file — no markdown fences, no prose. This file is "
            "the sole channel for your result; anything you print to stdout is ignored."
        )
    target = f"{base}/{call_id}/result.md"
    return (
        "\n\n---\n"
        "## RESULT PROTOCOL (required)\n"
        f"When you are done, write your FINAL answer to:\n"
        f"    {target}\n"
        "That directory ALREADY EXISTS — copy the path above exactly (do not retype it, "
        "and do not create a new directory: if the target directory seems missing, your "
        "path is mistyped). This file is the sole channel "
        "for your result; anything you print to stdout is ignored."
    )


def _retry_instruction(results_dir: Path, call_id: str, schema: dict | None) -> str:
    """Compose a continuation prompt from the CURRENT state of the result file."""
    ok, _value, error = read_and_validate_result(results_dir, call_id, schema)
    if ok:
        # Should not normally be reached (exit condition would have passed), but
        # keep the loop safe with a benign nudge.
        return "Your result file is valid. No further action is required."

    protocol = build_result_protocol_block(call_id, schema)
    if schema is not None:
        return (
            "Your result file is missing or does not satisfy the required schema.\n\n"
            f"Problems:\n{error}\n\n"
            "Fix your result file so it fully validates, then stop."
            f"{protocol}"
        )
    return (
        "Your result file is missing or empty.\n\n"
        f"Problem: {error}\n\n"
        "Write your final answer to the result file, then stop."
        f"{protocol}"
    )


def build_schema_exit_condition(
    results_dir: Path,
    call_id: str,
    schema: dict | None,
) -> Callable[[], Awaitable[bool]]:
    """Async exit condition for ``AgentTask.with_continuation`` (task.py:638).

    Returns ``True`` once the result file exists and validates. The workspace is
    synced back before this runs each attempt (task.py:598 -> :638), so it always
    sees the latest file.
    """

    async def _exit_condition() -> bool:
        ok, _value, _error = read_and_validate_result(results_dir, call_id, schema)
        return ok

    return _exit_condition


def build_schema_continuation_instruction(
    results_dir: Path,
    call_id: str,
    schema: dict | None,
) -> Callable[[], str]:
    """Sync continuation-instruction factory for ``with_continuation`` (task.py:557-558).

    Called with no arguments on each continuation; re-reads the result file so the
    agent is shown the latest validation errors.
    """

    def _instruction() -> str:
        return _retry_instruction(results_dir, call_id, schema)

    return _instruction


def build_schema_review_fn(
    results_dir: Path,
    call_id: str,
    schema: dict | None,
) -> Callable[..., Awaitable[ReviewGateResult]]:
    """Build a ``review_fn`` for ``sync="merge_to_main"`` schema calls ONLY.

    The review gate attaches only when the primary mount is git-with-sync
    (execution.py:117-120), which is the case for ``merge_to_main``. The gate
    calls ``review_fn(hostname, *, attempt_number=...)`` after each execution
    (review_gate.py:236) and merges to main only when ``passed`` is True.
    """

    async def _review_fn(_hostname: str, *, attempt_number: int = 1) -> ReviewGateResult:
        ok, _value, error = read_and_validate_result(results_dir, call_id, schema)
        if ok:
            return ReviewGateResult(passed=True, verdict="pass")
        feedback = _retry_instruction(results_dir, call_id, schema)
        return ReviewGateResult(
            passed=False,
            feedback=feedback,
            verdict="fail",
            failure_kind="invalid_output",
            result_data={"error": error, "attempt_number": attempt_number},
        )

    return _review_fn
