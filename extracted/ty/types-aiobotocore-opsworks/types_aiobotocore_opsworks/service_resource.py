"""
Type annotations for opsworks service ServiceResource.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_opsworks.service_resource import OpsWorksServiceResource
    import types_aiobotocore_opsworks.service_resource as opsworks_resources

    session = get_session()
    async with session.resource("opsworks") as resource:
        resource: OpsWorksServiceResource

        my_layer: opsworks_resources.Layer = resource.Layer(...)
        my_stack: opsworks_resources.Stack = resource.Stack(...)
        my_stack_summary: opsworks_resources.StackSummary = resource.StackSummary(...)
```
"""

from __future__ import annotations

import sys
from typing import NoReturn

from aioboto3.resources.base import AIOBoto3ServiceResource
from aioboto3.resources.collection import AIOResourceCollection

from .client import OpsWorksClient
from .literals import LayerAttributesKeysType, LayerTypeType, RootDeviceTypeType
from .type_defs import (
    ChefConfigurationTypeDef,
    CloudWatchLogsConfigurationOutputTypeDef,
    CreateLayerRequestStackCreateLayerTypeDef,
    CreateStackRequestServiceResourceCreateStackTypeDef,
    InstancesCountTypeDef,
    LifecycleEventConfigurationTypeDef,
    RecipesOutputTypeDef,
    SourceTypeDef,
    StackConfigurationManagerTypeDef,
    VolumeConfigurationTypeDef,
)

try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta  # type: ignore[assignment]
if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import AsyncIterator, Awaitable, Sequence
else:
    from typing import AsyncIterator, Awaitable, Dict, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = (
    "Layer",
    "OpsWorksServiceResource",
    "ServiceResourceStacksCollection",
    "Stack",
    "StackLayersCollection",
    "StackSummary",
)


class ServiceResourceStacksCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#OpsWorks.ServiceResource.stacks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
    """

    def all(self) -> ServiceResourceStacksCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#OpsWorks.ServiceResource.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def filter(  # type: ignore[override]
        self, *, StackIds: Sequence[str] = ...
    ) -> ServiceResourceStacksCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def limit(self, count: int) -> ServiceResourceStacksCollection:
        """
        Return at most this many Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def page_size(self, count: int) -> ServiceResourceStacksCollection:
        """
        Fetch at most this many Stacks per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Stack]]:
        """
        A generator which yields pages of Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """

    def __aiter__(self) -> AsyncIterator[Stack]:
        """
        A generator which yields Stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/stacks.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#serviceresourcestackscollection)
        """


class StackLayersCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#OpsWorks.Stack.layers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
    """

    def all(self) -> StackLayersCollection:
        """
        Get all items from the collection, optionally with a custom page size and item
        count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#OpsWorks.Stack.all)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """

    def filter(  # type: ignore[override]
        self, *, StackId: str = ..., LayerIds: Sequence[str] = ...
    ) -> StackLayersCollection:
        """
        Get items from the collection, passing keyword arguments along as parameters to
        the underlying service operation, which are typically used to filter the
        results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#filter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """

    def limit(self, count: int) -> StackLayersCollection:
        """
        Return at most this many Layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """

    def page_size(self, count: int) -> StackLayersCollection:
        """
        Fetch at most this many Layers per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#page_size)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """

    def pages(  # type: ignore[override]
        self,
    ) -> AsyncIterator[List[Layer]]:
        """
        A generator which yields pages of Layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#pages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """

    def __aiter__(self) -> AsyncIterator[Layer]:
        """
        A generator which yields Layers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/layers.html#__iter__)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacklayers)
        """


class Layer(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/layer/index.html#OpsWorks.Layer)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#layer)
    """

    id: str
    stack: Stack
    arn: Awaitable[str]
    stack_id: Awaitable[str]
    layer_id: Awaitable[str]
    type: Awaitable[LayerTypeType]
    name: Awaitable[str]
    shortname: Awaitable[str]
    attributes: Awaitable[Dict[LayerAttributesKeysType, str]]
    cloud_watch_logs_configuration: Awaitable[CloudWatchLogsConfigurationOutputTypeDef]
    custom_instance_profile_arn: Awaitable[str]
    custom_json: Awaitable[str]
    custom_security_group_ids: Awaitable[List[str]]
    default_security_group_names: Awaitable[List[str]]
    packages: Awaitable[List[str]]
    volume_configurations: Awaitable[List[VolumeConfigurationTypeDef]]
    enable_auto_healing: Awaitable[bool]
    auto_assign_elastic_ips: Awaitable[bool]
    auto_assign_public_ips: Awaitable[bool]
    default_recipes: Awaitable[RecipesOutputTypeDef]
    custom_recipes: Awaitable[RecipesOutputTypeDef]
    created_at: Awaitable[str]
    install_updates_on_boot: Awaitable[bool]
    use_ebs_optimized_instances: Awaitable[bool]
    lifecycle_event_configuration: Awaitable[LifecycleEventConfigurationTypeDef]
    meta: OpsWorksResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/layer/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#layerget_available_subresources-method)
        """

    async def delete(self) -> None:
        """
        Deletes a specified layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/layer/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#layerdelete-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/layer/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#layerload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/layer/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#layerreload-method)
        """


_Layer = Layer


class Stack(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/index.html#OpsWorks.Stack)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stack)
    """

    id: str
    layers: StackLayersCollection
    stack_id: Awaitable[str]
    name: Awaitable[str]
    arn: Awaitable[str]
    region: Awaitable[str]
    vpc_id: Awaitable[str]
    attributes: Awaitable[Dict[Literal["Color"], str]]
    service_role_arn: Awaitable[str]
    default_instance_profile_arn: Awaitable[str]
    default_os: Awaitable[str]
    hostname_theme: Awaitable[str]
    default_availability_zone: Awaitable[str]
    default_subnet_id: Awaitable[str]
    custom_json: Awaitable[str]
    configuration_manager: Awaitable[StackConfigurationManagerTypeDef]
    chef_configuration: Awaitable[ChefConfigurationTypeDef]
    use_custom_cookbooks: Awaitable[bool]
    use_opsworks_security_groups: Awaitable[bool]
    custom_cookbooks_source: Awaitable[SourceTypeDef]
    default_ssh_key_name: Awaitable[str]
    created_at: Awaitable[str]
    default_root_device_type: Awaitable[RootDeviceTypeType]
    agent_version: Awaitable[str]
    meta: OpsWorksResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stackget_available_subresources-method)
        """

    async def create_layer(
        self, **kwargs: Unpack[CreateLayerRequestStackCreateLayerTypeDef]
    ) -> _Layer:
        """
        Creates a layer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/create_layer.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stackcreate_layer-method)
        """

    async def delete(self) -> None:
        """
        Deletes a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/delete.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stackdelete-method)
        """

    async def Summary(self) -> _StackSummary:
        """
        Creates a StackSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/Summary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacksummary-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stackload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stack/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stackreload-method)
        """


_Stack = Stack


class StackSummary(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stacksummary/index.html#OpsWorks.StackSummary)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacksummary)
    """

    stack_id: str
    name: Awaitable[str]
    arn: Awaitable[str]
    layers_count: Awaitable[int]
    apps_count: Awaitable[int]
    instances_count: Awaitable[InstancesCountTypeDef]
    meta: OpsWorksResourceMeta  # type: ignore[override]

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this StackSummary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stacksummary/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacksummaryget_available_subresources-method)
        """

    async def Stack(self) -> _Stack:
        """
        Creates a Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stacksummary/Stack.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacksummarystack-method)
        """

    async def load(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stacksummary/load.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacksummaryload-method)
        """

    async def reload(self) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/stacksummary/reload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#stacksummaryreload-method)
        """


_StackSummary = StackSummary


class OpsWorksResourceMeta(ResourceMeta):
    client: OpsWorksClient  # type: ignore[override]


class OpsWorksServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/index.html)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/)
    """

    meta: OpsWorksResourceMeta  # type: ignore[override]
    stacks: ServiceResourceStacksCollection

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/get_available_subresources.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#opsworksserviceresourceget_available_subresources-method)
        """

    async def create_stack(
        self, **kwargs: Unpack[CreateStackRequestServiceResourceCreateStackTypeDef]
    ) -> _Stack:
        """
        Creates a new stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/create_stack.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#opsworksserviceresourcecreate_stack-method)
        """

    async def Layer(self, id: str) -> _Layer:
        """
        Creates a Layer resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/Layer.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#opsworksserviceresourcelayer-method)
        """

    async def Stack(self, id: str) -> _Stack:
        """
        Creates a Stack resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/Stack.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#opsworksserviceresourcestack-method)
        """

    async def StackSummary(self, stack_id: str) -> _StackSummary:
        """
        Creates a StackSummary resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opsworks/service-resource/StackSummary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opsworks/service_resource/#opsworksserviceresourcestacksummary-method)
        """
