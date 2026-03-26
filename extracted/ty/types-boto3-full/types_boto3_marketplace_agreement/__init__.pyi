"""
Main interface for marketplace-agreement service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_marketplace_agreement/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_marketplace_agreement import (
        AgreementServiceClient,
        Client,
        ListAgreementPaymentRequestsPaginator,
    )

    session = Session()
    client: AgreementServiceClient = session.client("marketplace-agreement")

    list_agreement_payment_requests_paginator: ListAgreementPaymentRequestsPaginator = client.get_paginator("list_agreement_payment_requests")
    ```
"""

from .client import AgreementServiceClient
from .paginator import ListAgreementPaymentRequestsPaginator

Client = AgreementServiceClient

__all__ = ("AgreementServiceClient", "Client", "ListAgreementPaymentRequestsPaginator")
