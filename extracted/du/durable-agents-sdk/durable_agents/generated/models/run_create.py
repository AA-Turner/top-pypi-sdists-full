from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .run_create_input import RunCreate_input
    from .run_create_mode import RunCreate_mode

@dataclass
class RunCreate(Parsable):
    # Bypass autonomous loop guardrails for a direct human-triggered run.
    force: Optional[bool] = None
    # The idempotency_key property
    idempotency_key: Optional[str] = None
    # The input property
    input: Optional[RunCreate_input] = None
    # The mode property
    mode: Optional[RunCreate_mode] = None
    # The timeout_seconds property
    timeout_seconds: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RunCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RunCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RunCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .run_create_input import RunCreate_input
        from .run_create_mode import RunCreate_mode

        from .run_create_input import RunCreate_input
        from .run_create_mode import RunCreate_mode

        fields: dict[str, Callable[[Any], None]] = {
            "force": lambda n : setattr(self, 'force', n.get_bool_value()),
            "idempotency_key": lambda n : setattr(self, 'idempotency_key', n.get_str_value()),
            "input": lambda n : setattr(self, 'input', n.get_object_value(RunCreate_input)),
            "mode": lambda n : setattr(self, 'mode', n.get_object_value(RunCreate_mode)),
            "timeout_seconds": lambda n : setattr(self, 'timeout_seconds', n.get_int_value()),
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
        writer.write_bool_value("force", self.force)
        writer.write_str_value("idempotency_key", self.idempotency_key)
        writer.write_object_value("input", self.input)
        writer.write_object_value("mode", self.mode)
        writer.write_int_value("timeout_seconds", self.timeout_seconds)
    

