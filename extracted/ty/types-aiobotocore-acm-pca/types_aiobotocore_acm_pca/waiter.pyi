"""
Type annotations for acm-pca service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_acm_pca.client import ACMPCAClient
    from types_aiobotocore_acm_pca.waiter import (
        AuditReportCreatedWaiter,
        CertificateAuthorityCSRCreatedWaiter,
        CertificateIssuedWaiter,
    )

    session = get_session()
    async with session.create_client("acm-pca") as client:
        client: ACMPCAClient

        audit_report_created_waiter: AuditReportCreatedWaiter = client.get_waiter("audit_report_created")
        certificate_authority_csr_created_waiter: CertificateAuthorityCSRCreatedWaiter = client.get_waiter("certificate_authority_csr_created")
        certificate_issued_waiter: CertificateIssuedWaiter = client.get_waiter("certificate_issued")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeCertificateAuthorityAuditReportRequestWaitTypeDef,
    GetCertificateAuthorityCsrRequestWaitTypeDef,
    GetCertificateRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "AuditReportCreatedWaiter",
    "CertificateAuthorityCSRCreatedWaiter",
    "CertificateIssuedWaiter",
)

class AuditReportCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/AuditReportCreated.html#ACMPCA.Waiter.AuditReportCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/#auditreportcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCertificateAuthorityAuditReportRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/AuditReportCreated.html#ACMPCA.Waiter.AuditReportCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/#auditreportcreatedwaiter)
        """

class CertificateAuthorityCSRCreatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateAuthorityCSRCreated.html#ACMPCA.Waiter.CertificateAuthorityCSRCreated)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/#certificateauthoritycsrcreatedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCertificateAuthorityCsrRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateAuthorityCSRCreated.html#ACMPCA.Waiter.CertificateAuthorityCSRCreated.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/#certificateauthoritycsrcreatedwaiter)
        """

class CertificateIssuedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateIssued.html#ACMPCA.Waiter.CertificateIssued)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/#certificateissuedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCertificateRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm-pca/waiter/CertificateIssued.html#ACMPCA.Waiter.CertificateIssued.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm_pca/waiters/#certificateissuedwaiter)
        """
