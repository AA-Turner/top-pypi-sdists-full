from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import ComposedTypeWrapper, Parsable, ParseNode, ParseNodeHelper, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .data_source_account_member1 import DataSource_accountMember1
    from .data_source_account_member2 import DataSource_accountMember2

@dataclass
class DataSource_account(ComposedTypeWrapper, Parsable):
    """
    Composed type wrapper for classes DataSource_accountMember1, DataSource_accountMember2
    """
    # Composed type representation for type DataSource_accountMember1
    data_source_account_member1: Optional[DataSource_accountMember1] = None
    # Composed type representation for type DataSource_accountMember2
    data_source_account_member2: Optional[DataSource_accountMember2] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataSource_account:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataSource_account
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        result = DataSource_account()
        from .data_source_account_member1 import DataSource_accountMember1

        result.data_source_account_member1 = DataSource_accountMember1()
        from .data_source_account_member2 import DataSource_accountMember2

        result.data_source_account_member2 = DataSource_accountMember2()
        return result
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .data_source_account_member1 import DataSource_accountMember1
        from .data_source_account_member2 import DataSource_accountMember2

        if self.data_source_account_member1 or self.data_source_account_member2:
            return ParseNodeHelper.merge_deserializers_for_intersection_wrapper(self.data_source_account_member1, self.data_source_account_member2)
        return {}
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_object_value(None, self.data_source_account_member1, self.data_source_account_member2)
    

