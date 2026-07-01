from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .teams_setup_guide_do_not_proceed_until_create import TeamsSetupGuide_do_not_proceed_until_create

@dataclass
class TeamsSetupGuide_do_not_proceed_until(Parsable):
    # The bind property
    bind: Optional[list[str]] = None
    # The create property
    create: Optional[list[TeamsSetupGuide_do_not_proceed_until_create]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TeamsSetupGuide_do_not_proceed_until:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TeamsSetupGuide_do_not_proceed_until
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TeamsSetupGuide_do_not_proceed_until()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .teams_setup_guide_do_not_proceed_until_create import TeamsSetupGuide_do_not_proceed_until_create

        from .teams_setup_guide_do_not_proceed_until_create import TeamsSetupGuide_do_not_proceed_until_create

        fields: dict[str, Callable[[Any], None]] = {
            "bind": lambda n : setattr(self, 'bind', n.get_collection_of_primitive_values(str)),
            "create": lambda n : setattr(self, 'create', n.get_collection_of_enum_values(TeamsSetupGuide_do_not_proceed_until_create)),
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
        writer.write_collection_of_primitive_values("bind", self.bind)
        writer.write_collection_of_enum_values("create", self.create)
    

