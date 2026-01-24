from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

from pydantic.v1 import Field

from bigeye_sdk.bigconfig_validation.yaml_model_base import (
    YamlModelWithValidatorContext,
)
from bigeye_sdk.exceptions.exceptions import InvalidConfigurationException
from bigeye_sdk.generated.com.bigeye.models.generated import (
    IntegrationType,
    CustomIntegrationType,
    CustomNodeType,
    CustomRepository,
)
from bigeye_sdk.serializable import File
from bigeye_sdk.log import get_logger

log = get_logger(__name__)


@dataclass
class CustomIntegrationDeploymentResult:
    """
    Result of deploying a custom integration.

    Attributes:
        integration_type_id: ID of the created/updated integration type
        node_type_ids: Dictionary mapping node type names to their IDs
        repository_ids: Dictionary mapping repository names to their IDs
        created: True if new resources were created
        updated: True if existing resources were updated
    """
    integration_type_id: int
    node_type_ids: Dict[str, int] = field(default_factory=dict)
    repository_ids: Dict[str, int] = field(default_factory=dict)
    created: bool = False
    updated: bool = False

    def get_node_type_id(self, name: str) -> Optional[int]:
        """Get node type ID by name"""
        return self.node_type_ids.get(name)

    def get_repository_id(self, name: str) -> Optional[int]:
        """Get repository ID by name"""
        return self.repository_ids.get(name)


class SimpleIntegrationType(enum.Enum):
    """
    Simple facade for IntegrationType enum.
    Maps user-friendly names to protobuf IntegrationType values.
    """
    UNSPECIFIED = "INTEGRATION_TYPE_UNSPECIFIED"
    BI_TOOL = "INTEGRATION_TYPE_BI_TOOL"
    ETL_TOOL = "INTEGRATION_TYPE_ETL_TOOL"
    DATABASE = "INTEGRATION_TYPE_DATABASE"

    def to_protobuf(self) -> IntegrationType:
        """Convert to protobuf IntegrationType"""
        return IntegrationType[self.value]


class SimpleCustomNodeType(YamlModelWithValidatorContext):
    """
    Represents a custom node type definition.

    Attributes:
        name: Singular display name (e.g., "Schema", "Table")
        name_plural: Plural display name (e.g., "Schemas", "Tables")
        allowed_parent_types: List of node type names that can be parents
        id: Optional ID if this node type already exists
    """
    name: str
    name_plural: str
    allowed_parent_types: Optional[List[str]] = None
    id: Optional[int] = None
    is_column_display: Optional[bool] = False

    def to_protobuf(self, integration_type_id: int) -> CustomNodeType:
        """
        Convert to protobuf CustomNodeType.

        Args:
            integration_type_id: ID of the integration type this node type belongs to

        Returns:
            CustomNodeType protobuf object
        """
        parent_types = []
        if self.allowed_parent_types:
            parent_types = [
                CustomNodeType(name=parent_name)
                for parent_name in self.allowed_parent_types
            ]

        return CustomNodeType(
            id=self.id or 0,
            name=self.name,
            name_plural=self.name_plural,
            integration_type=CustomIntegrationType(id=integration_type_id),
            allowed_parent_types=parent_types,
            is_column_display=self.is_column_display
        )


class SimpleCustomRepository(YamlModelWithValidatorContext):
    """
    Represents a custom repository instance.

    Attributes:
        name: Display name for the repository (e.g., "Analytics", "Production")
        id: Optional ID if this repository already exists
    """
    name: str
    id: Optional[int] = None

    def to_protobuf(self, integration_type_id: int, workspace_id: int) -> CustomRepository:
        """
        Convert to protobuf CustomRepository.

        Args:
            integration_type_id: ID of the integration type
            workspace_id: ID of the workspace

        Returns:
            CustomRepository protobuf object
        """
        return CustomRepository(
            id=self.id or 0,
            name=self.name,
            integration_type=CustomIntegrationType(id=integration_type_id),
            workspace_id=workspace_id
        )


class SimpleCustomIntegration(YamlModelWithValidatorContext):
    """
    Represents a complete custom integration definition including:
    - Integration type (e.g., TylerDB, custom ETL tool)
    - Node types (e.g., Schema, Table, Column)
    - Repository instances (e.g., Analytics database)

    This class provides a declarative way to define custom integrations
    that can be easily version controlled and deployed.

    Attributes:
        name: Display name for the integration type
        description: Description of the integration type
        type: Category of integration (DATABASE, BI_TOOL, ETL_TOOL)
        icon_url: Optional URL to an icon image
        node_types: List of node type definitions for this integration
        repositories: Optional list of repository instances
        integration_type_id: Optional ID if this integration type already exists

    """
    name: str
    description: Optional[str] = None
    type: SimpleIntegrationType = SimpleIntegrationType.DATABASE
    icon_url: Optional[str] = None
    node_types: List[SimpleCustomNodeType] = Field(default_factory=list)
    repositories: Optional[List[SimpleCustomRepository]] = None
    integration_type_id: Optional[int] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__verify_config()

    def __verify_config(self):
        """Verify the integration configuration is valid"""
        if not self.node_types:
            raise InvalidConfigurationException(
                f"Integration '{self.name}' must have at least one node type defined"
            )

        # Verify parent type references are valid
        node_type_names = {nt.name for nt in self.node_types}
        for node_type in self.node_types:
            if node_type.allowed_parent_types:
                for parent_name in node_type.allowed_parent_types:
                    if parent_name not in node_type_names:
                        raise InvalidConfigurationException(
                            f"Node type '{node_type.name}' references unknown parent type '{parent_name}'. "
                            f"Available types: {', '.join(node_type_names)}"
                        )

    def to_integration_type_protobuf(self) -> CustomIntegrationType:
        """
        Convert to protobuf CustomIntegrationType.

        Returns:
            CustomIntegrationType protobuf object
        """
        return CustomIntegrationType(
            id=self.integration_type_id or 0,
            name=self.name,
            description=self.description or "",
            type=self.type.to_protobuf(),
            icon_url=self.icon_url or ""
        )

    def get_node_types_protobuf(self) -> List[CustomNodeType]:
        """
        Convert node types to protobuf objects.

        Returns:
            List of CustomNodeType protobuf objects

        Raises:
            InvalidConfigurationException: If integration_type_id is not set
        """
        if not self.integration_type_id:
            raise InvalidConfigurationException(
                f"Integration type ID must be set before converting node types. "
                f"Create the integration type first, then set integration_type_id."
            )

        return [
            node_type.to_protobuf(self.integration_type_id)
            for node_type in self.node_types
        ]

    def get_repositories_protobuf(self, workspace_id: int) -> List[CustomRepository]:
        """
        Convert repositories to protobuf objects.

        Args:
            workspace_id: ID of the workspace

        Returns:
            List of CustomRepository protobuf objects

        Raises:
            InvalidConfigurationException: If integration_type_id is not set or no repositories defined
        """
        if not self.integration_type_id:
            raise InvalidConfigurationException(
                f"Integration type ID must be set before converting repositories. "
                f"Create the integration type first, then set integration_type_id."
            )

        if not self.repositories:
            return []

        return [
            repo.to_protobuf(self.integration_type_id, workspace_id)
            for repo in self.repositories
        ]


class CustomIntegrationConfigurationFile(File, type="CUSTOM_INTEGRATION_CONFIGURATION_FILE"):
    """
    Configuration file for defining custom integrations.

    This allows you to define custom integrations in YAML format and version control them.

    Attributes:
        integrations: List of custom integration definitions

    Example YAML:
        ```yaml
        type: CUSTOM_INTEGRATION_CONFIGURATION_FILE
        integrations:
          - name: TylerDB
            description: Custom database for analytics
            type: DATABASE
            icon_url: https://example.com/icon.svg
            node_types:
              - name: Schema
                name_plural: Schemas
              - name: Table
                name_plural: Tables
                allowed_parent_types:
                  - Schema
              - name: Column
                name_plural: Columns
                allowed_parent_types:
                  - Table
            repositories:
              - name: Analytics
              - name: Production
        ```
    """
    integrations: Optional[List[SimpleCustomIntegration]] = None

    def get_integration_by_name(self, name: str) -> Optional[SimpleCustomIntegration]:
        """
        Get an integration by name.

        Args:
            name: Name of the integration to find

        Returns:
            The integration if found, None otherwise
        """
        if not self.integrations:
            return None

        for integration in self.integrations:
            if integration.name == name:
                return integration

        return None