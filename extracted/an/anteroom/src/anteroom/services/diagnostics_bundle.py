"""Local-only redacted diagnostics bundle export."""

from __future__ import annotations

import importlib
import json
import os
import platform
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .. import __version__
from .debug_diagnostics import _sanitize_text
from .feedback import _redact_dict

SCHEMA_VERSION = "1"
DEFAULT_MAX_FILES = 8
DEFAULT_MAX_ENTRIES = 200
DEFAULT_MAX_SOURCE_BYTES = 512_000
DEFAULT_MAX_BUNDLE_BYTES = 2_000_000
DEFAULT_MAX_TIME_WINDOW_HOURS = 168

_SENSITIVE_KEY_RE = re.compile(r"(?i)(key|secret|password|token|passphrase|authorization|cookie|credential)")
_TOKEN_COUNT_KEYS = {"tokens", "token_chars", "prompt_tokens", "completion_tokens", "total_tokens"}
_RAW_CONTENT_KEYS = {
    "args",
    "arguments",
    "assistant_message",
    "completion",
    "content",
    "messages",
    "output",
    "prompt",
    "raw",
    "raw_text",
    "request_body",
    "response",
    "stderr",
    "stdout",
    "streamed_tokens",
    "text",
    "tool_input",
    "tool_output",
    "user_message",
}
_SAFE_RECORD_KEYS = {
    "code",
    "conversation_id",
    "correlation_id",
    "duration_ms",
    "duration_seconds",
    "ended_at",
    "error_code",
    "event_type",
    "level",
    "line",
    "message",
    "model",
    "phase",
    "provider",
    "request_id",
    "retryable",
    "session_id",
    "severity",
    "source",
    "started_at",
    "status",
    "status_code",
    "timestamp",
    "tool_name",
    "turn_id",
    "type",
}
_SAFE_DETAIL_KEYS = {
    "code",
    "correlation_id",
    "duration_ms",
    "duration_seconds",
    "error_code",
    "phase",
    "request_id",
    "status",
    "status_code",
    "turn_id",
}


@dataclass
class BundleOptions:
    conversation_id: str | None = None
    turn_id: str | None = None
    request_id: str | None = None
    since: datetime | None = None
    latest_failure: bool = False
    output: Path | None = None
    bundle_format: str = "directory"
    max_files: int | None = None
    max_entries: int | None = None
    max_source_bytes: int | None = None
    max_bundle_bytes: int | None = None
    max_time_window_hours: int | None = None


@dataclass
class SourceReport:
    name: str
    path: str
    entries: int = 0
    bytes: int = 0
    truncated: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass
class BundleResult:
    path: Path
    format: str
    size_bytes: int
    included_files: list[str]
    entries: int
    warnings: list[str]
    manifest: dict[str, Any]


def parse_since(value: str | None, *, now: datetime | None = None) -> datetime | None:
    """Parse a relative window such as ``2h``/``30m``/``7d`` or an ISO timestamp."""
    if not value:
        return None
    value = value.strip()
    now = now or datetime.now(timezone.utc)
    match = re.fullmatch(r"(\d+)([mhdw])", value)
    if match:
        amount = int(match.group(1))
        unit = match.group(2)
        delta = {
            "m": timedelta(minutes=amount),
            "h": timedelta(hours=amount),
            "d": timedelta(days=amount),
            "w": timedelta(weeks=amount),
        }[unit]
        return now - delta
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("expected a relative window like 2h, 30m, 7d, or an ISO timestamp") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def create_diagnostics_bundle(config: Any, options: BundleOptions | None = None) -> BundleResult:
    """Create a local diagnostics bundle directory or zip file.

    The command is intentionally local-only. This function writes files under
    the configured data directory or explicit output path and performs no
    network calls or feedback reporter dispatch.
    """
    options = options or BundleOptions()
    limits = _resolve_limits(config, options)
    generated_at = datetime.now(timezone.utc).isoformat()
    warnings: list[str] = []
    since = _bounded_since(options.since, limits["max_time_window_hours"], warnings)
    output_dir, final_path = _resolve_output_path(config, options, generated_at)
    output_dir.mkdir(parents=True, exist_ok=False)

    source_reports: list[SourceReport] = []
    files: dict[str, Any] = {}
    files["runtime.json"] = _runtime_summary(config)
    files["config-summary.json"] = _config_summary(config, limits)

    diagnostics_entries, diagnostics_report = _read_diagnostics_entries(config, options, since, limits)
    source_reports.append(diagnostics_report)
    if diagnostics_entries:
        files["diagnostics-errors.jsonl"] = diagnostics_entries

    debug_entries, debug_report = _read_jsonl_source_group(
        name="debug_summaries",
        paths=_debug_summary_paths(config),
        options=options,
        since=since,
        limits=limits,
        sanitizer=_sanitize_debug_summary,
    )
    source_reports.append(debug_report)
    if debug_entries:
        files["debug-summaries.jsonl"] = debug_entries

    audit_entries, audit_report = _read_jsonl_source_group(
        name="audit_refs",
        paths=_audit_paths(config, limits["max_files"]),
        options=options,
        since=since,
        limits=limits,
        sanitizer=_sanitize_audit_ref,
    )
    source_reports.append(audit_report)
    if audit_entries:
        files["audit-refs.jsonl"] = audit_entries

    manifest = _build_manifest(
        options=options,
        limits=limits,
        generated_at=generated_at,
        files=files,
        source_reports=source_reports,
        warnings=warnings,
    )
    files["manifest.json"] = manifest

    included_files = _write_bundle_files(output_dir, files, limits, warnings)
    size_bytes = _directory_size(output_dir)
    if size_bytes > limits["max_bundle_bytes"]:
        warnings.append("bundle exceeded max_bundle_bytes after writing; inspect manifest for truncated sources")

    manifest["warnings"] = warnings + [warning for report in source_reports for warning in report.warnings]
    _write_json(output_dir / "manifest.json", manifest)
    size_bytes = _directory_size(output_dir)

    if options.bundle_format == "zip":
        final_path = final_path or output_dir.with_suffix(".zip")
        _zip_directory(output_dir, final_path)
        shutil.rmtree(output_dir)
        size_bytes = final_path.stat().st_size
        output_path = final_path
        output_format = "zip"
    else:
        output_path = output_dir
        output_format = "directory"

    return BundleResult(
        path=output_path,
        format=output_format,
        size_bytes=size_bytes,
        included_files=included_files,
        entries=sum(report.entries for report in source_reports),
        warnings=manifest["warnings"],
        manifest=manifest,
    )


def _resolve_limits(config: Any, options: BundleOptions) -> dict[str, int]:
    cfg = getattr(config, "diagnostics_bundle", None)

    def pick(name: str, default: int, low: int, high: int) -> int:
        value = getattr(options, name, None)
        if value is None:
            value = getattr(cfg, name, default)
        try:
            if value is None:
                return default
            resolved = int(value)
            return max(low, min(high, resolved))
        except (TypeError, ValueError):
            return default

    return {
        "max_files": pick("max_files", DEFAULT_MAX_FILES, 1, 50),
        "max_entries": pick("max_entries", DEFAULT_MAX_ENTRIES, 1, 5_000),
        "max_source_bytes": pick("max_source_bytes", DEFAULT_MAX_SOURCE_BYTES, 10_000, 5_000_000),
        "max_bundle_bytes": pick("max_bundle_bytes", DEFAULT_MAX_BUNDLE_BYTES, 50_000, 50_000_000),
        "max_time_window_hours": pick(
            "max_time_window_hours",
            DEFAULT_MAX_TIME_WINDOW_HOURS,
            1,
            24 * 31,
        ),
    }


def _bounded_since(since: datetime | None, max_hours: int, warnings: list[str]) -> datetime:
    now = datetime.now(timezone.utc)
    earliest = now - timedelta(hours=max_hours)
    if since is None:
        return earliest
    if since.tzinfo is None:
        since = since.replace(tzinfo=timezone.utc)
    since = since.astimezone(timezone.utc)
    if since < earliest:
        warnings.append(f"since window exceeded {max_hours}h and was clamped")
        return earliest
    return since


def _resolve_output_path(config: Any, options: BundleOptions, generated_at: str) -> tuple[Path, Path | None]:
    stamp = generated_at.replace("+00:00", "Z").replace(":", "").replace(".", "")
    default_root = Path(getattr(config.app, "data_dir")) / "diagnostics-bundles"
    if options.output is None:
        output_dir = default_root / f"diagnostics-bundle-{stamp}"
        return _unique_path(output_dir), None

    output = options.output.expanduser()
    if options.bundle_format == "zip":
        final_path = output if output.suffix == ".zip" else output.with_suffix(".zip")
        if final_path.exists():
            raise FileExistsError(f"output already exists: {final_path}")
        work_dir = final_path.with_suffix("")
        return _unique_path(work_dir), final_path

    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    return output, None


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for idx in range(2, 100):
        candidate = path.with_name(f"{path.name}-{idx}")
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"could not allocate unique output path under {path.parent}")


def _runtime_summary(config: Any) -> dict[str, Any]:
    from ..tools.introspect import _gather_package

    return {
        "anteroom_version": __version__,
        "package": _gather_package(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "data_dir": _display_path(Path(getattr(config.app, "data_dir"))),
        "generated_locally": True,
    }


def _config_summary(config: Any, limits: dict[str, int]) -> dict[str, Any]:
    from ..tools.introspect import _gather_config, _gather_safety

    summary = {
        "config": _gather_config(config),
        "safety": _gather_safety(config),
        "audit": {
            "enabled": bool(getattr(config.audit, "enabled", False)),
            "log_path": _display_path(_audit_root(config)),
            "redact_content": bool(getattr(config.audit, "redact_content", True)),
            "retention_days": getattr(config.audit, "retention_days", None),
        },
        "diagnostics_bundle": limits,
    }
    return _redact_dict(summary)


def _build_manifest(
    *,
    options: BundleOptions,
    limits: dict[str, int],
    generated_at: str,
    files: dict[str, Any],
    source_reports: list[SourceReport],
    warnings: list[str],
) -> dict[str, Any]:
    included = []
    for name, content in files.items():
        if isinstance(content, list):
            entries = len(content)
        else:
            entries = 1
        included.append({"name": name, "entries": entries})

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "local_only": True,
        "redaction": {
            "status": "redacted",
            "raw_prompts": "omitted",
            "raw_responses": "omitted",
            "raw_tokens": "omitted",
            "raw_tool_arguments": "omitted",
            "raw_tool_output": "omitted",
            "secrets": "redacted",
        },
        "scope": {
            "conversation_id": options.conversation_id,
            "turn_id": options.turn_id,
            "request_id": options.request_id,
            "since": options.since.isoformat() if options.since else None,
            "latest_failure": options.latest_failure,
        },
        "limits": limits,
        "included": included,
        "sources": [
            {
                "name": report.name,
                "path": report.path,
                "entries": report.entries,
                "bytes": report.bytes,
                "truncated": report.truncated,
                "warnings": report.warnings,
            }
            for report in source_reports
        ],
        "warnings": list(warnings),
        "inspect_before_sharing": True,
    }


def _write_bundle_files(
    output_dir: Path,
    files: dict[str, Any],
    limits: dict[str, int],
    warnings: list[str],
) -> list[str]:
    del limits, warnings
    included: list[str] = []
    for name, content in files.items():
        path = output_dir / name
        if name.endswith(".jsonl"):
            _write_jsonl(path, content)
        else:
            _write_json(path, content)
        included.append(name)
    return included


def _read_diagnostics_entries(
    config: Any,
    options: BundleOptions,
    since: datetime,
    limits: dict[str, int],
) -> tuple[list[dict[str, Any]], SourceReport]:
    module_entries, module_report = _read_diagnostics_module(config, options, since, limits)
    if module_entries:
        return module_entries, module_report

    paths = _diagnostics_paths(config, limits["max_files"])
    entries, file_report = _read_jsonl_source_group(
        name="diagnostics_errors",
        paths=paths,
        options=options,
        since=since,
        limits=limits,
        sanitizer=_sanitize_diagnostics_entry,
    )
    if module_report.warnings:
        file_report.warnings.extend(module_report.warnings)
    return entries, file_report


def _read_diagnostics_module(
    config: Any,
    options: BundleOptions,
    since: datetime,
    limits: dict[str, int],
) -> tuple[list[dict[str, Any]], SourceReport]:
    report = SourceReport(name="diagnostics_errors", path="diagnostics_log module")
    try:
        module = importlib.import_module("anteroom.services.diagnostics_log")
    except ModuleNotFoundError:
        report.warnings.append("diagnostics_log source not available on this branch")
        return [], report

    reader = getattr(module, "read_diagnostics_entries", None) or getattr(module, "iter_diagnostics_entries", None)
    if reader is None:
        report.warnings.append("diagnostics_log source has no bundle reader")
        return [], report

    try:
        raw_entries = reader(
            config=config,
            conversation_id=options.conversation_id,
            turn_id=options.turn_id,
            request_id=options.request_id,
            since=since,
            latest_failure=options.latest_failure,
            limit=limits["max_entries"],
        )
        entries = [
            entry
            for entry in (_sanitize_diagnostics_entry(raw) for raw in raw_entries)
            if entry and _matches_scope(entry, options, since)
        ][: limits["max_entries"]]
    except TypeError:
        report.warnings.append("diagnostics_log reader signature is not bundle-compatible")
        return [], report
    except Exception as exc:
        report.warnings.append(f"diagnostics_log reader failed: {type(exc).__name__}")
        return [], report

    if options.latest_failure:
        entries = _latest_failure_only(entries)
    report.entries = len(entries)
    report.bytes = _json_size(entries)
    return entries, report


def _read_jsonl_source_group(
    *,
    name: str,
    paths: list[Path],
    options: BundleOptions,
    since: datetime,
    limits: dict[str, int],
    sanitizer: Any,
) -> tuple[list[dict[str, Any]], SourceReport]:
    selected_paths = [path for path in paths if path.exists() and path.is_file()]
    if not selected_paths:
        return [], SourceReport(
            name=name,
            path=", ".join(_display_path(path) for path in paths),
            warnings=["source absent"],
        )

    selected_paths = sorted(selected_paths, key=lambda path: path.stat().st_mtime, reverse=True)[: limits["max_files"]]
    report = SourceReport(name=name, path=", ".join(_display_path(path) for path in selected_paths))
    entries: list[dict[str, Any]] = []
    for path in selected_paths:
        try:
            raw_entries, truncated = _read_jsonl_file(path, limits["max_source_bytes"])
        except OSError as exc:
            report.warnings.append(f"skipped unreadable source {path.name}: {type(exc).__name__}")
            continue
        report.truncated = report.truncated or truncated
        for raw in raw_entries:
            entry = sanitizer(raw)
            if not entry or not _matches_scope(entry, options, since):
                continue
            entry.setdefault("source", path.name)
            entries.append(entry)
            if len(entries) >= limits["max_entries"]:
                report.truncated = True
                break
        if len(entries) >= limits["max_entries"]:
            break

    if options.latest_failure and name == "diagnostics_errors":
        entries = _latest_failure_only(entries)
    report.entries = len(entries)
    report.bytes = _json_size(entries)
    if not entries:
        report.warnings.append("no entries matched bundle scope")
    return entries, report


def _read_jsonl_file(path: Path, max_bytes: int) -> tuple[list[dict[str, Any]], bool]:
    size = path.stat().st_size
    start = max(0, size - max_bytes)
    truncated = start > 0
    entries: list[dict[str, Any]] = []
    with open(path, "rb") as handle:
        handle.seek(start)
        if start:
            handle.readline()
        for line_no, raw_line in enumerate(handle, start=1):
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                entries.append({"timestamp": None, "code": "corrupt_jsonl", "line": line_no})
                continue
            if isinstance(obj, dict):
                obj["_line"] = line_no
                entries.append(obj)
    return entries, truncated


def _sanitize_diagnostics_entry(raw: dict[str, Any]) -> dict[str, Any]:
    entry = _sanitize_record(raw, allowed_keys=_SAFE_RECORD_KEYS)
    details = raw.get("details")
    if isinstance(details, dict):
        safe_details = _sanitize_record(details, allowed_keys=_SAFE_DETAIL_KEYS)
        for key, value in safe_details.items():
            entry.setdefault(key, value)
    if "_line" in raw:
        entry["line"] = raw["_line"]
    return entry


def _sanitize_debug_summary(raw: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "active_tools",
        "counters",
        "ended_at",
        "errors",
        "final_phase",
        "model",
        "phases",
        "redaction",
        "retries",
        "runtime_events",
        "started_at",
        "stop_reason",
        "tools",
        "total_duration_seconds",
        "usage",
        "version",
    } | _SAFE_RECORD_KEYS
    out: dict[str, Any] = {}
    for key, value in raw.items():
        clean_key = str(key).removeprefix("_")
        if clean_key in allowed:
            out[clean_key] = _sanitize_freeform(clean_key, value)
    return out


def _sanitize_audit_ref(raw: dict[str, Any]) -> dict[str, Any]:
    entry = _sanitize_record(raw, allowed_keys=_SAFE_RECORD_KEYS)
    details = raw.get("details")
    if isinstance(details, dict):
        for key, value in _sanitize_record(details, allowed_keys=_SAFE_DETAIL_KEYS).items():
            entry.setdefault(key, value)
    if "_line" in raw:
        entry["line"] = raw["_line"]
    return entry


def _sanitize_record(raw: dict[str, Any], *, allowed_keys: set[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in raw.items():
        clean_key = str(key).removeprefix("_")
        if clean_key not in allowed_keys:
            continue
        out[clean_key] = _sanitize_value(clean_key, value)
    if "timestamp" not in out and "created_at" in raw:
        out["timestamp"] = _sanitize_value("timestamp", raw["created_at"])
    return out


def _sanitize_value(key: str, value: Any) -> Any:
    key_lower = key.lower()
    if _is_sensitive_key(key_lower):
        return "[redacted]" if value else value
    if key_lower in _RAW_CONTENT_KEYS:
        return "[omitted]"
    if isinstance(value, dict):
        return {
            str(k): _sanitize_value(str(k), v)
            for k, v in value.items()
            if str(k) in _SAFE_DETAIL_KEYS and str(k).lower() not in _RAW_CONTENT_KEYS
        }
    if isinstance(value, list):
        return [_sanitize_value(key, item) for item in value[:50]]
    if isinstance(value, str):
        return _sanitize_text(value, max_chars=240)
    return value


def _sanitize_freeform(key: str, value: Any) -> Any:
    clean_key = key.removeprefix("_")
    key_lower = clean_key.lower()
    if key_lower in _RAW_CONTENT_KEYS:
        return "[omitted]"
    if _is_sensitive_key(key_lower):
        return "[redacted]" if value else value
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for idx, (child_key, child_value) in enumerate(value.items()):
            if idx >= 50:
                out["truncated"] = True
                break
            out[str(child_key).removeprefix("_")] = _sanitize_freeform(str(child_key), child_value)
        return out
    if isinstance(value, list):
        return [_sanitize_freeform(clean_key, item) for item in value[:50]]
    if isinstance(value, str):
        return _sanitize_text(value, max_chars=240)
    return value


def _is_sensitive_key(key_lower: str) -> bool:
    if key_lower in _TOKEN_COUNT_KEYS:
        return False
    return bool(_SENSITIVE_KEY_RE.search(key_lower))


def _matches_scope(entry: dict[str, Any], options: BundleOptions, since: datetime) -> bool:
    timestamp = _parse_timestamp(entry.get("timestamp") or entry.get("started_at") or entry.get("ended_at"))
    if timestamp is not None and timestamp < since:
        return False
    if options.conversation_id and entry.get("conversation_id") != options.conversation_id:
        return False
    if options.turn_id and entry.get("turn_id") != options.turn_id:
        return False
    if options.request_id and entry.get("request_id") != options.request_id:
        return False
    return True


def _latest_failure_only(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failure_codes = {"error", "failed", "failure", "exception", "timeout"}
    failures = [
        entry
        for entry in entries
        if any(str(entry.get(key, "")).lower() in failure_codes for key in ("level", "severity", "status", "code"))
        or entry.get("error_code")
    ]
    if not failures:
        return entries[:1]
    return sorted(
        failures,
        key=lambda entry: _parse_timestamp(entry.get("timestamp")) or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )[:1]


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _diagnostics_root(config: Any) -> Path:
    data_dir = Path(getattr(config.app, "data_dir"))
    diagnostics_cfg = getattr(config, "diagnostics", None)
    raw_log_path = getattr(diagnostics_cfg, "log_path", "") if diagnostics_cfg is not None else ""
    if raw_log_path:
        return Path(raw_log_path).expanduser()
    return data_dir / "diagnostics"


def _diagnostics_paths(config: Any, max_files: int) -> list[Path]:
    data_dir = Path(getattr(config.app, "data_dir"))
    root = _diagnostics_root(config)
    return [
        *_diagnostics_daily_paths(root, max_files),
        root / "diagnostics-errors.jsonl",
        root / "errors.jsonl",
        data_dir / "diagnostics-log.jsonl",
        data_dir / "diagnostics.jsonl",
    ]


def _diagnostics_daily_paths(root: Path, max_files: int) -> list[Path]:
    if not root.exists():
        return [root / "diagnostics-YYYY-MM-DD.jsonl*"]
    paths = [path for path in root.glob("diagnostics-[0-9][0-9][0-9][0-9]-*.jsonl*") if path.is_file()]
    return sorted(paths, key=lambda path: path.stat().st_mtime, reverse=True)[:max_files]


def _debug_summary_paths(config: Any) -> list[Path]:
    data_dir = Path(getattr(config.app, "data_dir"))
    return [
        data_dir / "debug-diagnostics" / "debug-summaries.jsonl",
        data_dir / "debug-summaries.jsonl",
    ]


def _audit_root(config: Any) -> Path:
    raw_path = getattr(config.audit, "log_path", "") or ""
    return Path(raw_path).expanduser() if raw_path else Path(getattr(config.app, "data_dir")) / "audit"


def _audit_paths(config: Any, max_files: int) -> list[Path]:
    root = _audit_root(config)
    if root.is_file():
        return [root]
    if not root.exists():
        return [root / "audit-*.jsonl"]
    paths = list(root.glob("audit-*.jsonl"))
    return sorted(paths, key=lambda path: path.stat().st_mtime, reverse=True)[:max_files]


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, default=str) + "\n")


def _zip_directory(directory: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(directory.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(directory.parent))


def _directory_size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    total = 0
    for root, _, files in os.walk(path):
        for filename in files:
            try:
                total += (Path(root) / filename).stat().st_size
            except OSError:
                continue
    return total


def _json_size(value: Any) -> int:
    return len(json.dumps(value, default=str).encode("utf-8"))


def _display_path(path: Path) -> str:
    try:
        return str(path.expanduser())
    except RuntimeError:
        return str(path)
