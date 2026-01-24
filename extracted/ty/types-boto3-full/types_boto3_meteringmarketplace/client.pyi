"""
Type annotations for meteringmarketplace service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_meteringmarketplace.client import MarketplaceMeteringClient

    session = Session()
    client: MarketplaceMeteringClient = session.client("meteringmarketplace")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    BatchMeterUsageRequestTypeDef,
    BatchMeterUsageResultTypeDef,
    MeterUsageRequestTypeDef,
    MeterUsageResultTypeDef,
    RegisterUsageRequestTypeDef,
    RegisterUsageResultTypeDef,
    ResolveCustomerRequestTypeDef,
    ResolveCustomerResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("MarketplaceMeteringClient",)

class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    CustomerNotEntitledException: type[BotocoreClientError]
    DisabledApiException: type[BotocoreClientError]
    DuplicateRequestException: type[BotocoreClientError]
    ExpiredTokenException: type[BotocoreClientError]
    IdempotencyConflictException: type[BotocoreClientError]
    InternalServiceErrorException: type[BotocoreClientError]
    InvalidCustomerIdentifierException: type[BotocoreClientError]
    InvalidEndpointRegionException: type[BotocoreClientError]
    InvalidProductCodeException: type[BotocoreClientError]
    InvalidPublicKeyVersionException: type[BotocoreClientError]
    InvalidRegionException: type[BotocoreClientError]
    InvalidTagException: type[BotocoreClientError]
    InvalidTokenException: type[BotocoreClientError]
    InvalidUsageAllocationsException: type[BotocoreClientError]
    InvalidUsageDimensionException: type[BotocoreClientError]
    PlatformNotSupportedException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TimestampOutOfBoundsException: type[BotocoreClientError]

class MarketplaceMeteringClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MarketplaceMeteringClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace.html#MarketplaceMetering.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#generate_presigned_url)
        """

    def batch_meter_usage(
        self, **kwargs: Unpack[BatchMeterUsageRequestTypeDef]
    ) -> BatchMeterUsageResultTypeDef:
        """
        The <code>CustomerIdentifier</code> and <code>CustomerAWSAccountID</code> are
        mutually exclusive parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/batch_meter_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#batch_meter_usage)
        """

    def meter_usage(self, **kwargs: Unpack[MeterUsageRequestTypeDef]) -> MeterUsageResultTypeDef:
        """
        As a seller, your software hosted in the buyer's Amazon Web Services account
        uses this API action to emit metering records directly to Amazon Web Services
        Marketplace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/meter_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#meter_usage)
        """

    def register_usage(
        self, **kwargs: Unpack[RegisterUsageRequestTypeDef]
    ) -> RegisterUsageResultTypeDef:
        """
        Paid container software products sold through Amazon Web Services Marketplace
        must integrate with the Amazon Web Services Marketplace Metering Service and
        call the <code>RegisterUsage</code> operation for software entitlement and
        metering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/register_usage.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#register_usage)
        """

    def resolve_customer(
        self, **kwargs: Unpack[ResolveCustomerRequestTypeDef]
    ) -> ResolveCustomerResultTypeDef:
        """
        <code>ResolveCustomer</code> is called by a SaaS application during the
        registration process.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/meteringmarketplace/client/resolve_customer.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_meteringmarketplace/client/#resolve_customer)
        """
