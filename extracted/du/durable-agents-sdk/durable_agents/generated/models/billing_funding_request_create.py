from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class BillingFundingRequestCreate(Parsable):
    # The credits property
    credits: Optional[float] = None
    # The payment_method property
    payment_method: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingRequestCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingRequestCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingRequestCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "credits": lambda n : setattr(self, 'credits', n.get_float_value()),
            "payment_method": lambda n : setattr(self, 'payment_method', n.get_str_value()),
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
        writer.write_float_value("credits", self.credits)
        writer.write_str_value("payment_method", self.payment_method)
    

