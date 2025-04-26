"""
Main interface for sns service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sns import (
        Client,
        ListEndpointsByPlatformApplicationPaginator,
        ListOriginationNumbersPaginator,
        ListPhoneNumbersOptedOutPaginator,
        ListPlatformApplicationsPaginator,
        ListSMSSandboxPhoneNumbersPaginator,
        ListSubscriptionsByTopicPaginator,
        ListSubscriptionsPaginator,
        ListTopicsPaginator,
        SNSClient,
        SNSServiceResource,
        ServiceResource,
    )

    session = get_session()
    async with session.create_client("sns") as client:
        client: SNSClient
        ...


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

from .client import SNSClient
from .paginator import (
    ListEndpointsByPlatformApplicationPaginator,
    ListOriginationNumbersPaginator,
    ListPhoneNumbersOptedOutPaginator,
    ListPlatformApplicationsPaginator,
    ListSMSSandboxPhoneNumbersPaginator,
    ListSubscriptionsByTopicPaginator,
    ListSubscriptionsPaginator,
    ListTopicsPaginator,
)

try:
    from .service_resource import SNSServiceResource
except ImportError:
    from builtins import object as SNSServiceResource  # type: ignore[assignment]

Client = SNSClient

ServiceResource = SNSServiceResource

__all__ = (
    "Client",
    "ListEndpointsByPlatformApplicationPaginator",
    "ListOriginationNumbersPaginator",
    "ListPhoneNumbersOptedOutPaginator",
    "ListPlatformApplicationsPaginator",
    "ListSMSSandboxPhoneNumbersPaginator",
    "ListSubscriptionsByTopicPaginator",
    "ListSubscriptionsPaginator",
    "ListTopicsPaginator",
    "SNSClient",
    "SNSServiceResource",
    "ServiceResource",
)
