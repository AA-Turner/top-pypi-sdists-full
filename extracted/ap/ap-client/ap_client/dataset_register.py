"""Dataset metadata registration command backed by Instance Repo ingest."""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any, List, Optional
from urllib.parse import quote

import typer

from . import dataset_commands as datasets

_TERMINAL_SUCCESS = {"completed"}
_TERMINAL_FAILURE = {"failed"}
_TERMINAL_CANCELED = {"canceled", "cancelled"}


def _payload(outcome: str, dataset: str, result: Any) -> dict:
    return {**datasets._model_dict(result), "outcome": outcome, "dataset": dataset}


def _emit_preview_stderr(payload: dict, output_format: str) -> None:
    typer.echo("Preview:", err=True)
    if output_format == "yaml":
        try:
            import yaml
        except ImportError as exc:
            raise typer.BadParameter("--format yaml requires PyYAML to be installed") from exc
        typer.echo(yaml.safe_dump(payload, allow_unicode=True, sort_keys=False).rstrip(), err=True)
        return
    typer.echo(json.dumps(payload, ensure_ascii=False, indent=2), err=True)


def _parse_request_timeout() -> float:
    """Read ``AP_REQUEST_TIMEOUT`` from the environment, falling back to 30 s.

    Empty, missing, or non-numeric values all resolve to the default rather
    than raising ``ValueError`` at import time (which would break ``ap --help``).
    """
    raw = os.environ.get("AP_REQUEST_TIMEOUT", "").strip()
    if not raw:
        return 30.0
    try:
        value = float(raw)
    except (TypeError, ValueError):
        return 30.0
    return value if math.isfinite(value) and value > 0 else 30.0


def _set_sdk_request_timeout(repo: Any, timeout: float) -> None:
    """Override the IR SDK per-request HTTP timeout on the shared Transport.

    All sub-clients (``datasets``, ``versions``, ``instances``) share
    ``repo.transport``, so a single assignment covers every control-plane
    call the register command makes (preview and submission alike).
    Falls back to setting the attribute on each sub-client's ``_t`` when the
    ``transport`` attribute is absent (older SDK shapes).
    """
    transport = getattr(repo, "transport", None)
    if transport is not None and hasattr(transport, "timeout"):
        transport.timeout = timeout
        return
    for name in ("datasets", "versions", "instances", "images"):
        client = getattr(repo, name, None)
        t = getattr(client, "_t", None)
        if t is not None and hasattr(t, "timeout"):
            t.timeout = timeout


def _confirm(dataset: str, *, yes: bool) -> None:
    if yes:
        return
    if not sys.stdin.isatty():
        raise datasets._fail(
            f"Registering dataset {dataset} requires confirmation after preview",
            "Add --yes (-y) to confirm the registration",
            exit_code=2,
        )
    if not typer.confirm(
        f"Register the previewed data for dataset {dataset}?", default=False, err=True
    ):
        raise datasets._fail(
            "Registration canceled; nothing was written remotely",
            "Rerun the command and confirm, or add --yes (-y)",
        )


def _claim_without_workspace(
    repo: Any, dataset_id: str, current_user: str, benchmark_id: str
) -> dict:
    # API allows omitted workspace (ClaimAllowsOmittedWorkspace). SDK 1.3.2's
    # claim() still rejects it locally, so keep the authenticated transport shim.
    body = {"owner": current_user}
    if benchmark_id:
        body["benchmark_id"] = benchmark_id
    return repo.transport.post(
        f"/apis/v1/datasets/series/{quote(dataset_id, safe='')}/claim",
        body,
    )


def _create_owned_dataset(repo: Any, dataset: str, benchmark_id: str) -> dict:
    from .dataset_name import (
        DatasetNameError,
        DatasetNameUpgradeRequired,
        parse_dataset_name,
    )

    try:
        name = parse_dataset_name(dataset)
    except DatasetNameUpgradeRequired as exc:
        raise datasets._fail(
            f"Failed to create dataset {dataset}: {exc}",
            "pip install 'ap-client[dataset]' --upgrade",
            exit_code=2,
        ) from exc
    except DatasetNameError:
        raise datasets._fail(
            f"Failed to create dataset {dataset}: the name must be one or more "
            "canonical path segments",
            "Use a dataset name such as my-bench, your-team/my-bench, "
            "or gdpval/synthetic/my-bench",
            exit_code=2,
        )

    from instance_repo.models import DatasetSeries

    fields: dict[str, Any] = {
        "dataset_name": dataset,
        "dataset_l1": name.l1,
        "dataset_l2": name.l2,
        "visibility": "private",
    }
    if benchmark_id:
        fields["benchmark_id"] = benchmark_id
    record = repo.datasets.create(DatasetSeries(**fields), require_benchmark=False)
    return datasets._model_dict(record)


def _ensure_current_user_owns(
    repo: Any, dataset: str, environment: str, benchmark: Optional[str]
) -> None:
    from . import cli
    from .irepo_sdk import _reason

    try:
        current_user = cli.get_client()._resolve_self_user_id()
    except Exception as exc:  # noqa: BLE001 - keep the CLI error contract
        raise datasets._fail(
            f"Failed to resolve the current user: {_reason(exc)}",
            "Check AP_API_KEY and the current cluster, then retry",
        ) from exc
    if not current_user:
        raise datasets._fail(
            "Failed to resolve the current user for --owner @me",
            "Check AP_API_KEY and the current cluster, then retry",
        )

    missing = False
    try:
        raw_detail = repo.datasets.get_detail(dataset, **datasets._env_kwargs(environment))
        detail = datasets._model_dict(raw_detail)
        missing = raw_detail is None or detail.get("registered") is False
    except Exception as exc:  # noqa: BLE001 - dataset absence permits create
        if datasets._business_code(exc) not in (92001, 94021):
            raise datasets._fail(
                f"Failed to inspect ownership for dataset {dataset}: {_reason(exc)}",
                f"Check access with: ap dataset get {dataset}",
            ) from exc
        missing = True
        detail = {}
    if missing:
        benchmark_id = datasets._resolve_benchmark_id(repo, benchmark) if benchmark else ""
        try:
            created = _create_owned_dataset(repo, dataset, benchmark_id)
        except typer.Exit:
            raise
        except Exception as create_exc:  # noqa: BLE001 - server remains authoritative
            raise datasets._fail(
                f"Failed to create dataset {dataset}: {_reason(create_exc)}",
                f"Check the name and benchmark, then inspect: ap dataset get {dataset}",
            ) from create_exc
        created_owner = str(created.get("owner") or "").strip()
        if not created_owner:
            try:
                refreshed = datasets._model_dict(
                    repo.datasets.get_detail(dataset, **datasets._env_kwargs(environment))
                )
                created_owner = str(refreshed.get("owner") or "").strip()
            except Exception as exc:  # noqa: BLE001 - creation may already have succeeded
                raise datasets._fail(
                    f"Dataset {dataset} was created, but ownership could not be verified: {_reason(exc)}",
                    f"Inspect ownership before registering again: ap dataset get {dataset}",
                ) from exc
            if not created_owner:
                raise datasets._fail(
                    f"Dataset {dataset} was created, but the server returned no owner",
                    f"Verify ownership before registering again: ap dataset get {dataset}",
                )
        if created_owner != current_user:
            shown_owner = created_owner or "<unknown>"
            raise datasets._fail(
                f"Dataset {dataset} was created or claimed concurrently by {shown_owner}",
                "Do not retry with --owner @me; ask the current dataset admin for access",
            )
        return

    owner = str(detail.get("owner") or "").strip()
    if owner == current_user:
        return
    if owner:
        raise datasets._fail(
            f"Dataset {dataset} is owned by {owner}; --owner @me cannot take it over",
            "Ask the existing dataset admin to run the registration or grant access",
        )
    if not detail.get("claimable", False):
        raise datasets._fail(
            f"Dataset {dataset} cannot be claimed because it already has an admin",
            "Ask an existing dataset admin to run the registration or grant access",
        )
    dataset_id = str(detail.get("dataset_id") or "").strip()
    if not dataset_id:
        raise datasets._fail(
            f"Failed to claim dataset {dataset}: the server returned no dataset_id",
            f"Inspect the dataset with: ap dataset get {dataset}",
        )
    benchmark_id = datasets._resolve_benchmark_id(repo, benchmark) if benchmark else ""
    try:
        _claim_without_workspace(repo, dataset_id, current_user, benchmark_id)
    except Exception as exc:  # noqa: BLE001 - preserve SDK transport error mapping
        hint = datasets._DATASET_CODE_HINTS.get(datasets._business_code(exc)) or (
            "Ask an existing dataset admin for access, or verify that the dataset is still claimable"
        )
        raise datasets._fail(
            f"Failed to claim dataset {dataset}: {_reason(exc)}",
            hint,
        ) from exc


def dataset_register(
    dataset: str = typer.Argument(..., help="Dataset name"),
    version: Optional[str] = typer.Option(None, "--version", help=datasets._VERSION_HELP),
    splits: Optional[List[str]] = typer.Option(None, "--split", help="Split to scan; repeatable"),
    unversioned: bool = typer.Option(
        False,
        "--unversioned",
        help="Scan the version-less space; mutually exclusive with --version",
    ),
    environment: Optional[str] = typer.Option(
        None, "--environment", help=datasets._ENVIRONMENT_HELP
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview without submitting registration"
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the registration confirmation"),
    wait: bool = typer.Option(False, "--wait", help="Wait for the ingest task to finish"),
    timeout: float = typer.Option(1800.0, "--timeout", help="Local wait timeout in seconds"),
    request_timeout: float = typer.Option(
        _parse_request_timeout(),
        "--request-timeout",
        help="Per-request HTTP timeout in seconds for control-plane calls "
        "(env: AP_REQUEST_TIMEOUT, default: 30). "
        "Increase for datasets with many objects where the preview scan takes longer.",
    ),
    output_format: Optional[str] = typer.Option(None, "--format", help=datasets._FORMAT_HELP),
    owner: Optional[str] = typer.Option(
        None, "--owner", help="Ensure ownership before ingest; the only supported value is @me"
    ),
    benchmark: Optional[str] = typer.Option(
        None, "--benchmark", help="Benchmark for create/claim when using --owner @me"
    ),
) -> None:
    """Preview and register existing dataset data through an ingest task."""
    from .irepo_sdk import _reason

    fmt = datasets._fmt(output_format)
    dataset = dataset.strip()
    if not dataset:
        raise datasets._fail(
            "Failed to register dataset: name is empty",
            "Pass a non-empty dataset name, e.g. ap dataset register alibaba/a",
            exit_code=2,
        )
    selected_version = str(version or "").strip() or None
    selected_splits = [str(value).strip() for value in (splits or []) if str(value).strip()]
    if selected_version and unversioned:
        raise datasets._fail(
            "--version and --unversioned are mutually exclusive",
            "Choose a version or the version-less space",
            exit_code=2,
        )
    if unversioned and not selected_splits:
        raise datasets._fail(
            "--unversioned requires at least one --split",
            "Repeat --split for each version-less split to register",
            exit_code=2,
        )
    if owner is not None and owner != "@me":
        raise datasets._fail(
            "--owner only supports @me",
            "Use --owner @me or omit --owner to leave ownership unchanged",
            exit_code=2,
        )
    if benchmark and owner != "@me":
        raise datasets._fail(
            "--benchmark requires --owner @me because it is only used during create or claim",
            "Add --owner @me or omit --benchmark",
            exit_code=2,
        )
    if not math.isfinite(timeout) or timeout <= 0:
        raise datasets._fail(
            "--timeout must be a positive finite number",
            "Pass a positive number of seconds",
            exit_code=2,
        )

    env = datasets._environment(environment)
    repo = datasets._dataset_repo(request_timeout=request_timeout)
    # Override the IR SDK per-request HTTP timeout. All sub-clients
    # (datasets, versions, instances) share repo.transport, so one
    # assignment covers preview and submission alike.
    if not math.isfinite(request_timeout) or request_timeout <= 0:
        raise datasets._fail(
            "--request-timeout must be a positive finite number",
            "Pass a positive number of seconds",
            exit_code=2,
        )
    _set_sdk_request_timeout(repo, request_timeout)
    datasets._check_storage_side(repo, env)
    ingest = getattr(getattr(repo, "versions", None), "ingest", None)
    if not callable(ingest):
        raise datasets._fail(
            "The installed Instance Repo SDK does not support dataset ingest",
            "Install or upgrade ap-client[dataset] to a version with versions.ingest",
            exit_code=2,
        )

    kwargs = {
        "splits": selected_splits or None,
        **datasets._env_kwargs(env),
        "allow_layout_inference": selected_version is None and not selected_splits,
        "dry_run": True,
        "wait": False,
        "timeout_sec": timeout,
        "raise_on_failure": False,
    }
    try:
        preview = datasets._model_dict(ingest(dataset, selected_version, **kwargs))
    except Exception as exc:  # noqa: BLE001 - SDK failures use the CLI contract
        raise datasets._fail(
            f"Failed to preview registration for dataset {dataset}: {_reason(exc)}",
            "Check the dataset scope, cluster storage, and environment, then retry",
        ) from exc

    preview_payload = _payload("preview", dataset, preview)
    if dry_run:
        datasets._emit_detail(preview_payload, fmt)
    else:
        _emit_preview_stderr(preview_payload, fmt)
    preview_status = str(preview.get("status") or "").strip().lower()
    if preview_status in _TERMINAL_FAILURE | _TERMINAL_CANCELED:
        raise datasets._fail(
            f"Registration preview {preview_status}: "
            f"{preview.get('error_message') or preview.get('error_msg') or 'no details returned'}",
            "Fix the preview error before submitting registration",
        )
    if dry_run:
        return
    counts = preview.get("counts")
    if preview.get("instance_count") == 0 or (
        isinstance(counts, dict) and counts.get("instances") == 0
    ):
        raise datasets._fail(
            "Registration preview found no instances",
            "Check the dataset scope and storage layout before submitting registration",
        )
    _confirm(dataset, yes=yes)
    if owner == "@me":
        _ensure_current_user_owns(repo, dataset, env, benchmark)

    submission_kwargs = {**kwargs, "dry_run": False, "wait": wait}
    if wait:
        typer.echo(
            f"Waiting up to {timeout:g} seconds for the registration task to finish...",
            err=True,
        )
    try:
        result = datasets._model_dict(ingest(dataset, selected_version, **submission_kwargs))
    except Exception as exc:  # noqa: BLE001 - SDK failures use the CLI contract
        if wait:
            failed_job = datasets._model_dict(getattr(exc, "job", None))
            ingest_id = str(failed_job.get("ingest_id") or failed_job.get("id") or "").strip()
            task_hint = f" task {ingest_id}" if ingest_id else " the task"
            raise datasets._fail(
                f"Failed to submit or wait for registration of dataset {dataset}: {_reason(exc)}",
                f"The request may have been accepted and{task_hint} may still be running; "
                "inspect dataset metadata before deciding whether to submit again",
            ) from exc
        raise datasets._fail(
            f"Failed to submit registration for dataset {dataset}: {_reason(exc)}",
            "The preview did not write metadata; inspect the error and retry the command",
        ) from exc

    status = str(result.get("status") or "").strip().lower()
    if status in _TERMINAL_SUCCESS:
        outcome = "completed"
    elif status in _TERMINAL_FAILURE:
        outcome = "failed"
    elif status in _TERMINAL_CANCELED:
        outcome = "canceled"
    elif wait:
        outcome = "timed_out"
    else:
        outcome = "submitted"

    datasets._emit_detail(_payload(outcome, dataset, result), fmt)
    ingest_id = str(result.get("ingest_id") or result.get("id") or "").strip()
    if outcome == "failed":
        raise datasets._fail(
            f"Registration task {ingest_id or '<unknown>'} failed: "
            f"{result.get('error_message') or result.get('error_msg') or 'no details returned'}",
            "Fix the reported data or metadata issue, then run the same registration command again",
        )
    if outcome == "canceled":
        raise datasets._fail(
            f"Registration task {ingest_id or '<unknown>'} was canceled",
            "Inspect the dataset metadata before deciding whether to submit again",
        )
    if outcome == "timed_out":
        raise datasets._fail(
            "Registration wait timed out; the background task continues running",
            f"Inspect dataset metadata after task {ingest_id or '<unknown>'} finishes",
        )
