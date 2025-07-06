"""
Type annotations for proton service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_proton.client import ProtonClient
    from types_aiobotocore_proton.waiter import (
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

    session = get_session()
    async with session.create_client("proton") as client:
        client: ProtonClient

        component_deleted_waiter: ComponentDeletedWaiter = client.get_waiter("component_deleted")
        component_deployed_waiter: ComponentDeployedWaiter = client.get_waiter("component_deployed")
        environment_deployed_waiter: EnvironmentDeployedWaiter = client.get_waiter("environment_deployed")
        environment_template_version_registered_waiter: EnvironmentTemplateVersionRegisteredWaiter = client.get_waiter("environment_template_version_registered")
        service_created_waiter: ServiceCreatedWaiter = client.get_waiter("service_created")
        service_deleted_waiter: ServiceDeletedWaiter = client.get_waiter("service_deleted")
        service_instance_deployed_waiter: ServiceInstanceDeployedWaiter = client.get_waiter("service_instance_deployed")
        service_pipeline_deployed_waiter: ServicePipelineDeployedWaiter = client.get_waiter("service_pipeline_deployed")
        service_template_version_registered_waiter: ServiceTemplateVersionRegisteredWaiter = client.get_waiter("service_template_version_registered")
        service_updated_waiter: ServiceUpdatedWaiter = client.get_waiter("service_updated")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetComponentInputWaitExtraTypeDef,
    GetComponentInputWaitTypeDef,
    GetEnvironmentInputWaitTypeDef,
    GetEnvironmentTemplateVersionInputWaitTypeDef,
    GetServiceInputWaitExtraExtraExtraTypeDef,
    GetServiceInputWaitExtraExtraTypeDef,
    GetServiceInputWaitExtraTypeDef,
    GetServiceInputWaitTypeDef,
    GetServiceInstanceInputWaitTypeDef,
    GetServiceTemplateVersionInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ComponentDeletedWaiter",
    "ComponentDeployedWaiter",
    "EnvironmentDeployedWaiter",
    "EnvironmentTemplateVersionRegisteredWaiter",
    "ServiceCreatedWaiter",
    "ServiceDeletedWaiter",
    "ServiceInstanceDeployedWaiter",
    "ServicePipelineDeployedWaiter",
    "ServiceTemplateVersionRegisteredWaiter",
    "ServiceUpdatedWaiter",
)

class ComponentDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeleted.html#Proton.Waiter.ComponentDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#componentdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetComponentInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeleted.html#Proton.Waiter.ComponentDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#componentdeletedwaiter)
        """

class ComponentDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeployed.html#Proton.Waiter.ComponentDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#componentdeployedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetComponentInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ComponentDeployed.html#Proton.Waiter.ComponentDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#componentdeployedwaiter)
        """

class EnvironmentDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentDeployed.html#Proton.Waiter.EnvironmentDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmentdeployedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetEnvironmentInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentDeployed.html#Proton.Waiter.EnvironmentDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmentdeployedwaiter)
        """

class EnvironmentTemplateVersionRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentTemplateVersionRegistered.html#Proton.Waiter.EnvironmentTemplateVersionRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmenttemplateversionregisteredwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetEnvironmentTemplateVersionInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/EnvironmentTemplateVersionRegistered.html#Proton.Waiter.EnvironmentTemplateVersionRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#environmenttemplateversionregisteredwaiter)
        """

class ServiceCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceCreated.html#Proton.Waiter.ServiceCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicecreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceCreated.html#Proton.Waiter.ServiceCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicecreatedwaiter)
        """

class ServiceDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceDeleted.html#Proton.Waiter.ServiceDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicedeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceDeleted.html#Proton.Waiter.ServiceDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicedeletedwaiter)
        """

class ServiceInstanceDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceInstanceDeployed.html#Proton.Waiter.ServiceInstanceDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceinstancedeployedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceInstanceInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceInstanceDeployed.html#Proton.Waiter.ServiceInstanceDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceinstancedeployedwaiter)
        """

class ServicePipelineDeployedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServicePipelineDeployed.html#Proton.Waiter.ServicePipelineDeployed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicepipelinedeployedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceInputWaitExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServicePipelineDeployed.html#Proton.Waiter.ServicePipelineDeployed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicepipelinedeployedwaiter)
        """

class ServiceTemplateVersionRegisteredWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceTemplateVersionRegistered.html#Proton.Waiter.ServiceTemplateVersionRegistered)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicetemplateversionregisteredwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceTemplateVersionInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceTemplateVersionRegistered.html#Proton.Waiter.ServiceTemplateVersionRegistered.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#servicetemplateversionregisteredwaiter)
        """

class ServiceUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceUpdated.html#Proton.Waiter.ServiceUpdated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceupdatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceInputWaitExtraExtraExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/proton/waiter/ServiceUpdated.html#Proton.Waiter.ServiceUpdated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_proton/waiters/#serviceupdatedwaiter)
        """
