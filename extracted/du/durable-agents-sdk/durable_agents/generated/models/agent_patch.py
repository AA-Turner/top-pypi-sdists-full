from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .agent_mode import AgentMode
    from .agent_mutable_state import AgentMutableState
    from .agent_trigger import AgentTrigger
    from .channel import Channel
    from .effort import Effort
    from .heartbeat import Heartbeat
    from .ref import Ref
    from .schedule import Schedule
    from .target import Target

@dataclass
class AgentPatch(Parsable):
    """
    Agent fields only. Manage inboxes and channel bindings through the channel endpoints and bindings APIs.
    """
    # The channels property
    channels: Optional[list[Channel]] = None
    # The description property
    description: Optional[str] = None
    # The effort property
    effort: Optional[Effort] = None
    # The focus property
    focus: Optional[str] = None
    # The heartbeat property
    heartbeat: Optional[Heartbeat] = None
    # The mode property
    mode: Optional[AgentMode] = None
    # The model property
    model: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The persona property
    persona: Optional[Ref] = None
    # The prompt property
    prompt: Optional[str] = None
    # The schedule property
    schedule: Optional[Schedule] = None
    # The state property
    state: Optional[AgentMutableState] = None
    # The targets property
    targets: Optional[list[Target]] = None
    # The trigger property
    trigger: Optional[AgentTrigger] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AgentPatch:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AgentPatch
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AgentPatch()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .agent_mode import AgentMode
        from .agent_mutable_state import AgentMutableState
        from .agent_trigger import AgentTrigger
        from .channel import Channel
        from .effort import Effort
        from .heartbeat import Heartbeat
        from .ref import Ref
        from .schedule import Schedule
        from .target import Target

        from .agent_mode import AgentMode
        from .agent_mutable_state import AgentMutableState
        from .agent_trigger import AgentTrigger
        from .channel import Channel
        from .effort import Effort
        from .heartbeat import Heartbeat
        from .ref import Ref
        from .schedule import Schedule
        from .target import Target

        fields: dict[str, Callable[[Any], None]] = {
            "channels": lambda n : setattr(self, 'channels', n.get_collection_of_object_values(Channel)),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "effort": lambda n : setattr(self, 'effort', n.get_enum_value(Effort)),
            "focus": lambda n : setattr(self, 'focus', n.get_str_value()),
            "heartbeat": lambda n : setattr(self, 'heartbeat', n.get_object_value(Heartbeat)),
            "mode": lambda n : setattr(self, 'mode', n.get_enum_value(AgentMode)),
            "model": lambda n : setattr(self, 'model', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "persona": lambda n : setattr(self, 'persona', n.get_object_value(Ref)),
            "prompt": lambda n : setattr(self, 'prompt', n.get_str_value()),
            "schedule": lambda n : setattr(self, 'schedule', n.get_object_value(Schedule)),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(AgentMutableState)),
            "targets": lambda n : setattr(self, 'targets', n.get_collection_of_object_values(Target)),
            "trigger": lambda n : setattr(self, 'trigger', n.get_object_value(AgentTrigger)),
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
        writer.write_collection_of_object_values("channels", self.channels)
        writer.write_str_value("description", self.description)
        writer.write_enum_value("effort", self.effort)
        writer.write_str_value("focus", self.focus)
        writer.write_object_value("heartbeat", self.heartbeat)
        writer.write_enum_value("mode", self.mode)
        writer.write_str_value("model", self.model)
        writer.write_str_value("name", self.name)
        writer.write_object_value("persona", self.persona)
        writer.write_str_value("prompt", self.prompt)
        writer.write_object_value("schedule", self.schedule)
        writer.write_enum_value("state", self.state)
        writer.write_collection_of_object_values("targets", self.targets)
        writer.write_object_value("trigger", self.trigger)
    

