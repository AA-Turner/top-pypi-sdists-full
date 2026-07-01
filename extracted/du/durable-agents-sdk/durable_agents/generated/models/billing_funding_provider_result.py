from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class BillingFundingProviderResult(Parsable):
    # The charge_id property
    charge_id: Optional[str] = None
    # The kind property
    kind: Optional[str] = None
    # The payment_intent_id property
    payment_intent_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingProviderResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingProviderResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingProviderResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "charge_id": lambda n : setattr(self, 'charge_id', n.get_str_value()),
            "kind": lambda n : setattr(self, 'kind', n.get_str_value()),
            "payment_intent_id": lambda n : setattr(self, 'payment_intent_id', n.get_str_value()),
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
        writer.write_str_value("charge_id", self.charge_id)
        writer.write_str_value("kind", self.kind)
        writer.write_str_value("payment_intent_id", self.payment_intent_id)
    

