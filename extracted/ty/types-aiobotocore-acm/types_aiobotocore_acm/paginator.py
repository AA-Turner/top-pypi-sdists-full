"""
Type annotations for acm service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm.client import ACMClient
    from types_aiobotocore_acm.paginator import (
        ListAcmeAccountsPaginator,
        ListAcmeDomainValidationsPaginator,
        ListAcmeEndpointsPaginator,
        ListAcmeExternalAccountBindingsPaginator,
        ListCertificatesPaginator,
        SearchCertificatesPaginator,
    )

    session = get_session()
    with session.create_client("acm") as client:
        client: ACMClient

        list_acme_accounts_paginator: ListAcmeAccountsPaginator = client.get_paginator("list_acme_accounts")
        list_acme_domain_validations_paginator: ListAcmeDomainValidationsPaginator = client.get_paginator("list_acme_domain_validations")
        list_acme_endpoints_paginator: ListAcmeEndpointsPaginator = client.get_paginator("list_acme_endpoints")
        list_acme_external_account_bindings_paginator: ListAcmeExternalAccountBindingsPaginator = client.get_paginator("list_acme_external_account_bindings")
        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
        search_certificates_paginator: SearchCertificatesPaginator = client.get_paginator("search_certificates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAcmeAccountsRequestPaginateTypeDef,
    ListAcmeAccountsResponseTypeDef,
    ListAcmeDomainValidationsRequestPaginateTypeDef,
    ListAcmeDomainValidationsResponseTypeDef,
    ListAcmeEndpointsRequestPaginateTypeDef,
    ListAcmeEndpointsResponseTypeDef,
    ListAcmeExternalAccountBindingsRequestPaginateTypeDef,
    ListAcmeExternalAccountBindingsResponseTypeDef,
    ListCertificatesRequestPaginateTypeDef,
    ListCertificatesResponseTypeDef,
    SearchCertificatesRequestPaginateTypeDef,
    SearchCertificatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAcmeAccountsPaginator",
    "ListAcmeDomainValidationsPaginator",
    "ListAcmeEndpointsPaginator",
    "ListAcmeExternalAccountBindingsPaginator",
    "ListCertificatesPaginator",
    "SearchCertificatesPaginator",
)


if TYPE_CHECKING:
    _ListAcmeAccountsPaginatorBase = AioPaginator[ListAcmeAccountsResponseTypeDef]
else:
    _ListAcmeAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAcmeAccountsPaginator(_ListAcmeAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeAccounts.html#ACM.Paginator.ListAcmeAccounts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmeaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeAccountsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAcmeAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeAccounts.html#ACM.Paginator.ListAcmeAccounts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmeaccountspaginator)
        """


if TYPE_CHECKING:
    _ListAcmeDomainValidationsPaginatorBase = AioPaginator[ListAcmeDomainValidationsResponseTypeDef]
else:
    _ListAcmeDomainValidationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAcmeDomainValidationsPaginator(_ListAcmeDomainValidationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeDomainValidations.html#ACM.Paginator.ListAcmeDomainValidations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmedomainvalidationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeDomainValidationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAcmeDomainValidationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeDomainValidations.html#ACM.Paginator.ListAcmeDomainValidations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmedomainvalidationspaginator)
        """


if TYPE_CHECKING:
    _ListAcmeEndpointsPaginatorBase = AioPaginator[ListAcmeEndpointsResponseTypeDef]
else:
    _ListAcmeEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAcmeEndpointsPaginator(_ListAcmeEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeEndpoints.html#ACM.Paginator.ListAcmeEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmeendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAcmeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeEndpoints.html#ACM.Paginator.ListAcmeEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmeendpointspaginator)
        """


if TYPE_CHECKING:
    _ListAcmeExternalAccountBindingsPaginatorBase = AioPaginator[
        ListAcmeExternalAccountBindingsResponseTypeDef
    ]
else:
    _ListAcmeExternalAccountBindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAcmeExternalAccountBindingsPaginator(_ListAcmeExternalAccountBindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeExternalAccountBindings.html#ACM.Paginator.ListAcmeExternalAccountBindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmeexternalaccountbindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeExternalAccountBindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAcmeExternalAccountBindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeExternalAccountBindings.html#ACM.Paginator.ListAcmeExternalAccountBindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listacmeexternalaccountbindingspaginator)
        """


if TYPE_CHECKING:
    _ListCertificatesPaginatorBase = AioPaginator[ListCertificatesResponseTypeDef]
else:
    _ListCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCertificatesPaginator(_ListCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listcertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#listcertificatespaginator)
        """


if TYPE_CHECKING:
    _SearchCertificatesPaginatorBase = AioPaginator[SearchCertificatesResponseTypeDef]
else:
    _SearchCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchCertificatesPaginator(_SearchCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/SearchCertificates.html#ACM.Paginator.SearchCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#searchcertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/SearchCertificates.html#ACM.Paginator.SearchCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/paginators/#searchcertificatespaginator)
        """
