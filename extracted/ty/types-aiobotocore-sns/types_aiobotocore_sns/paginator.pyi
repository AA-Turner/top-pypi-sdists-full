"""
Type annotations for sns service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sns.client import SNSClient
    from types_aiobotocore_sns.paginator import (
        ListEndpointsByPlatformApplicationPaginator,
        ListOriginationNumbersPaginator,
        ListPhoneNumbersOptedOutPaginator,
        ListPlatformApplicationsPaginator,
        ListSMSSandboxPhoneNumbersPaginator,
        ListSubscriptionsByTopicPaginator,
        ListSubscriptionsPaginator,
        ListTopicsPaginator,
    )

    session = get_session()
    with session.create_client("sns") as client:
        client: SNSClient

        list_endpoints_by_platform_application_paginator: ListEndpointsByPlatformApplicationPaginator = client.get_paginator("list_endpoints_by_platform_application")
        list_origination_numbers_paginator: ListOriginationNumbersPaginator = client.get_paginator("list_origination_numbers")
        list_phone_numbers_opted_out_paginator: ListPhoneNumbersOptedOutPaginator = client.get_paginator("list_phone_numbers_opted_out")
        list_platform_applications_paginator: ListPlatformApplicationsPaginator = client.get_paginator("list_platform_applications")
        list_sms_sandbox_phone_numbers_paginator: ListSMSSandboxPhoneNumbersPaginator = client.get_paginator("list_sms_sandbox_phone_numbers")
        list_subscriptions_by_topic_paginator: ListSubscriptionsByTopicPaginator = client.get_paginator("list_subscriptions_by_topic")
        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
        list_topics_paginator: ListTopicsPaginator = client.get_paginator("list_topics")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListEndpointsByPlatformApplicationInputPaginateTypeDef,
    ListEndpointsByPlatformApplicationResponseTypeDef,
    ListOriginationNumbersRequestPaginateTypeDef,
    ListOriginationNumbersResultTypeDef,
    ListPhoneNumbersOptedOutInputPaginateTypeDef,
    ListPhoneNumbersOptedOutResponseTypeDef,
    ListPlatformApplicationsInputPaginateTypeDef,
    ListPlatformApplicationsResponseTypeDef,
    ListSMSSandboxPhoneNumbersInputPaginateTypeDef,
    ListSMSSandboxPhoneNumbersResultTypeDef,
    ListSubscriptionsByTopicInputPaginateTypeDef,
    ListSubscriptionsByTopicResponseTypeDef,
    ListSubscriptionsInputPaginateTypeDef,
    ListSubscriptionsResponseTypeDef,
    ListTopicsInputPaginateTypeDef,
    ListTopicsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListEndpointsByPlatformApplicationPaginator",
    "ListOriginationNumbersPaginator",
    "ListPhoneNumbersOptedOutPaginator",
    "ListPlatformApplicationsPaginator",
    "ListSMSSandboxPhoneNumbersPaginator",
    "ListSubscriptionsByTopicPaginator",
    "ListSubscriptionsPaginator",
    "ListTopicsPaginator",
)

if TYPE_CHECKING:
    _ListEndpointsByPlatformApplicationPaginatorBase = AioPaginator[
        ListEndpointsByPlatformApplicationResponseTypeDef
    ]
else:
    _ListEndpointsByPlatformApplicationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEndpointsByPlatformApplicationPaginator(_ListEndpointsByPlatformApplicationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListEndpointsByPlatformApplication.html#SNS.Paginator.ListEndpointsByPlatformApplication)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listendpointsbyplatformapplicationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointsByPlatformApplicationInputPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointsByPlatformApplicationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListEndpointsByPlatformApplication.html#SNS.Paginator.ListEndpointsByPlatformApplication.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listendpointsbyplatformapplicationpaginator)
        """

if TYPE_CHECKING:
    _ListOriginationNumbersPaginatorBase = AioPaginator[ListOriginationNumbersResultTypeDef]
else:
    _ListOriginationNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOriginationNumbersPaginator(_ListOriginationNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListOriginationNumbers.html#SNS.Paginator.ListOriginationNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listoriginationnumberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOriginationNumbersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOriginationNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListOriginationNumbers.html#SNS.Paginator.ListOriginationNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listoriginationnumberspaginator)
        """

if TYPE_CHECKING:
    _ListPhoneNumbersOptedOutPaginatorBase = AioPaginator[ListPhoneNumbersOptedOutResponseTypeDef]
else:
    _ListPhoneNumbersOptedOutPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPhoneNumbersOptedOutPaginator(_ListPhoneNumbersOptedOutPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPhoneNumbersOptedOut.html#SNS.Paginator.ListPhoneNumbersOptedOut)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listphonenumbersoptedoutpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPhoneNumbersOptedOutInputPaginateTypeDef]
    ) -> AioPageIterator[ListPhoneNumbersOptedOutResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPhoneNumbersOptedOut.html#SNS.Paginator.ListPhoneNumbersOptedOut.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listphonenumbersoptedoutpaginator)
        """

if TYPE_CHECKING:
    _ListPlatformApplicationsPaginatorBase = AioPaginator[ListPlatformApplicationsResponseTypeDef]
else:
    _ListPlatformApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPlatformApplicationsPaginator(_ListPlatformApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPlatformApplications.html#SNS.Paginator.ListPlatformApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listplatformapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlatformApplicationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPlatformApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListPlatformApplications.html#SNS.Paginator.ListPlatformApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listplatformapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListSMSSandboxPhoneNumbersPaginatorBase = AioPaginator[ListSMSSandboxPhoneNumbersResultTypeDef]
else:
    _ListSMSSandboxPhoneNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSMSSandboxPhoneNumbersPaginator(_ListSMSSandboxPhoneNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSMSSandboxPhoneNumbers.html#SNS.Paginator.ListSMSSandboxPhoneNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsmssandboxphonenumberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSMSSandboxPhoneNumbersInputPaginateTypeDef]
    ) -> AioPageIterator[ListSMSSandboxPhoneNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSMSSandboxPhoneNumbers.html#SNS.Paginator.ListSMSSandboxPhoneNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsmssandboxphonenumberspaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionsByTopicPaginatorBase = AioPaginator[ListSubscriptionsByTopicResponseTypeDef]
else:
    _ListSubscriptionsByTopicPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionsByTopicPaginator(_ListSubscriptionsByTopicPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptionsByTopic.html#SNS.Paginator.ListSubscriptionsByTopic)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionsbytopicpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsByTopicInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionsByTopicResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptionsByTopic.html#SNS.Paginator.ListSubscriptionsByTopic.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionsbytopicpaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = AioPaginator[ListSubscriptionsResponseTypeDef]
else:
    _ListSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptions.html#SNS.Paginator.ListSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListSubscriptions.html#SNS.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionspaginator)
        """

if TYPE_CHECKING:
    _ListTopicsPaginatorBase = AioPaginator[ListTopicsResponseTypeDef]
else:
    _ListTopicsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTopicsPaginator(_ListTopicsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListTopics.html#SNS.Paginator.ListTopics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listtopicspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTopicsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTopicsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/paginator/ListTopics.html#SNS.Paginator.ListTopics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listtopicspaginator)
        """
