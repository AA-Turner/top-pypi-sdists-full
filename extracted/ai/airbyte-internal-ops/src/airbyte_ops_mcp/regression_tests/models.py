# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Models for live tests - connector testing without Dagger."""

from __future__ import annotations

import contextlib
import json
import logging
import re
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import IO, Any, Iterator

from airbyte_protocol.models import (
    AirbyteCatalog,
    AirbyteMessage,
    ConfiguredAirbyteCatalog,
)
from airbyte_protocol.models import Type as AirbyteMessageType
from pydantic import ValidationError


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


@dataclass
class ExecutionResult:
    """Result of executing a connector command."""

    connector_under_test: ConnectorUnderTest
    command: Command
    stdout_file_path: Path
    stderr_file_path: Path
    success: bool
    exit_code: int
    configured_catalog: ConfiguredAirbyteCatalog | None = None
    config: dict[str, Any] | None = None
    _airbyte_messages: list[AirbyteMessage] = field(default_factory=list)
    _messages_loaded: bool = field(default=False, repr=False)

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(
            f"{self.connector_under_test.target_or_control.value}-{self.command.value}"
        )

    @cached_property
    def airbyte_messages(self) -> list[AirbyteMessage]:
        """Parse and return all Airbyte messages from stdout."""
        if self._messages_loaded:
            return self._airbyte_messages

        messages = []
        for line in self.stdout_file_path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            with contextlib.suppress(ValidationError):
                messages.append(AirbyteMessage.parse_raw(line))
        self._airbyte_messages = messages
        self._messages_loaded = True
        return messages

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

    def get_message_count_per_type(self) -> dict[AirbyteMessageType, int]:
        """Count messages by type."""
        counts: dict[AirbyteMessageType, int] = defaultdict(int)
        for message in self.airbyte_messages:
            counts[message.type] += 1
        return dict(counts)

    def get_record_count_per_stream(self) -> dict[str, int]:
        """Count records by stream name.

        Returns:
            Dictionary mapping stream names to record counts.
        """
        counts: dict[str, int] = defaultdict(int)
        for message in self.get_records():
            counts[message.record.stream] += 1
        return dict(counts)

    def get_catalog(self) -> AirbyteCatalog | None:
        """Get discovered catalog from messages."""
        for message in self.airbyte_messages:
            if message.type is AirbyteMessageType.CATALOG:
                return message.catalog
        return None

    def get_spec(self) -> Any | None:
        """Get connector spec from messages."""
        for message in self.airbyte_messages:
            if message.type is AirbyteMessageType.SPEC:
                return message.spec
        return None

    def get_connection_status(self) -> Any | None:
        """Get connection status from check command."""
        for message in self.airbyte_messages:
            if message.type is AirbyteMessageType.CONNECTION_STATUS:
                return message.connectionStatus
        return None

    def is_check_successful(self) -> bool:
        """Check if the check command was successful."""
        status = self.get_connection_status()
        if status is None:
            return False
        return status.status.value == "SUCCEEDED"

    def save_artifacts(self, output_dir: Path) -> None:
        """Save execution artifacts to the output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)

        airbyte_messages_dir = output_dir / "airbyte_messages"
        airbyte_messages_dir.mkdir(parents=True, exist_ok=True)

        messages_by_type: dict[str, list[str]] = defaultdict(list)
        for message in self.airbyte_messages:
            type_name = message.type.value.lower()
            messages_by_type[type_name].append(message.model_dump_json())

        for type_name, messages in messages_by_type.items():
            file_path = airbyte_messages_dir / f"{type_name}.jsonl"
            file_path.write_text("\n".join(messages))

        # Save configured catalog (input) if available
        if self.configured_catalog is not None:
            catalog_path = output_dir / "configured_catalog.json"
            catalog_path.write_text(self.configured_catalog.model_dump_json(indent=2))
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
    stream at a time, does the full protocol validation once per record
    instead of twice. Records are never held in memory and at most
    `MAX_OPEN_RECORD_FILES` file handles are open at once (least recently
    written streams are closed and reopened in append mode), so this scales
    to arbitrarily large outputs and stream counts; the per-stream files
    double as debugging artifacts.

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
        with stdout_path.open() as stdout:
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
    runs would double a comparison's peak memory for the sake of two small
    objects. These two are bounded, so this is what outlives the run: the flat
    result dict several consumers already read stays about counts and exit
    status, and the comparison gets the protocol objects themselves.

    Both are `None` for a command that does not emit them, and for a run that
    failed before it could.
    """

    spec: Any | None = None
    catalog: AirbyteCatalog | None = None

    @classmethod
    def from_execution_result(cls, result: ExecutionResult) -> ComparableOutputs:
        """Lift the comparable objects out of a finished run."""
        return cls(spec=result.get_spec(), catalog=result.get_catalog())
