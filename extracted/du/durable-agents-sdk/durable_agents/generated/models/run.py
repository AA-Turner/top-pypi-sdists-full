from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .ref import Ref
    from .run_error import RunError
    from .run_input import Run_input
    from .run_mode import RunMode
    from .run_output import Run_output
    from .run_status import RunStatus
    from .usage_summary import UsageSummary

@dataclass
class Run(Parsable):
    # The agent property
    agent: Optional[Ref] = None
    # The completed_at property
    completed_at: Optional[datetime.datetime] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The current_execution_id property
    current_execution_id: Optional[str] = None
    # Status of the current execution when known.
    current_execution_status: Optional[RunStatus] = None
    # The error property
    error: Optional[RunError] = None
    # True when the current or latest execution is not terminal.
    has_active_execution: Optional[bool] = None
    # The id property
    id: Optional[str] = None
    # The input property
    input: Optional[Run_input] = None
    # The latest_execution_id property
    latest_execution_id: Optional[str] = None
    # Status of the latest execution when known.
    latest_execution_status: Optional[RunStatus] = None
    # The mode property
    mode: Optional[RunMode] = None
    # The output property
    output: Optional[Run_output] = None
    # The started_at property
    started_at: Optional[datetime.datetime] = None
    # The status property
    status: Optional[RunStatus] = None
    # The terminal_execution_id property
    terminal_execution_id: Optional[str] = None
    # Status of the most recent terminal execution when known.
    terminal_execution_status: Optional[RunStatus] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    # The usage property
    usage: Optional[UsageSummary] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Run:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Run
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Run()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .ref import Ref
        from .run_error import RunError
        from .run_input import Run_input
        from .run_mode import RunMode
        from .run_output import Run_output
        from .run_status import RunStatus
        from .usage_summary import UsageSummary

        from .ref import Ref
        from .run_error import RunError
        from .run_input import Run_input
        from .run_mode import RunMode
        from .run_output import Run_output
        from .run_status import RunStatus
        from .usage_summary import UsageSummary

        fields: dict[str, Callable[[Any], None]] = {
            "agent": lambda n : setattr(self, 'agent', n.get_object_value(Ref)),
            "completed_at": lambda n : setattr(self, 'completed_at', n.get_datetime_value()),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "current_execution_id": lambda n : setattr(self, 'current_execution_id', n.get_str_value()),
            "current_execution_status": lambda n : setattr(self, 'current_execution_status', n.get_enum_value(RunStatus)),
            "error": lambda n : setattr(self, 'error', n.get_object_value(RunError)),
            "has_active_execution": lambda n : setattr(self, 'has_active_execution', n.get_bool_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "input": lambda n : setattr(self, 'input', n.get_object_value(Run_input)),
            "latest_execution_id": lambda n : setattr(self, 'latest_execution_id', n.get_str_value()),
            "latest_execution_status": lambda n : setattr(self, 'latest_execution_status', n.get_enum_value(RunStatus)),
            "mode": lambda n : setattr(self, 'mode', n.get_enum_value(RunMode)),
            "output": lambda n : setattr(self, 'output', n.get_object_value(Run_output)),
            "started_at": lambda n : setattr(self, 'started_at', n.get_datetime_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(RunStatus)),
            "terminal_execution_id": lambda n : setattr(self, 'terminal_execution_id', n.get_str_value()),
            "terminal_execution_status": lambda n : setattr(self, 'terminal_execution_status', n.get_enum_value(RunStatus)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
            "usage": lambda n : setattr(self, 'usage', n.get_object_value(UsageSummary)),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_object_value("agent", self.agent)
        writer.write_datetime_value("completed_at", self.completed_at)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("current_execution_id", self.current_execution_id)
        writer.write_enum_value("current_execution_status", self.current_execution_status)
        writer.write_object_value("error", self.error)
        writer.write_bool_value("has_active_execution", self.has_active_execution)
        writer.write_str_value("id", self.id)
        writer.write_object_value("input", self.input)
        writer.write_str_value("latest_execution_id", self.latest_execution_id)
        writer.write_enum_value("latest_execution_status", self.latest_execution_status)
        writer.write_enum_value("mode", self.mode)
        writer.write_object_value("output", self.output)
        writer.write_datetime_value("started_at", self.started_at)
        writer.write_enum_value("status", self.status)
        writer.write_str_value("terminal_execution_id", self.terminal_execution_id)
        writer.write_enum_value("terminal_execution_status", self.terminal_execution_status)
        writer.write_datetime_value("updated_at", self.updated_at)
        writer.write_object_value("usage", self.usage)
    

