"""
Type annotations for service-quotas service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_service_quotas.client import ServiceQuotasClient
    from types_aiobotocore_service_quotas.paginator import (
        ListAWSDefaultServiceQuotasPaginator,
        ListRequestedServiceQuotaChangeHistoryByQuotaPaginator,
        ListRequestedServiceQuotaChangeHistoryPaginator,
        ListServiceQuotaIncreaseRequestsInTemplatePaginator,
        ListServiceQuotasPaginator,
        ListServicesPaginator,
    )

    session = get_session()
    with session.create_client("service-quotas") as client:
        client: ServiceQuotasClient

        list_aws_default_service_quotas_paginator: ListAWSDefaultServiceQuotasPaginator = client.get_paginator("list_aws_default_service_quotas")
        list_requested_service_quota_change_history_by_quota_paginator: ListRequestedServiceQuotaChangeHistoryByQuotaPaginator = client.get_paginator("list_requested_service_quota_change_history_by_quota")
        list_requested_service_quota_change_history_paginator: ListRequestedServiceQuotaChangeHistoryPaginator = client.get_paginator("list_requested_service_quota_change_history")
        list_service_quota_increase_requests_in_template_paginator: ListServiceQuotaIncreaseRequestsInTemplatePaginator = client.get_paginator("list_service_quota_increase_requests_in_template")
        list_service_quotas_paginator: ListServiceQuotasPaginator = client.get_paginator("list_service_quotas")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAWSDefaultServiceQuotasRequestPaginateTypeDef,
    ListAWSDefaultServiceQuotasResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryByQuotaRequestPaginateTypeDef,
    ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef,
    ListRequestedServiceQuotaChangeHistoryRequestPaginateTypeDef,
    ListRequestedServiceQuotaChangeHistoryResponseTypeDef,
    ListServiceQuotaIncreaseRequestsInTemplateRequestPaginateTypeDef,
    ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef,
    ListServiceQuotasRequestPaginateTypeDef,
    ListServiceQuotasResponseTypeDef,
    ListServicesRequestPaginateTypeDef,
    ListServicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAWSDefaultServiceQuotasPaginator",
    "ListRequestedServiceQuotaChangeHistoryByQuotaPaginator",
    "ListRequestedServiceQuotaChangeHistoryPaginator",
    "ListServiceQuotaIncreaseRequestsInTemplatePaginator",
    "ListServiceQuotasPaginator",
    "ListServicesPaginator",
)

if TYPE_CHECKING:
    _ListAWSDefaultServiceQuotasPaginatorBase = AioPaginator[
        ListAWSDefaultServiceQuotasResponseTypeDef
    ]
else:
    _ListAWSDefaultServiceQuotasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAWSDefaultServiceQuotasPaginator(_ListAWSDefaultServiceQuotasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListAWSDefaultServiceQuotas.html#ServiceQuotas.Paginator.ListAWSDefaultServiceQuotas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listawsdefaultservicequotaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAWSDefaultServiceQuotasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAWSDefaultServiceQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListAWSDefaultServiceQuotas.html#ServiceQuotas.Paginator.ListAWSDefaultServiceQuotas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listawsdefaultservicequotaspaginator)
        """

if TYPE_CHECKING:
    _ListRequestedServiceQuotaChangeHistoryByQuotaPaginatorBase = AioPaginator[
        ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef
    ]
else:
    _ListRequestedServiceQuotaChangeHistoryByQuotaPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRequestedServiceQuotaChangeHistoryByQuotaPaginator(
    _ListRequestedServiceQuotaChangeHistoryByQuotaPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistoryByQuota.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistoryByQuota)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listrequestedservicequotachangehistorybyquotapaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequestedServiceQuotaChangeHistoryByQuotaRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRequestedServiceQuotaChangeHistoryByQuotaResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistoryByQuota.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistoryByQuota.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listrequestedservicequotachangehistorybyquotapaginator)
        """

if TYPE_CHECKING:
    _ListRequestedServiceQuotaChangeHistoryPaginatorBase = AioPaginator[
        ListRequestedServiceQuotaChangeHistoryResponseTypeDef
    ]
else:
    _ListRequestedServiceQuotaChangeHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRequestedServiceQuotaChangeHistoryPaginator(
    _ListRequestedServiceQuotaChangeHistoryPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistory.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listrequestedservicequotachangehistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRequestedServiceQuotaChangeHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRequestedServiceQuotaChangeHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListRequestedServiceQuotaChangeHistory.html#ServiceQuotas.Paginator.ListRequestedServiceQuotaChangeHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listrequestedservicequotachangehistorypaginator)
        """

if TYPE_CHECKING:
    _ListServiceQuotaIncreaseRequestsInTemplatePaginatorBase = AioPaginator[
        ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef
    ]
else:
    _ListServiceQuotaIncreaseRequestsInTemplatePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceQuotaIncreaseRequestsInTemplatePaginator(
    _ListServiceQuotaIncreaseRequestsInTemplatePaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotaIncreaseRequestsInTemplate.html#ServiceQuotas.Paginator.ListServiceQuotaIncreaseRequestsInTemplate)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listservicequotaincreaserequestsintemplatepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceQuotaIncreaseRequestsInTemplateRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceQuotaIncreaseRequestsInTemplateResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotaIncreaseRequestsInTemplate.html#ServiceQuotas.Paginator.ListServiceQuotaIncreaseRequestsInTemplate.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listservicequotaincreaserequestsintemplatepaginator)
        """

if TYPE_CHECKING:
    _ListServiceQuotasPaginatorBase = AioPaginator[ListServiceQuotasResponseTypeDef]
else:
    _ListServiceQuotasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceQuotasPaginator(_ListServiceQuotasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotas.html#ServiceQuotas.Paginator.ListServiceQuotas)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listservicequotaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceQuotasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServiceQuotasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServiceQuotas.html#ServiceQuotas.Paginator.ListServiceQuotas.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listservicequotaspaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesResponseTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServices.html#ServiceQuotas.Paginator.ListServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/service-quotas/paginator/ListServices.html#ServiceQuotas.Paginator.ListServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_service_quotas/paginators/#listservicespaginator)
        """
