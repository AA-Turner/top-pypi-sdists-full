# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Models for live tests - connector testing without Dagger."""

from __future__ import annotations

import json
import logging
import re
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import IO, Any, Callable, Iterator, Literal

from airbyte_protocol.models import (
    AirbyteCatalog,
    AirbyteMessage,
    AirbyteStateType,
    AirbyteStreamState,
    ConfiguredAirbyteCatalog,
    TraceType,
)
from airbyte_protocol.models import Type as AirbyteMessageType
from pydantic import ValidationError

from airbyte_ops_mcp.regression_tests.normalization import to_plain_dict, to_stream_id

# The labels the two states that belong to no single stream are compared under.
# Parenthesised so they read as not-a-stream -- and because they are keyed like
# any other stream, a connector that names one of these anyway is disambiguated
# when the comparison labels it rather than silently merged into it.
SHARED_STATE_LABEL = "(shared)"
LEGACY_STATE_LABEL = "(legacy)"

# How a run's output is written: `masked` masks it in the write pass, so raw
# records never reach disk; `raw` keeps what the connector emitted. Here
# rather than in `masking`, so the MCP tool can name the modes without
# importing the masking library and the comparators behind it.
OutputMode = Literal["masked", "raw"]
OUTPUT_MODES: tuple[OutputMode, ...] = ("masked", "raw")

# The identities those two are keyed by, alongside the real streams. The empty
# namespace is what makes them unreachable as a stream: `to_stream_id` maps a falsy
# namespace to `None`, so no connector-declared stream can key here, not even one
# that names itself `(shared)`. It still *labels* as the bare sentinel, because
# `stream_label` treats an empty namespace as no namespace.
SHARED_STATE_KEY: tuple[str | None, str] = ("", SHARED_STATE_LABEL)
LEGACY_STATE_KEY: tuple[str | None, str] = ("", LEGACY_STATE_LABEL)

MAX_STREAM_STATUSES_PER_STREAM = 16
MAX_STREAM_ERRORS_PER_KEY = 5
MAX_ERROR_MESSAGE_CHARS = 200


class Command(Enum):
    """Airbyte connector commands."""

    CHECK = "check"
    DISCOVER = "discover"
    READ = "read"
    READ_WITH_STATE = "read-with-state"
    SPEC = "spec"

    def needs_config(self) -> bool:
        return self in {
            Command.CHECK,
            Command.DISCOVER,
            Command.READ,
            Command.READ_WITH_STATE,
        }

    def needs_catalog(self) -> bool:
        return self in {Command.READ, Command.READ_WITH_STATE}

    def needs_state(self) -> bool:
        return self in {Command.READ_WITH_STATE}


class TargetOrControl(Enum):
    """Indicates whether a connector is the target (new) or control (baseline) version."""

    TARGET = "target"
    CONTROL = "control"


class ActorType(Enum):
    """Type of Airbyte actor."""

    SOURCE = "source"
    DESTINATION = "destination"


@dataclass
class ConnectorUnderTest:
    """Represents a connector being tested.

    In validation tests, there would be one connector under test.
    When running regression tests, there would be two connectors under test:
    the target and the control versions of the same connector.
    """

    image_name: str
    target_or_control: TargetOrControl

    @property
    def name(self) -> str:
        """Get connector name without registry prefix."""
        return self.image_name.replace("airbyte/", "").split(":")[0]

    @property
    def name_without_type_prefix(self) -> str:
        """Get connector name without actor type prefix."""
        return self.name.replace(f"{self.actor_type.value}-", "")

    @property
    def version(self) -> str:
        """Get connector version from image tag."""
        return self.image_name.replace("airbyte/", "").split(":")[1]

    @property
    def actor_type(self) -> ActorType:
        """Infer actor type from image name."""
        if "airbyte/destination-" in self.image_name:
            return ActorType.DESTINATION
        elif "airbyte/source-" in self.image_name:
            return ActorType.SOURCE
        else:
            raise ValueError(
                f"Can't infer the actor type. Connector image name {self.image_name} "
                "does not contain 'airbyte/source' or 'airbyte/destination'"
            )

    @classmethod
    def from_image_name(
        cls,
        image_name: str,
        target_or_control: TargetOrControl,
    ) -> ConnectorUnderTest:
        """Create a ConnectorUnderTest from an image name."""
        return cls(image_name, target_or_control)


@dataclass
class ExecutionInputs:
    """Inputs for executing a connector command."""

    connector_under_test: ConnectorUnderTest
    command: Command
    output_dir: Path
    config: dict[str, Any] | None = None
    configured_catalog: ConfiguredAirbyteCatalog | None = None
    state: dict[str, Any] | None = None
    environment_variables: dict[str, str] | None = None

    def __post_init__(self) -> None:
        """Validate that required inputs are present for the command."""
        if self.command.needs_config() and self.config is None:
            raise ValueError(f"Config is required for {self.command.value} command")
        if self.command.needs_catalog() and self.configured_catalog is None:
            raise ValueError(f"Catalog is required for {self.command.value} command")
        if self.command.needs_state() and self.state is None:
            raise ValueError(f"State is required for {self.command.value} command")


@dataclass(frozen=True)
class StoppedEarly:
    """Why the harness cut a run short, instead of the connector ending it.

    A read stopped at a deadline or a record cap is not a crash and not a
    complete run: its output is real up to the point it stopped, and nothing
    past that point can be compared. `records_seen` is the number of RECORD
    messages in the stdout that was kept.
    """

    reason: Literal["timeout", "cap"]
    records_seen: int
    elapsed_s: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "reason": self.reason,
            "records_seen": self.records_seen,
            "elapsed_s": self.elapsed_s,
        }


@dataclass(frozen=True)
class StreamError:
    failure_type: str | None
    message: str | None


# Distinct `ANALYTICS` types one summary keeps. The CDK emits a handful per
# run; the cap is what keeps the summary bounded if a connector emits one per
# page instead.
MAX_ANALYTICS_TYPES = 32


@dataclass
class MessageSummary:
    """Everything bounded that one pass over a run's messages can collect.

    A `read` emits the whole dataset, so nothing here may grow with it: counts,
    the first spec, catalog and connection status, one state blob per stream,
    and the last value of each analytics counter -- the CDK emits those once
    per run, so they number a handful whatever the dataset. `ExecutionResult`
    fills one of these the first time anything asks, and `save_artifacts`
    fills it on the same pass that writes the files, so the output is parsed
    once however many questions are asked of it.
    """

    message_counts: dict[AirbyteMessageType, int] = field(
        default_factory=lambda: defaultdict(int)
    )
    record_counts_per_stream: dict[str, int] = field(
        default_factory=lambda: defaultdict(int)
    )
    spec: Any | None = None
    catalog: AirbyteCatalog | None = None
    connection_status: Any | None = None
    final_states: dict[tuple[str | None, str], Any] = field(default_factory=dict)
    stream_statuses: dict[str, list[str]] = field(default_factory=dict)
    stream_errors: dict[str | None, list[StreamError]] = field(default_factory=dict)
    # `ANALYTICS` trace type to the value it last carried, as the protocol
    # carries it: a string, or `None` when the message declared no value. Last
    # one wins, which is the pair that saw the whole run if a run somehow
    # emitted two. Reading a number out of it is the caller's job; see
    # `http_metrics.parse_connector_cache_metrics`. Capped at
    # `MAX_ANALYTICS_TYPES` distinct types, so a connector that mints a type
    # per page cannot grow this with the read.
    analytics: dict[str, str | None] = field(default_factory=dict)

    def add(self, message: AirbyteMessage) -> None:
        kind = message.type
        self.message_counts[kind] += 1
        if kind is AirbyteMessageType.RECORD:
            self.record_counts_per_stream[message.record.stream] += 1
        elif kind is AirbyteMessageType.STATE and message.state is not None:
            _fold_state(self.final_states, message.state)
        elif kind is AirbyteMessageType.TRACE and message.trace is not None:
            trace = message.trace
            if trace.type is TraceType.ANALYTICS and trace.analytics is not None:
                name = trace.analytics.type
                # The first `MAX_ANALYTICS_TYPES` types are kept and updated;
                # a type past the cap is dropped. A run that floods the cap
                # before its counters arrive loses them, and reads as "not
                # reported" -- bounded memory is the property that matters.
                if name in self.analytics or len(self.analytics) < MAX_ANALYTICS_TYPES:
                    self.analytics[name] = trace.analytics.value
            elif (
                trace.type is TraceType.STREAM_STATUS
                and trace.stream_status is not None
                and trace.stream_status.stream_descriptor is not None
            ):
                name = trace.stream_status.stream_descriptor.name
                statuses = self.stream_statuses.setdefault(name, [])
                if len(statuses) < MAX_STREAM_STATUSES_PER_STREAM:
                    status = trace.stream_status.status
                    statuses.append(str(getattr(status, "value", status)))
            elif trace.type is TraceType.ERROR and trace.error is not None:
                descriptor = trace.error.stream_descriptor
                name = descriptor.name if descriptor is not None else None
                errors = self.stream_errors.setdefault(name, [])
                if len(errors) < MAX_STREAM_ERRORS_PER_KEY:
                    failure_type = trace.error.failure_type
                    errors.append(
                        StreamError(
                            failure_type=(
                                str(getattr(failure_type, "value", failure_type))
                                if failure_type is not None
                                else None
                            ),
                            message=(
                                trace.error.message[:MAX_ERROR_MESSAGE_CHARS]
                                if trace.error.message is not None
                                else None
                            ),
                        )
                    )
        elif kind is AirbyteMessageType.SPEC and self.spec is None:
            self.spec = message.spec
        elif kind is AirbyteMessageType.CATALOG and self.catalog is None:
            self.catalog = message.catalog
        elif (
            kind is AirbyteMessageType.CONNECTION_STATUS
            and self.connection_status is None
        ):
            self.connection_status = message.connectionStatus


def _fold_state(final_states: dict[tuple[str | None, str], Any], state: Any) -> None:
    """Overwrite the resume point of every stream this state message carries.

    See `ExecutionResult.get_final_state_per_stream` for why all three state
    types are kept and how they are keyed.
    """
    if state.type is AirbyteStateType.GLOBAL and state.global_ is not None:
        for stream_state in state.global_.stream_states or []:
            stream_id, value = _stream_state_entry(stream_state)
            final_states[stream_id] = value
        if state.global_.shared_state is not None:
            final_states[SHARED_STATE_KEY] = to_plain_dict(
                state.global_.shared_state, exclude_none=False
            )
    elif state.type is AirbyteStateType.STREAM and state.stream is not None:
        stream_id, value = _stream_state_entry(state.stream)
        final_states[stream_id] = value
    elif state.data is not None:
        # LEGACY, and a message that declared no type at all: the protocol's
        # own default, and still what the connector resumes from.
        final_states[LEGACY_STATE_KEY] = state.data


def _stream_state_entry(
    stream_state: AirbyteStreamState,
) -> tuple[tuple[str | None, str], Any]:
    """One stream's state, under the identity comparisons key streams by."""
    descriptor = stream_state.stream_descriptor

    return (
        to_stream_id(descriptor.namespace, descriptor.name),
        # `exclude_none=False`: a `null` inside a state blob is the connector's
        # own data, not an unset protocol optional. Dropping the key would
        # report a cursor one version emits as `null` and the other omits as
        # an unchanged state.
        to_plain_dict(stream_state.stream_state, exclude_none=False),
    )


@dataclass
class ExecutionResult:
    """Result of executing a connector command.

    The messages the run emitted stay on disk in `stdout_file_path`: for a
    `read` they are the whole dataset, and holding them would make the
    harness's memory grow with the connector's output. `airbyte_messages`
    walks the file; the questions that have bounded answers -- counts, the
    spec, the catalog, the final states -- are answered from one `MessageSummary`
    collected on the first pass that needs it.
    """

    connector_under_test: ConnectorUnderTest
    command: Command
    stdout_file_path: Path
    stderr_file_path: Path
    success: bool
    exit_code: int
    configured_catalog: ConfiguredAirbyteCatalog | None = None
    config: dict[str, Any] | None = None
    stopped_early: StoppedEarly | None = None
    _summary: MessageSummary | None = field(default=None, init=False, repr=False)

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(
            f"{self.connector_under_test.target_or_control.value}-{self.command.value}"
        )

    @property
    def airbyte_messages(self) -> Iterator[AirbyteMessage]:
        """The run's messages, parsed from stdout one line at a time.

        A fresh pass over the file on every access, and never a list: a
        `read`'s output is the dataset, and the comparison keeps two results
        alive at once.
        """
        # `errors="replace"`: a byte that does not decode becomes U+FFFD and the
        # line fails validation below like any other malformed one, rather than
        # the iteration itself raising and taking the whole run's report with it.
        with self.stdout_file_path.open(errors="replace") as stdout:
            for line in stdout:
                line = line.strip()
                if not line:
                    continue
                try:
                    message = AirbyteMessage.model_validate_json(line)
                except ValidationError:
                    continue
                yield message

    def _scan(
        self, on_message: Callable[[AirbyteMessage], None] | None = None
    ) -> MessageSummary:
        """One pass over the messages: collect the summary, hand each to `on_message`."""
        summary = MessageSummary()
        for message in self.airbyte_messages:
            summary.add(message)
            if on_message is not None:
                on_message(message)
        self._summary = summary
        return summary

    @property
    def summary(self) -> MessageSummary:
        """The bounded facts about the run, parsed from stdout at most once."""
        if self._summary is None:
            return self._scan()
        return self._summary

    @property
    def configured_streams(self) -> list[str]:
        """Get list of configured stream names."""
        if not self.configured_catalog:
            return []
        return [stream.stream.name for stream in self.configured_catalog.streams]

    def get_records(self) -> Iterator[AirbyteMessage]:
        """Iterate over record messages."""
        for message in self.airbyte_messages:
            if message.type is AirbyteMessageType.RECORD:
                yield message

    def get_records_per_stream(self, stream: str) -> Iterator[AirbyteMessage]:
        """Get records for a specific stream."""
        for message in self.get_records():
            if message.record.stream == stream:
                yield message

    def get_states(self) -> Iterator[AirbyteMessage]:
        """Iterate over state messages."""
        for message in self.airbyte_messages:
            if message.type is AirbyteMessageType.STATE:
                yield message

    def get_final_state_per_stream(self) -> dict[tuple[str | None, str], Any]:
        """The state each stream would resume from, keyed by stream identity.

        A connector emits state as it goes, so only the last message for a
        stream describes where the next sync starts -- earlier ones are
        checkpoints it has already moved past. Messages are walked in emission
        order and later ones overwrite earlier ones, which is exactly how the
        platform stores them.

        Keyed by `(namespace, name)` rather than by the `namespace.name` label it
        displays as, for the reason the catalog index is: a stream literally
        called `public.users` must not share a key with `users` in the `public`
        namespace and silently take the other's state with it. The comparison
        turns these into the labels a reviewer reads, qualifying the collision
        instead of collapsing it.

        The three state types are all kept, because all three are what a
        connector resumes from:

        - `STREAM` -- one entry per stream, under its own identity.
        - `GLOBAL` -- unpacked into one entry per stream, plus the shared state
          under `SHARED_STATE_KEY`.
        - `LEGACY` -- the protocol carries no stream identity here, so the whole
          blob is one entry under `LEGACY_STATE_KEY`. Skipping it would let a
          comparison report "state unchanged" over a state nothing looked at.

        `sourceStats` and `destinationStats` are left out: they live beside the
        state rather than in it, and `recordCount` legitimately differs between
        two runs -- record counts are compared in their own table.

        Returns:
            Stream identity to state value, empty when the run emitted no state.
        """
        return dict(self.summary.final_states)

    def get_stream_statuses(self) -> dict[str, list[str]]:
        """Get the bounded stream statuses emitted during the run."""
        return {
            name: list(statuses)
            for name, statuses in self.summary.stream_statuses.items()
        }

    def get_stream_errors(self) -> dict[str | None, list[StreamError]]:
        """Get the bounded, public details of stream error traces."""
        return {
            name: list(errors) for name, errors in self.summary.stream_errors.items()
        }

    def get_message_count_per_type(self) -> dict[AirbyteMessageType, int]:
        """Count messages by type."""
        return dict(self.summary.message_counts)

    def get_record_count_per_stream(self) -> dict[str, int]:
        """Count records by stream name.

        Returns:
            Dictionary mapping stream names to record counts.
        """
        return dict(self.summary.record_counts_per_stream)

    def get_catalog(self) -> AirbyteCatalog | None:
        """Get discovered catalog from messages."""
        return self.summary.catalog

    def get_spec(self) -> Any | None:
        """Get connector spec from messages."""
        return self.summary.spec

    def get_connection_status(self) -> Any | None:
        """Get connection status from check command."""
        return self.summary.connection_status

    def is_check_successful(self) -> bool:
        """Check if the check command was successful."""
        status = self.get_connection_status()
        if status is None:
            return False
        return status.status.value == "SUCCEEDED"

    def save_artifacts(self, output_dir: Path) -> None:
        """Save execution artifacts to the output directory.

        One streaming pass writes every message to `airbyte_messages/<type>.jsonl`
        and collects the run's summary, so the counts and declared objects the
        caller asks for next cost no second parse. One handle per message type
        stays open for the pass: the protocol has a handful of types, not a
        stream's worth.
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        airbyte_messages_dir = output_dir / "airbyte_messages"
        airbyte_messages_dir.mkdir(parents=True, exist_ok=True)

        handles: dict[str, IO[str]] = {}

        def write(message: AirbyteMessage) -> None:
            type_name = message.type.value.lower()
            handle = handles.get(type_name)
            if handle is None:
                handle = (airbyte_messages_dir / f"{type_name}.jsonl").open("w")
                handles[type_name] = handle
            else:
                handle.write("\n")
            handle.write(message.model_dump_json())

        try:
            self._scan(write)
        finally:
            for handle in handles.values():
                handle.close()

        # Save configured catalog (input) if available
        if self.configured_catalog is not None:
            catalog_path = output_dir / "configured_catalog.json"
            catalog_path.write_text(
                self.configured_catalog.model_dump_json(indent=2, exclude_none=True)
            )
            self.logger.info(f"Saved configured catalog to {catalog_path}")

        self.logger.info(f"Artifacts saved to {output_dir}")


def get_primary_keys_per_stream(
    configured_catalog: ConfiguredAirbyteCatalog,
) -> dict[str, list[list[str]] | None]:
    """Extract primary key paths per stream from a configured catalog.

    Prefers the source-defined primary key (which comes from the discovered
    catalog) and falls back to the primary key configured on the stream.
    Streams with no primary key map to None.

    The whole record-comparison pipeline downstream of this map keys streams
    by name alone (the RECORD messages are routed on `record.stream`), so a
    name that repeats across namespaces -- `public.users` and
    `reporting.users` on any database source -- would merge two streams'
    records and apply one stream's PK to the other's rows, reporting phantom
    duplicate PKs on a run where nothing changed. Until the pipeline is
    namespace-aware, such names degrade to no-PK (count-comparison-only),
    which is safe rather than falsely failing; the caller is expected to
    surface `duplicate_stream_names` as a warning.

    Returns:
        Mapping of stream name to primary key paths in protocol format
        (a list of nested field paths, e.g. [["id"]]). Names that appear
        more than once in the catalog map to None.
    """
    primary_keys: dict[str, list[list[str]] | None] = {}
    for configured_stream in configured_catalog.streams:
        pk = (
            configured_stream.stream.source_defined_primary_key
            or configured_stream.primary_key
            or None
        )
        primary_keys[configured_stream.stream.name] = pk
    for name in duplicate_stream_names(configured_catalog):
        primary_keys[name] = None
    return primary_keys


def duplicate_stream_names(configured_catalog: ConfiguredAirbyteCatalog) -> list[str]:
    """Stream names that appear more than once in the catalog.

    Two streams share a name when a table repeats across namespaces (schemas),
    which is routine for database sources. Sorted, so callers' warnings and
    reports are deterministic.
    """
    counts = Counter(
        configured_stream.stream.name
        for configured_stream in configured_catalog.streams
    )

    return sorted(name for name, count in counts.items() if count > 1)


def _stream_file_name(stream: str, used: set[str]) -> str:
    """Build a filesystem-safe, collision-free file stem for a stream name."""
    base = re.sub(r"[^\w.-]", "_", stream) or "stream"
    name = base
    suffix = 2
    while name in used:
        name = f"{base}_{suffix}"
        suffix += 1
    used.add(name)
    return name


# Open per-stream file handles the splitter holds at once. Database sources
# can sync thousands of tables, and one handle per stream would cross the
# process fd limit (macOS defaults its soft limit to 256). Connector output
# emits streams in contiguous chunks, so with an LRU this size the
# evict-and-reopen path stays cold.
MAX_OPEN_RECORD_FILES = 64


def split_records_per_stream(
    stdout_path: Path,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    """Split a run's stdout into one records-only jsonl file per stream.

    Single streaming pass over the connector output: each RECORD message
    line is appended to `<output_dir>/<stream>.jsonl`; lines that are not
    JSON RECORD messages (e.g. plain log lines) are skipped. Splitting
    needs only the message type and stream name, so lines are routed on a
    plain JSON parse -- the comparison layer, which reads these files one
    stream at a time, does the full protocol validation. Records are never
    held in memory and at most `MAX_OPEN_RECORD_FILES` file handles are open
    at once (least recently written streams are closed and reopened in
    append mode), so this scales to arbitrarily large outputs and stream
    counts; the per-stream files double as debugging artifacts.

    Args:
        stdout_path: The connector run's stdout file.
        output_dir: Where to write the per-stream files. Defaults to a
            `records_per_stream` directory next to the stdout file.

    Returns:
        Mapping of stream name to its records file. Streams with no
        records have no entry.
    """
    records_dir = (
        output_dir
        if output_dir is not None
        else stdout_path.parent / "records_per_stream"
    )
    records_dir.mkdir(parents=True, exist_ok=True)

    paths: dict[str, Path] = {}
    handles: OrderedDict[str, IO[str]] = OrderedDict()
    used_names: set[str] = set()

    def handle_for(stream: str) -> IO[str]:
        handle = handles.get(stream)
        if handle is not None:
            handles.move_to_end(stream)
            return handle
        if stream not in paths:
            path = records_dir / f"{_stream_file_name(stream, used_names)}.jsonl"
            # Truncate exactly once per run, so appending after an LRU
            # eviction keeps the same rerun semantics as a single open("w").
            path.write_text("")
            paths[stream] = path
        if len(handles) >= MAX_OPEN_RECORD_FILES:
            _, evicted = handles.popitem(last=False)
            evicted.close()
        handle = paths[stream].open("a")
        handles[stream] = handle
        return handle

    try:
        # Same backstop as `ExecutionResult.airbyte_messages`: an undecodable
        # byte spoils one line, not the pass.
        with stdout_path.open(errors="replace") as stdout:
            for line in stdout:
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(payload, dict) or payload.get("type") != "RECORD":
                    continue
                record = payload.get("record")
                if not isinstance(record, dict):
                    continue
                stream = record.get("stream")
                if not isinstance(stream, str):
                    continue
                handle_for(stream).write(line + "\n")
    finally:
        for handle in handles.values():
            handle.close()
    return paths


@dataclass(frozen=True)
class ComparableOutputs:
    """What a connector declared about itself, kept for the comparison.

    An `ExecutionResult` holds every message the run emitted -- for a `read`,
    the whole dataset -- so keeping one alive per side while the other version
    runs would double a comparison's peak memory for the sake of three small
    objects. These three are bounded, so this is what outlives the run: the flat
    result dict several consumers already read stays about counts and exit
    status, and the comparison gets the protocol objects themselves. The spec,
    the discovered catalog, and the final state per stream -- one state blob per
    stream, not the checkpoints that led to it.

    All three are `None` for a command that does not emit them, and for a run
    that failed before it could. `final_states` distinguishes the two absences a
    `read` can have: `None` is "nothing collected this", `{}` is "the run
    emitted no state", and only the second is something to report. That
    distinction is why `from_execution_result` collects it for a `read` and
    leaves it `None` otherwise -- extracting `{}` from a `spec` run would make
    the two absences indistinguishable, and "this command emits no state" would
    read as "this read resumed from nothing".
    """

    spec: Any | None = None
    catalog: AirbyteCatalog | None = None
    final_states: dict[tuple[str | None, str], Any] | None = None
    stream_statuses: dict[str, list[str]] | None = None
    stream_errors: dict[str | None, list[StreamError]] | None = None

    @classmethod
    def from_execution_result(cls, result: ExecutionResult) -> ComparableOutputs:
        """Lift the comparable objects out of a finished run.

        `get_spec` and `get_catalog` return `None` on a run that emitted no such
        message, so they carry the "not this command" case themselves.
        `get_final_state_per_stream` returns `{}` instead, which is a finding for
        a `read` and meaningless anywhere else -- so the command decides whether
        it is collected at all.
        """
        emits_read = result.command in (Command.READ, Command.READ_WITH_STATE)

        return cls(
            spec=result.get_spec(),
            catalog=result.get_catalog(),
            final_states=(result.get_final_state_per_stream() if emits_read else None),
            stream_statuses=(result.get_stream_statuses() if emits_read else None),
            stream_errors=(result.get_stream_errors() if emits_read else None),
        )
