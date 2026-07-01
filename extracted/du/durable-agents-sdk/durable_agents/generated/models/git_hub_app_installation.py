from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .git_hub_app_installation_repository_selection import GitHubAppInstallation_repository_selection

@dataclass
class GitHubAppInstallation(Parsable):
    # GitHub organization or user account for the installation, when known.
    account: Optional[str] = None
    # GitHub App installation identifier returned during OAuth authorization.
    installation_id: Optional[str] = None
    # Best-known GitHub settings URL for managing the installation.
    manage_url: Optional[str] = None
    # Repository access selection for the installation, when known.
    repository_selection: Optional[GitHubAppInstallation_repository_selection] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> GitHubAppInstallation:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: GitHubAppInstallation
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return GitHubAppInstallation()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .git_hub_app_installation_repository_selection import GitHubAppInstallation_repository_selection

        from .git_hub_app_installation_repository_selection import GitHubAppInstallation_repository_selection

        fields: dict[str, Callable[[Any], None]] = {
            "account": lambda n : setattr(self, 'account', n.get_str_value()),
            "installation_id": lambda n : setattr(self, 'installation_id', n.get_str_value()),
            "manage_url": lambda n : setattr(self, 'manage_url', n.get_str_value()),
            "repository_selection": lambda n : setattr(self, 'repository_selection', n.get_enum_value(GitHubAppInstallation_repository_selection)),
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
        writer.write_str_value("account", self.account)
        writer.write_str_value("installation_id", self.installation_id)
        writer.write_str_value("manage_url", self.manage_url)
        writer.write_enum_value("repository_selection", self.repository_selection)
    

