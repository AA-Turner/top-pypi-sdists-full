"""
Type annotations for endusermessaging service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_endusermessaging.client import EndUserMessagingClient
    from types_aiobotocore_endusermessaging.paginator import (
        ListBrandProfileAttributesPaginator,
        ListBrandProfilesPaginator,
        ListJobsPaginator,
        ListNotifyCodeConfigurationsPaginator,
        ListRegistrationsFromBrandProfilePaginator,
    )

    session = get_session()
    with session.create_client("endusermessaging") as client:
        client: EndUserMessagingClient

        list_brand_profile_attributes_paginator: ListBrandProfileAttributesPaginator = client.get_paginator("list_brand_profile_attributes")
        list_brand_profiles_paginator: ListBrandProfilesPaginator = client.get_paginator("list_brand_profiles")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_notify_code_configurations_paginator: ListNotifyCodeConfigurationsPaginator = client.get_paginator("list_notify_code_configurations")
        list_registrations_from_brand_profile_paginator: ListRegistrationsFromBrandProfilePaginator = client.get_paginator("list_registrations_from_brand_profile")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBrandProfileAttributesInputPaginateTypeDef,
    ListBrandProfileAttributesOutputTypeDef,
    ListBrandProfilesInputPaginateTypeDef,
    ListBrandProfilesOutputTypeDef,
    ListJobsInputPaginateTypeDef,
    ListJobsOutputTypeDef,
    ListNotifyCodeConfigurationsInputPaginateTypeDef,
    ListNotifyCodeConfigurationsOutputTypeDef,
    ListRegistrationsFromBrandProfileInputPaginateTypeDef,
    ListRegistrationsFromBrandProfileOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBrandProfileAttributesPaginator",
    "ListBrandProfilesPaginator",
    "ListJobsPaginator",
    "ListNotifyCodeConfigurationsPaginator",
    "ListRegistrationsFromBrandProfilePaginator",
)

if TYPE_CHECKING:
    _ListBrandProfileAttributesPaginatorBase = AioPaginator[ListBrandProfileAttributesOutputTypeDef]
else:
    _ListBrandProfileAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBrandProfileAttributesPaginator(_ListBrandProfileAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfileAttributes.html#EndUserMessaging.Paginator.ListBrandProfileAttributes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listbrandprofileattributespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrandProfileAttributesInputPaginateTypeDef]
    ) -> AioPageIterator[ListBrandProfileAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfileAttributes.html#EndUserMessaging.Paginator.ListBrandProfileAttributes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listbrandprofileattributespaginator)
        """

if TYPE_CHECKING:
    _ListBrandProfilesPaginatorBase = AioPaginator[ListBrandProfilesOutputTypeDef]
else:
    _ListBrandProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBrandProfilesPaginator(_ListBrandProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfiles.html#EndUserMessaging.Paginator.ListBrandProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listbrandprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrandProfilesInputPaginateTypeDef]
    ) -> AioPageIterator[ListBrandProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfiles.html#EndUserMessaging.Paginator.ListBrandProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listbrandprofilespaginator)
        """

if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsOutputTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListJobs.html#EndUserMessaging.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListJobs.html#EndUserMessaging.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listjobspaginator)
        """

if TYPE_CHECKING:
    _ListNotifyCodeConfigurationsPaginatorBase = AioPaginator[
        ListNotifyCodeConfigurationsOutputTypeDef
    ]
else:
    _ListNotifyCodeConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListNotifyCodeConfigurationsPaginator(_ListNotifyCodeConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListNotifyCodeConfigurations.html#EndUserMessaging.Paginator.ListNotifyCodeConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listnotifycodeconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotifyCodeConfigurationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListNotifyCodeConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListNotifyCodeConfigurations.html#EndUserMessaging.Paginator.ListNotifyCodeConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listnotifycodeconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListRegistrationsFromBrandProfilePaginatorBase = AioPaginator[
        ListRegistrationsFromBrandProfileOutputTypeDef
    ]
else:
    _ListRegistrationsFromBrandProfilePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRegistrationsFromBrandProfilePaginator(_ListRegistrationsFromBrandProfilePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListRegistrationsFromBrandProfile.html#EndUserMessaging.Paginator.ListRegistrationsFromBrandProfile)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listregistrationsfrombrandprofilepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistrationsFromBrandProfileInputPaginateTypeDef]
    ) -> AioPageIterator[ListRegistrationsFromBrandProfileOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListRegistrationsFromBrandProfile.html#EndUserMessaging.Paginator.ListRegistrationsFromBrandProfile.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_endusermessaging/paginators/#listregistrationsfrombrandprofilepaginator)
        """
