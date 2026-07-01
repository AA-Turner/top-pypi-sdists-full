from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .run_prompt_input import RunPrompt_input
    from .run_prompt_mode import RunPrompt_mode

@dataclass
class RunPrompt(Parsable):
    # Bypass autonomous loop guardrails for a direct human-triggered prompt.
    force: Optional[bool] = None
    # The input property
    input: Optional[RunPrompt_input] = None
    # The mode property
    mode: Optional[RunPrompt_mode] = None
    # The timeout_seconds property
    timeout_seconds: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RunPrompt:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RunPrompt
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RunPrompt()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .run_prompt_input import RunPrompt_input
        from .run_prompt_mode import RunPrompt_mode

        from .run_prompt_input import RunPrompt_input
        from .run_prompt_mode import RunPrompt_mode

        fields: dict[str, Callable[[Any], None]] = {
            "force": lambda n : setattr(self, 'force', n.get_bool_value()),
            "input": lambda n : setattr(self, 'input', n.get_object_value(RunPrompt_input)),
            "mode": lambda n : setattr(self, 'mode', n.get_object_value(RunPrompt_mode)),
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
        writer.write_object_value("input", self.input)
        writer.write_object_value("mode", self.mode)
        writer.write_int_value("timeout_seconds", self.timeout_seconds)
    

