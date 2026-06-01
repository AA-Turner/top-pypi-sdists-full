# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Models for live tests - connector testing without Dagger."""

from __future__ import annotations

import contextlib
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Any, Iterator

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
