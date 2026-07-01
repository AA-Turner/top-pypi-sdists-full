from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class ConnectorAuthStatus(Parsable):
    # The authenticated_as property
    authenticated_as: Optional[str] = None
    # The authenticated_at property
    authenticated_at: Optional[datetime.datetime] = None
    # The expires_at property
    expires_at: Optional[datetime.datetime] = None
    # The has_refresh_token property
    has_refresh_token: Optional[bool] = None
    # The is_authenticated property
    is_authenticated: Optional[bool] = None
    # The last_refresh_attempt_at property
    last_refresh_attempt_at: Optional[datetime.datetime] = None
    # The last_refresh_error property
    last_refresh_error: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    # The reauth_required property
    reauth_required: Optional[bool] = None
    # The token_state property
    token_state: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ConnectorAuthStatus:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ConnectorAuthStatus
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ConnectorAuthStatus()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "authenticated_as": lambda n : setattr(self, 'authenticated_as', n.get_str_value()),
            "authenticated_at": lambda n : setattr(self, 'authenticated_at', n.get_datetime_value()),
            "expires_at": lambda n : setattr(self, 'expires_at', n.get_datetime_value()),
            "has_refresh_token": lambda n : setattr(self, 'has_refresh_token', n.get_bool_value()),
            "is_authenticated": lambda n : setattr(self, 'is_authenticated', n.get_bool_value()),
            "last_refresh_attempt_at": lambda n : setattr(self, 'last_refresh_attempt_at', n.get_datetime_value()),
            "last_refresh_error": lambda n : setattr(self, 'last_refresh_error', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "reauth_required": lambda n : setattr(self, 'reauth_required', n.get_bool_value()),
            "token_state": lambda n : setattr(self, 'token_state', n.get_str_value()),
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
        writer.write_str_value("authenticated_as", self.authenticated_as)
        writer.write_datetime_value("authenticated_at", self.authenticated_at)
        writer.write_datetime_value("expires_at", self.expires_at)
        writer.write_bool_value("has_refresh_token", self.has_refresh_token)
        writer.write_bool_value("is_authenticated", self.is_authenticated)
        writer.write_datetime_value("last_refresh_attempt_at", self.last_refresh_attempt_at)
        writer.write_str_value("last_refresh_error", self.last_refresh_error)
        writer.write_str_value("provider", self.provider)
        writer.write_bool_value("reauth_required", self.reauth_required)
        writer.write_str_value("token_state", self.token_state)
    

