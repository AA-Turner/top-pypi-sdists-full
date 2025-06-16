"""
Type annotations for iot-managed-integrations service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot_managed_integrations.client import ManagedintegrationsforIoTDeviceManagementClient
    from types_aiobotocore_iot_managed_integrations.paginator import (
        ListCredentialLockersPaginator,
        ListDestinationsPaginator,
        ListEventLogConfigurationsPaginator,
        ListManagedThingSchemasPaginator,
        ListManagedThingsPaginator,
        ListNotificationConfigurationsPaginator,
        ListOtaTaskConfigurationsPaginator,
        ListOtaTaskExecutionsPaginator,
        ListOtaTasksPaginator,
        ListProvisioningProfilesPaginator,
        ListSchemaVersionsPaginator,
    )

    session = get_session()
    with session.create_client("iot-managed-integrations") as client:
        client: ManagedintegrationsforIoTDeviceManagementClient

        list_credential_lockers_paginator: ListCredentialLockersPaginator = client.get_paginator("list_credential_lockers")
        list_destinations_paginator: ListDestinationsPaginator = client.get_paginator("list_destinations")
        list_event_log_configurations_paginator: ListEventLogConfigurationsPaginator = client.get_paginator("list_event_log_configurations")
        list_managed_thing_schemas_paginator: ListManagedThingSchemasPaginator = client.get_paginator("list_managed_thing_schemas")
        list_managed_things_paginator: ListManagedThingsPaginator = client.get_paginator("list_managed_things")
        list_notification_configurations_paginator: ListNotificationConfigurationsPaginator = client.get_paginator("list_notification_configurations")
        list_ota_task_configurations_paginator: ListOtaTaskConfigurationsPaginator = client.get_paginator("list_ota_task_configurations")
        list_ota_task_executions_paginator: ListOtaTaskExecutionsPaginator = client.get_paginator("list_ota_task_executions")
        list_ota_tasks_paginator: ListOtaTasksPaginator = client.get_paginator("list_ota_tasks")
        list_provisioning_profiles_paginator: ListProvisioningProfilesPaginator = client.get_paginator("list_provisioning_profiles")
        list_schema_versions_paginator: ListSchemaVersionsPaginator = client.get_paginator("list_schema_versions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCredentialLockersRequestPaginateTypeDef,
    ListCredentialLockersResponseTypeDef,
    ListDestinationsRequestPaginateTypeDef,
    ListDestinationsResponseTypeDef,
    ListEventLogConfigurationsRequestPaginateTypeDef,
    ListEventLogConfigurationsResponseTypeDef,
    ListManagedThingSchemasRequestPaginateTypeDef,
    ListManagedThingSchemasResponseTypeDef,
    ListManagedThingsRequestPaginateTypeDef,
    ListManagedThingsResponseTypeDef,
    ListNotificationConfigurationsRequestPaginateTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListOtaTaskConfigurationsRequestPaginateTypeDef,
    ListOtaTaskConfigurationsResponseTypeDef,
    ListOtaTaskExecutionsRequestPaginateTypeDef,
    ListOtaTaskExecutionsResponseTypeDef,
    ListOtaTasksRequestPaginateTypeDef,
    ListOtaTasksResponseTypeDef,
    ListProvisioningProfilesRequestPaginateTypeDef,
    ListProvisioningProfilesResponseTypeDef,
    ListSchemaVersionsRequestPaginateTypeDef,
    ListSchemaVersionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCredentialLockersPaginator",
    "ListDestinationsPaginator",
    "ListEventLogConfigurationsPaginator",
    "ListManagedThingSchemasPaginator",
    "ListManagedThingsPaginator",
    "ListNotificationConfigurationsPaginator",
    "ListOtaTaskConfigurationsPaginator",
    "ListOtaTaskExecutionsPaginator",
    "ListOtaTasksPaginator",
    "ListProvisioningProfilesPaginator",
    "ListSchemaVersionsPaginator",
)

if TYPE_CHECKING:
    _ListCredentialLockersPaginatorBase = AioPaginator[ListCredentialLockersResponseTypeDef]
else:
    _ListCredentialLockersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCredentialLockersPaginator(_ListCredentialLockersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListCredentialLockers.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListCredentialLockers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listcredentiallockerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCredentialLockersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCredentialLockersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListCredentialLockers.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListCredentialLockers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listcredentiallockerspaginator)
        """

if TYPE_CHECKING:
    _ListDestinationsPaginatorBase = AioPaginator[ListDestinationsResponseTypeDef]
else:
    _ListDestinationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDestinationsPaginator(_ListDestinationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListDestinations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListDestinations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listdestinationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDestinationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListDestinations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListDestinations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listdestinationspaginator)
        """

if TYPE_CHECKING:
    _ListEventLogConfigurationsPaginatorBase = AioPaginator[
        ListEventLogConfigurationsResponseTypeDef
    ]
else:
    _ListEventLogConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventLogConfigurationsPaginator(_ListEventLogConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListEventLogConfigurations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListEventLogConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listeventlogconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventLogConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventLogConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListEventLogConfigurations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListEventLogConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listeventlogconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListManagedThingSchemasPaginatorBase = AioPaginator[ListManagedThingSchemasResponseTypeDef]
else:
    _ListManagedThingSchemasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedThingSchemasPaginator(_ListManagedThingSchemasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListManagedThingSchemas.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListManagedThingSchemas)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listmanagedthingschemaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedThingSchemasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedThingSchemasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListManagedThingSchemas.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListManagedThingSchemas.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listmanagedthingschemaspaginator)
        """

if TYPE_CHECKING:
    _ListManagedThingsPaginatorBase = AioPaginator[ListManagedThingsResponseTypeDef]
else:
    _ListManagedThingsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedThingsPaginator(_ListManagedThingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListManagedThings.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListManagedThings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listmanagedthingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedThingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListManagedThings.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListManagedThings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listmanagedthingspaginator)
        """

if TYPE_CHECKING:
    _ListNotificationConfigurationsPaginatorBase = AioPaginator[
        ListNotificationConfigurationsResponseTypeDef
    ]
else:
    _ListNotificationConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNotificationConfigurationsPaginator(_ListNotificationConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListNotificationConfigurations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListNotificationConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listnotificationconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNotificationConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListNotificationConfigurations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListNotificationConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listnotificationconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListOtaTaskConfigurationsPaginatorBase = AioPaginator[ListOtaTaskConfigurationsResponseTypeDef]
else:
    _ListOtaTaskConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOtaTaskConfigurationsPaginator(_ListOtaTaskConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListOtaTaskConfigurations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListOtaTaskConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listotataskconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOtaTaskConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOtaTaskConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListOtaTaskConfigurations.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListOtaTaskConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listotataskconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListOtaTaskExecutionsPaginatorBase = AioPaginator[ListOtaTaskExecutionsResponseTypeDef]
else:
    _ListOtaTaskExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOtaTaskExecutionsPaginator(_ListOtaTaskExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListOtaTaskExecutions.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListOtaTaskExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listotataskexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOtaTaskExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOtaTaskExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListOtaTaskExecutions.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListOtaTaskExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listotataskexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListOtaTasksPaginatorBase = AioPaginator[ListOtaTasksResponseTypeDef]
else:
    _ListOtaTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOtaTasksPaginator(_ListOtaTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListOtaTasks.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListOtaTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listotataskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOtaTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOtaTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListOtaTasks.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListOtaTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listotataskspaginator)
        """

if TYPE_CHECKING:
    _ListProvisioningProfilesPaginatorBase = AioPaginator[ListProvisioningProfilesResponseTypeDef]
else:
    _ListProvisioningProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProvisioningProfilesPaginator(_ListProvisioningProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListProvisioningProfiles.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListProvisioningProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listprovisioningprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisioningProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProvisioningProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListProvisioningProfiles.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListProvisioningProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listprovisioningprofilespaginator)
        """

if TYPE_CHECKING:
    _ListSchemaVersionsPaginatorBase = AioPaginator[ListSchemaVersionsResponseTypeDef]
else:
    _ListSchemaVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSchemaVersionsPaginator(_ListSchemaVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListSchemaVersions.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListSchemaVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listschemaversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchemaVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSchemaVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/paginator/ListSchemaVersions.html#ManagedintegrationsforIoTDeviceManagement.Paginator.ListSchemaVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/paginators/#listschemaversionspaginator)
        """
