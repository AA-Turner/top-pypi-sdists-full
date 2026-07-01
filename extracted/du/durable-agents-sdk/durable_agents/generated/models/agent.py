from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .agent_mode import AgentMode
    from .agent_mutable_state import AgentMutableState
    from .agent_trigger import AgentTrigger
    from .channel_input import ChannelInput
    from .effort import Effort
    from .heartbeat import Heartbeat
    from .ref import Ref
    from .schedule import Schedule
    from .target_input import TargetInput

@dataclass
class Agent(Parsable):
    # The channels property
    channels: Optional[list[ChannelInput]] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The description property
    description: Optional[str] = None
    # The effort property
    effort: Optional[Effort] = None
    # The focus property
    focus: Optional[str] = None
    # The heartbeat property
    heartbeat: Optional[Heartbeat] = None
    # The id property
    id: Optional[str] = None
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
    targets: Optional[list[TargetInput]] = None
    # The trigger property
    trigger: Optional[AgentTrigger] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    # The webhook_url property
    webhook_url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Agent:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Agent
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Agent()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .agent_mode import AgentMode
        from .agent_mutable_state import AgentMutableState
        from .agent_trigger import AgentTrigger
        from .channel_input import ChannelInput
        from .effort import Effort
        from .heartbeat import Heartbeat
        from .ref import Ref
        from .schedule import Schedule
        from .target_input import TargetInput

        from .agent_mode import AgentMode
        from .agent_mutable_state import AgentMutableState
        from .agent_trigger import AgentTrigger
        from .channel_input import ChannelInput
        from .effort import Effort
        from .heartbeat import Heartbeat
        from .ref import Ref
        from .schedule import Schedule
        from .target_input import TargetInput

        fields: dict[str, Callable[[Any], None]] = {
            "channels": lambda n : setattr(self, 'channels', n.get_collection_of_object_values(ChannelInput)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "effort": lambda n : setattr(self, 'effort', n.get_enum_value(Effort)),
            "focus": lambda n : setattr(self, 'focus', n.get_str_value()),
            "heartbeat": lambda n : setattr(self, 'heartbeat', n.get_object_value(Heartbeat)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "mode": lambda n : setattr(self, 'mode', n.get_enum_value(AgentMode)),
            "model": lambda n : setattr(self, 'model', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "persona": lambda n : setattr(self, 'persona', n.get_object_value(Ref)),
            "prompt": lambda n : setattr(self, 'prompt', n.get_str_value()),
            "schedule": lambda n : setattr(self, 'schedule', n.get_object_value(Schedule)),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(AgentMutableState)),
            "targets": lambda n : setattr(self, 'targets', n.get_collection_of_object_values(TargetInput)),
            "trigger": lambda n : setattr(self, 'trigger', n.get_object_value(AgentTrigger)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
            "webhook_url": lambda n : setattr(self, 'webhook_url', n.get_str_value()),
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
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("description", self.description)
        writer.write_enum_value("effort", self.effort)
        writer.write_str_value("focus", self.focus)
        writer.write_object_value("heartbeat", self.heartbeat)
        writer.write_str_value("id", self.id)
        writer.write_enum_value("mode", self.mode)
        writer.write_str_value("model", self.model)
        writer.write_str_value("name", self.name)
        writer.write_object_value("persona", self.persona)
        writer.write_str_value("prompt", self.prompt)
        writer.write_object_value("schedule", self.schedule)
        writer.write_enum_value("state", self.state)
        writer.write_collection_of_object_values("targets", self.targets)
        writer.write_object_value("trigger", self.trigger)
        writer.write_datetime_value("updated_at", self.updated_at)
        writer.write_str_value("webhook_url", self.webhook_url)
    

