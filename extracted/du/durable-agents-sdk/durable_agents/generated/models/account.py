from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .account_provider import AccountProvider
    from .account_status import AccountStatus
    from .git_hub_app_installation import GitHubAppInstallation

@dataclass
class Account(Parsable):
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The email property
    email: Optional[str] = None
    # The github_app_installation property
    github_app_installation: Optional[GitHubAppInstallation] = None
    # The id property
    id: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[AccountProvider] = None
    # The status property
    status: Optional[AccountStatus] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Account:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Account
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Account()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .account_provider import AccountProvider
        from .account_status import AccountStatus
        from .git_hub_app_installation import GitHubAppInstallation

        from .account_provider import AccountProvider
        from .account_status import AccountStatus
        from .git_hub_app_installation import GitHubAppInstallation

        fields: dict[str, Callable[[Any], None]] = {
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "email": lambda n : setattr(self, 'email', n.get_str_value()),
            "github_app_installation": lambda n : setattr(self, 'github_app_installation', n.get_object_value(GitHubAppInstallation)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(AccountProvider)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(AccountStatus)),
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
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("email", self.email)
        writer.write_object_value("github_app_installation", self.github_app_installation)
        writer.write_str_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("provider", self.provider)
        writer.write_enum_value("status", self.status)
    

