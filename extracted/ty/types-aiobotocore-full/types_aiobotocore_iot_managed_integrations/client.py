"""
Type annotations for iot-managed-integrations service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot_managed_integrations.client import ManagedintegrationsforIoTDeviceManagementClient

    session = get_session()
    async with session.create_client("iot-managed-integrations") as client:
        client: ManagedintegrationsforIoTDeviceManagementClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
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
from .type_defs import (
    CreateCredentialLockerRequestTypeDef,
    CreateCredentialLockerResponseTypeDef,
    CreateDestinationRequestTypeDef,
    CreateDestinationResponseTypeDef,
    CreateEventLogConfigurationRequestTypeDef,
    CreateEventLogConfigurationResponseTypeDef,
    CreateManagedThingRequestTypeDef,
    CreateManagedThingResponseTypeDef,
    CreateNotificationConfigurationRequestTypeDef,
    CreateNotificationConfigurationResponseTypeDef,
    CreateOtaTaskConfigurationRequestTypeDef,
    CreateOtaTaskConfigurationResponseTypeDef,
    CreateOtaTaskRequestTypeDef,
    CreateOtaTaskResponseTypeDef,
    CreateProvisioningProfileRequestTypeDef,
    CreateProvisioningProfileResponseTypeDef,
    DeleteCredentialLockerRequestTypeDef,
    DeleteDestinationRequestTypeDef,
    DeleteEventLogConfigurationRequestTypeDef,
    DeleteManagedThingRequestTypeDef,
    DeleteNotificationConfigurationRequestTypeDef,
    DeleteOtaTaskConfigurationRequestTypeDef,
    DeleteOtaTaskRequestTypeDef,
    DeleteProvisioningProfileRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCredentialLockerRequestTypeDef,
    GetCredentialLockerResponseTypeDef,
    GetCustomEndpointResponseTypeDef,
    GetDefaultEncryptionConfigurationResponseTypeDef,
    GetDestinationRequestTypeDef,
    GetDestinationResponseTypeDef,
    GetDeviceDiscoveryRequestTypeDef,
    GetDeviceDiscoveryResponseTypeDef,
    GetEventLogConfigurationRequestTypeDef,
    GetEventLogConfigurationResponseTypeDef,
    GetHubConfigurationResponseTypeDef,
    GetManagedThingCapabilitiesRequestTypeDef,
    GetManagedThingCapabilitiesResponseTypeDef,
    GetManagedThingConnectivityDataRequestTypeDef,
    GetManagedThingConnectivityDataResponseTypeDef,
    GetManagedThingMetaDataRequestTypeDef,
    GetManagedThingMetaDataResponseTypeDef,
    GetManagedThingRequestTypeDef,
    GetManagedThingResponseTypeDef,
    GetManagedThingStateRequestTypeDef,
    GetManagedThingStateResponseTypeDef,
    GetNotificationConfigurationRequestTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetOtaTaskConfigurationRequestTypeDef,
    GetOtaTaskConfigurationResponseTypeDef,
    GetOtaTaskRequestTypeDef,
    GetOtaTaskResponseTypeDef,
    GetProvisioningProfileRequestTypeDef,
    GetProvisioningProfileResponseTypeDef,
    GetRuntimeLogConfigurationRequestTypeDef,
    GetRuntimeLogConfigurationResponseTypeDef,
    GetSchemaVersionRequestTypeDef,
    GetSchemaVersionResponseTypeDef,
    ListCredentialLockersRequestTypeDef,
    ListCredentialLockersResponseTypeDef,
    ListDestinationsRequestTypeDef,
    ListDestinationsResponseTypeDef,
    ListEventLogConfigurationsRequestTypeDef,
    ListEventLogConfigurationsResponseTypeDef,
    ListManagedThingSchemasRequestTypeDef,
    ListManagedThingSchemasResponseTypeDef,
    ListManagedThingsRequestTypeDef,
    ListManagedThingsResponseTypeDef,
    ListNotificationConfigurationsRequestTypeDef,
    ListNotificationConfigurationsResponseTypeDef,
    ListOtaTaskConfigurationsRequestTypeDef,
    ListOtaTaskConfigurationsResponseTypeDef,
    ListOtaTaskExecutionsRequestTypeDef,
    ListOtaTaskExecutionsResponseTypeDef,
    ListOtaTasksRequestTypeDef,
    ListOtaTasksResponseTypeDef,
    ListProvisioningProfilesRequestTypeDef,
    ListProvisioningProfilesResponseTypeDef,
    ListSchemaVersionsRequestTypeDef,
    ListSchemaVersionsResponseTypeDef,
    PutDefaultEncryptionConfigurationRequestTypeDef,
    PutDefaultEncryptionConfigurationResponseTypeDef,
    PutHubConfigurationRequestTypeDef,
    PutHubConfigurationResponseTypeDef,
    PutRuntimeLogConfigurationRequestTypeDef,
    RegisterCustomEndpointResponseTypeDef,
    ResetRuntimeLogConfigurationRequestTypeDef,
    SendManagedThingCommandRequestTypeDef,
    SendManagedThingCommandResponseTypeDef,
    StartDeviceDiscoveryRequestTypeDef,
    StartDeviceDiscoveryResponseTypeDef,
    UpdateDestinationRequestTypeDef,
    UpdateEventLogConfigurationRequestTypeDef,
    UpdateManagedThingRequestTypeDef,
    UpdateNotificationConfigurationRequestTypeDef,
    UpdateOtaTaskRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ManagedintegrationsforIoTDeviceManagementClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ManagedintegrationsforIoTDeviceManagementClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations.html#ManagedintegrationsforIoTDeviceManagement.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ManagedintegrationsforIoTDeviceManagementClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations.html#ManagedintegrationsforIoTDeviceManagement.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#generate_presigned_url)
        """

    async def create_credential_locker(
        self, **kwargs: Unpack[CreateCredentialLockerRequestTypeDef]
    ) -> CreateCredentialLockerResponseTypeDef:
        """
        Create a product credential locker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_credential_locker.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_credential_locker)
        """

    async def create_destination(
        self, **kwargs: Unpack[CreateDestinationRequestTypeDef]
    ) -> CreateDestinationResponseTypeDef:
        """
        Create a destination.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_destination)
        """

    async def create_event_log_configuration(
        self, **kwargs: Unpack[CreateEventLogConfigurationRequestTypeDef]
    ) -> CreateEventLogConfigurationResponseTypeDef:
        """
        Set the event log configuration for the account, resource type, or specific
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_event_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_event_log_configuration)
        """

    async def create_managed_thing(
        self, **kwargs: Unpack[CreateManagedThingRequestTypeDef]
    ) -> CreateManagedThingResponseTypeDef:
        """
        Creates a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_managed_thing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_managed_thing)
        """

    async def create_notification_configuration(
        self, **kwargs: Unpack[CreateNotificationConfigurationRequestTypeDef]
    ) -> CreateNotificationConfigurationResponseTypeDef:
        """
        Creates a notification configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_notification_configuration)
        """

    async def create_ota_task(
        self, **kwargs: Unpack[CreateOtaTaskRequestTypeDef]
    ) -> CreateOtaTaskResponseTypeDef:
        """
        Create an over-the-air (OTA) task to update a device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_ota_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_ota_task)
        """

    async def create_ota_task_configuration(
        self, **kwargs: Unpack[CreateOtaTaskConfigurationRequestTypeDef]
    ) -> CreateOtaTaskConfigurationResponseTypeDef:
        """
        Create a configuraiton for the over-the-air (OTA) task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_ota_task_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_ota_task_configuration)
        """

    async def create_provisioning_profile(
        self, **kwargs: Unpack[CreateProvisioningProfileRequestTypeDef]
    ) -> CreateProvisioningProfileResponseTypeDef:
        """
        Create a provisioning profile for a device to execute the provisioning flows
        using a provisioning template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/create_provisioning_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#create_provisioning_profile)
        """

    async def delete_credential_locker(
        self, **kwargs: Unpack[DeleteCredentialLockerRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a credential locker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_credential_locker.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_credential_locker)
        """

    async def delete_destination(
        self, **kwargs: Unpack[DeleteDestinationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a customer-managed destination specified by id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_destination)
        """

    async def delete_event_log_configuration(
        self, **kwargs: Unpack[DeleteEventLogConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete an event log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_event_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_event_log_configuration)
        """

    async def delete_managed_thing(
        self, **kwargs: Unpack[DeleteManagedThingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_managed_thing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_managed_thing)
        """

    async def delete_notification_configuration(
        self, **kwargs: Unpack[DeleteNotificationConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a notification configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_notification_configuration)
        """

    async def delete_ota_task(
        self, **kwargs: Unpack[DeleteOtaTaskRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the over-the-air (OTA) task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_ota_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_ota_task)
        """

    async def delete_ota_task_configuration(
        self, **kwargs: Unpack[DeleteOtaTaskConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the over-the-air (OTA) task configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_ota_task_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_ota_task_configuration)
        """

    async def delete_provisioning_profile(
        self, **kwargs: Unpack[DeleteProvisioningProfileRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete a provisioning profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/delete_provisioning_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#delete_provisioning_profile)
        """

    async def get_credential_locker(
        self, **kwargs: Unpack[GetCredentialLockerRequestTypeDef]
    ) -> GetCredentialLockerResponseTypeDef:
        """
        Get information on an existing credential locker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_credential_locker.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_credential_locker)
        """

    async def get_custom_endpoint(self) -> GetCustomEndpointResponseTypeDef:
        """
        Returns the IoT managed integrations custom endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_custom_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_custom_endpoint)
        """

    async def get_default_encryption_configuration(
        self,
    ) -> GetDefaultEncryptionConfigurationResponseTypeDef:
        """
        Retrieves information about the default encryption configuration for the Amazon
        Web Services account in the default or specified region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_default_encryption_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_default_encryption_configuration)
        """

    async def get_destination(
        self, **kwargs: Unpack[GetDestinationRequestTypeDef]
    ) -> GetDestinationResponseTypeDef:
        """
        Gets a destination by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_destination)
        """

    async def get_device_discovery(
        self, **kwargs: Unpack[GetDeviceDiscoveryRequestTypeDef]
    ) -> GetDeviceDiscoveryResponseTypeDef:
        """
        Get the current state of a device discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_device_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_device_discovery)
        """

    async def get_event_log_configuration(
        self, **kwargs: Unpack[GetEventLogConfigurationRequestTypeDef]
    ) -> GetEventLogConfigurationResponseTypeDef:
        """
        Get an event log configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_event_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_event_log_configuration)
        """

    async def get_hub_configuration(self) -> GetHubConfigurationResponseTypeDef:
        """
        Get a hub configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_hub_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_hub_configuration)
        """

    async def get_managed_thing(
        self, **kwargs: Unpack[GetManagedThingRequestTypeDef]
    ) -> GetManagedThingResponseTypeDef:
        """
        Get the attributes and capabilities associated with a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_managed_thing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_managed_thing)
        """

    async def get_managed_thing_capabilities(
        self, **kwargs: Unpack[GetManagedThingCapabilitiesRequestTypeDef]
    ) -> GetManagedThingCapabilitiesResponseTypeDef:
        """
        Get the capabilities for a managed thing using the device ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_managed_thing_capabilities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_managed_thing_capabilities)
        """

    async def get_managed_thing_connectivity_data(
        self, **kwargs: Unpack[GetManagedThingConnectivityDataRequestTypeDef]
    ) -> GetManagedThingConnectivityDataResponseTypeDef:
        """
        Get the connectivity status of a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_managed_thing_connectivity_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_managed_thing_connectivity_data)
        """

    async def get_managed_thing_meta_data(
        self, **kwargs: Unpack[GetManagedThingMetaDataRequestTypeDef]
    ) -> GetManagedThingMetaDataResponseTypeDef:
        """
        Get the metadata information for a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_managed_thing_meta_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_managed_thing_meta_data)
        """

    async def get_managed_thing_state(
        self, **kwargs: Unpack[GetManagedThingStateRequestTypeDef]
    ) -> GetManagedThingStateResponseTypeDef:
        """
        Returns the managed thing state for the given device Id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_managed_thing_state.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_managed_thing_state)
        """

    async def get_notification_configuration(
        self, **kwargs: Unpack[GetNotificationConfigurationRequestTypeDef]
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Get a notification configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_notification_configuration)
        """

    async def get_ota_task(
        self, **kwargs: Unpack[GetOtaTaskRequestTypeDef]
    ) -> GetOtaTaskResponseTypeDef:
        """
        Get the over-the-air (OTA) task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_ota_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_ota_task)
        """

    async def get_ota_task_configuration(
        self, **kwargs: Unpack[GetOtaTaskConfigurationRequestTypeDef]
    ) -> GetOtaTaskConfigurationResponseTypeDef:
        """
        Get a configuraiton for the over-the-air (OTA) task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_ota_task_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_ota_task_configuration)
        """

    async def get_provisioning_profile(
        self, **kwargs: Unpack[GetProvisioningProfileRequestTypeDef]
    ) -> GetProvisioningProfileResponseTypeDef:
        """
        Get a provisioning profile by template name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_provisioning_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_provisioning_profile)
        """

    async def get_runtime_log_configuration(
        self, **kwargs: Unpack[GetRuntimeLogConfigurationRequestTypeDef]
    ) -> GetRuntimeLogConfigurationResponseTypeDef:
        """
        Get the runtime log configuration for a specific managed thing or for all
        managed things as a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_runtime_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_runtime_log_configuration)
        """

    async def get_schema_version(
        self, **kwargs: Unpack[GetSchemaVersionRequestTypeDef]
    ) -> GetSchemaVersionResponseTypeDef:
        """
        Gets a schema version with the provided information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_schema_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_schema_version)
        """

    async def list_credential_lockers(
        self, **kwargs: Unpack[ListCredentialLockersRequestTypeDef]
    ) -> ListCredentialLockersResponseTypeDef:
        """
        List information on an existing credential locker.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_credential_lockers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_credential_lockers)
        """

    async def list_destinations(
        self, **kwargs: Unpack[ListDestinationsRequestTypeDef]
    ) -> ListDestinationsResponseTypeDef:
        """
        List all destination names under one Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_destinations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_destinations)
        """

    async def list_event_log_configurations(
        self, **kwargs: Unpack[ListEventLogConfigurationsRequestTypeDef]
    ) -> ListEventLogConfigurationsResponseTypeDef:
        """
        List all event log configurations for an account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_event_log_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_event_log_configurations)
        """

    async def list_managed_thing_schemas(
        self, **kwargs: Unpack[ListManagedThingSchemasRequestTypeDef]
    ) -> ListManagedThingSchemasResponseTypeDef:
        """
        List schemas associated with a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_managed_thing_schemas.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_managed_thing_schemas)
        """

    async def list_managed_things(
        self, **kwargs: Unpack[ListManagedThingsRequestTypeDef]
    ) -> ListManagedThingsResponseTypeDef:
        """
        List all of the associations and statuses for a managed thing by its owner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_managed_things.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_managed_things)
        """

    async def list_notification_configurations(
        self, **kwargs: Unpack[ListNotificationConfigurationsRequestTypeDef]
    ) -> ListNotificationConfigurationsResponseTypeDef:
        """
        List all notification configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_notification_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_notification_configurations)
        """

    async def list_ota_task_configurations(
        self, **kwargs: Unpack[ListOtaTaskConfigurationsRequestTypeDef]
    ) -> ListOtaTaskConfigurationsResponseTypeDef:
        """
        List all of the over-the-air (OTA) task configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_ota_task_configurations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_ota_task_configurations)
        """

    async def list_ota_task_executions(
        self, **kwargs: Unpack[ListOtaTaskExecutionsRequestTypeDef]
    ) -> ListOtaTaskExecutionsResponseTypeDef:
        """
        List all of the over-the-air (OTA) task executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_ota_task_executions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_ota_task_executions)
        """

    async def list_ota_tasks(
        self, **kwargs: Unpack[ListOtaTasksRequestTypeDef]
    ) -> ListOtaTasksResponseTypeDef:
        """
        List all of the over-the-air (OTA) tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_ota_tasks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_ota_tasks)
        """

    async def list_provisioning_profiles(
        self, **kwargs: Unpack[ListProvisioningProfilesRequestTypeDef]
    ) -> ListProvisioningProfilesResponseTypeDef:
        """
        List the provisioning profiles within the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_provisioning_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_provisioning_profiles)
        """

    async def list_schema_versions(
        self, **kwargs: Unpack[ListSchemaVersionsRequestTypeDef]
    ) -> ListSchemaVersionsResponseTypeDef:
        """
        Lists schema versions with the provided information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/list_schema_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#list_schema_versions)
        """

    async def put_default_encryption_configuration(
        self, **kwargs: Unpack[PutDefaultEncryptionConfigurationRequestTypeDef]
    ) -> PutDefaultEncryptionConfigurationResponseTypeDef:
        """
        Sets the default encryption configuration for the Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/put_default_encryption_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#put_default_encryption_configuration)
        """

    async def put_hub_configuration(
        self, **kwargs: Unpack[PutHubConfigurationRequestTypeDef]
    ) -> PutHubConfigurationResponseTypeDef:
        """
        Update a hub configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/put_hub_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#put_hub_configuration)
        """

    async def put_runtime_log_configuration(
        self, **kwargs: Unpack[PutRuntimeLogConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Set the runtime log configuration for a specific managed thing or for all
        managed things as a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/put_runtime_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#put_runtime_log_configuration)
        """

    async def register_custom_endpoint(self) -> RegisterCustomEndpointResponseTypeDef:
        """
        Customers can request IoT managed integrations to manage the server trust for
        them or bring their own external server trusts for the custom domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/register_custom_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#register_custom_endpoint)
        """

    async def reset_runtime_log_configuration(
        self, **kwargs: Unpack[ResetRuntimeLogConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Reset a runtime log configuration for a specific managed thing or for all
        managed things as a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/reset_runtime_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#reset_runtime_log_configuration)
        """

    async def send_managed_thing_command(
        self, **kwargs: Unpack[SendManagedThingCommandRequestTypeDef]
    ) -> SendManagedThingCommandResponseTypeDef:
        """
        Send the command to the device represented by the managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/send_managed_thing_command.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#send_managed_thing_command)
        """

    async def start_device_discovery(
        self, **kwargs: Unpack[StartDeviceDiscoveryRequestTypeDef]
    ) -> StartDeviceDiscoveryResponseTypeDef:
        """
        During user-guided setup, this is used to start device discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/start_device_discovery.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#start_device_discovery)
        """

    async def update_destination(
        self, **kwargs: Unpack[UpdateDestinationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update a destination specified by id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/update_destination.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#update_destination)
        """

    async def update_event_log_configuration(
        self, **kwargs: Unpack[UpdateEventLogConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update an event log configuration by log configuration ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/update_event_log_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#update_event_log_configuration)
        """

    async def update_managed_thing(
        self, **kwargs: Unpack[UpdateManagedThingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update the attributes and capabilities associated with a managed thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/update_managed_thing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#update_managed_thing)
        """

    async def update_notification_configuration(
        self, **kwargs: Unpack[UpdateNotificationConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update a notification configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/update_notification_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#update_notification_configuration)
        """

    async def update_ota_task(
        self, **kwargs: Unpack[UpdateOtaTaskRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Update an over-the-air (OTA) task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/update_ota_task.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#update_ota_task)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_credential_lockers"]
    ) -> ListCredentialLockersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_destinations"]
    ) -> ListDestinationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_log_configurations"]
    ) -> ListEventLogConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_thing_schemas"]
    ) -> ListManagedThingSchemasPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_things"]
    ) -> ListManagedThingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_notification_configurations"]
    ) -> ListNotificationConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ota_task_configurations"]
    ) -> ListOtaTaskConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ota_task_executions"]
    ) -> ListOtaTaskExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ota_tasks"]
    ) -> ListOtaTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_provisioning_profiles"]
    ) -> ListProvisioningProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_schema_versions"]
    ) -> ListSchemaVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations.html#ManagedintegrationsforIoTDeviceManagement.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-managed-integrations.html#ManagedintegrationsforIoTDeviceManagement.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_managed_integrations/client/)
        """
