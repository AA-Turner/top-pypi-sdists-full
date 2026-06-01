"""Smpl SDK Management — top-level :class:`SmplManagementClient` and namespaces.

The :class:`SmplManagementClient` (and its async variant) is the single
entry point for every management/CRUD operation in the SDK. It is the
counterpart to the runtime :class:`smplkit.SmplClient`, which is now
strictly for instrumentation: flag evaluation, config reads, log emission,
and audit-event recording.

Exposed namespaces:

- ``mgmt.contexts.*``
- ``mgmt.context_types.*``
- ``mgmt.environments.*``
- ``mgmt.services.*``
- ``mgmt.account_settings.*``
- ``mgmt.config.*``
- ``mgmt.flags.*``
- ``mgmt.loggers.*``
- ``mgmt.log_groups.*``
- ``mgmt.audit.*``
"""

from __future__ import annotations

from smplkit.audit.models import ForwarderType, TransformType
from smplkit.management.audit import (
    AsyncAuditClient as AsyncMgmtAuditClient,
    AuditClient as MgmtAuditClient,
    ForwarderListPage as AuditForwarderListPage,
    ForwardersClient as AuditForwardersClient,
)
from smplkit.management.client import (
    AccountSettingsClient,
    AsyncAccountSettingsClient,
    AsyncConfigClient,
    AsyncContextsClient,
    AsyncContextTypesClient,
    AsyncEnvironmentsClient,
    AsyncFlagsClient,
    AsyncLogGroupsClient,
    AsyncLoggersClient,
    AsyncServicesClient,
    AsyncSmplManagementClient,
    ConfigClient,
    ContextsClient,
    ContextTypesClient,
    EnvironmentsClient,
    FlagsClient,
    LogGroupsClient,
    LoggersClient,
    ServicesClient,
    SmplManagementClient,
)
from smplkit.management.models import (
    AccountSettings,
    AsyncAccountSettings,
    AsyncContextType,
    AsyncEnvironment,
    AsyncService,
    ContextType,
    Environment,
    Service,
)
from smplkit.management.types import EnvironmentClassification

__all__ = [
    "AccountSettings",
    "AccountSettingsClient",
    "AsyncAccountSettings",
    "AsyncAccountSettingsClient",
    "AsyncConfigClient",
    "AsyncContextType",
    "AsyncContextTypesClient",
    "AsyncContextsClient",
    "AsyncEnvironment",
    "AsyncEnvironmentsClient",
    "AsyncFlagsClient",
    "AsyncLogGroupsClient",
    "AsyncLoggersClient",
    "AsyncMgmtAuditClient",
    "AsyncService",
    "AsyncServicesClient",
    "AsyncSmplManagementClient",
    "AuditForwarderListPage",
    "AuditForwardersClient",
    "ConfigClient",
    "ContextType",
    "ContextTypesClient",
    "ContextsClient",
    "Environment",
    "EnvironmentClassification",
    "EnvironmentsClient",
    "FlagsClient",
    "ForwarderType",
    "LogGroupsClient",
    "LoggersClient",
    "MgmtAuditClient",
    "Service",
    "ServicesClient",
    "SmplManagementClient",
    "TransformType",
]
