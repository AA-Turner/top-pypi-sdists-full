"""
Type annotations for iotthingsgraph service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotthingsgraph.client import IoTThingsGraphClient
    from types_aiobotocore_iotthingsgraph.paginator import (
        GetFlowTemplateRevisionsPaginator,
        GetSystemTemplateRevisionsPaginator,
        ListFlowExecutionMessagesPaginator,
        ListTagsForResourcePaginator,
        SearchEntitiesPaginator,
        SearchFlowExecutionsPaginator,
        SearchFlowTemplatesPaginator,
        SearchSystemInstancesPaginator,
        SearchSystemTemplatesPaginator,
        SearchThingsPaginator,
    )

    session = get_session()
    with session.create_client("iotthingsgraph") as client:
        client: IoTThingsGraphClient

        get_flow_template_revisions_paginator: GetFlowTemplateRevisionsPaginator = client.get_paginator("get_flow_template_revisions")
        get_system_template_revisions_paginator: GetSystemTemplateRevisionsPaginator = client.get_paginator("get_system_template_revisions")
        list_flow_execution_messages_paginator: ListFlowExecutionMessagesPaginator = client.get_paginator("list_flow_execution_messages")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        search_entities_paginator: SearchEntitiesPaginator = client.get_paginator("search_entities")
        search_flow_executions_paginator: SearchFlowExecutionsPaginator = client.get_paginator("search_flow_executions")
        search_flow_templates_paginator: SearchFlowTemplatesPaginator = client.get_paginator("search_flow_templates")
        search_system_instances_paginator: SearchSystemInstancesPaginator = client.get_paginator("search_system_instances")
        search_system_templates_paginator: SearchSystemTemplatesPaginator = client.get_paginator("search_system_templates")
        search_things_paginator: SearchThingsPaginator = client.get_paginator("search_things")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetFlowTemplateRevisionsRequestPaginateTypeDef,
    GetFlowTemplateRevisionsResponseTypeDef,
    GetSystemTemplateRevisionsRequestPaginateTypeDef,
    GetSystemTemplateRevisionsResponseTypeDef,
    ListFlowExecutionMessagesRequestPaginateTypeDef,
    ListFlowExecutionMessagesResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchEntitiesRequestPaginateTypeDef,
    SearchEntitiesResponseTypeDef,
    SearchFlowExecutionsRequestPaginateTypeDef,
    SearchFlowExecutionsResponseTypeDef,
    SearchFlowTemplatesRequestPaginateTypeDef,
    SearchFlowTemplatesResponseTypeDef,
    SearchSystemInstancesRequestPaginateTypeDef,
    SearchSystemInstancesResponseTypeDef,
    SearchSystemTemplatesRequestPaginateTypeDef,
    SearchSystemTemplatesResponseTypeDef,
    SearchThingsRequestPaginateTypeDef,
    SearchThingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetFlowTemplateRevisionsPaginator",
    "GetSystemTemplateRevisionsPaginator",
    "ListFlowExecutionMessagesPaginator",
    "ListTagsForResourcePaginator",
    "SearchEntitiesPaginator",
    "SearchFlowExecutionsPaginator",
    "SearchFlowTemplatesPaginator",
    "SearchSystemInstancesPaginator",
    "SearchSystemTemplatesPaginator",
    "SearchThingsPaginator",
)


if TYPE_CHECKING:
    _GetFlowTemplateRevisionsPaginatorBase = AioPaginator[GetFlowTemplateRevisionsResponseTypeDef]
else:
    _GetFlowTemplateRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetFlowTemplateRevisionsPaginator(_GetFlowTemplateRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetFlowTemplateRevisions.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getflowtemplaterevisionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetFlowTemplateRevisionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetFlowTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetFlowTemplateRevisions.html#IoTThingsGraph.Paginator.GetFlowTemplateRevisions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getflowtemplaterevisionspaginator)
        """


if TYPE_CHECKING:
    _GetSystemTemplateRevisionsPaginatorBase = AioPaginator[
        GetSystemTemplateRevisionsResponseTypeDef
    ]
else:
    _GetSystemTemplateRevisionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetSystemTemplateRevisionsPaginator(_GetSystemTemplateRevisionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetSystemTemplateRevisions.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getsystemtemplaterevisionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetSystemTemplateRevisionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetSystemTemplateRevisionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/GetSystemTemplateRevisions.html#IoTThingsGraph.Paginator.GetSystemTemplateRevisions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#getsystemtemplaterevisionspaginator)
        """


if TYPE_CHECKING:
    _ListFlowExecutionMessagesPaginatorBase = AioPaginator[ListFlowExecutionMessagesResponseTypeDef]
else:
    _ListFlowExecutionMessagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFlowExecutionMessagesPaginator(_ListFlowExecutionMessagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListFlowExecutionMessages.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listflowexecutionmessagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowExecutionMessagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowExecutionMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListFlowExecutionMessages.html#IoTThingsGraph.Paginator.ListFlowExecutionMessages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listflowexecutionmessagespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListTagsForResource.html#IoTThingsGraph.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/ListTagsForResource.html#IoTThingsGraph.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _SearchEntitiesPaginatorBase = AioPaginator[SearchEntitiesResponseTypeDef]
else:
    _SearchEntitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchEntitiesPaginator(_SearchEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchEntities.html#IoTThingsGraph.Paginator.SearchEntities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchentitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchEntitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchEntities.html#IoTThingsGraph.Paginator.SearchEntities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchentitiespaginator)
        """


if TYPE_CHECKING:
    _SearchFlowExecutionsPaginatorBase = AioPaginator[SearchFlowExecutionsResponseTypeDef]
else:
    _SearchFlowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchFlowExecutionsPaginator(_SearchFlowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowExecutions.html#IoTThingsGraph.Paginator.SearchFlowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFlowExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowExecutions.html#IoTThingsGraph.Paginator.SearchFlowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowexecutionspaginator)
        """


if TYPE_CHECKING:
    _SearchFlowTemplatesPaginatorBase = AioPaginator[SearchFlowTemplatesResponseTypeDef]
else:
    _SearchFlowTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchFlowTemplatesPaginator(_SearchFlowTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowTemplates.html#IoTThingsGraph.Paginator.SearchFlowTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchFlowTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchFlowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchFlowTemplates.html#IoTThingsGraph.Paginator.SearchFlowTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchflowtemplatespaginator)
        """


if TYPE_CHECKING:
    _SearchSystemInstancesPaginatorBase = AioPaginator[SearchSystemInstancesResponseTypeDef]
else:
    _SearchSystemInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchSystemInstancesPaginator(_SearchSystemInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemInstances.html#IoTThingsGraph.Paginator.SearchSystemInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsysteminstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchSystemInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchSystemInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemInstances.html#IoTThingsGraph.Paginator.SearchSystemInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsysteminstancespaginator)
        """


if TYPE_CHECKING:
    _SearchSystemTemplatesPaginatorBase = AioPaginator[SearchSystemTemplatesResponseTypeDef]
else:
    _SearchSystemTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchSystemTemplatesPaginator(_SearchSystemTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemTemplates.html#IoTThingsGraph.Paginator.SearchSystemTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsystemtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchSystemTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchSystemTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchSystemTemplates.html#IoTThingsGraph.Paginator.SearchSystemTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchsystemtemplatespaginator)
        """


if TYPE_CHECKING:
    _SearchThingsPaginatorBase = AioPaginator[SearchThingsResponseTypeDef]
else:
    _SearchThingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchThingsPaginator(_SearchThingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchThings.html#IoTThingsGraph.Paginator.SearchThings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchthingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchThingsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotthingsgraph/paginator/SearchThings.html#IoTThingsGraph.Paginator.SearchThings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotthingsgraph/paginators/#searchthingspaginator)
        """
