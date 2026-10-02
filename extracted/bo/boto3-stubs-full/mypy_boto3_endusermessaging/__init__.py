"""
Main interface for endusermessaging service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_endusermessaging import (
        BrandProfileActiveWaiter,
        Client,
        EndUserMessagingClient,
        JobSuccessWaiter,
        ListBrandProfileAttributesPaginator,
        ListBrandProfilesPaginator,
        ListJobsPaginator,
        ListNotifyCodeConfigurationsPaginator,
        ListRegistrationsFromBrandProfilePaginator,
    )

    session = Session()
    client: EndUserMessagingClient = session.client("endusermessaging")

    brand_profile_active_waiter: BrandProfileActiveWaiter = client.get_waiter("brand_profile_active")
    job_success_waiter: JobSuccessWaiter = client.get_waiter("job_success")

    list_brand_profile_attributes_paginator: ListBrandProfileAttributesPaginator = client.get_paginator("list_brand_profile_attributes")
    list_brand_profiles_paginator: ListBrandProfilesPaginator = client.get_paginator("list_brand_profiles")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_notify_code_configurations_paginator: ListNotifyCodeConfigurationsPaginator = client.get_paginator("list_notify_code_configurations")
    list_registrations_from_brand_profile_paginator: ListRegistrationsFromBrandProfilePaginator = client.get_paginator("list_registrations_from_brand_profile")
    ```
"""

from .client import EndUserMessagingClient
from .paginator import (
    ListBrandProfileAttributesPaginator,
    ListBrandProfilesPaginator,
    ListJobsPaginator,
    ListNotifyCodeConfigurationsPaginator,
    ListRegistrationsFromBrandProfilePaginator,
)
from .waiter import BrandProfileActiveWaiter, JobSuccessWaiter

Client = EndUserMessagingClient


__all__ = (
    "BrandProfileActiveWaiter",
    "Client",
    "EndUserMessagingClient",
    "JobSuccessWaiter",
    "ListBrandProfileAttributesPaginator",
    "ListBrandProfilesPaginator",
    "ListJobsPaginator",
    "ListNotifyCodeConfigurationsPaginator",
    "ListRegistrationsFromBrandProfilePaginator",
)
