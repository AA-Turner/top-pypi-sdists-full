# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Read compactions in flight from a LanceDB Enterprise Job Registry (GEN-994).

Read-only: Geneva never writes to the registry. The agent records each
compaction it runs as a job under
``<root>/_jobs/v1/l/<hash>_tb/<db>:<namespace>$<table>/``, one directory per
job holding ``active.lance`` until the job finishes. This module lists a
table's unfinished ``compact`` jobs so a Geneva job can wait for them before it
plans. An unreadable record stops admission: skipping it could let a backfill
plan against fragments a compaction is still replacing.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import time
from typing import Any, Protocol

import attrs

_LOG = logging.getLogger(__name__)

U64_MAX = (1 << 64) - 1

# Sophon's job_type for a compaction of a table.
COMPACTION_JOB_TYPE = "compact"
FOOTER_KEY = "lancedb.job_coordinator.job_event_file"
ACTIVE_FILE = "active.lance"
TERMINAL_STATES = frozenset({"succeeded", "failed", "canceled", "timed_out"})
RECORD_FILES = frozenset({ACTIVE_FILE, *(f"{s}.lance" for s in TERMINAL_STATES)})
LIVE_PREFIX = "_jobs/v1/l"
# Match Sophon's registry-managed terminal-record retention. Cancellation
# fences new claims, but an already executing commit can still be draining.
WORKER_DRAIN_MARGIN_MS = 5 * 60 * 1000
PRELAUNCH_FAILURE_PHASES = frozenset(
    {"geneva_backfill_active", "geneva_backfill_check"}
)

_CONNECT_TIMEOUT_S = 10
_READ_TIMEOUT_S = 30


def distribution_hash(value: str) -> str:
    """Sophon's ``distribution_hash_prefix``: FNV-1a-64, bits reversed, top 32."""
    h = 0xCBF29CE484222325
    for byte in value.encode():
        h = ((h ^ byte) * 0x100000001B3) & U64_MAX
    reversed_bits = int(f"{h:064b}"[::-1], 2)
    return f"{reversed_bits >> 32:08x}"


@attrs.define(frozen=True)
class RegistryTableRef:
    """A table as Sophon's registry names it."""

    database: str
    namespace: tuple[str, ...]
    table: str

    @classmethod
    def for_table(cls, database: str, table_id: list[str]) -> RegistryTableRef:
        """Mirror Sophon's ``registry_table_ref_from_parts``.

        Path segments of ``database`` after the first lead the namespace, and
        the root namespace is named ``public``.
        """
        db_name, *db_namespace = database.split("/")
        *namespace, table = table_id
        if namespace == ["public"]:
            namespace = []
        full = (*db_namespace, *namespace) or ("public",)
        return cls(db_name, full, table)

    @property
    def dist_key(self) -> str:
        return f"{self.database}:{'$'.join(self.namespace)}${self.table}"

    @property
    def prefix(self) -> str:
        """The record directory for this table, relative to the registry root."""
        table_hash = distribution_hash("tb_" + self.dist_key)
        return f"{LIVE_PREFIX}/{table_hash}_tb/{self.dist_key}"


class RecordReader(Protocol):
    """The read operations listing a table's records needs."""

    def get(self, key: str) -> bytes: ...
    def list(self, prefix: str) -> list[str]: ...


class S3RecordReader:
    """Records under ``s3://bucket/prefix``."""

    def __init__(
        self,
        bucket: str,
        prefix: str,
        *,
        region: str | None,
        client: Any = None,
    ) -> None:
        self._bucket = bucket
        self._prefix = prefix.strip("/")
        self._client = client or self._default_client(region)

    @staticmethod
    def _default_client(region: str | None) -> Any:
        import boto3
        from botocore.config import Config

        return boto3.client(
            "s3",
            region_name=region,
            config=Config(
                connect_timeout=_CONNECT_TIMEOUT_S,
                read_timeout=_READ_TIMEOUT_S,
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        )

    def _key(self, key: str) -> str:
        return f"{self._prefix}/{key}" if self._prefix else key

    def get(self, key: str) -> bytes:
        from botocore.exceptions import ClientError

        try:
            out = self._client.get_object(Bucket=self._bucket, Key=self._key(key))
        except ClientError as exc:
            code = str(getattr(exc, "response", {}).get("Error", {}).get("Code", ""))
            if code == "NoSuchKey":
                raise FileNotFoundError(key) from exc
            raise
        return out["Body"].read()

    def list(self, prefix: str) -> list[str]:
        full = self._key(prefix).rstrip("/") + "/"
        strip = len(self._key(""))
        keys = []
        for page in self._client.get_paginator("list_objects_v2").paginate(
            Bucket=self._bucket, Prefix=full
        ):
            keys.extend(obj["Key"][strip:] for obj in page.get("Contents", []))
        return keys


class LocalRecordReader:
    """Records under a local directory, for tests and local deployments."""

    def __init__(self, root: str) -> None:
        self._root = root

    def _path(self, key: str) -> str:
        return os.path.join(self._root, *key.split("/"))

    def get(self, key: str) -> bytes:
        with open(self._path(key), "rb") as f:
            return f.read()

    def list(self, prefix: str) -> list[str]:
        def fail(error: OSError) -> None:
            raise error

        keys = []
        path = self._path(prefix)
        if not os.path.isdir(self._root):
            raise FileNotFoundError(self._root)
        # The registry root must exist, but a table with no jobs has no prefix.
        if not os.path.exists(path):
            return []
        for dirpath, _, files in os.walk(path, onerror=fail):
            for name in files:
                rel = os.path.relpath(os.path.join(dirpath, name), self._root)
                keys.append(rel.replace(os.sep, "/"))
        return keys


def reader_for(root_uri: str, region: str | None = None) -> RecordReader | None:
    """The reader for a registry root, or None for an unsupported scheme."""
    if root_uri.startswith("s3://"):
        bucket, _, prefix = root_uri.removeprefix("s3://").partition("/")
        region = region or os.environ.get("AWS_REGION")
        region = region or os.environ.get("AWS_DEFAULT_REGION")
        return S3RecordReader(bucket, prefix, region=region)
    if root_uri.startswith("file://") or "://" not in root_uri:
        return LocalRecordReader(root_uri.removeprefix("file://"))
    _LOG.warning(
        "Job registry root %s is not supported (S3 or local only); "
        "not checking it for running compactions",
        root_uri,
    )
    return None


def decode_footer(data: bytes) -> dict[str, Any]:
    """The footer of a registry record: JSON in the Lance file's schema metadata."""
    from lance.file import LanceFileReader

    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, "record.lance")
        with open(path, "wb") as f:
            f.write(data)
        metadata = LanceFileReader(path).metadata().schema.metadata or {}
    return json.loads(metadata[FOOTER_KEY.encode()])


def _record_job_type(record_dir: str) -> str | None:
    """The job type of ``<rev16>-<job_key>-<job_type>``, or None if malformed."""
    parts = record_dir.split("-", 2)
    if len(parts) != 3 or len(parts[0]) != 16:
        return None
    try:
        int(parts[0], 16)
    except ValueError:
        return None
    return parts[2]


def _may_have_workers(footer: dict[str, Any], now_ms: int) -> bool:
    state = footer["latest_state"]
    started = footer.get("execution_started_at_millis")
    epoch = footer.get("active_execution_epoch")
    if state == "succeeded":
        return False  # the single commit owner finished publishing
    if state in {"created", "queued"}:
        # Never wait for jobs that still need admission. They publish InProgress
        # before checking Geneva, so they cannot pass our already active row.
        return footer["version"] < 4 or (
            (started is not None or epoch is not None)
            and footer.get("pause_drained_at_millis") is None
        )
    if state == "in_progress":
        return True
    if state not in TERMINAL_STATES:
        raise ValueError(f"Unknown compaction state: {state!r}")
    failure = footer.get("failure") or {}
    if state == "failed" and failure.get("phase") in PRELAUNCH_FAILURE_PHASES:
        return False  # Sophon's Geneva check failed before launching any worker
    if started is None and epoch is None:
        # Old metadata did not persist execution provenance. Only current
        # records can prove this job was canceled before it ever started.
        return footer["version"] < 4
    ttl = footer.get("execution_ttl_millis")
    completed = footer.get("completed_at_millis")
    if not isinstance(ttl, int) or ttl <= 0 or not isinstance(completed, int):
        return True
    return now_ms <= completed + ttl + WORKER_DRAIN_MARGIN_MS


def in_flight_compactions(
    reader: RecordReader, table: RegistryTableRef, *, now_ms: int | None = None
) -> list[str]:
    """Compactions that can still replace fragments, including terminal drains.

    Read failures propagate. A disappearing active file is followed to its
    terminal file, which may still have workers draining after cancellation.
    """
    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
    job_ids = []
    for key in reader.list(table.prefix):
        record_dir, _, file_name = key.rpartition("/")
        job_type = _record_job_type(record_dir.rsplit("/", 1)[-1])
        if file_name not in RECORD_FILES or job_type != COMPACTION_JOB_TYPE:
            continue
        try:
            footer = decode_footer(reader.get(key))
        except FileNotFoundError:
            if file_name != ACTIVE_FILE:
                raise
            # Terminalization writes the terminal file before deleting active.
            # Follow the move instead of missing a canceled worker's drain.
            for state in sorted(TERMINAL_STATES):
                try:
                    footer = decode_footer(reader.get(f"{record_dir}/{state}.lance"))
                    break
                except FileNotFoundError:
                    continue
            else:
                raise
        if (
            not isinstance(footer.get("version"), int)
            or footer["version"] < 1
            or footer["version"] > 7
            or footer.get("job_type") != COMPACTION_JOB_TYPE
            or not isinstance(footer.get("job_id"), str)
            or not footer["job_id"]
            or not isinstance(footer.get("latest_state"), str)
        ):
            raise ValueError(f"Invalid compaction registry metadata: {key}")
        for field in (
            "execution_started_at_millis",
            "active_execution_epoch",
            "execution_ttl_millis",
            "completed_at_millis",
            "pause_drained_at_millis",
        ):
            if footer.get(field) is not None and type(footer[field]) is not int:
                raise ValueError(f"Invalid compaction {field}: {key}")
        if _may_have_workers(footer, now_ms) and footer["job_id"] not in job_ids:
            job_ids.append(footer["job_id"])
    return job_ids
