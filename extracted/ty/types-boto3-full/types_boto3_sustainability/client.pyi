"""
Type annotations for sustainability service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sustainability.client import SustainabilityClient

    session = Session()
    client: SustainabilityClient = session.client("sustainability")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetEstimatedCarbonEmissionsDimensionValuesPaginator,
    GetEstimatedCarbonEmissionsPaginator,
)
from .type_defs import (
    GetEstimatedCarbonEmissionsDimensionValuesRequestTypeDef,
    GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef,
    GetEstimatedCarbonEmissionsRequestTypeDef,
    GetEstimatedCarbonEmissionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("SustainabilityClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class SustainabilityClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability.html#Sustainability.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SustainabilityClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability.html#Sustainability.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#generate_presigned_url)
        """

    def get_estimated_carbon_emissions(
        self, **kwargs: Unpack[GetEstimatedCarbonEmissionsRequestTypeDef]
    ) -> GetEstimatedCarbonEmissionsResponseTypeDef:
        """
        Returns estimated carbon emission values based on customer grouping and
        filtering parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/client/get_estimated_carbon_emissions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#get_estimated_carbon_emissions)
        """

    def get_estimated_carbon_emissions_dimension_values(
        self, **kwargs: Unpack[GetEstimatedCarbonEmissionsDimensionValuesRequestTypeDef]
    ) -> GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef:
        """
        Returns the possible dimension values available for a customer's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/client/get_estimated_carbon_emissions_dimension_values.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#get_estimated_carbon_emissions_dimension_values)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_estimated_carbon_emissions_dimension_values"]
    ) -> GetEstimatedCarbonEmissionsDimensionValuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_estimated_carbon_emissions"]
    ) -> GetEstimatedCarbonEmissionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/client/#get_paginator)
        """
