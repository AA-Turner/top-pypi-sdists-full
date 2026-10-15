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


@dataclass(frozen=True)
class CaseExpectations:
    records: dict[str, list[dict[str, Any]]]
    final_state: dict[str, Any] = field(default_factory=dict)
    control_error_contains: str | None = None

    @classmethod
    def from_json(cls, payload: Any) -> CaseExpectations:
        if not isinstance(payload, dict):
            raise ValueError("expectations.json must be a JSON object")
        unknown = set(payload) - {"records", "final_state", "control_error_contains"}
        if unknown:
            raise ValueError(f"Unknown expectations keys: {', '.join(sorted(unknown))}")
        records = payload.get("records")
        if not isinstance(records, dict) or not records:
            raise ValueError("expectations.json needs a non-empty `records` object")
        for stream, rows in records.items():
            if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
                raise ValueError(f"`records.{stream}` must be a list of objects")
        final_state = payload.get("final_state", {})
        if not isinstance(final_state, dict):
            raise ValueError("`final_state` must be an object keyed by stream")
        error = payload.get("control_error_contains")
        if error is not None and (not isinstance(error, str) or not error):
            raise ValueError("`control_error_contains` must be a non-empty string")
        return cls(
            records=records, final_state=final_state, control_error_contains=error
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
            if behavior.exists() and not isinstance(
                json.loads(behavior.read_text()), dict
            ):
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
        return cls(directory, expectations, primary_keys, origin)


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


def restore_side(sandbox: SandboxCli, scenario_id: str) -> SandboxSide:
    """Restore the baseline before one side and note the generation it starts."""
    try:
        return SandboxSide(generation=sandbox.restore(scenario_id))
    except (SandboxError, json.JSONDecodeError) as exc:
        return SandboxSide(restore_error=str(exc))


def check_twin_gaps(
    sandbox: SandboxCli, scenario_id: str, side: SandboxSide
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
    requests = sum(trace.get("generation") == side.generation for trace in traces)
    return replace(side, twin_gaps=tuple(gaps), requests=requests)


@dataclass(frozen=True)
class SideEvaluation:
    outcome: SideOutcome
    reason: str
    findings: tuple[str, ...] = ()


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
    error_texts: list[str] = field(default_factory=list)


def _pk_value(record: Mapping[str, Any], path: Sequence[str]) -> Any:
    value: Any = record
    for part in path:
        value = value.get(part) if isinstance(value, Mapping) else None
    return value


def _parse_read_output(stdout_file: Path, case: ReproCase) -> _ReadOutput:
    output = _ReadOutput()
    if not stdout_file.is_file():
        return output
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
                if isinstance(stream, str) and stream in case.expectations.records:
                    key = tuple(
                        json.dumps(_pk_value(record.get("data") or {}, path))
                        for path in case.primary_keys[stream]
                    )
                    output.records.setdefault(stream, Counter())[key] += 1
            elif message_type == "TRACE":
                trace = message.get("trace")
                error = trace.get("error") if isinstance(trace, dict) else None
                if not isinstance(error, dict):
                    continue
                # Not `message`: the CDK's generic user-facing text would let a
                # loose `control_error_contains` match any crash.
                for key in ("internal_message", "stack_trace"):
                    if isinstance(error.get(key), str):
                        output.error_texts.append(error[key])
    return output


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

    if not result.get("success"):
        expected_error = case.expectations.control_error_contains
        stderr_file = Path(str(result.get("stderr_file", "")))
        stderr = (
            stderr_file.read_text(errors="replace") if stderr_file.is_file() else ""
        )
        if expected_error and any(
            expected_error in text for text in (*output.error_texts, stderr)
        ):
            return SideEvaluation(
                SideOutcome.VIOLATES,
                f"failed with the expected error ({expected_error!r})",
            )
        errors = [text.splitlines()[0][:300] for text in output.error_texts if text]
        return SideEvaluation(
            SideOutcome.INCONCLUSIVE,
            f"failed (exit {result.get('exit_code')}) without the expected error",
            tuple(errors[:3] or stderr.strip().splitlines()[-3:]),
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

    findings: list[str] = []
    for stream, rows in case.expectations.records.items():
        expected = {
            tuple(json.dumps(row[".".join(path)]) for path in case.primary_keys[stream])
            for row in rows
        }
        counts = output.records.get(stream, Counter())
        missing = sorted(expected - set(counts))
        unexpected = sorted(set(counts) - expected)
        # A record emitted twice is the boundary bug class this lane exists for.
        duplicated = sorted(key for key, count in counts.items() if count > 1)
        if missing:
            findings.append(f"{stream}: missing {len(missing)} record(s) {missing[:5]}")
        if unexpected:
            findings.append(
                f"{stream}: {len(unexpected)} unexpected record(s) {unexpected[:5]}"
            )
        if duplicated:
            findings.append(
                f"{stream}: {len(duplicated)} record(s) emitted more than once "
                f"{duplicated[:5]}"
            )
    states = {name: state for (_namespace, name), state in (final_states or {}).items()}
    for stream, expected_state in case.expectations.final_state.items():
        if stream not in states:
            # Distinct from an emitted `null`, which an expected `null` matches.
            findings.append(f"{stream}: emitted no final state")
            continue
        actual_state = states[stream]
        if not _contains(actual_state, expected_state):
            findings.append(
                f"{stream}: final state {json.dumps(actual_state)[:300]} does not "
                f"contain {json.dumps(expected_state)[:300]}"
            )

    if findings:
        return SideEvaluation(
            SideOutcome.VIOLATES,
            "completed but missed the expectation",
            tuple(findings),
        )
    return SideEvaluation(SideOutcome.SATISFIES, "completed and met the expectation")


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
