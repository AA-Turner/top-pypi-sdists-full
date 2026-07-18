"""
Type annotations for acm service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm.client import ACMClient
    from types_aiobotocore_acm.waiter import (
        AcmeDomainValidationDeletedWaiter,
        AcmeDomainValidationValidatedWaiter,
        AcmeEndpointActiveWaiter,
        AcmeEndpointDeletedWaiter,
        CertificateValidatedWaiter,
    )

    session = get_session()
    async with session.create_client("acm") as client:
        client: ACMClient

        acme_domain_validation_deleted_waiter: AcmeDomainValidationDeletedWaiter = client.get_waiter("acme_domain_validation_deleted")
        acme_domain_validation_validated_waiter: AcmeDomainValidationValidatedWaiter = client.get_waiter("acme_domain_validation_validated")
        acme_endpoint_active_waiter: AcmeEndpointActiveWaiter = client.get_waiter("acme_endpoint_active")
        acme_endpoint_deleted_waiter: AcmeEndpointDeletedWaiter = client.get_waiter("acme_endpoint_deleted")
        certificate_validated_waiter: CertificateValidatedWaiter = client.get_waiter("certificate_validated")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

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

class AcmeDomainValidationDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationDeleted.html#ACM.Waiter.AcmeDomainValidationDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmedomainvalidationdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeDomainValidationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationDeleted.html#ACM.Waiter.AcmeDomainValidationDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmedomainvalidationdeletedwaiter)
        """

class AcmeDomainValidationValidatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationValidated.html#ACM.Waiter.AcmeDomainValidationValidated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmedomainvalidationvalidatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeDomainValidationRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeDomainValidationValidated.html#ACM.Waiter.AcmeDomainValidationValidated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmedomainvalidationvalidatedwaiter)
        """

class AcmeEndpointActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointActive.html#ACM.Waiter.AcmeEndpointActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmeendpointactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointActive.html#ACM.Waiter.AcmeEndpointActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmeendpointactivewaiter)
        """

class AcmeEndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointDeleted.html#ACM.Waiter.AcmeEndpointDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmeendpointdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAcmeEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/AcmeEndpointDeleted.html#ACM.Waiter.AcmeEndpointDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#acmeendpointdeletedwaiter)
        """

class CertificateValidatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/CertificateValidated.html#ACM.Waiter.CertificateValidated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#certificatevalidatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCertificateRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/waiter/CertificateValidated.html#ACM.Waiter.CertificateValidated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/waiters/#certificatevalidatedwaiter)
        """
