from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class UsageSummary(Parsable):
    # The billed_usage_units property
    billed_usage_units: Optional[float] = None
    # The channel_delivery property
    channel_delivery: Optional[float] = None
    # The code_executions property
    code_executions: Optional[float] = None
    # The estimated_cost_usd property
    estimated_cost_usd: Optional[float] = None
    # The shell_executions property
    shell_executions: Optional[float] = None
    # The tokens property
    tokens: Optional[float] = None
    # The tool_calls property
    tool_calls: Optional[float] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> UsageSummary:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: UsageSummary
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return UsageSummary()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "billed_usage_units": lambda n : setattr(self, 'billed_usage_units', n.get_float_value()),
            "channel_delivery": lambda n : setattr(self, 'channel_delivery', n.get_float_value()),
            "code_executions": lambda n : setattr(self, 'code_executions', n.get_float_value()),
            "estimated_cost_usd": lambda n : setattr(self, 'estimated_cost_usd', n.get_float_value()),
            "shell_executions": lambda n : setattr(self, 'shell_executions', n.get_float_value()),
            "tokens": lambda n : setattr(self, 'tokens', n.get_float_value()),
            "tool_calls": lambda n : setattr(self, 'tool_calls', n.get_float_value()),
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
        writer.write_float_value("billed_usage_units", self.billed_usage_units)
        writer.write_float_value("channel_delivery", self.channel_delivery)
        writer.write_float_value("code_executions", self.code_executions)
        writer.write_float_value("estimated_cost_usd", self.estimated_cost_usd)
        writer.write_float_value("shell_executions", self.shell_executions)
        writer.write_float_value("tokens", self.tokens)
        writer.write_float_value("tool_calls", self.tool_calls)
    

