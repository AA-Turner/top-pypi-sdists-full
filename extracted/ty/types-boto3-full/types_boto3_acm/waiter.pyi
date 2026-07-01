"""
Type annotations for acm service client waiters.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_acm.client import ACMClient
    from types_boto3_acm.waiter import (
        AcmeDomainValidationDeletedWaiter,
        AcmeDomainValidationValidatedWaiter,
        AcmeEndpointActiveWaiter,
        AcmeEndpointDeletedWaiter,
        CertificateValidatedWaiter,
    )

    session = Session()
    client: ACMClient = session.client("acm")

    acme_domain_validation_deleted_waiter: AcmeDomainValidationDeletedWaiter = client.get_waiter("acme_domain_validation_deleted")
    acme_domain_validation_validated_waiter: AcmeDomainValidationValidatedWaiter = client.get_waiter("acme_domain_validation_validated")
    acme_endpoint_active_waiter: AcmeEndpointActiveWaiter = client.get_waiter("acme_endpoint_active")
    acme_endpoint_deleted_waiter: AcmeEndpointDeletedWaiter = client.get_waiter("acme_endpoint_deleted")
    certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeAcmeDomainValidationRequestWaitExtraTypeDef,
    DescribeAcmeDomainValidationRequestWaitTypeDef,
    DescribeAcmeEndpointRequestWaitExtraTypeDef,
    DescribeAcmeEndpointRequestWaitTypeDef,
    DescribeCertificateRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AcmeDomainValidationDeletedWaiter",
    "AcmeDomainValidationValidatedWaiter",
    "AcmeEndpointActiveWaiter",
    "AcmeEndpointDeletedWaiter",
    "CertificateValidatedWaiter",
)

class AcmeDomainValidationDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationDeleted.html#ACM.Waiter.AcmeDomainValidationDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmedomainvalidationdeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeDomainValidationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationDeleted.html#ACM.Waiter.AcmeDomainValidationDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmedomainvalidationdeletedwaiter)
        """

class AcmeDomainValidationValidatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationValidated.html#ACM.Waiter.AcmeDomainValidationValidated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmedomainvalidationvalidatedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeDomainValidationRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationValidated.html#ACM.Waiter.AcmeDomainValidationValidated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmedomainvalidationvalidatedwaiter)
        """

class AcmeEndpointActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointActive.html#ACM.Waiter.AcmeEndpointActive)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmeendpointactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointActive.html#ACM.Waiter.AcmeEndpointActive.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmeendpointactivewaiter)
        """

class AcmeEndpointDeletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointDeleted.html#ACM.Waiter.AcmeEndpointDeleted)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmeendpointdeletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointDeleted.html#ACM.Waiter.AcmeEndpointDeleted.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#acmeendpointdeletedwaiter)
        """

class CertificateValidatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/CertificateValidated.html#ACM.Waiter.CertificateValidated)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#certificatevalidatedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCertificateRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/CertificateValidated.html#ACM.Waiter.CertificateValidated.wait)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_acm/waiters/#certificatevalidatedwaiter)
        """
