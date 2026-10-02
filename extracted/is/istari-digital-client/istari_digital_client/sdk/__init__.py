"""New facade code for the Istari SDK.

.. warning::
   **Beta — API subject to change.** This facade (``Istari`` / ``IstariIntegrations``
   / ``IstariAdmin``) is under active development; its surface may change without a
   deprecation cycle. The stable surface today is the legacy client
   (``Client`` / ``V3Client``). Adopt this facade only where you can absorb breaking
   changes between releases.

This package contains the high-level, user-friendly SDK interfaces:
- Istari: Main client for common user operations
- IstariIntegrations: Client for integration/automation workflows
- IstariAdmin: Client for administrative operations
- Configuration: SDK configuration
- Domain types: Resource, System, Job, Agent, etc.
- Error types: IstariError, NotFoundError, etc.
"""

# Clients
from istari_digital_client.sdk._client import Istari, IstariIntegrations, IstariAdmin

# Configuration
from istari_digital_client.sdk._configuration import Configuration

# Domain types - Resources
from istari_digital_client.sdk._common.resource_types import (
    Resource,
    ResourceRevision,
    TrackedResource,
    Comment,
)

# Domain types - Systems
from istari_digital_client.sdk._common.system_types import (
    System,
    Branch,
    Subsystem,
    ChangeRequest,
)

# Domain types - Jobs
from istari_digital_client.sdk._common.job_types import Job

# Domain types - Workflows
from istari_digital_client.sdk._common.workflow_types import (
    WorkflowLogEntry,
    WorkflowOutput,
)

# Domain types - Integrations
from istari_digital_client.sdk._integrations.integration_types import (
    Agent,
    AgentPool,
    Module,
    ModuleVersion,
    Tool,
    ToolVersion,
    Function,
    OperatingSystem,
    FunctionAuthSecret,
)

# Domain types - Admin
from istari_digital_client.sdk._admin.admin_types import (
    User,
    PersonalAccessToken,
)

# Error types
from istari_digital_client.sdk._exceptions import (
    IstariError,
    DetachedInstanceError,
    APIConnectionError,
    APIStatusError,
    BadRequestError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ConflictError,
    ValidationError,
    RateLimitError,
    InternalServerError,
    PATsDeprecatedError,
)

__all__ = [
    # Clients
    "Istari",
    "IstariIntegrations",
    "IstariAdmin",
    # Configuration
    "Configuration",
    # Domain types - Resources
    "Resource",
    "ResourceRevision",
    "TrackedResource",
    "Comment",
    # Domain types - Systems
    "System",
    "Branch",
    "Subsystem",
    "ChangeRequest",
    # Domain types - Jobs
    "Job",
    # Domain types - Workflows
    "WorkflowLogEntry",
    "WorkflowOutput",
    # Domain types - Integrations
    "Agent",
    "AgentPool",
    "Module",
    "ModuleVersion",
    "Tool",
    "ToolVersion",
    "Function",
    "OperatingSystem",
    "FunctionAuthSecret",
    # Domain types - Admin
    "User",
    "PersonalAccessToken",
    # Error types
    "IstariError",
    "DetachedInstanceError",
    "APIConnectionError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "ValidationError",
    "RateLimitError",
    "InternalServerError",
    "PATsDeprecatedError",
]
