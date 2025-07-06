"""
Type annotations for pinpoint-email service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pinpoint_email.client import PinpointEmailClient
    from types_aiobotocore_pinpoint_email.paginator import (
        GetDedicatedIpsPaginator,
        ListConfigurationSetsPaginator,
        ListDedicatedIpPoolsPaginator,
        ListDeliverabilityTestReportsPaginator,
        ListEmailIdentitiesPaginator,
    )

    session = get_session()
    with session.create_client("pinpoint-email") as client:
        client: PinpointEmailClient

        get_dedicated_ips_paginator: GetDedicatedIpsPaginator = client.get_paginator("get_dedicated_ips")
        list_configuration_sets_paginator: ListConfigurationSetsPaginator = client.get_paginator("list_configuration_sets")
        list_dedicated_ip_pools_paginator: ListDedicatedIpPoolsPaginator = client.get_paginator("list_dedicated_ip_pools")
        list_deliverability_test_reports_paginator: ListDeliverabilityTestReportsPaginator = client.get_paginator("list_deliverability_test_reports")
        list_email_identities_paginator: ListEmailIdentitiesPaginator = client.get_paginator("list_email_identities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetDedicatedIpsRequestPaginateTypeDef,
    GetDedicatedIpsResponseTypeDef,
    ListConfigurationSetsRequestPaginateTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListDedicatedIpPoolsRequestPaginateTypeDef,
    ListDedicatedIpPoolsResponseTypeDef,
    ListDeliverabilityTestReportsRequestPaginateTypeDef,
    ListDeliverabilityTestReportsResponseTypeDef,
    ListEmailIdentitiesRequestPaginateTypeDef,
    ListEmailIdentitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetDedicatedIpsPaginator",
    "ListConfigurationSetsPaginator",
    "ListDedicatedIpPoolsPaginator",
    "ListDeliverabilityTestReportsPaginator",
    "ListEmailIdentitiesPaginator",
)


if TYPE_CHECKING:
    _GetDedicatedIpsPaginatorBase = AioPaginator[GetDedicatedIpsResponseTypeDef]
else:
    _GetDedicatedIpsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDedicatedIpsPaginator(_GetDedicatedIpsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/GetDedicatedIps.html#PinpointEmail.Paginator.GetDedicatedIps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#getdedicatedipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDedicatedIpsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetDedicatedIpsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/GetDedicatedIps.html#PinpointEmail.Paginator.GetDedicatedIps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#getdedicatedipspaginator)
        """


if TYPE_CHECKING:
    _ListConfigurationSetsPaginatorBase = AioPaginator[ListConfigurationSetsResponseTypeDef]
else:
    _ListConfigurationSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationSetsPaginator(_ListConfigurationSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListConfigurationSets.html#PinpointEmail.Paginator.ListConfigurationSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listconfigurationsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListConfigurationSets.html#PinpointEmail.Paginator.ListConfigurationSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listconfigurationsetspaginator)
        """


if TYPE_CHECKING:
    _ListDedicatedIpPoolsPaginatorBase = AioPaginator[ListDedicatedIpPoolsResponseTypeDef]
else:
    _ListDedicatedIpPoolsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDedicatedIpPoolsPaginator(_ListDedicatedIpPoolsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListDedicatedIpPools.html#PinpointEmail.Paginator.ListDedicatedIpPools)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listdedicatedippoolspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDedicatedIpPoolsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDedicatedIpPoolsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListDedicatedIpPools.html#PinpointEmail.Paginator.ListDedicatedIpPools.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listdedicatedippoolspaginator)
        """


if TYPE_CHECKING:
    _ListDeliverabilityTestReportsPaginatorBase = AioPaginator[
        ListDeliverabilityTestReportsResponseTypeDef
    ]
else:
    _ListDeliverabilityTestReportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeliverabilityTestReportsPaginator(_ListDeliverabilityTestReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListDeliverabilityTestReports.html#PinpointEmail.Paginator.ListDeliverabilityTestReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listdeliverabilitytestreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeliverabilityTestReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeliverabilityTestReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListDeliverabilityTestReports.html#PinpointEmail.Paginator.ListDeliverabilityTestReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listdeliverabilitytestreportspaginator)
        """


if TYPE_CHECKING:
    _ListEmailIdentitiesPaginatorBase = AioPaginator[ListEmailIdentitiesResponseTypeDef]
else:
    _ListEmailIdentitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEmailIdentitiesPaginator(_ListEmailIdentitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListEmailIdentities.html#PinpointEmail.Paginator.ListEmailIdentities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listemailidentitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEmailIdentitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEmailIdentitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pinpoint-email/paginator/ListEmailIdentities.html#PinpointEmail.Paginator.ListEmailIdentities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pinpoint_email/paginators/#listemailidentitiespaginator)
        """
