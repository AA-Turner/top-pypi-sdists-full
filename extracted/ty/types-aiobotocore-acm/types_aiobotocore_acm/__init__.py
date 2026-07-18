"""
Main interface for acm service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_acm import (
        ACMClient,
        AcmeDomainValidationDeletedWaiter,
        AcmeDomainValidationValidatedWaiter,
        AcmeEndpointActiveWaiter,
        AcmeEndpointDeletedWaiter,
        CertificateValidatedWaiter,
        Client,
        ListAcmeAccountsPaginator,
        ListAcmeDomainValidationsPaginator,
        ListAcmeEndpointsPaginator,
        ListAcmeExternalAccountBindingsPaginator,
        ListCertificatesPaginator,
        SearchCertificatesPaginator,
    )

    session = get_session()
    async with session.create_client("acm") as client:
        client: ACMClient
        ...


    acme_domain_validation_deleted_waiter: AcmeDomainValidationDeletedWaiter = client.get_waiter("acme_domain_validation_deleted")
    acme_domain_validation_validated_waiter: AcmeDomainValidationValidatedWaiter = client.get_waiter("acme_domain_validation_validated")
    acme_endpoint_active_waiter: AcmeEndpointActiveWaiter = client.get_waiter("acme_endpoint_active")
    acme_endpoint_deleted_waiter: AcmeEndpointDeletedWaiter = client.get_waiter("acme_endpoint_deleted")
    certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")

    list_acme_accounts_paginator: ListAcmeAccountsPaginator = client.get_paginator("list_acme_accounts")
    list_acme_domain_validations_paginator: ListAcmeDomainValidationsPaginator = client.get_paginator("list_acme_domain_validations")
    list_acme_endpoints_paginator: ListAcmeEndpointsPaginator = client.get_paginator("list_acme_endpoints")
    list_acme_external_account_bindings_paginator: ListAcmeExternalAccountBindingsPaginator = client.get_paginator("list_acme_external_account_bindings")
    list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
    search_certificates_paginator: SearchCertificatesPaginator = client.get_paginator("search_certificates")
    ```
"""

from .client import ACMClient
from .paginator import (
    ListAcmeAccountsPaginator,
    ListAcmeDomainValidationsPaginator,
    ListAcmeEndpointsPaginator,
    ListAcmeExternalAccountBindingsPaginator,
    ListCertificatesPaginator,
    SearchCertificatesPaginator,
)
from .waiter import (
    AcmeDomainValidationDeletedWaiter,
    AcmeDomainValidationValidatedWaiter,
    AcmeEndpointActiveWaiter,
    AcmeEndpointDeletedWaiter,
    CertificateValidatedWaiter,
)

Client = ACMClient


__all__ = (
    "ACMClient",
    "AcmeDomainValidationDeletedWaiter",
    "AcmeDomainValidationValidatedWaiter",
    "AcmeEndpointActiveWaiter",
    "AcmeEndpointDeletedWaiter",
    "CertificateValidatedWaiter",
    "Client",
    "ListAcmeAccountsPaginator",
    "ListAcmeDomainValidationsPaginator",
    "ListAcmeEndpointsPaginator",
    "ListAcmeExternalAccountBindingsPaginator",
    "ListCertificatesPaginator",
    "SearchCertificatesPaginator",
)
