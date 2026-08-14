"""
Type annotations for acm service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_acm.client import ACMClient
    from mypy_boto3_acm.paginator import (
        ListAcmeAccountsPaginator,
        ListAcmeDomainValidationsPaginator,
        ListAcmeEndpointsPaginator,
        ListAcmeExternalAccountBindingsPaginator,
        ListCertificateDomainValidationsPaginator,
        ListCertificatesPaginator,
        SearchCertificatesPaginator,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    list_acme_accounts_paginator: ListAcmeAccountsPaginator = client.get_paginator("list_acme_accounts")
    list_acme_domain_validations_paginator: ListAcmeDomainValidationsPaginator = client.get_paginator("list_acme_domain_validations")
    list_acme_endpoints_paginator: ListAcmeEndpointsPaginator = client.get_paginator("list_acme_endpoints")
    list_acme_external_account_bindings_paginator: ListAcmeExternalAccountBindingsPaginator = client.get_paginator("list_acme_external_account_bindings")
    list_certificate_domain_validations_paginator: ListCertificateDomainValidationsPaginator = client.get_paginator("list_certificate_domain_validations")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    search_certificates_paginator: SearchCertificatesPaginator = client.get_paginator("search_certificates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAcmeAccountsRequestPaginateTypeDef,
    ListAcmeAccountsResponseTypeDef,
    ListAcmeDomainValidationsRequestPaginateTypeDef,
    ListAcmeDomainValidationsResponseTypeDef,
    ListAcmeEndpointsRequestPaginateTypeDef,
    ListAcmeEndpointsResponseTypeDef,
    ListAcmeExternalAccountBindingsRequestPaginateTypeDef,
    ListAcmeExternalAccountBindingsResponseTypeDef,
    ListCertificateDomainValidationsRequestPaginateTypeDef,
    ListCertificateDomainValidationsResponseTypeDef,
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
    "ListCertificateDomainValidationsPaginator",
    "ListCertificatesPaginator",
    "SearchCertificatesPaginator",
)

if TYPE_CHECKING:
    _ListAcmeAccountsPaginatorBase = Paginator[ListAcmeAccountsResponseTypeDef]
else:
    _ListAcmeAccountsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAcmeAccountsPaginator(_ListAcmeAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeAccounts.html#ACM.Paginator.ListAcmeAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmeaccountspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeAccountsRequestPaginateTypeDef]
    ) -> PageIterator[ListAcmeAccountsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeAccounts.html#ACM.Paginator.ListAcmeAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmeaccountspaginator)
        """

if TYPE_CHECKING:
    _ListAcmeDomainValidationsPaginatorBase = Paginator[ListAcmeDomainValidationsResponseTypeDef]
else:
    _ListAcmeDomainValidationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAcmeDomainValidationsPaginator(_ListAcmeDomainValidationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeDomainValidations.html#ACM.Paginator.ListAcmeDomainValidations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmedomainvalidationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeDomainValidationsRequestPaginateTypeDef]
    ) -> PageIterator[ListAcmeDomainValidationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeDomainValidations.html#ACM.Paginator.ListAcmeDomainValidations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmedomainvalidationspaginator)
        """

if TYPE_CHECKING:
    _ListAcmeEndpointsPaginatorBase = Paginator[ListAcmeEndpointsResponseTypeDef]
else:
    _ListAcmeEndpointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAcmeEndpointsPaginator(_ListAcmeEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeEndpoints.html#ACM.Paginator.ListAcmeEndpoints)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmeendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeEndpointsRequestPaginateTypeDef]
    ) -> PageIterator[ListAcmeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeEndpoints.html#ACM.Paginator.ListAcmeEndpoints.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmeendpointspaginator)
        """

if TYPE_CHECKING:
    _ListAcmeExternalAccountBindingsPaginatorBase = Paginator[
        ListAcmeExternalAccountBindingsResponseTypeDef
    ]
else:
    _ListAcmeExternalAccountBindingsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAcmeExternalAccountBindingsPaginator(_ListAcmeExternalAccountBindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeExternalAccountBindings.html#ACM.Paginator.ListAcmeExternalAccountBindings)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmeexternalaccountbindingspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcmeExternalAccountBindingsRequestPaginateTypeDef]
    ) -> PageIterator[ListAcmeExternalAccountBindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListAcmeExternalAccountBindings.html#ACM.Paginator.ListAcmeExternalAccountBindings.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listacmeexternalaccountbindingspaginator)
        """

if TYPE_CHECKING:
    _ListCertificateDomainValidationsPaginatorBase = Paginator[
        ListCertificateDomainValidationsResponseTypeDef
    ]
else:
    _ListCertificateDomainValidationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListCertificateDomainValidationsPaginator(_ListCertificateDomainValidationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificateDomainValidations.html#ACM.Paginator.ListCertificateDomainValidations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatedomainvalidationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificateDomainValidationsRequestPaginateTypeDef]
    ) -> PageIterator[ListCertificateDomainValidationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificateDomainValidations.html#ACM.Paginator.ListCertificateDomainValidations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatedomainvalidationspaginator)
        """

if TYPE_CHECKING:
    _ListCertificatesPaginatorBase = Paginator[ListCertificatesResponseTypeDef]
else:
    _ListCertificatesPaginatorBase = Paginator  # type: ignore[assignment]

class ListCertificatesPaginator(_ListCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificatesRequestPaginateTypeDef]
    ) -> PageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/ListCertificates.html#ACM.Paginator.ListCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#listcertificatespaginator)
        """

if TYPE_CHECKING:
    _SearchCertificatesPaginatorBase = Paginator[SearchCertificatesResponseTypeDef]
else:
    _SearchCertificatesPaginatorBase = Paginator  # type: ignore[assignment]

class SearchCertificatesPaginator(_SearchCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/SearchCertificates.html#ACM.Paginator.SearchCertificates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#searchcertificatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchCertificatesRequestPaginateTypeDef]
    ) -> PageIterator[SearchCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/paginator/SearchCertificates.html#ACM.Paginator.SearchCertificates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_acm/paginators/#searchcertificatespaginator)
        """
