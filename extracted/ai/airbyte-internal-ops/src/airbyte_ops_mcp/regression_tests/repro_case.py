# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Reproduction cases: two connector versions against one seeded SaaS Sandbox scenario.

A case directory pins everything a reproduction needs -- the provider data, the
starting connector state, the catalog and what the run must produce -- so the
verdict is "the affected release violates the expectation and the fix
satisfies it", decided mechanically instead of by comparing two live runs.

Layout of `<case-dir>`; everything the sandbox consumes sits under `sandbox/`,
everything the connector and the regression CLI consume at the top level:

- `sandbox/dataset.json`: the twin's data (single provider), for
  `sandbox scenario apply`.
- `sandbox/behavior.json` (optional): a SaaS Sandbox behavior spec (failure
  rules), applied together with the dataset and kept in the baseline snapshot,
  so both sides see the same failures.
- `config.template.json`: connector config; the string `${SANDBOX_CREDENTIAL}`
  is replaced with the scenario's synthetic credential.
- `catalog.json`: the Airbyte configured catalog.
- `state.json` (optional): Airbyte input state for a warm read.
- `expectations.json`: the regression CLI's verdict input -- `records`
  (expected primary keys per stream), optional `final_state` (per-stream subset
  of the last emitted state) and optional `control_error_contains`.
- `origin.json` (optional): what the case reproduces -- the `ticket` URL, the
  `affected_image` release and the `affected_ref` commit of that release's
  source, so a case can be checked without the workflow inputs of one run.

The sandbox is driven only through its CLI. Every invocation inherits the same
`SAAS_API_URL`, `SAAS_API_KEY`, `SAAS_WORKSPACE_ID` and `XDG_STATE_HOME`, and
none passes `--local` or `--state-dir`: `--local` is rejected whenever
`SAAS_API_URL` is set, which `sandbox exec` exports to the wrapped CLI, and a
shared `XDG_STATE_HOME` keeps these calls on the same local state as `exec`.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import requests
import yaml
from airbyte_protocol.models import ConfiguredAirbyteCatalog
from pydantic import ValidationError

from airbyte_ops_mcp.docker_hub import is_image_on_docker_hub
from airbyte_ops_mcp.github_api import get_file_contents_at_ref
from airbyte_ops_mcp.regression_tests.models import (
    LEGACY_STATE_KEY,
    get_primary_keys_per_stream,
)

BASELINE_SNAPSHOT = "baseline"
CREDENTIAL_PLACEHOLDER = "${SANDBOX_CREDENTIAL}"
SANDBOX_ENV_VARS = (
    "SAAS_API_URL",
    "SAAS_API_KEY",
    "SAAS_WORKSPACE_ID",
    "XDG_STATE_HOME",
)
SANDBOX_COMMAND_TIMEOUT_SECONDS = 120
SANDBOX_INPUTS_DIR = "sandbox"
# What `scenario state` retains; a side that made more requests than this may
# have had its earliest traces, and so a twin gap, evicted.
SANDBOX_TRACE_RETENTION = 1000
# Only these prove the connector itself ran; a launcher's own JSON log line must
# not count as connector output.
AIRBYTE_MESSAGE_TYPES = frozenset(
    {
        "RECORD",
        "STATE",
        "LOG",
        "TRACE",
        "SPEC",
        "CATALOG",
        "CONNECTION_STATUS",
        "CONTROL",
    }
)


class SandboxError(RuntimeError):
    """A sandbox CLI call failed."""


class SandboxCli:
    """The one place that knows how ops-mcp invokes the `sandbox` CLI."""

    def __init__(
        self,
        executable: str = "sandbox",
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self.environment = dict(os.environ if environment is None else environment)
        missing = [name for name in SANDBOX_ENV_VARS if not self.environment.get(name)]
        if missing:
            raise SandboxError(
                "Reproduction cases need the sandbox connection variables: "
                f"{', '.join(missing)} not set"
            )
        resolved = shutil.which(executable, path=self.environment.get("PATH"))
        if resolved is None:
            raise SandboxError(f"`{executable}` CLI not found on PATH")
        self.executable = resolved

    def run(self, *arguments: str) -> str:
        """Run one sandbox command and return its stdout."""
        command = [self.executable, *arguments]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                env=self.environment,
                timeout=SANDBOX_COMMAND_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise SandboxError(
                f"`sandbox {' '.join(arguments)}` failed: {exc}"
            ) from exc
        if result.returncode != 0:
            raise SandboxError(
                f"`sandbox {' '.join(arguments)}` exited {result.returncode}: "
                f"{result.stderr.strip()[-500:]}"
            )
        return result.stdout

    def apply(self, name: str, dataset: Path, behavior: Path | None = None) -> str:
        """Create or reset a scenario from a dataset; returns its UUID.

        Without `behavior` the sandbox clears any failure rules the scenario had.
        """
        arguments = ["scenario", "apply", name, "--dataset", str(dataset)]
        if behavior is not None:
            arguments += ["--behavior", str(behavior)]
        payload = json.loads(self.run(*arguments, "--json"))
        scenario_id = payload.get("id") if isinstance(payload, dict) else None
        if not isinstance(scenario_id, str) or not scenario_id:
            raise SandboxError(f"`scenario apply` returned no scenario id: {payload!r}")
        return scenario_id

    def snapshot(self, scenario_id: str, name: str = BASELINE_SNAPSHOT) -> None:
        self.run("scenario", "snapshot", scenario_id, name)

    def restore(self, scenario_id: str, name: str = BASELINE_SNAPSHOT) -> int:
        """Restore a snapshot; returns the scenario generation it starts."""
        payload = json.loads(self.run("scenario", "restore", scenario_id, name))
        generation = payload.get("generation") if isinstance(payload, dict) else None
        if type(generation) is not int:
            raise SandboxError(
                f"`scenario restore` returned no generation: {payload!r}"
            )
        return generation

    def traces(self, scenario_id: str) -> list[dict[str, Any]]:
        """The scenario's retained request traces (the newest 1,000)."""
        payload = json.loads(self.run("scenario", "state", scenario_id))
        traces = payload.get("traces") if isinstance(payload, dict) else None
        if not isinstance(traces, list):
            raise SandboxError("`scenario state` returned no traces")
        return [trace for trace in traces if isinstance(trace, dict)]

    def credential(self, scenario_id: str) -> str:
        payload = json.loads(self.run("scenario", "credentials", scenario_id, "--json"))
        api_key = payload.get("api_key") if isinstance(payload, dict) else None
        if not isinstance(api_key, str) or not api_key:
            raise SandboxError("`scenario credentials` returned no api_key")
        return api_key


CASE_COMMANDS = ("read", "check")
FAILURE_TYPES = ("config_error", "system_error", "transient_error")
# The CHECK outcome a fix can be held to; "FAILED" needs a case to judge it by.
CHECK_STATUSES = ("SUCCEEDED",)
_RECORDS_MODE_KEYS = (
    "records",
    "final_state",
    "record_fields",
    "allow_duplicate_pks",
    "new_streams",
)
_FAILURE_KEYS = ("target_error_contains", "target_failure_type")
EXPECTATION_KEYS = frozenset(
    {
        "command",
        *_RECORDS_MODE_KEYS,
        *_FAILURE_KEYS,
        "check_status",
        "control_error_contains",
    }
)


def _optional_text(payload: Mapping[str, Any], key: str) -> str | None:
    value = payload.get(key)
    if value is not None and (not isinstance(value, str) or not value):
        raise ValueError(f"`{key}` must be a non-empty string")
    return value


def _stream_list(payload: Mapping[str, Any], key: str) -> tuple[str, ...]:
    value = payload.get(key, [])
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(f"`{key}` must be a list of stream names")
    if len(set(value)) != len(value):
        raise ValueError(f"`{key}` lists a stream twice")
    return tuple(value)


@dataclass(frozen=True)
class CaseExpectations:
    """What the fixed connector does, which each side is held to.

    Three modes: **records** (a read's records and final state, the default),
    **failure** (`target_error_contains`: the fixed read fails that way) and
    **check** (`command: check`: the fixed CHECK outcome).
    """

    records: dict[str, list[dict[str, Any]]]
    final_state: dict[str, Any] = field(default_factory=dict)
    control_error_contains: str | None = None
    command: str = "read"
    record_fields: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    allow_duplicate_pks: tuple[str, ...] = ()
    new_streams: tuple[str, ...] = ()
    target_error_contains: str | None = None
    target_failure_type: str | None = None
    check_status: str | None = None

    @property
    def mode(self) -> str:
        if self.command == "check":
            return "check"
        return "failure" if self.target_error_contains else "records"

    @classmethod
    def from_json(cls, payload: Any) -> CaseExpectations:
        if not isinstance(payload, dict):
            raise ValueError("expectations.json must be a JSON object")
        unknown = set(payload) - EXPECTATION_KEYS
        if unknown:
            raise ValueError(f"Unknown expectations keys: {', '.join(sorted(unknown))}")
        command = payload.get("command", "read")
        if command not in CASE_COMMANDS:
            raise ValueError(f"`command` must be one of {', '.join(CASE_COMMANDS)}")
        error = _optional_text(payload, "control_error_contains")
        target_error = _optional_text(payload, "target_error_contains")
        failure_type = payload.get("target_failure_type")
        if failure_type is not None and failure_type not in FAILURE_TYPES:
            raise ValueError(
                f"`target_failure_type` must be one of {', '.join(FAILURE_TYPES)}"
            )
        check_status = payload.get("check_status")
        if check_status is not None and check_status not in CHECK_STATUSES:
            raise ValueError(
                f"`check_status` must be one of {', '.join(CHECK_STATUSES)}"
            )
        present = set(payload)
        if command == "check":
            # A CHECK reads no records, and a failed CHECK only reproduces the
            # bug when it fails for the case's reason.
            if check_status is None or error is None:
                raise ValueError(
                    "a `command: check` case needs `check_status` and "
                    "`control_error_contains`"
                )
            refused = present & {*_RECORDS_MODE_KEYS, *_FAILURE_KEYS}
        elif "check_status" in present:
            raise ValueError("`check_status` needs `command: check`")
        elif target_error is not None or failure_type is not None:
            if target_error is None:
                raise ValueError("`target_failure_type` needs `target_error_contains`")
            refused = present & set(_RECORDS_MODE_KEYS)
        else:
            refused = set()
        if refused:
            raise ValueError(
                f"{', '.join(sorted(refused))} cannot be combined with "
                f"{'`command: check`' if command == 'check' else '`target_error_contains`'}"
            )
        records = payload.get("records", {})
        if (
            command == "read"
            and target_error is None
            and (not isinstance(records, dict) or not records)
        ):
            raise ValueError("expectations.json needs a non-empty `records` object")
        for stream, rows in records.items():
            if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
                raise ValueError(f"`records.{stream}` must be a list of objects")
        final_state = payload.get("final_state", {})
        if not isinstance(final_state, dict):
            raise ValueError("`final_state` must be an object keyed by stream")
        record_fields = payload.get("record_fields", {})
        if not isinstance(record_fields, dict) or not all(
            isinstance(rows, list) and rows and all(isinstance(r, dict) for r in rows)
            for rows in record_fields.values()
        ):
            raise ValueError(
                "`record_fields` must map streams to non-empty lists of objects"
            )
        return cls(
            records=records,
            final_state=final_state,
            control_error_contains=error,
            command=command,
            record_fields=record_fields,
            allow_duplicate_pks=_stream_list(payload, "allow_duplicate_pks"),
            new_streams=_stream_list(payload, "new_streams"),
            target_error_contains=target_error,
            target_failure_type=failure_type,
            check_status=check_status,
        )


CONNECTOR_REPOS = ("airbyte", "airbyte-enterprise")
IMAGE_PATTERN = re.compile(r"[a-z0-9][a-z0-9._/-]*:[A-Za-z0-9._-]+")
SHA_PATTERN = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True)
class CaseOrigin:
    """What a case reproduces: the ticket and the affected release and source."""

    ticket: str
    affected_image: str
    affected_ref: str
    repo: str = "airbyte"
    # The saas-sandbox commit the case was validated on.
    sandbox_ref: str | None = None

    @property
    def image_repository(self) -> str:
        return self.affected_image.rsplit(":", 1)[0]

    @property
    def image_tag(self) -> str:
        return self.affected_image.rsplit(":", 1)[1]

    @classmethod
    def from_json(cls, payload: Any) -> CaseOrigin:
        if not isinstance(payload, dict):
            raise ValueError("origin.json must be a JSON object")
        keys = {"ticket", "affected_image", "affected_ref", "repo", "sandbox_ref"}
        unknown = set(payload) - keys
        if unknown:
            raise ValueError(f"Unknown origin keys: {', '.join(sorted(unknown))}")
        missing = keys - {"repo", "sandbox_ref"} - set(payload)
        if missing:
            raise ValueError(f"origin.json is missing {', '.join(sorted(missing))}")
        ticket = payload["ticket"]
        if not isinstance(ticket, str) or not ticket.startswith("https://"):
            raise ValueError("`ticket` must be an https URL")
        image = payload["affected_image"]
        if not isinstance(image, str) or not IMAGE_PATTERN.fullmatch(image):
            raise ValueError(
                "`affected_image` must be a tagged image, e.g. airbyte/source-x:1.2.3"
            )
        ref = payload["affected_ref"]
        # A full SHA, because a branch or tag could move after the case is frozen.
        if not isinstance(ref, str) or not SHA_PATTERN.fullmatch(ref):
            raise ValueError("`affected_ref` must be a full 40-character commit SHA")
        repo = payload.get("repo", "airbyte")
        if repo not in CONNECTOR_REPOS:
            raise ValueError(f"`repo` must be one of {', '.join(CONNECTOR_REPOS)}")
        sandbox_ref = payload.get("sandbox_ref")
        if sandbox_ref is not None and (
            not isinstance(sandbox_ref, str) or not SHA_PATTERN.fullmatch(sandbox_ref)
        ):
            raise ValueError(
                "origin.json sandbox_ref must be a full 40-character commit SHA"
            )
        return cls(
            ticket=ticket,
            affected_image=image,
            affected_ref=ref,
            repo=repo,
            sandbox_ref=sandbox_ref,
        )


def origin_metadata_problems(
    origin: CaseOrigin, metadata: Mapping[str, Any]
) -> list[str]:
    """Where a connector's `metadata.yaml` at `affected_ref` disagrees with the origin.

    The affected source must be the source of the affected release, or a case
    checked against both could pass on two different connectors.
    """
    data = metadata.get("data", metadata)
    problems = []
    if data.get("dockerRepository") != origin.image_repository:
        problems.append(
            f"metadata.yaml at {origin.affected_ref} names dockerRepository "
            f"{data.get('dockerRepository')!r}, not {origin.image_repository!r}"
        )
    if str(data.get("dockerImageTag")) != origin.image_tag:
        problems.append(
            f"metadata.yaml at {origin.affected_ref} has dockerImageTag "
            f"{data.get('dockerImageTag')!r}, not {origin.image_tag!r}"
        )
    return problems


def check_case_origin(
    origin: CaseOrigin, connector_name: str, token: str | None
) -> list[str]:
    """Problems with an origin, read from GitHub and Docker Hub; empty if none."""
    path = f"airbyte-integrations/connectors/{connector_name}/metadata.yaml"
    text = get_file_contents_at_ref(
        "airbytehq", origin.repo, path, origin.affected_ref, token
    )
    if text is None:
        return [f"{path} not found in airbytehq/{origin.repo} at {origin.affected_ref}"]
    problems = origin_metadata_problems(origin, yaml.safe_load(text) or {})
    try:
        published = is_image_on_docker_hub(origin.image_repository, origin.image_tag)
    except requests.HTTPError as exc:
        if exc.response is None or exc.response.status_code != 404:
            raise
        published = False
    if not published:
        problems.append(f"{origin.affected_image} is not published on Docker Hub")
    return problems


@dataclass(frozen=True)
class ReproCase:
    directory: Path
    expectations: CaseExpectations
    primary_keys: dict[str, list[list[str]]]
    origin: CaseOrigin | None = None
    # Per `record_fields` stream, the cursor a deduplicating destination keeps
    # the highest record by, or None when it keeps the last one emitted.
    dedup_cursors: dict[str, tuple[str, ...] | None] = field(default_factory=dict)
    # Per `record_fields` stream, the primary keys whose kept record is checked.
    checked_keys: dict[str, frozenset[tuple[str, ...]]] = field(default_factory=dict)
    # The failure rules the case's behavior.json injects.
    injected_failures: tuple[InjectedFailure, ...] = ()

    @property
    def name(self) -> str:
        return self.directory.name

    @property
    def dataset_path(self) -> Path:
        return self.directory / SANDBOX_INPUTS_DIR / "dataset.json"

    @property
    def behavior_path(self) -> Path | None:
        path = self.directory / SANDBOX_INPUTS_DIR / "behavior.json"
        return path if path.exists() else None

    @property
    def config_template_path(self) -> Path:
        return self.directory / "config.template.json"

    @property
    def catalog_path(self) -> Path:
        return self.directory / "catalog.json"

    @property
    def state_path(self) -> Path | None:
        path = self.directory / "state.json"
        return path if path.exists() else None

    @classmethod
    def load(cls, directory: Path) -> ReproCase:
        """Load and validate a case, so a malformed file fails here with a message."""
        # A case can come from an unreviewed PR head and is read as data only,
        # so nothing in it may point outside it.
        links = [directory] if directory.is_symlink() else []
        for parent, names, files in os.walk(directory):
            links.extend(
                path
                for path in (Path(parent) / name for name in (*names, *files))
                if path.is_symlink()
            )
        if links:
            raise ValueError(
                f"Reproduction case {directory} must not contain symlinks: "
                + ", ".join(str(link) for link in links)
            )
        directory = directory.resolve()
        for required in (
            f"{SANDBOX_INPUTS_DIR}/dataset.json",
            "config.template.json",
            "catalog.json",
            "expectations.json",
        ):
            if not (directory / required).is_file():
                raise ValueError(f"Reproduction case {directory} is missing {required}")
        try:
            expectations = CaseExpectations.from_json(
                json.loads((directory / "expectations.json").read_text())
            )
            origin_path = directory / "origin.json"
            origin = (
                CaseOrigin.from_json(json.loads(origin_path.read_text()))
                if origin_path.exists()
                else None
            )
            catalog = ConfiguredAirbyteCatalog.model_validate_json(
                (directory / "catalog.json").read_text()
            )
            # The sandbox validates the spec itself on apply; this only makes
            # an unreadable file fail when the case loads.
            behavior = directory / SANDBOX_INPUTS_DIR / "behavior.json"
            behavior_spec = (
                json.loads(behavior.read_text()) if behavior.exists() else None
            )
            if behavior.exists() and not isinstance(behavior_spec, dict):
                raise ValueError(f"{behavior} must be a JSON object")
            # Its presence alone makes the read a warm one, so an unreadable or
            # `null` state must not get that far.
            state = directory / "state.json"
            if state.exists() and not isinstance(
                json.loads(state.read_text()), (list, dict)
            ):
                raise ValueError(f"{state} must be a JSON list or object")
        except (json.JSONDecodeError, ValidationError) as exc:
            raise ValueError(
                f"Reproduction case {directory} is malformed: {exc}"
            ) from exc
        primary_keys = {
            stream: pk
            for stream, pk in get_primary_keys_per_stream(catalog).items()
            if pk
        }
        for stream, rows in expectations.records.items():
            if stream not in primary_keys:
                raise ValueError(
                    f"Expected stream {stream!r} has no primary key in catalog.json"
                )
            keys = {".".join(path) for path in primary_keys[stream]}
            seen: set[str] = set()
            for row in rows:
                if set(row) != keys:
                    raise ValueError(
                        f"Expected {stream} record {row!r} must have exactly the "
                        f"primary key fields {sorted(keys)}"
                    )
                # Rows are compared as a set, so a duplicate would silently
                # expect one record where the author meant two.
                key = json.dumps(row, sort_keys=True)
                if key in seen:
                    raise ValueError(
                        f"Expected {stream} record {row!r} is listed twice"
                    )
                seen.add(key)
        # A misspelled stream would make both sides miss the state, which goal
        # `reproduced` would read as both reproducing the bug.
        catalog_streams = {stream.stream.name for stream in catalog.streams}
        for stream in expectations.final_state:
            if stream not in catalog_streams:
                raise ValueError(
                    f"Expected final state for {stream!r}, which catalog.json "
                    "does not configure"
                )
        if expectations.mode == "failure":
            # A clean exit violates only after a response attributable to one
            # of the case's failure rules.
            problems = _failure_mode_rule_problems(behavior_spec)
            if problems:
                raise ValueError(
                    "A case with `target_error_contains` " + "; ".join(problems)
                )
        return cls(
            directory,
            expectations,
            primary_keys,
            origin,
            dedup_cursors=_check_v2_streams(expectations, catalog, primary_keys),
            checked_keys={
                stream: frozenset(_pk_tuple(row, primary_keys[stream]) for row in rows)
                for stream, rows in expectations.record_fields.items()
            },
            injected_failures=_injected_failures(behavior_spec),
        )


def _pk_tuple(row: Mapping[str, Any], pk: Sequence[Sequence[str]]) -> tuple[str, ...]:
    return tuple(json.dumps(row[".".join(path)]) for path in pk)


def _check_v2_streams(
    expectations: CaseExpectations,
    catalog: ConfiguredAirbyteCatalog,
    primary_keys: Mapping[str, list[list[str]]],
) -> dict[str, tuple[str, ...] | None]:
    """Validate the streams the v2 keys name; returns each `record_fields` cursor."""
    for key in ("allow_duplicate_pks", "new_streams", "record_fields"):
        for stream in getattr(expectations, key):
            if stream not in expectations.records:
                raise ValueError(f"`{key}` names {stream!r}, which `records` does not")
    for stream in expectations.new_streams:
        # The fix must be able to show the stream works.
        if not expectations.records[stream]:
            raise ValueError(f"`new_streams` stream {stream!r} needs expected records")
    configured = {entry.stream.name: entry for entry in catalog.streams}
    cursors: dict[str, tuple[str, ...] | None] = {}
    for stream, rows in expectations.record_fields.items():
        pk = primary_keys[stream]
        keys = {".".join(path) for path in pk}
        expected = {_pk_tuple(row, pk) for row in expectations.records[stream]}
        seen: set[tuple[str, ...]] = set()
        for row in rows:
            if not keys <= set(row) or not set(row) - keys:
                raise ValueError(
                    f"`record_fields.{stream}` row {row!r} needs the primary key "
                    f"fields {sorted(keys)} and at least one other field"
                )
            key = _pk_tuple(row, pk)
            if key not in expected:
                raise ValueError(
                    f"`record_fields.{stream}` row {row!r} is for a record "
                    "`records` does not expect"
                )
            if key in seen:
                raise ValueError(f"`record_fields.{stream}` lists {key} twice")
            seen.add(key)
        entry = configured[stream]
        dedup = (
            entry.sync_mode.value == "incremental"
            and entry.destination_sync_mode.value == "append_dedup"
        )
        cursor = entry.cursor_field or entry.stream.default_cursor_field
        cursors[stream] = tuple(cursor) if dedup and cursor else None
    return cursors


@dataclass(frozen=True)
class InjectedFailure:
    """One failure rule: the status it sets and the method and path it matches."""

    status: int
    provider: str
    method: str
    path: str

    def answered(self, trace: Mapping[str, Any]) -> bool:
        """Whether a trace is a response this rule could have produced.

        Traces carry no rule id (nor operation id or query), so the status
        must be the rule's and the request's method and path the rule's, as
        the sandbox matches them: a `{param}` path template matches any one
        segment, so a request whose parameter value spans path segments is
        never attributed and leaves a clean exit inconclusive. A rule's `when` schedule
        is not checked, so the twin's own response with the same status to the
        same request also counts.
        """
        if trace.get("status") != self.status or trace.get("unsupported"):
            return False
        if trace.get("provider") not in (None, self.provider):
            return False
        if trace.get("method") != self.method:
            return False
        pattern = re.sub(r"\\\{[^/]*?\\\}", "[^/]+", re.escape(self.path))
        return re.fullmatch(pattern, str(trace.get("path"))) is not None


def _failure_rules(behavior: Any) -> list[tuple[str, dict[str, Any]]]:
    """A behavior spec's failure rules with their provider (the sandbox validates it)."""
    providers = behavior.get("providers") if isinstance(behavior, dict) else None
    if not isinstance(providers, dict):
        return []
    return [
        (str(provider), rule)
        for provider, spec in providers.items()
        for rule in (spec.get("failures") if isinstance(spec, dict) else None) or []
        if isinstance(rule, dict)
    ]


def _injected_failures(behavior: Any) -> tuple[InjectedFailure, ...]:
    """The failure rules a trace can be attributed to: by method and path."""
    failures = []
    for provider, rule in _failure_rules(behavior):
        match = rule.get("match")
        if (
            type(rule.get("status")) is int
            and isinstance(match, dict)
            and isinstance(match.get("method"), str)
            and isinstance(match.get("path"), str)
            and "query" not in match
        ):
            failures.append(
                InjectedFailure(
                    rule["status"], provider, match["method"], match["path"]
                )
            )
    return tuple(failures)


def _failure_mode_rule_problems(behavior: Any) -> list[str]:
    """Why a failure case's rules cannot show that the failure reached a side."""
    rules = _failure_rules(behavior)
    if not rules:
        return ["needs sandbox/behavior.json with at least one failure rule"]
    problems = []
    for _provider, rule in rules:
        match = rule.get("match")
        if not isinstance(match, dict):
            match = {}
        name = rule.get("id", "?")
        if "operation" in match:
            # Request traces record method and path, not the operation id.
            problems.append(
                f"failure rule {name!r} must match by method and path in failure "
                "mode, not by operation"
            )
        elif "query" in match:
            problems.append(
                f"failure rule {name!r} cannot match on query in failure mode: "
                "request traces do not record it"
            )
    return problems


def render_config(template_path: Path, credential: str, destination: Path) -> Path:
    """Write the connector config with the scenario credential substituted."""
    template = json.loads(template_path.read_text())

    def substitute(value: Any) -> Any:
        if isinstance(value, str):
            return value.replace(CREDENTIAL_PLACEHOLDER, credential)
        if isinstance(value, list):
            return [substitute(item) for item in value]
        if isinstance(value, dict):
            return {key: substitute(item) for key, item in value.items()}
        return value

    rendered = substitute(template)
    if rendered == template:
        raise ValueError(f"{template_path} does not contain {CREDENTIAL_PLACEHOLDER}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(rendered, indent=2))
    # Only the CLI reads this file; it writes its own copy for the container.
    destination.chmod(0o600)
    return destination


def set_up_scenario(
    case: ReproCase,
    sandbox: SandboxCli,
    *,
    scenario_name: str,
    config_destination: Path,
) -> tuple[str, Path, str]:
    """Apply the dataset and behavior, snapshot the baseline and render the config.

    Returns:
        The scenario UUID, the rendered config path and the credential (for
        masking).
    """
    scenario_id = sandbox.apply(scenario_name, case.dataset_path, case.behavior_path)
    sandbox.snapshot(scenario_id)
    credential = sandbox.credential(scenario_id)
    config_path = render_config(
        case.config_template_path, credential, config_destination
    )
    return scenario_id, config_path, credential


class SideOutcome(Enum):
    SATISFIES = "satisfies"
    VIOLATES = "violates"
    INCONCLUSIVE = "inconclusive"
    # The twin marked a request it does not support, so the run says nothing
    # about the connector; the caller should fall back to a live account.
    TWIN_GAP = "twin_gap"


@dataclass(frozen=True)
class SandboxSide:
    """What the sandbox reported around one side's connector run."""

    restore_error: str | None = None
    generation: int | None = None
    twin_gaps: tuple[str, ...] = ()
    gap_check_error: str | None = None
    # Requests the twin traced for this side; None until the traces are read.
    requests: int | None = None
    # Of those, responses with a status the case's failure rules inject.
    injected_responses: int | None = None


def restore_side(sandbox: SandboxCli, scenario_id: str) -> SandboxSide:
    """Restore the baseline before one side and note the generation it starts."""
    try:
        return SandboxSide(generation=sandbox.restore(scenario_id))
    except (SandboxError, json.JSONDecodeError) as exc:
        return SandboxSide(restore_error=str(exc))


def check_twin_gaps(
    sandbox: SandboxCli,
    scenario_id: str,
    side: SandboxSide,
    injected_failures: Sequence[InjectedFailure] = (),
) -> SandboxSide:
    """Collect the requests the twin marked unsupported during one side.

    The baseline restore starts a new scenario generation, so the side's
    requests are exactly the traces carrying that generation. A twin gap is a
    trace with an `X-Sandbox-Unsupported` marker (an operation or parameter the
    twin does not implement) or a 501 response.
    """
    if side.restore_error or side.generation is None:
        return side
    try:
        traces = sandbox.traces(scenario_id)
    except (SandboxError, json.JSONDecodeError) as exc:
        return replace(side, gap_check_error=f"could not read traces: {exc}")
    gaps = sorted(
        {
            f"{trace.get('method')} {trace.get('path')}: "
            + str(trace.get("unsupported") or "unsupported operation (HTTP 501)")
            for trace in traces
            if trace.get("generation") == side.generation
            and (trace.get("unsupported") or trace.get("status") == 501)
        }
    )
    if (
        not gaps
        and len(traces) >= SANDBOX_TRACE_RETENTION
        and all(trace.get("generation") == side.generation for trace in traces)
    ):
        return replace(
            side,
            gap_check_error=(
                f"the side made at least {SANDBOX_TRACE_RETENTION} requests (the "
                "trace retention limit), so the sandbox may have evicted a twin gap"
            ),
        )
    own = [trace for trace in traces if trace.get("generation") == side.generation]
    injected = sum(
        any(failure.answered(trace) for failure in injected_failures) for trace in own
    )
    return replace(
        side, twin_gaps=tuple(gaps), requests=len(own), injected_responses=injected
    )


@dataclass(frozen=True)
class SideEvaluation:
    outcome: SideOutcome
    reason: str
    findings: tuple[str, ...] = ()


@dataclass(frozen=True)
class StreamFinding:
    """One way a completed side missed the case, and the stream it is about.

    `stream` is None for a finding that is not about one stream; such a finding
    always counts as evidence.
    """

    stream: str | None
    message: str


def classify_findings(
    findings: Sequence[StreamFinding], record_counts: Mapping[str, int]
) -> SideEvaluation:
    """Judge a completed side by its findings and the records it emitted per stream.

    A stream the side emitted no records for cannot supply its violation: an
    empty read still emits a start cursor and misses every expected record, so
    two such sides would otherwise pass `reproduced` without reproducing
    anything. A side whose findings are all on such streams is inconclusive.
    """
    if not findings:
        return SideEvaluation(
            SideOutcome.SATISFIES, "completed and met the expectation"
        )
    messages = tuple(finding.message for finding in findings)
    if any(
        finding.stream is None or record_counts.get(finding.stream, 0) > 0
        for finding in findings
    ):
        return SideEvaluation(
            SideOutcome.VIOLATES, "completed but missed the expectation", messages
        )
    empty = sorted(
        {finding.stream for finding in findings if finding.stream is not None}
    )
    return SideEvaluation(
        SideOutcome.INCONCLUSIVE,
        f"completed without emitting a record for {', '.join(empty)}, so nothing "
        "was reproduced there",
        messages,
    )


class ReproGoal(Enum):
    """What a case run must show."""

    # The affected release reproduces the bug and the fix does not.
    FIXED = "fixed"
    # Both sides reproduce it: the case gate's check, with the unmodified
    # source of the affected release as the target.
    REPRODUCED = "reproduced"


@dataclass(frozen=True)
class ReproductionVerdict:
    """The case-mode verdict, in the vocabulary every report surface shares."""

    success: bool
    regression_detected: bool
    label: str
    detail: str
    control: SideEvaluation
    target: SideEvaluation
    goal: ReproGoal = ReproGoal.FIXED

    @property
    def sides(self) -> tuple[tuple[str, SideEvaluation], ...]:
        return (("control", self.control), ("target", self.target))

    @property
    def details(self) -> tuple[str, ...]:
        return tuple(
            f"{side}: {finding}"
            for side, evaluation in self.sides
            for finding in evaluation.findings
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "label": self.label,
            "detail": self.detail,
            **self.sides_dict(),
        }

    def sides_dict(self) -> dict[str, dict[str, Any]]:
        return {
            side: {
                "outcome": evaluation.outcome.value,
                "reason": evaluation.reason,
                "findings": list(evaluation.findings),
            }
            for side, evaluation in self.sides
        }


@dataclass
class _ReadOutput:
    protocol_messages: int = 0
    records: dict[str, Counter[tuple[str, ...]]] = field(default_factory=dict)
    # Records per stream the case judges (`records` and `final_state`), by name.
    record_counts: Counter[str] = field(default_factory=Counter)
    # Every stream a RECORD, STATE or stream-status TRACE names.
    mentioned_streams: set[str] = field(default_factory=set)
    # Per `record_fields` stream and primary key, the record a deduplicating
    # destination keeps, with its cursor value.
    kept_records: dict[str, dict[tuple[str, ...], tuple[Any, Any]]] = field(
        default_factory=dict
    )
    # ERROR traces' `failure_type`, `message`, `internal_message`, `stack_trace`.
    errors: list[dict[str, Any]] = field(default_factory=list)


def _cursor_key(value: Any) -> tuple[str, Any] | None:
    """How a non-null cursor value sorts; None when it compares with nothing."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        # Kept as is: Python compares ints and floats exactly.
        return ("number", value)
    if isinstance(value, str):
        try:
            instant = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        if instant.tzinfo is None:
            instant = instant.replace(tzinfo=timezone.utc)
        return ("instant", instant)
    return None


def _replaces(new: Any, kept: Any) -> bool:
    """Whether a destination keeps the later-emitted cursor `new` over `kept`.

    Highest cursor first, nulls last, then the record emitted last: a null
    never wins over a value, and values that do not compare are a tie.
    """
    if new is None:
        return kept is None
    if kept is None:
        return True
    new_key, kept_key = _cursor_key(new), _cursor_key(kept)
    if new_key is None or kept_key is None or new_key[0] != kept_key[0]:
        return True
    return bool(new_key[1] >= kept_key[1])


def _state_streams(message: Mapping[str, Any]) -> list[Any]:
    state = message.get("state")
    if not isinstance(state, dict):
        return []
    entries = [state.get("stream")]
    global_state = state.get("global")
    if isinstance(global_state, dict) and isinstance(
        global_state.get("stream_states"), list
    ):
        entries += global_state["stream_states"]
    return [
        entry["stream_descriptor"].get("name")
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("stream_descriptor"), dict)
    ]


def _pk_value(record: Mapping[str, Any], path: Sequence[str]) -> Any:
    value: Any = record
    for part in path:
        value = value.get(part) if isinstance(value, Mapping) else None
    return value


def _parse_read_output(stdout_file: Path, case: ReproCase) -> _ReadOutput:
    output = _ReadOutput()
    if not stdout_file.is_file():
        return output
    judged = {*case.expectations.records, *case.expectations.final_state}
    with stdout_file.open(errors="replace") as lines:
        for raw in lines:
            line = raw.strip()
            if not line.startswith("{"):
                continue
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                continue
            message_type = message.get("type") if isinstance(message, dict) else None
            # Connector stdout is arbitrary JSON; an unhashable `type` must not
            # crash the membership test.
            if not isinstance(message_type, str) or (
                message_type not in AIRBYTE_MESSAGE_TYPES
            ):
                continue
            output.protocol_messages += 1
            if message_type == "RECORD":
                record = message.get("record")
                if not isinstance(record, dict):
                    continue
                stream = record.get("stream")
                if isinstance(stream, str):
                    output.mentioned_streams.add(stream)
                if isinstance(stream, str) and stream in judged:
                    output.record_counts[stream] += 1
                    if stream in case.expectations.records:
                        data = record.get("data") or {}
                        key = tuple(
                            json.dumps(_pk_value(data, path))
                            for path in case.primary_keys[stream]
                        )
                        output.records.setdefault(stream, Counter())[key] += 1
                        if key in case.checked_keys.get(stream, ()):
                            _keep_record(output, case, stream, key, data)
            elif message_type == "STATE":
                output.mentioned_streams.update(
                    name for name in _state_streams(message) if isinstance(name, str)
                )
            elif message_type == "TRACE":
                trace = message.get("trace")
                if not isinstance(trace, dict):
                    continue
                status = trace.get("stream_status")
                descriptor = (
                    status.get("stream_descriptor")
                    if isinstance(status, dict)
                    else None
                )
                # The CDK reports a configured stream the source does not
                # define as INCOMPLETE and nothing else, so that alone is no
                # sign the release knows it.
                if (
                    isinstance(descriptor, dict)
                    and isinstance(descriptor.get("name"), str)
                    and status.get("status") != "INCOMPLETE"
                ):
                    output.mentioned_streams.add(descriptor["name"])
                error = trace.get("error")
                if not isinstance(error, dict):
                    continue
                output.errors.append(
                    {
                        key: error.get(key)
                        for key in (
                            "failure_type",
                            "message",
                            "internal_message",
                            "stack_trace",
                        )
                    }
                )
    return output


def _keep_record(
    output: _ReadOutput,
    case: ReproCase,
    stream: str,
    key: tuple[str, ...],
    data: Any,
) -> None:
    """Keep the record a deduplicating destination would keep for this key."""
    cursor_path = case.dedup_cursors[stream]
    cursor = (
        _pk_value(data, cursor_path)
        if cursor_path is not None and isinstance(data, Mapping)
        else None
    )
    kept = output.kept_records.setdefault(stream, {})
    if key not in kept or cursor_path is None or _replaces(cursor, kept[key][0]):
        kept[key] = (cursor, data)


def _contains(actual: Any, expected: Any) -> bool:
    """Whether `actual` holds `expected`: dict keys recursively, anything else equal."""
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(
            key in actual and _contains(actual[key], value)
            for key, value in expected.items()
        )
    return actual == expected


def evaluate_side(
    result: Mapping[str, Any],
    case: ReproCase,
    *,
    sandbox_side: SandboxSide,
    final_states: Mapping[tuple[str | None, str], Any] | None,
) -> SideEvaluation:
    """Classify one side as satisfying, violating or inconclusive.

    Precedence matters: a side must first have *completed* -- its baseline
    restore succeeded, the twin supported every request it made, and the
    connector itself ran (it emitted protocol messages) -- before its output or
    errors count. Anything else is inconclusive (or a twin gap) however its
    logs read.

    Args:
        final_states: The side's final state per `(namespace, stream)`, as
            `ComparableOutputs.final_states` collects it (STREAM, GLOBAL and
            LEGACY state alike).
    """
    blocked = _sandbox_side_evaluation(sandbox_side)
    if blocked is not None:
        return blocked

    output = _parse_read_output(Path(str(result.get("stdout_file", ""))), case)
    if output.protocol_messages == 0:
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"no Airbyte protocol output (exit {result.get('exit_code')}); the "
            "connector did not run, which points at the sandbox launcher or Docker",
        )

    if case.expectations.mode == "check":
        return _evaluate_check(result, output, case, sandbox_side)
    if case.expectations.mode == "failure":
        return _evaluate_failure(result, output, case, sandbox_side)

    if not result.get("success"):
        expected_error = case.expectations.control_error_contains
        stderr = _stderr(result)
        if expected_error and _expected_error_found(output, stderr, expected_error):
            return SideEvaluation(
                SideOutcome.VIOLATES,
                f"failed with the expected error ({expected_error!r})",
            )
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"failed (exit {result.get('exit_code')}) without the expected error",
            _error_summary(output, stderr),
        )

    # Positive evidence, so it holds even with no request and no record: the
    # gate confirms the stream is absent from the affected release's manifest.
    undefined = [
        stream
        for stream in case.expectations.new_streams
        if stream not in output.mentioned_streams
    ]
    if undefined:
        return SideEvaluation(
            SideOutcome.VIOLATES,
            "completed without any output for a stream the case declares new",
            tuple(
                f"{stream}: the release does not define this stream"
                for stream in undefined
            ),
        )

    if sandbox_side.requests == 0:
        # A clean exit that never reached the twin says nothing about the bug:
        # judged as "violates", two such sides would pass `reproduced`.
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            "completed without a single request to the twin",
        )

    if case.expectations.final_state and LEGACY_STATE_KEY in (final_states or {}):
        # A legacy state blob has no per-stream entries to hold the expectation
        # against, and missing them on both sides would pass `reproduced`.
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            "emitted LEGACY state, which cannot be checked against the case's "
            "per-stream final_state",
        )

    findings: list[StreamFinding] = []
    for stream, rows in case.expectations.records.items():
        expected = {
            tuple(json.dumps(row[".".join(path)]) for path in case.primary_keys[stream])
            for row in rows
        }
        counts = output.records.get(stream, Counter())
        missing = sorted(expected - set(counts))
        unexpected = sorted(set(counts) - expected)
        # A record emitted twice is the boundary bug class this lane exists for,
        # unless the stream legitimately emits one per event.
        duplicated = (
            []
            if stream in case.expectations.allow_duplicate_pks
            else sorted(key for key, count in counts.items() if count > 1)
        )
        if missing:
            findings.append(
                StreamFinding(
                    stream, f"{stream}: missing {len(missing)} record(s) {missing[:5]}"
                )
            )
        if unexpected:
            findings.append(
                StreamFinding(
                    stream,
                    f"{stream}: {len(unexpected)} unexpected record(s) {unexpected[:5]}",
                )
            )
        if duplicated:
            findings.append(
                StreamFinding(
                    stream,
                    f"{stream}: {len(duplicated)} record(s) emitted more than once "
                    f"{duplicated[:5]}",
                )
            )
    for stream, rows in case.expectations.record_fields.items():
        kept = output.kept_records.get(stream, {})
        pk_fields = {".".join(path) for path in case.primary_keys[stream]}
        for row in rows:
            key = _pk_tuple(row, case.primary_keys[stream])
            if key not in kept:
                findings.append(
                    StreamFinding(
                        stream, f"{stream}: no record {key} to check fields of"
                    )
                )
                continue
            data = kept[key][1]
            fields = {
                name: value for name, value in row.items() if name not in pk_fields
            }
            if not _contains(data, fields):
                shown = (
                    {name: data.get(name) for name in fields}
                    if isinstance(data, Mapping)
                    else data
                )
                findings.append(
                    StreamFinding(
                        stream,
                        f"{stream}: the kept record {key} has "
                        f"{json.dumps(shown)[:300]}, not {json.dumps(fields)[:300]}",
                    )
                )
    states = {name: state for (_namespace, name), state in (final_states or {}).items()}
    for stream, expected_state in case.expectations.final_state.items():
        if stream not in states:
            # Distinct from an emitted `null`, which an expected `null` matches.
            findings.append(StreamFinding(stream, f"{stream}: emitted no final state"))
            continue
        actual_state = states[stream]
        if not _contains(actual_state, expected_state):
            findings.append(
                StreamFinding(
                    stream,
                    f"{stream}: final state {json.dumps(actual_state)[:300]} does "
                    f"not contain {json.dumps(expected_state)[:300]}",
                )
            )

    return classify_findings(findings, output.record_counts)


def _stderr(result: Mapping[str, Any]) -> str:
    stderr_file = Path(str(result.get("stderr_file", "")))
    return stderr_file.read_text(errors="replace") if stderr_file.is_file() else ""


_ERROR_TEXT_KEYS = ("message", "internal_message", "stack_trace")
# Not `message`: the CDK's generic user-facing text would let a loose
# `control_error_contains` match any crash.
_CONTROL_ERROR_KEYS = ("internal_message", "stack_trace")


def _error_texts(
    output: _ReadOutput, keys: Sequence[str] = _CONTROL_ERROR_KEYS
) -> list[str]:
    return [
        error[key]
        for error in output.errors
        for key in keys
        if isinstance(error.get(key), str)
    ]


def _expected_error_found(output: _ReadOutput, stderr: str, expected: str) -> bool:
    return any(expected in text for text in (*_error_texts(output), stderr))


def _error_summary(
    output: _ReadOutput, stderr: str, keys: Sequence[str] = _CONTROL_ERROR_KEYS
) -> tuple[str, ...]:
    errors = [text.splitlines()[0][:300] for text in _error_texts(output, keys) if text]
    return tuple(errors[:3] or stderr.strip().splitlines()[-3:])


def _matches_fixed_error(output: _ReadOutput, expectations: CaseExpectations) -> bool:
    """Whether one ERROR trace has the fixed failure's text and failure type."""
    text = expectations.target_error_contains or ""
    return any(
        (
            expectations.target_failure_type is None
            or error.get("failure_type") == expectations.target_failure_type
        )
        and any(
            isinstance(error.get(key), str) and text in error[key]
            for key in _ERROR_TEXT_KEYS
        )
        for error in output.errors
    )


def _evaluate_failure(
    result: Mapping[str, Any],
    output: _ReadOutput,
    case: ReproCase,
    side: SandboxSide,
) -> SideEvaluation:
    """A case whose fixed read fails with `target_error_contains`.

    `message` counts here, unlike for `control_error_contains`: a declarative
    `HttpResponseFilter`'s `error_message` reaches only `message`.
    """
    expectations = case.expectations
    reached_twin = side.requests != 0
    if not result.get("success"):
        stderr = _stderr(result)
        if reached_twin and _matches_fixed_error(output, expectations):
            return SideEvaluation(
                SideOutcome.SATISFIES,
                f"failed with the fixed error ({expectations.target_error_contains!r})",
            )
        expected_error = expectations.control_error_contains
        if (
            reached_twin
            and expected_error
            and _expected_error_found(output, stderr, expected_error)
        ):
            return SideEvaluation(
                SideOutcome.VIOLATES,
                f"failed with the expected error ({expected_error!r})",
            )
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"failed (exit {result.get('exit_code')}) without the fixed or the "
            "expected error"
            + ("" if reached_twin else ", before a single request to the twin"),
            _error_summary(output, stderr, _ERROR_TEXT_KEYS),
        )
    if side.injected_responses:
        return SideEvaluation(
            SideOutcome.VIOLATES,
            f"completed although the twin answered {side.injected_responses} "
            "request(s) with the case's injected failure",
        )
    return SideEvaluation(
        SideOutcome.INCONCLUSIVE,
        "completed without a response carrying the case's injected failure, so "
        "the failure never reached the connector",
    )


def _exited_cleanly(result: Mapping[str, Any]) -> bool:
    """The container's exit status, never the CHECK verdict.

    A run result's `success` is the exit status, but an annotated copy (see
    `_annotate_run_verdict`) carries the verdict there and the exit status as
    `exited_cleanly`.
    """
    if "exited_cleanly" in result:
        return bool(result["exited_cleanly"])
    return result.get("exit_code") == 0


def _evaluate_check(
    result: Mapping[str, Any],
    output: _ReadOutput,
    case: ReproCase,
    side: SandboxSide,
) -> SideEvaluation:
    """A `command: check` case: the fixed CHECK succeeds."""
    status = result.get("connection_status")
    message = str(result.get("connection_status_message") or "")
    expected_error = case.expectations.control_error_contains or ""
    if side.requests == 0:
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"CHECK {status or 'emitted no status'} without a single request to the twin",
        )
    if status in ("SUCCEEDED", "FAILED") and not _exited_cleanly(result):
        # The CDK exits 0 after either status; a crash after it says nothing,
        # and two such crashes would otherwise pass `reproduced`.
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"CHECK reported {status} but exited {result.get('exit_code')}",
            (message[:300],) if message else (),
        )
    if status == "SUCCEEDED":
        return SideEvaluation(SideOutcome.SATISFIES, "CHECK succeeded")
    texts = [message, *_error_texts(output, _ERROR_TEXT_KEYS)]
    if status == "FAILED" and any(expected_error in text for text in texts):
        return SideEvaluation(
            SideOutcome.VIOLATES,
            f"CHECK failed with the expected error ({expected_error!r})",
        )
    if status is None:
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"emitted no connection status (exit {result.get('exit_code')})",
            _error_summary(output, _stderr(result)),
        )
    return SideEvaluation(
        SideOutcome.INCONCLUSIVE,
        f"CHECK {status} without the expected error",
        (message[:300],) if message else (),
    )


def _sandbox_side_evaluation(side: SandboxSide) -> SideEvaluation | None:
    """The outcome the sandbox alone decides for a side, if it decides one."""
    if side.restore_error:
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE, f"baseline restore failed: {side.restore_error}"
        )
    if side.twin_gaps:
        return SideEvaluation(
            SideOutcome.TWIN_GAP, f"twin gap: {side.twin_gaps[0]}", side.twin_gaps
        )
    if side.gap_check_error:
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE, f"twin-gap check failed: {side.gap_check_error}"
        )
    return None


def evaluate_reproduction(
    control: SideEvaluation,
    target: SideEvaluation,
    goal: ReproGoal = ReproGoal.FIXED,
) -> ReproductionVerdict:
    """Pass only when the sides do what `goal` asks of them.

    A twin gap takes precedence over everything else, because it tells the
    caller to switch to a live account; an inconclusive side comes next.
    """
    outcomes = (control.outcome, target.outcome)
    if SideOutcome.TWIN_GAP in outcomes:
        success, regression, label, conclusion = (
            False,
            False,
            "FAIL (twin gap)",
            "the twin does not support a request the connector made; test against "
            "a live account instead",
        )
    elif SideOutcome.INCONCLUSIVE in outcomes:
        success, regression, label, conclusion = (
            False,
            False,
            "FAIL (inconclusive)",
            "inconclusive",
        )
    elif goal is ReproGoal.REPRODUCED:
        satisfied = [
            side
            for side, evaluation in (("control", control), ("target", target))
            if evaluation.outcome is SideOutcome.SATISFIES
        ]
        success, regression, label, conclusion = (
            (
                False,
                False,
                "FAIL (not reproduced)",
                f"the {' and the '.join(satisfied)} satisfies the case",
            )
            if satisfied
            else (
                True,
                False,
                "PASS (reproduced)",
                "reproduced on both the control and the target",
            )
        )
    elif target.outcome is SideOutcome.VIOLATES:
        success, regression, label, conclusion = (
            False,
            True,
            "FAIL (not fixed)",
            "the target does not satisfy the case",
        )
    elif control.outcome is SideOutcome.SATISFIES:
        success, regression, label, conclusion = (
            False,
            False,
            "FAIL (not reproduced)",
            "the control does not reproduce the bug",
        )
    else:
        success, regression, label, conclusion = (
            True,
            False,
            "PASS (reproduced and fixed)",
            "reproduced on the control, fixed on the target",
        )
    detail = (
        f"control {control.outcome.value} ({control.reason}); "
        f"target {target.outcome.value} ({target.reason}) — {conclusion}"
    )
    return ReproductionVerdict(
        success, regression, label, detail, control, target, goal
    )


CASE_RESULT_FILE = "result.json"
CASE_RESULT_SCHEMA_VERSION = 1


def case_result(
    verdict: ReproductionVerdict,
    case: ReproCase,
    *,
    control_image: str,
    target_image: str,
) -> dict[str, Any]:
    """The `result.json` a case run leaves behind, as far as the CLI knows it.

    `sandbox-case-run.yml` fills the keys left as None (where the case and the
    target came from, the saas-sandbox commit and the run URL), and writes the
    same shape itself, with verdict `ERROR`, when there is no verdict.
    """
    return {
        "schema_version": CASE_RESULT_SCHEMA_VERSION,
        "verdict": verdict.label,
        "passed": verdict.success,
        "goal": verdict.goal.value,
        "detail": verdict.detail,
        "error": None,
        "case": {
            "connector": case.directory.parent.name,
            "name": case.name,
            "root": None,
            "ref": None,
        },
        "control": {"image": control_image},
        "target": {
            "image": target_image,
            "pr": None,
            "connector_ref": None,
            "commit": None,
        },
        "twin_gaps": sorted(
            {
                gap
                for _side, evaluation in verdict.sides
                if evaluation.outcome is SideOutcome.TWIN_GAP
                for gap in evaluation.findings
            }
        ),
        "sides": verdict.sides_dict(),
        "sandbox_ref": None,
        "run_url": None,
    }
