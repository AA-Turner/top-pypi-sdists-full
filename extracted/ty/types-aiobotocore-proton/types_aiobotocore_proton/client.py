"""
Type annotations for proton service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_proton.client import ProtonClient

    session = get_session()
    async with session.create_client("proton") as client:
        client: ProtonClient
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
    ListComponentOutputsPaginator,
    ListComponentProvisionedResourcesPaginator,
    ListComponentsPaginator,
    ListDeploymentsPaginator,
    ListEnvironmentAccountConnectionsPaginator,
    ListEnvironmentOutputsPaginator,
    ListEnvironmentProvisionedResourcesPaginator,
    ListEnvironmentsPaginator,
    ListEnvironmentTemplatesPaginator,
    ListEnvironmentTemplateVersionsPaginator,
    ListRepositoriesPaginator,
    ListRepositorySyncDefinitionsPaginator,
    ListServiceInstanceOutputsPaginator,
    ListServiceInstanceProvisionedResourcesPaginator,
    ListServiceInstancesPaginator,
    ListServicePipelineOutputsPaginator,
    ListServicePipelineProvisionedResourcesPaginator,
    ListServicesPaginator,
    ListServiceTemplatesPaginator,
    ListServiceTemplateVersionsPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AcceptEnvironmentAccountConnectionInputTypeDef,
    AcceptEnvironmentAccountConnectionOutputTypeDef,
    CancelComponentDeploymentInputTypeDef,
    CancelComponentDeploymentOutputTypeDef,
    CancelEnvironmentDeploymentInputTypeDef,
    CancelEnvironmentDeploymentOutputTypeDef,
    CancelServiceInstanceDeploymentInputTypeDef,
    CancelServiceInstanceDeploymentOutputTypeDef,
    CancelServicePipelineDeploymentInputTypeDef,
    CancelServicePipelineDeploymentOutputTypeDef,
    CreateComponentInputTypeDef,
    CreateComponentOutputTypeDef,
    CreateEnvironmentAccountConnectionInputTypeDef,
    CreateEnvironmentAccountConnectionOutputTypeDef,
    CreateEnvironmentInputTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateEnvironmentTemplateInputTypeDef,
    CreateEnvironmentTemplateOutputTypeDef,
    CreateEnvironmentTemplateVersionInputTypeDef,
    CreateEnvironmentTemplateVersionOutputTypeDef,
    CreateRepositoryInputTypeDef,
    CreateRepositoryOutputTypeDef,
    CreateServiceInputTypeDef,
    CreateServiceInstanceInputTypeDef,
    CreateServiceInstanceOutputTypeDef,
    CreateServiceOutputTypeDef,
    CreateServiceSyncConfigInputTypeDef,
    CreateServiceSyncConfigOutputTypeDef,
    CreateServiceTemplateInputTypeDef,
    CreateServiceTemplateOutputTypeDef,
    CreateServiceTemplateVersionInputTypeDef,
    CreateServiceTemplateVersionOutputTypeDef,
    CreateTemplateSyncConfigInputTypeDef,
    CreateTemplateSyncConfigOutputTypeDef,
    DeleteComponentInputTypeDef,
    DeleteComponentOutputTypeDef,
    DeleteDeploymentInputTypeDef,
    DeleteDeploymentOutputTypeDef,
    DeleteEnvironmentAccountConnectionInputTypeDef,
    DeleteEnvironmentAccountConnectionOutputTypeDef,
    DeleteEnvironmentInputTypeDef,
    DeleteEnvironmentOutputTypeDef,
    DeleteEnvironmentTemplateInputTypeDef,
    DeleteEnvironmentTemplateOutputTypeDef,
    DeleteEnvironmentTemplateVersionInputTypeDef,
    DeleteEnvironmentTemplateVersionOutputTypeDef,
    DeleteRepositoryInputTypeDef,
    DeleteRepositoryOutputTypeDef,
    DeleteServiceInputTypeDef,
    DeleteServiceOutputTypeDef,
    DeleteServiceSyncConfigInputTypeDef,
    DeleteServiceSyncConfigOutputTypeDef,
    DeleteServiceTemplateInputTypeDef,
    DeleteServiceTemplateOutputTypeDef,
    DeleteServiceTemplateVersionInputTypeDef,
    DeleteServiceTemplateVersionOutputTypeDef,
    DeleteTemplateSyncConfigInputTypeDef,
    DeleteTemplateSyncConfigOutputTypeDef,
    GetAccountSettingsOutputTypeDef,
    GetComponentInputTypeDef,
    GetComponentOutputTypeDef,
    GetDeploymentInputTypeDef,
    GetDeploymentOutputTypeDef,
    GetEnvironmentAccountConnectionInputTypeDef,
    GetEnvironmentAccountConnectionOutputTypeDef,
    GetEnvironmentInputTypeDef,
    GetEnvironmentOutputTypeDef,
    GetEnvironmentTemplateInputTypeDef,
    GetEnvironmentTemplateOutputTypeDef,
    GetEnvironmentTemplateVersionInputTypeDef,
    GetEnvironmentTemplateVersionOutputTypeDef,
    GetRepositoryInputTypeDef,
    GetRepositoryOutputTypeDef,
    GetRepositorySyncStatusInputTypeDef,
    GetRepositorySyncStatusOutputTypeDef,
    GetResourcesSummaryOutputTypeDef,
    GetServiceInputTypeDef,
    GetServiceInstanceInputTypeDef,
    GetServiceInstanceOutputTypeDef,
    GetServiceInstanceSyncStatusInputTypeDef,
    GetServiceInstanceSyncStatusOutputTypeDef,
    GetServiceOutputTypeDef,
    GetServiceSyncBlockerSummaryInputTypeDef,
    GetServiceSyncBlockerSummaryOutputTypeDef,
    GetServiceSyncConfigInputTypeDef,
    GetServiceSyncConfigOutputTypeDef,
    GetServiceTemplateInputTypeDef,
    GetServiceTemplateOutputTypeDef,
    GetServiceTemplateVersionInputTypeDef,
    GetServiceTemplateVersionOutputTypeDef,
    GetTemplateSyncConfigInputTypeDef,
    GetTemplateSyncConfigOutputTypeDef,
    GetTemplateSyncStatusInputTypeDef,
    GetTemplateSyncStatusOutputTypeDef,
    ListComponentOutputsInputTypeDef,
    ListComponentOutputsOutputTypeDef,
    ListComponentProvisionedResourcesInputTypeDef,
    ListComponentProvisionedResourcesOutputTypeDef,
    ListComponentsInputTypeDef,
    ListComponentsOutputTypeDef,
    ListDeploymentsInputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListEnvironmentAccountConnectionsInputTypeDef,
    ListEnvironmentAccountConnectionsOutputTypeDef,
    ListEnvironmentOutputsInputTypeDef,
    ListEnvironmentOutputsOutputTypeDef,
    ListEnvironmentProvisionedResourcesInputTypeDef,
    ListEnvironmentProvisionedResourcesOutputTypeDef,
    ListEnvironmentsInputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListEnvironmentTemplatesInputTypeDef,
    ListEnvironmentTemplatesOutputTypeDef,
    ListEnvironmentTemplateVersionsInputTypeDef,
    ListEnvironmentTemplateVersionsOutputTypeDef,
    ListRepositoriesInputTypeDef,
    ListRepositoriesOutputTypeDef,
    ListRepositorySyncDefinitionsInputTypeDef,
    ListRepositorySyncDefinitionsOutputTypeDef,
    ListServiceInstanceOutputsInputTypeDef,
    ListServiceInstanceOutputsOutputTypeDef,
    ListServiceInstanceProvisionedResourcesInputTypeDef,
    ListServiceInstanceProvisionedResourcesOutputTypeDef,
    ListServiceInstancesInputTypeDef,
    ListServiceInstancesOutputTypeDef,
    ListServicePipelineOutputsInputTypeDef,
    ListServicePipelineOutputsOutputTypeDef,
    ListServicePipelineProvisionedResourcesInputTypeDef,
    ListServicePipelineProvisionedResourcesOutputTypeDef,
    ListServicesInputTypeDef,
    ListServicesOutputTypeDef,
    ListServiceTemplatesInputTypeDef,
    ListServiceTemplatesOutputTypeDef,
    ListServiceTemplateVersionsInputTypeDef,
    ListServiceTemplateVersionsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    NotifyResourceDeploymentStatusChangeInputTypeDef,
    RejectEnvironmentAccountConnectionInputTypeDef,
    RejectEnvironmentAccountConnectionOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateAccountSettingsInputTypeDef,
    UpdateAccountSettingsOutputTypeDef,
    UpdateComponentInputTypeDef,
    UpdateComponentOutputTypeDef,
    UpdateEnvironmentAccountConnectionInputTypeDef,
    UpdateEnvironmentAccountConnectionOutputTypeDef,
    UpdateEnvironmentInputTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateEnvironmentTemplateInputTypeDef,
    UpdateEnvironmentTemplateOutputTypeDef,
    UpdateEnvironmentTemplateVersionInputTypeDef,
    UpdateEnvironmentTemplateVersionOutputTypeDef,
    UpdateServiceInputTypeDef,
    UpdateServiceInstanceInputTypeDef,
    UpdateServiceInstanceOutputTypeDef,
    UpdateServiceOutputTypeDef,
    UpdateServicePipelineInputTypeDef,
    UpdateServicePipelineOutputTypeDef,
    UpdateServiceSyncBlockerInputTypeDef,
    UpdateServiceSyncBlockerOutputTypeDef,
    UpdateServiceSyncConfigInputTypeDef,
    UpdateServiceSyncConfigOutputTypeDef,
    UpdateServiceTemplateInputTypeDef,
    UpdateServiceTemplateOutputTypeDef,
    UpdateServiceTemplateVersionInputTypeDef,
    UpdateServiceTemplateVersionOutputTypeDef,
    UpdateTemplateSyncConfigInputTypeDef,
    UpdateTemplateSyncConfigOutputTypeDef,
)
from .waiter import (
    ComponentDeletedWaiter,
    ComponentDeployedWaiter,
    EnvironmentDeployedWaiter,
    EnvironmentTemplateVersionRegisteredWaiter,
    ServiceCreatedWaiter,
    ServiceDeletedWaiter,
    ServiceInstanceDeployedWaiter,
    ServicePipelineDeployedWaiter,
    ServiceTemplateVersionRegisteredWaiter,
    ServiceUpdatedWaiter,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("ProtonClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ProtonClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ProtonClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#generate_presigned_url)
        """

    async def accept_environment_account_connection(
        self, **kwargs: Unpack[AcceptEnvironmentAccountConnectionInputTypeDef]
    ) -> AcceptEnvironmentAccountConnectionOutputTypeDef:
        """
        In a management account, an environment account connection request is accepted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/accept_environment_account_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#accept_environment_account_connection)
        """

    async def cancel_component_deployment(
        self, **kwargs: Unpack[CancelComponentDeploymentInputTypeDef]
    ) -> CancelComponentDeploymentOutputTypeDef:
        """
        Attempts to cancel a component deployment (for a component that is in the
        <code>IN_PROGRESS</code> deployment status).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_component_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_component_deployment)
        """

    async def cancel_environment_deployment(
        self, **kwargs: Unpack[CancelEnvironmentDeploymentInputTypeDef]
    ) -> CancelEnvironmentDeploymentOutputTypeDef:
        """
        Attempts to cancel an environment deployment on an <a>UpdateEnvironment</a>
        action, if the deployment is <code>IN_PROGRESS</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_environment_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_environment_deployment)
        """

    async def cancel_service_instance_deployment(
        self, **kwargs: Unpack[CancelServiceInstanceDeploymentInputTypeDef]
    ) -> CancelServiceInstanceDeploymentOutputTypeDef:
        """
        Attempts to cancel a service instance deployment on an
        <a>UpdateServiceInstance</a> action, if the deployment is
        <code>IN_PROGRESS</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_service_instance_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_service_instance_deployment)
        """

    async def cancel_service_pipeline_deployment(
        self, **kwargs: Unpack[CancelServicePipelineDeploymentInputTypeDef]
    ) -> CancelServicePipelineDeploymentOutputTypeDef:
        """
        Attempts to cancel a service pipeline deployment on an
        <a>UpdateServicePipeline</a> action, if the deployment is
        <code>IN_PROGRESS</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/cancel_service_pipeline_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#cancel_service_pipeline_deployment)
        """

    async def create_component(
        self, **kwargs: Unpack[CreateComponentInputTypeDef]
    ) -> CreateComponentOutputTypeDef:
        """
        Create an Proton component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_component)
        """

    async def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentInputTypeDef]
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Deploy a new environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment)
        """

    async def create_environment_account_connection(
        self, **kwargs: Unpack[CreateEnvironmentAccountConnectionInputTypeDef]
    ) -> CreateEnvironmentAccountConnectionOutputTypeDef:
        """
        Create an environment account connection in an environment account so that
        environment infrastructure resources can be provisioned in the environment
        account from a management account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment_account_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment_account_connection)
        """

    async def create_environment_template(
        self, **kwargs: Unpack[CreateEnvironmentTemplateInputTypeDef]
    ) -> CreateEnvironmentTemplateOutputTypeDef:
        """
        Create an environment template for Proton.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment_template)
        """

    async def create_environment_template_version(
        self, **kwargs: Unpack[CreateEnvironmentTemplateVersionInputTypeDef]
    ) -> CreateEnvironmentTemplateVersionOutputTypeDef:
        """
        Create a new major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_environment_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_environment_template_version)
        """

    async def create_repository(
        self, **kwargs: Unpack[CreateRepositoryInputTypeDef]
    ) -> CreateRepositoryOutputTypeDef:
        """
        Create and register a link to a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_repository.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_repository)
        """

    async def create_service(
        self, **kwargs: Unpack[CreateServiceInputTypeDef]
    ) -> CreateServiceOutputTypeDef:
        """
        Create an Proton service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service)
        """

    async def create_service_instance(
        self, **kwargs: Unpack[CreateServiceInstanceInputTypeDef]
    ) -> CreateServiceInstanceOutputTypeDef:
        """
        Create a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service_instance)
        """

    async def create_service_sync_config(
        self, **kwargs: Unpack[CreateServiceSyncConfigInputTypeDef]
    ) -> CreateServiceSyncConfigOutputTypeDef:
        """
        Create the Proton Ops configuration file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service_sync_config)
        """

    async def create_service_template(
        self, **kwargs: Unpack[CreateServiceTemplateInputTypeDef]
    ) -> CreateServiceTemplateOutputTypeDef:
        """
        Create a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service_template)
        """

    async def create_service_template_version(
        self, **kwargs: Unpack[CreateServiceTemplateVersionInputTypeDef]
    ) -> CreateServiceTemplateVersionOutputTypeDef:
        """
        Create a new major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_service_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_service_template_version)
        """

    async def create_template_sync_config(
        self, **kwargs: Unpack[CreateTemplateSyncConfigInputTypeDef]
    ) -> CreateTemplateSyncConfigOutputTypeDef:
        """
        Set up a template to create new template versions automatically by tracking a
        linked repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/create_template_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#create_template_sync_config)
        """

    async def delete_component(
        self, **kwargs: Unpack[DeleteComponentInputTypeDef]
    ) -> DeleteComponentOutputTypeDef:
        """
        Delete an Proton component resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_component)
        """

    async def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentInputTypeDef]
    ) -> DeleteDeploymentOutputTypeDef:
        """
        Delete the deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_deployment)
        """

    async def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentInputTypeDef]
    ) -> DeleteEnvironmentOutputTypeDef:
        """
        Delete an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment)
        """

    async def delete_environment_account_connection(
        self, **kwargs: Unpack[DeleteEnvironmentAccountConnectionInputTypeDef]
    ) -> DeleteEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, delete an environment account connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment_account_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment_account_connection)
        """

    async def delete_environment_template(
        self, **kwargs: Unpack[DeleteEnvironmentTemplateInputTypeDef]
    ) -> DeleteEnvironmentTemplateOutputTypeDef:
        """
        If no other major or minor versions of an environment template exist, delete
        the environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment_template)
        """

    async def delete_environment_template_version(
        self, **kwargs: Unpack[DeleteEnvironmentTemplateVersionInputTypeDef]
    ) -> DeleteEnvironmentTemplateVersionOutputTypeDef:
        """
        If no other minor versions of an environment template exist, delete a major
        version of the environment template if it's not the <code>Recommended</code>
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_environment_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_environment_template_version)
        """

    async def delete_repository(
        self, **kwargs: Unpack[DeleteRepositoryInputTypeDef]
    ) -> DeleteRepositoryOutputTypeDef:
        """
        De-register and unlink your repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_repository.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_repository)
        """

    async def delete_service(
        self, **kwargs: Unpack[DeleteServiceInputTypeDef]
    ) -> DeleteServiceOutputTypeDef:
        """
        Delete a service, with its instances and pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service)
        """

    async def delete_service_sync_config(
        self, **kwargs: Unpack[DeleteServiceSyncConfigInputTypeDef]
    ) -> DeleteServiceSyncConfigOutputTypeDef:
        """
        Delete the Proton Ops file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service_sync_config)
        """

    async def delete_service_template(
        self, **kwargs: Unpack[DeleteServiceTemplateInputTypeDef]
    ) -> DeleteServiceTemplateOutputTypeDef:
        """
        If no other major or minor versions of the service template exist, delete the
        service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service_template)
        """

    async def delete_service_template_version(
        self, **kwargs: Unpack[DeleteServiceTemplateVersionInputTypeDef]
    ) -> DeleteServiceTemplateVersionOutputTypeDef:
        """
        If no other minor versions of a service template exist, delete a major version
        of the service template if it's not the <code>Recommended</code> version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_service_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_service_template_version)
        """

    async def delete_template_sync_config(
        self, **kwargs: Unpack[DeleteTemplateSyncConfigInputTypeDef]
    ) -> DeleteTemplateSyncConfigOutputTypeDef:
        """
        Delete a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/delete_template_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#delete_template_sync_config)
        """

    async def get_account_settings(self) -> GetAccountSettingsOutputTypeDef:
        """
        Get detail data for Proton account-wide settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_account_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_account_settings)
        """

    async def get_component(
        self, **kwargs: Unpack[GetComponentInputTypeDef]
    ) -> GetComponentOutputTypeDef:
        """
        Get detailed data for a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_component)
        """

    async def get_deployment(
        self, **kwargs: Unpack[GetDeploymentInputTypeDef]
    ) -> GetDeploymentOutputTypeDef:
        """
        Get detailed data for a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_deployment)
        """

    async def get_environment(
        self, **kwargs: Unpack[GetEnvironmentInputTypeDef]
    ) -> GetEnvironmentOutputTypeDef:
        """
        Get detailed data for an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment)
        """

    async def get_environment_account_connection(
        self, **kwargs: Unpack[GetEnvironmentAccountConnectionInputTypeDef]
    ) -> GetEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, get the detailed data for an environment account
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment_account_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment_account_connection)
        """

    async def get_environment_template(
        self, **kwargs: Unpack[GetEnvironmentTemplateInputTypeDef]
    ) -> GetEnvironmentTemplateOutputTypeDef:
        """
        Get detailed data for an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment_template)
        """

    async def get_environment_template_version(
        self, **kwargs: Unpack[GetEnvironmentTemplateVersionInputTypeDef]
    ) -> GetEnvironmentTemplateVersionOutputTypeDef:
        """
        Get detailed data for a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_environment_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_environment_template_version)
        """

    async def get_repository(
        self, **kwargs: Unpack[GetRepositoryInputTypeDef]
    ) -> GetRepositoryOutputTypeDef:
        """
        Get detail data for a linked repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_repository.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_repository)
        """

    async def get_repository_sync_status(
        self, **kwargs: Unpack[GetRepositorySyncStatusInputTypeDef]
    ) -> GetRepositorySyncStatusOutputTypeDef:
        """
        Get the sync status of a repository used for Proton template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_repository_sync_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_repository_sync_status)
        """

    async def get_resources_summary(self) -> GetResourcesSummaryOutputTypeDef:
        """
        Get counts of Proton resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_resources_summary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_resources_summary)
        """

    async def get_service(
        self, **kwargs: Unpack[GetServiceInputTypeDef]
    ) -> GetServiceOutputTypeDef:
        """
        Get detailed data for a service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service)
        """

    async def get_service_instance(
        self, **kwargs: Unpack[GetServiceInstanceInputTypeDef]
    ) -> GetServiceInstanceOutputTypeDef:
        """
        Get detailed data for a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_instance)
        """

    async def get_service_instance_sync_status(
        self, **kwargs: Unpack[GetServiceInstanceSyncStatusInputTypeDef]
    ) -> GetServiceInstanceSyncStatusOutputTypeDef:
        """
        Get the status of the synced service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_instance_sync_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_instance_sync_status)
        """

    async def get_service_sync_blocker_summary(
        self, **kwargs: Unpack[GetServiceSyncBlockerSummaryInputTypeDef]
    ) -> GetServiceSyncBlockerSummaryOutputTypeDef:
        """
        Get detailed data for the service sync blocker summary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_sync_blocker_summary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_sync_blocker_summary)
        """

    async def get_service_sync_config(
        self, **kwargs: Unpack[GetServiceSyncConfigInputTypeDef]
    ) -> GetServiceSyncConfigOutputTypeDef:
        """
        Get detailed information for the service sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_sync_config)
        """

    async def get_service_template(
        self, **kwargs: Unpack[GetServiceTemplateInputTypeDef]
    ) -> GetServiceTemplateOutputTypeDef:
        """
        Get detailed data for a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_template)
        """

    async def get_service_template_version(
        self, **kwargs: Unpack[GetServiceTemplateVersionInputTypeDef]
    ) -> GetServiceTemplateVersionOutputTypeDef:
        """
        Get detailed data for a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_service_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_service_template_version)
        """

    async def get_template_sync_config(
        self, **kwargs: Unpack[GetTemplateSyncConfigInputTypeDef]
    ) -> GetTemplateSyncConfigOutputTypeDef:
        """
        Get detail data for a template sync configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_template_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_template_sync_config)
        """

    async def get_template_sync_status(
        self, **kwargs: Unpack[GetTemplateSyncStatusInputTypeDef]
    ) -> GetTemplateSyncStatusOutputTypeDef:
        """
        Get the status of a template sync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_template_sync_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_template_sync_status)
        """

    async def list_component_outputs(
        self, **kwargs: Unpack[ListComponentOutputsInputTypeDef]
    ) -> ListComponentOutputsOutputTypeDef:
        """
        Get a list of component Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_component_outputs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_component_outputs)
        """

    async def list_component_provisioned_resources(
        self, **kwargs: Unpack[ListComponentProvisionedResourcesInputTypeDef]
    ) -> ListComponentProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a component with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_component_provisioned_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_component_provisioned_resources)
        """

    async def list_components(
        self, **kwargs: Unpack[ListComponentsInputTypeDef]
    ) -> ListComponentsOutputTypeDef:
        """
        List components with summary data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_components.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_components)
        """

    async def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsInputTypeDef]
    ) -> ListDeploymentsOutputTypeDef:
        """
        List deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_deployments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_deployments)
        """

    async def list_environment_account_connections(
        self, **kwargs: Unpack[ListEnvironmentAccountConnectionsInputTypeDef]
    ) -> ListEnvironmentAccountConnectionsOutputTypeDef:
        """
        View a list of environment account connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_account_connections.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_account_connections)
        """

    async def list_environment_outputs(
        self, **kwargs: Unpack[ListEnvironmentOutputsInputTypeDef]
    ) -> ListEnvironmentOutputsOutputTypeDef:
        """
        List the infrastructure as code outputs for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_outputs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_outputs)
        """

    async def list_environment_provisioned_resources(
        self, **kwargs: Unpack[ListEnvironmentProvisionedResourcesInputTypeDef]
    ) -> ListEnvironmentProvisionedResourcesOutputTypeDef:
        """
        List the provisioned resources for your environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_provisioned_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_provisioned_resources)
        """

    async def list_environment_template_versions(
        self, **kwargs: Unpack[ListEnvironmentTemplateVersionsInputTypeDef]
    ) -> ListEnvironmentTemplateVersionsOutputTypeDef:
        """
        List major or minor versions of an environment template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_template_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_template_versions)
        """

    async def list_environment_templates(
        self, **kwargs: Unpack[ListEnvironmentTemplatesInputTypeDef]
    ) -> ListEnvironmentTemplatesOutputTypeDef:
        """
        List environment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environment_templates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environment_templates)
        """

    async def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsInputTypeDef]
    ) -> ListEnvironmentsOutputTypeDef:
        """
        List environments with detail data summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_environments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_environments)
        """

    async def list_repositories(
        self, **kwargs: Unpack[ListRepositoriesInputTypeDef]
    ) -> ListRepositoriesOutputTypeDef:
        """
        List linked repositories with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_repositories.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_repositories)
        """

    async def list_repository_sync_definitions(
        self, **kwargs: Unpack[ListRepositorySyncDefinitionsInputTypeDef]
    ) -> ListRepositorySyncDefinitionsOutputTypeDef:
        """
        List repository sync definitions with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_repository_sync_definitions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_repository_sync_definitions)
        """

    async def list_service_instance_outputs(
        self, **kwargs: Unpack[ListServiceInstanceOutputsInputTypeDef]
    ) -> ListServiceInstanceOutputsOutputTypeDef:
        """
        Get a list service of instance Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_instance_outputs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_instance_outputs)
        """

    async def list_service_instance_provisioned_resources(
        self, **kwargs: Unpack[ListServiceInstanceProvisionedResourcesInputTypeDef]
    ) -> ListServiceInstanceProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a service instance with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_instance_provisioned_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_instance_provisioned_resources)
        """

    async def list_service_instances(
        self, **kwargs: Unpack[ListServiceInstancesInputTypeDef]
    ) -> ListServiceInstancesOutputTypeDef:
        """
        List service instances with summary data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_instances.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_instances)
        """

    async def list_service_pipeline_outputs(
        self, **kwargs: Unpack[ListServicePipelineOutputsInputTypeDef]
    ) -> ListServicePipelineOutputsOutputTypeDef:
        """
        Get a list of service pipeline Infrastructure as Code (IaC) outputs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_pipeline_outputs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_pipeline_outputs)
        """

    async def list_service_pipeline_provisioned_resources(
        self, **kwargs: Unpack[ListServicePipelineProvisionedResourcesInputTypeDef]
    ) -> ListServicePipelineProvisionedResourcesOutputTypeDef:
        """
        List provisioned resources for a service and pipeline with details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_pipeline_provisioned_resources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_pipeline_provisioned_resources)
        """

    async def list_service_template_versions(
        self, **kwargs: Unpack[ListServiceTemplateVersionsInputTypeDef]
    ) -> ListServiceTemplateVersionsOutputTypeDef:
        """
        List major or minor versions of a service template with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_template_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_template_versions)
        """

    async def list_service_templates(
        self, **kwargs: Unpack[ListServiceTemplatesInputTypeDef]
    ) -> ListServiceTemplatesOutputTypeDef:
        """
        List service templates with detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_service_templates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_service_templates)
        """

    async def list_services(
        self, **kwargs: Unpack[ListServicesInputTypeDef]
    ) -> ListServicesOutputTypeDef:
        """
        List services with summaries of detail data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_services.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_services)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#list_tags_for_resource)
        """

    async def notify_resource_deployment_status_change(
        self, **kwargs: Unpack[NotifyResourceDeploymentStatusChangeInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Notify Proton of status changes to a provisioned resource when you use
        self-managed provisioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/notify_resource_deployment_status_change.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#notify_resource_deployment_status_change)
        """

    async def reject_environment_account_connection(
        self, **kwargs: Unpack[RejectEnvironmentAccountConnectionInputTypeDef]
    ) -> RejectEnvironmentAccountConnectionOutputTypeDef:
        """
        In a management account, reject an environment account connection from another
        environment account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/reject_environment_account_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#reject_environment_account_connection)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Tag a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Remove a customer tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#untag_resource)
        """

    async def update_account_settings(
        self, **kwargs: Unpack[UpdateAccountSettingsInputTypeDef]
    ) -> UpdateAccountSettingsOutputTypeDef:
        """
        Update Proton settings that are used for multiple services in the Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_account_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_account_settings)
        """

    async def update_component(
        self, **kwargs: Unpack[UpdateComponentInputTypeDef]
    ) -> UpdateComponentOutputTypeDef:
        """
        Update a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_component)
        """

    async def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentInputTypeDef]
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Update an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment)
        """

    async def update_environment_account_connection(
        self, **kwargs: Unpack[UpdateEnvironmentAccountConnectionInputTypeDef]
    ) -> UpdateEnvironmentAccountConnectionOutputTypeDef:
        """
        In an environment account, update an environment account connection to use a
        new IAM role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment_account_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment_account_connection)
        """

    async def update_environment_template(
        self, **kwargs: Unpack[UpdateEnvironmentTemplateInputTypeDef]
    ) -> UpdateEnvironmentTemplateOutputTypeDef:
        """
        Update an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment_template)
        """

    async def update_environment_template_version(
        self, **kwargs: Unpack[UpdateEnvironmentTemplateVersionInputTypeDef]
    ) -> UpdateEnvironmentTemplateVersionOutputTypeDef:
        """
        Update a major or minor version of an environment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_environment_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_environment_template_version)
        """

    async def update_service(
        self, **kwargs: Unpack[UpdateServiceInputTypeDef]
    ) -> UpdateServiceOutputTypeDef:
        """
        Edit a service description or use a spec to add and delete service instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service)
        """

    async def update_service_instance(
        self, **kwargs: Unpack[UpdateServiceInstanceInputTypeDef]
    ) -> UpdateServiceInstanceOutputTypeDef:
        """
        Update a service instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_instance.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_instance)
        """

    async def update_service_pipeline(
        self, **kwargs: Unpack[UpdateServicePipelineInputTypeDef]
    ) -> UpdateServicePipelineOutputTypeDef:
        """
        Update the service pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_pipeline.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_pipeline)
        """

    async def update_service_sync_blocker(
        self, **kwargs: Unpack[UpdateServiceSyncBlockerInputTypeDef]
    ) -> UpdateServiceSyncBlockerOutputTypeDef:
        """
        Update the service sync blocker by resolving it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_sync_blocker.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_sync_blocker)
        """

    async def update_service_sync_config(
        self, **kwargs: Unpack[UpdateServiceSyncConfigInputTypeDef]
    ) -> UpdateServiceSyncConfigOutputTypeDef:
        """
        Update the Proton Ops config file.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_sync_config)
        """

    async def update_service_template(
        self, **kwargs: Unpack[UpdateServiceTemplateInputTypeDef]
    ) -> UpdateServiceTemplateOutputTypeDef:
        """
        Update a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_template.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_template)
        """

    async def update_service_template_version(
        self, **kwargs: Unpack[UpdateServiceTemplateVersionInputTypeDef]
    ) -> UpdateServiceTemplateVersionOutputTypeDef:
        """
        Update a major or minor version of a service template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_service_template_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_service_template_version)
        """

    async def update_template_sync_config(
        self, **kwargs: Unpack[UpdateTemplateSyncConfigInputTypeDef]
    ) -> UpdateTemplateSyncConfigOutputTypeDef:
        """
        Update template sync configuration parameters, except for the
        <code>templateName</code> and <code>templateType</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/update_template_sync_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#update_template_sync_config)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_component_outputs"]
    ) -> ListComponentOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_component_provisioned_resources"]
    ) -> ListComponentProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_components"]
    ) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environment_account_connections"]
    ) -> ListEnvironmentAccountConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environment_outputs"]
    ) -> ListEnvironmentOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environment_provisioned_resources"]
    ) -> ListEnvironmentProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environment_template_versions"]
    ) -> ListEnvironmentTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environment_templates"]
    ) -> ListEnvironmentTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_repositories"]
    ) -> ListRepositoriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_repository_sync_definitions"]
    ) -> ListRepositorySyncDefinitionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_instance_outputs"]
    ) -> ListServiceInstanceOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_instance_provisioned_resources"]
    ) -> ListServiceInstanceProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_instances"]
    ) -> ListServiceInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_pipeline_outputs"]
    ) -> ListServicePipelineOutputsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_pipeline_provisioned_resources"]
    ) -> ListServicePipelineProvisionedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_template_versions"]
    ) -> ListServiceTemplateVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_service_templates"]
    ) -> ListServiceTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_services"]
    ) -> ListServicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["component_deleted"]
    ) -> ComponentDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["component_deployed"]
    ) -> ComponentDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["environment_deployed"]
    ) -> EnvironmentDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["environment_template_version_registered"]
    ) -> EnvironmentTemplateVersionRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_created"]
    ) -> ServiceCreatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_deleted"]
    ) -> ServiceDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_instance_deployed"]
    ) -> ServiceInstanceDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_pipeline_deployed"]
    ) -> ServicePipelineDeployedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_template_version_registered"]
    ) -> ServiceTemplateVersionRegisteredWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["service_updated"]
    ) -> ServiceUpdatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton.html#Proton.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/client/)
        """
