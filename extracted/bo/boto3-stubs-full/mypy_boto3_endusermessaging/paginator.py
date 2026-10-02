"""
Type annotations for endusermessaging service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_endusermessaging.client import EndUserMessagingClient
    from mypy_boto3_endusermessaging.paginator import (
        ListBrandProfileAttributesPaginator,
        ListBrandProfilesPaginator,
        ListJobsPaginator,
        ListNotifyCodeConfigurationsPaginator,
        ListRegistrationsFromBrandProfilePaginator,
    )

    session = Session()
    client: EndUserMessagingClient = session.client("endusermessaging")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListBrandProfileAttributesPaginatorBase = Paginator[ListBrandProfileAttributesOutputTypeDef]
else:
    _ListBrandProfileAttributesPaginatorBase = Paginator  # type: ignore[assignment]


class ListBrandProfileAttributesPaginator(_ListBrandProfileAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfileAttributes.html#EndUserMessaging.Paginator.ListBrandProfileAttributes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listbrandprofileattributespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrandProfileAttributesInputPaginateTypeDef]
    ) -> PageIterator[ListBrandProfileAttributesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfileAttributes.html#EndUserMessaging.Paginator.ListBrandProfileAttributes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listbrandprofileattributespaginator)
        """


if TYPE_CHECKING:
    _ListBrandProfilesPaginatorBase = Paginator[ListBrandProfilesOutputTypeDef]
else:
    _ListBrandProfilesPaginatorBase = Paginator  # type: ignore[assignment]


class ListBrandProfilesPaginator(_ListBrandProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfiles.html#EndUserMessaging.Paginator.ListBrandProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listbrandprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrandProfilesInputPaginateTypeDef]
    ) -> PageIterator[ListBrandProfilesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListBrandProfiles.html#EndUserMessaging.Paginator.ListBrandProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listbrandprofilespaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = Paginator[ListJobsOutputTypeDef]
else:
    _ListJobsPaginatorBase = Paginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListJobs.html#EndUserMessaging.Paginator.ListJobs)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsInputPaginateTypeDef]
    ) -> PageIterator[ListJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListJobs.html#EndUserMessaging.Paginator.ListJobs.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListNotifyCodeConfigurationsPaginatorBase = Paginator[
        ListNotifyCodeConfigurationsOutputTypeDef
    ]
else:
    _ListNotifyCodeConfigurationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListNotifyCodeConfigurationsPaginator(_ListNotifyCodeConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListNotifyCodeConfigurations.html#EndUserMessaging.Paginator.ListNotifyCodeConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listnotifycodeconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNotifyCodeConfigurationsInputPaginateTypeDef]
    ) -> PageIterator[ListNotifyCodeConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListNotifyCodeConfigurations.html#EndUserMessaging.Paginator.ListNotifyCodeConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listnotifycodeconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListRegistrationsFromBrandProfilePaginatorBase = Paginator[
        ListRegistrationsFromBrandProfileOutputTypeDef
    ]
else:
    _ListRegistrationsFromBrandProfilePaginatorBase = Paginator  # type: ignore[assignment]


class ListRegistrationsFromBrandProfilePaginator(_ListRegistrationsFromBrandProfilePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListRegistrationsFromBrandProfile.html#EndUserMessaging.Paginator.ListRegistrationsFromBrandProfile)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listregistrationsfrombrandprofilepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistrationsFromBrandProfileInputPaginateTypeDef]
    ) -> PageIterator[ListRegistrationsFromBrandProfileOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/paginator/ListRegistrationsFromBrandProfile.html#EndUserMessaging.Paginator.ListRegistrationsFromBrandProfile.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_endusermessaging/paginators/#listregistrationsfrombrandprofilepaginator)
        """
