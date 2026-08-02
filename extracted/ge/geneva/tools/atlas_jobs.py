#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Standalone Atlas Geneva jobs CLI.

Requires the Geneva client stack at runtime. PyYAML is optional; without it,
this can still read simple flat `key: value` config files like config-atlas.yaml.

Examples:
  python atlas_jobs.py --config config-atlas.yaml
  python atlas_jobs.py --status RUNNING
  python atlas_jobs.py show <job_id> --full-events
  python atlas_jobs.py tail <job_id>
  python atlas_jobs.py kill <job_id> --yes   # marks the job row CANCELLED only
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = Path("config-atlas.yaml")
DEFAULT_DB_URI = "db://atlas"
DEFAULT_TABLE_NAME = "images"
ACTIVE_STATUSES = ["RUNNING", "PENDING"]
ALL_STATUSES = ["PENDING", "RUNNING", "DONE", "FAILED", "CANCELLED"]
TERMINAL_STATUSES = {"DONE", "FAILED", "CANCELLED"}

logger = logging.getLogger("atlas_jobs")


@dataclass
class Config:
    geneva_host: str
    db_uri: str = DEFAULT_DB_URI
    table_name: str = DEFAULT_TABLE_NAME
    lancedb_api_key: str | None = None
    lancedb_region: str | None = None
    r2_access_key: str | None = None
    r2_secret_key: str | None = None
    r2_endpoint: str | None = None
    r2_region: str | None = None
    aws_allow_http: str = "false"
    azure_storage_account_name: str | None = None
    azure_storage_account_key: str | None = None
    azure_storage_sas_token: str | None = None

    def storage_options(self) -> dict[str, str] | None:
        options: dict[str, str] = {}

        if (
            self.r2_access_key
            and self.r2_secret_key
            and self.r2_endpoint
            and self.r2_region
        ):
            options.update(
                {
                    "aws_access_key_id": self.r2_access_key,
                    "aws_secret_access_key": self.r2_secret_key,
                    "aws_endpoint": self.r2_endpoint,
                    "aws_region": self.r2_region,
                    "aws_s3_force_path_style": "true",
                    "aws_allow_http": self.aws_allow_http,
                }
            )

        if self.azure_storage_account_name:
            options["account_name"] = self.azure_storage_account_name
            options["azure_storage_account_name"] = self.azure_storage_account_name
        if self.azure_storage_account_key:
            options["account_key"] = self.azure_storage_account_key
            options["azure_storage_account_key"] = self.azure_storage_account_key
        if self.azure_storage_sas_token:
            options["sas_token"] = self.azure_storage_sas_token
            options["azure_storage_sas_token"] = self.azure_storage_sas_token

        return options or None


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _strip_inline_comment(value: str) -> str:
    """Drop a trailing `#` comment from an unquoted value, matching PyYAML.

    Quoted values are left untouched so a `#` inside quotes survives; for
    unquoted values, the comment must be preceded by whitespace (so `a#b`
    stays intact, mirroring `yaml.safe_load`).
    """
    if value[:1] in {"'", '"'}:
        return value
    for index, char in enumerate(value):
        if char == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].strip()
    return value


def _read_simple_yaml(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        value = _strip_inline_comment(value)
        if value.startswith("#") or value == "":
            data[key] = None
            continue
        data[key] = _strip_quotes(value)
    return data


def _read_config_file(path: Path) -> dict[str, Any]:
    try:
        import yaml
    except Exception:
        return _read_simple_yaml(path)

    loaded = yaml.safe_load(path.read_text())
    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise RuntimeError(f"config file must contain a mapping: {path}")
    return loaded


def _as_optional_str(value: Any) -> str | None:
    if value is None or value == "":
        return None
    return str(value)


def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise RuntimeError(
            f"config file not found: {config_path} "
            "(create config-atlas.yaml or pass --config)"
        )

    data = _read_config_file(config_path)
    geneva_host = _as_optional_str(data.get("geneva_host"))
    if not geneva_host:
        raise RuntimeError(f"missing required config in {config_path}: geneva_host")

    return Config(
        geneva_host=geneva_host,
        db_uri=_as_optional_str(data.get("db_uri")) or DEFAULT_DB_URI,
        table_name=_as_optional_str(data.get("table_name")) or DEFAULT_TABLE_NAME,
        lancedb_api_key=_as_optional_str(data.get("lancedb_api_key")),
        lancedb_region=_as_optional_str(data.get("lancedb_region")),
        r2_access_key=_as_optional_str(data.get("r2_access_key")),
        r2_secret_key=_as_optional_str(data.get("r2_secret_key")),
        r2_endpoint=_as_optional_str(data.get("r2_endpoint")),
        r2_region=_as_optional_str(data.get("r2_region")),
        aws_allow_http=_as_optional_str(data.get("aws_allow_http")) or "false",
        azure_storage_account_name=_as_optional_str(
            data.get("azure_storage_account_name") or data.get("account_name")
        ),
        azure_storage_account_key=_as_optional_str(
            data.get("azure_storage_account_key") or data.get("account_key")
        ),
        azure_storage_sas_token=_as_optional_str(
            data.get("azure_storage_sas_token") or data.get("sas_token")
        ),
    )


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def connect(config: Config) -> Any:
    import geneva

    kwargs: dict[str, Any] = {
        "uri": config.db_uri,
        "host_override": config.geneva_host,
        "storage_options": config.storage_options(),
    }
    if config.lancedb_api_key:
        kwargs["api_key"] = config.lancedb_api_key
    if config.lancedb_region:
        kwargs["region"] = config.lancedb_region
    return geneva.connect(**kwargs)


def open_connection(args: argparse.Namespace) -> tuple[Config, Any]:
    setup_logging(getattr(args, "log_level", "WARNING"))
    config = load_config(Path(getattr(args, "config", DEFAULT_CONFIG)))
    if getattr(args, "db_uri", None):
        config.db_uri = args.db_uri
    return config, connect(config)


def job_status(job_record: object) -> str:
    status = getattr(job_record, "status", None)
    return getattr(status, "value", str(status))


def list_job_records(
    conn: object, table: str | None, statuses: list[str]
) -> list[object]:
    merged: dict[object, object] = {}
    for status in statuses:
        try:
            for job_record in conn.list_jobs(table_name=table, status=status):
                key = getattr(job_record, "job_id", None) or id(job_record)
                merged[key] = job_record
        except Exception as exc:
            logger.warning("list_jobs(status=%s) failed: %s", status, exc)
    return list(merged.values())


def fmt_dt(value: object) -> str:
    if not isinstance(value, datetime):
        return "-"
    return value.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def elapsed(job_record: object) -> str:
    start = getattr(job_record, "launched_at", None)
    if not isinstance(start, datetime):
        return "-"
    end = getattr(job_record, "completed_at", None)
    if not isinstance(end, datetime):
        end = datetime.now(timezone.utc)
    seconds = max(0, int((end - start).total_seconds()))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:d}:{minutes:02d}:{seconds:02d}"


def metrics_line(job_record: object) -> str:
    parts = []
    for metric in getattr(job_record, "metrics", None) or []:
        name = getattr(metric, "name", "?")
        done = getattr(metric, "n", "?")
        total = getattr(metric, "total", "?")
        parts.append(f"{name} {done}/{total}")
    return "  ".join(parts)


def fmt_config(value: object) -> str:
    if not value:
        return ""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            return value
    try:
        return json.dumps(value, indent=2, default=str, sort_keys=True)
    except (TypeError, ValueError):
        return str(value)


def print_detail(job_record: object, events_limit: int | None = 10) -> None:
    print(f"job_id:     {getattr(job_record, 'job_id', '-')}")
    print(f"status:     {job_status(job_record)}")
    print(f"type:       {getattr(job_record, 'job_type', '-')}")
    print(
        "target:     "
        f"{getattr(job_record, 'table_name', '-')}.{getattr(job_record, 'column_name', '-')}"
    )
    print(f"cluster:    {getattr(job_record, 'cluster_name', None) or '-'}")
    print(
        f"launched:   {fmt_dt(getattr(job_record, 'launched_at', None))} "
        f"by {getattr(job_record, 'launched_by', None) or '-'}"
    )
    print(f"updated:    {fmt_dt(getattr(job_record, 'updated_at', None))}")
    print(f"completed:  {fmt_dt(getattr(job_record, 'completed_at', None))}")
    print(f"elapsed:    {elapsed(job_record)}")

    object_ref = getattr(job_record, "object_ref", None)
    if object_ref:
        print(f"object_ref: {object_ref}")

    manifest_id = getattr(job_record, "manifest_id", None)
    if manifest_id:
        checksum = getattr(job_record, "manifest_checksum", None) or "-"
        print(f"manifest:   {manifest_id} (checksum {checksum})")

    config = fmt_config(getattr(job_record, "config", None))
    if config:
        print("config:")
        for line in config.splitlines():
            print(f"    {line}")

    metrics = getattr(job_record, "metrics", None) or []
    if metrics:
        print("metrics:")
        for metric in metrics:
            name = getattr(metric, "name", "?")
            done = getattr(metric, "n", "?")
            total = getattr(metric, "total", "?")
            desc = getattr(metric, "desc", "")
            print(f"    {name}: {done}/{total} {desc}")

    events = getattr(job_record, "events", None) or []
    if events:
        shown = events if events_limit is None else events[-events_limit:]
        hidden = len(events) - len(shown)
        label = f"events ({len(events)} total"
        label += f", showing last {len(shown)})" if hidden > 0 else ")"
        print(f"{label}:")
        for event in shown:
            print(f"    {event}")


def command_list(args: argparse.Namespace) -> int:
    config, conn = open_connection(args)

    if getattr(args, "job_id", None):
        try:
            job_record = conn.get_job(args.job_id)
        except ValueError:
            print(f"job {args.job_id} not found on {config.db_uri}", file=sys.stderr)
            return 1
        print_detail(job_record, events_limit=None if args.full_events else 10)
        return 0

    if args.status:
        statuses = [args.status.upper()]
    elif args.show_all:
        statuses = ALL_STATUSES
    else:
        statuses = ACTIVE_STATUSES

    records = list_job_records(conn, args.table, statuses)
    records.sort(
        key=lambda job_record: (
            getattr(job_record, "launched_at", None)
            or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=True,
    )

    scope = args.status or ("all" if args.show_all else "active (PENDING/RUNNING)")
    print(
        f"db_uri: {config.db_uri}   filter: {scope}   "
        f"showing: {min(len(records), args.limit)}/{len(records)}"
    )

    if not records:
        print("  (no matching jobs)")
        return 0

    header = (
        f"{'STATUS':<9} {'TYPE':<10} {'ELAPSED':>9}  "
        f"{'LAUNCHED (UTC)':<19}  TARGET / JOB"
    )
    print(header)
    print("-" * len(header))

    for job_record in records[: args.limit]:
        target = f"{getattr(job_record, 'table_name', '-')}.{getattr(job_record, 'column_name', '-')}"
        print(
            f"{job_status(job_record):<9} "
            f"{getattr(job_record, 'job_type', '-'):<10} "
            f"{elapsed(job_record):>9}  "
            f"{fmt_dt(getattr(job_record, 'launched_at', None)):<19}  "
            f"{target}  {getattr(job_record, 'job_id', '-')}"
        )
    return 0


def command_show(args: argparse.Namespace) -> int:
    config, conn = open_connection(args)
    try:
        job_record = conn.get_job(args.job_id)
    except ValueError:
        print(f"job {args.job_id} not found on {config.db_uri}", file=sys.stderr)
        return 1

    print_detail(job_record, events_limit=None if args.full_events else 10)
    return 0


def command_kill(args: argparse.Namespace) -> int:
    config, conn = open_connection(args)
    try:
        job_record = conn.get_job(args.job_id)
    except ValueError:
        print(f"job {args.job_id} not found on {config.db_uri}", file=sys.stderr)
        return 1

    status = job_status(job_record)
    target = f"{getattr(job_record, 'table_name', '-')}.{getattr(job_record, 'column_name', '-')}"

    if status in TERMINAL_STATUSES and not args.force:
        print(
            f"job {args.job_id} ({target}) is already {status}; nothing to mark "
            "(use --force to mark CANCELLED anyway)."
        )
        return 0

    # NOTE: this only flips the job row to CANCELLED in the _geneva_jobs table.
    # There is no public cancel API and no runner polls for an externally-set
    # CANCELLED status, so the driver, Ray actors, and workers keep running
    # until they finish on their own (and may overwrite the row with DONE/
    # FAILED). Be explicit so the user is not misled into thinking the
    # workload was terminated.
    if not args.yes:
        answer = input(
            f"Mark {status} job {args.job_id} ({target}) as CANCELLED? "
            "Running workers are NOT terminated and will continue until they "
            "finish. [y/N] "
        )
        if answer.strip().lower() not in {"y", "yes"}:
            print("aborted")
            return 1

    conn._history.set_completed(args.job_id, status="CANCELLED")
    print(
        f"marked job {args.job_id} row CANCELLED "
        "(running workers, if any, are not terminated)"
    )
    print_detail(conn.get_job(args.job_id))
    return 0


def command_tail(args: argparse.Namespace) -> int:
    config, conn = open_connection(args)
    try:
        job_record = conn.get_job(args.job_id)
    except ValueError:
        print(f"job {args.job_id} not found on {config.db_uri}", file=sys.stderr)
        return 1

    target = f"{getattr(job_record, 'table_name', '-')}.{getattr(job_record, 'column_name', '-')}"
    print(f"tailing job {args.job_id} ({target}) on {config.db_uri}")

    printed = 0
    last_metrics = ""
    last_status: str | None = None

    try:
        while True:
            events = getattr(job_record, "events", None) or []
            for event in events[printed:]:
                print(f"  {event}")
            printed = len(events)

            status = job_status(job_record)
            if status != last_status:
                print(f"  [status: {status}]")
                last_status = status

            metrics = metrics_line(job_record)
            if metrics and metrics != last_metrics:
                print(f"  [metrics: {metrics}]")
                last_metrics = metrics

            if args.once or status in TERMINAL_STATUSES:
                break

            time.sleep(max(0.5, args.interval))
            job_record = conn.get_job(args.job_id)
    except KeyboardInterrupt:
        print("")
        return 0

    print("")
    print_detail(job_record)
    return 0


def add_connection_options(
    parser: argparse.ArgumentParser, *, suppress_defaults: bool = False
) -> None:
    default = argparse.SUPPRESS if suppress_defaults else None
    config_default = argparse.SUPPRESS if suppress_defaults else DEFAULT_CONFIG
    parser.add_argument("--config", type=Path, default=config_default)
    parser.add_argument("--log-level", default=default or "WARNING")
    parser.add_argument("--db-uri", default=default)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Atlas jobs CLI: Geneva job records via port-forwarded Console API."
    )
    add_connection_options(parser)
    parser.add_argument("--job-id")
    parser.add_argument("--full-events", action="store_true")
    parser.add_argument("--table")
    parser.add_argument("--status")
    parser.add_argument("--all", dest="show_all", action="store_true")
    parser.add_argument("--limit", type=int, default=50)

    subparsers = parser.add_subparsers(dest="command")

    show_parser = subparsers.add_parser("show")
    add_connection_options(show_parser, suppress_defaults=True)
    show_parser.add_argument("job_id")
    show_parser.add_argument(
        "--full-events", action="store_true", default=argparse.SUPPRESS
    )

    kill_parser = subparsers.add_parser(
        "kill",
        help=(
            "Mark a job row CANCELLED. Does not terminate running workers; "
            "there is no cooperative cancel signal yet."
        ),
    )
    add_connection_options(kill_parser, suppress_defaults=True)
    kill_parser.add_argument("job_id")
    kill_parser.add_argument("--force", action="store_true")
    kill_parser.add_argument("--yes", "-y", action="store_true")

    tail_parser = subparsers.add_parser("tail")
    add_connection_options(tail_parser, suppress_defaults=True)
    tail_parser.add_argument("job_id")
    tail_parser.add_argument("--interval", type=float, default=2.0)
    tail_parser.add_argument("--once", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "config"):
        args.config = DEFAULT_CONFIG
    if not hasattr(args, "log_level") or args.log_level is None:
        args.log_level = "WARNING"
    if not hasattr(args, "db_uri"):
        args.db_uri = None
    if not hasattr(args, "full_events"):
        args.full_events = False

    try:
        if args.command == "show":
            return command_show(args)
        if args.command == "kill":
            return command_kill(args)
        if args.command == "tail":
            return command_tail(args)
        return command_list(args)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except ImportError as exc:
        print(
            "error: could not import a required package. Install the Geneva client "
            f"environment first. Details: {exc}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
