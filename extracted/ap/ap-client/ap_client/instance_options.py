"""Local option parsing for instance directory reads and uploads."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

import typer


def relative_path(value: str | None) -> str | None:
    if value is None:
        return None
    path = value.strip().rstrip("/")
    if path in ("", ".") and not value.strip().startswith("/"):
        return ""
    if (
        path.startswith("/")
        or "\\" in path
        or ":" in path
        or any(ord(char) < 32 or ord(char) == 127 for char in path)
        or any(part in ("", ".", "..") for part in path.split("/"))
    ):
        raise ValueError("--path must be relative to the instance root; use '.' for the root")
    return path


def sdk_options(owner: Any, method: str, options: dict[str, Any]) -> dict[str, Any]:
    function = getattr(owner, method, None)
    if not callable(function):
        raise ValueError(f"The installed instance-repo does not support {method}")
    parameters = inspect.signature(function).parameters
    if not any(p.kind is inspect.Parameter.VAR_KEYWORD for p in parameters.values()):
        missing = set(options) - set(parameters)
        if missing:
            raise ValueError(
                f"The installed instance-repo does not support {method} options: "
                + ", ".join(sorted(missing))
            )
    return options


def read_hashes(path: str | None) -> dict[str, str]:
    if path is None:
        return {}
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or any(
        not isinstance(key, str) or not key.strip() or not isinstance(item, str) or not item.strip()
        for key, item in value.items()
    ):
        raise ValueError(
            "--content-hashes must contain a JSON object of instance IDs to nonempty hashes"
        )
    return value


def upload_hashes(records: list[dict], supplied: dict[str, str], skip: bool) -> dict[str, str]:
    hashes = dict(supplied)
    if not skip:
        return hashes
    from instance_repo import compute_source_hash

    for record in records:
        instance = record["instance"]
        path = Path(record["path"])
        if not path.is_dir():
            raise ValueError("--skip-unchanged currently supports instance directories only")
        if instance in hashes:
            continue
        hashes[instance] = compute_source_hash(path)
    return hashes


def require_working_prune() -> None:
    raise ValueError(
        "--prune is disabled before uploading: instance-repo does not support safe pruning. "
        "Upload without --prune; review and delete obsolete instance metadata explicitly."
    )


def progress_callback(completed: int, total: int, result: Any) -> None:
    instance = str(getattr(result, "instance_id", "") or type(result).__name__)
    instance = "".join(char if char.isprintable() else repr(char)[1:-1] for char in instance)
    status = "skipped" if getattr(result, "skipped", False) else "uploaded"
    if isinstance(result, BaseException):
        status = "failed"
    typer.echo(f"progress: {completed}/{total} {instance} {status}", err=True)
