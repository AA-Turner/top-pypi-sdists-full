from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .agent_property_patch_properties import AgentPropertyPatch_properties

@dataclass
class AgentPropertyPatch(Parsable):
    """
    Property-oriented agent patch. Keys are typed property paths and valuesare the replacement value, or `null` for clearable properties.Supported property paths:- `name`: string, not clearable- `description`: string or null- `state`: `enabled` or `disabled`, not clearable- `mode`: `interactive`, `heartbeat`, `scheduled`, `triggered`, or `webhook`, not clearable- `model`: model preset/specification ID or null- `effort`: `quick`, `standard`, `deep`, `exhaustive`, or null- `persona`: ref ID/object or null- `prompt`: string or null; automation creates receive a default prompt when omitted, and automation updates cannot clear it- `focus`: string or null- `trigger`: full trigger object or null- `trigger.kinds`: string array or null- `trigger.sources`: source ref array or null- `schedule`: full schedule object or null- `schedule.cron`: string or null- `schedule.timezone`: string or null- `schedule.recurrence_type`: `monitor`, `once`, `repeat`, or null- `schedule.repeat_interval`: string or null- `heartbeat`: full heartbeat object, not clearable; use `mode: interactive` to disable heartbeat automation- `heartbeat.frequency_minutes`: number, not clearable- `heartbeat.off_hours_frequency_minutes`: number or null- `heartbeat.active_hours_start`: string, not clearable- `heartbeat.active_hours_end`: string, not clearable- `heartbeat.active_days`: number array, not clearable- `heartbeat.timezone`: string, not clearable- `heartbeat.probe_thresholds`: object or null- `heartbeat.probe_thresholds.new_content_min`: number or null- `heartbeat.probe_thresholds.volume_spike_multiplier`: number or nullParent/child path conflicts are rejected. For example, do not patchboth `schedule` and `schedule.cron` in one request.
    """
    # The properties property
    properties: Optional[AgentPropertyPatch_properties] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AgentPropertyPatch:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AgentPropertyPatch
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AgentPropertyPatch()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .agent_property_patch_properties import AgentPropertyPatch_properties

        from .agent_property_patch_properties import AgentPropertyPatch_properties

        fields: dict[str, Callable[[Any], None]] = {
            "properties": lambda n : setattr(self, 'properties', n.get_object_value(AgentPropertyPatch_properties)),
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
        writer.write_object_value("properties", self.properties)
    

