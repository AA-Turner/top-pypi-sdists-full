"""
Type annotations for sustainability service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sustainability.client import SustainabilityClient
    from types_aiobotocore_sustainability.paginator import (
        GetEstimatedCarbonEmissionsDimensionValuesPaginator,
        GetEstimatedCarbonEmissionsPaginator,
        GetEstimatedWaterAllocationDimensionValuesPaginator,
        GetEstimatedWaterAllocationPaginator,
    )

    session = get_session()
    with session.create_client("sustainability") as client:
        client: SustainabilityClient

        get_estimated_carbon_emissions_dimension_values_paginator: GetEstimatedCarbonEmissionsDimensionValuesPaginator = client.get_paginator("get_estimated_carbon_emissions_dimension_values")
        get_estimated_carbon_emissions_paginator: GetEstimatedCarbonEmissionsPaginator = client.get_paginator("get_estimated_carbon_emissions")
        get_estimated_water_allocation_dimension_values_paginator: GetEstimatedWaterAllocationDimensionValuesPaginator = client.get_paginator("get_estimated_water_allocation_dimension_values")
        get_estimated_water_allocation_paginator: GetEstimatedWaterAllocationPaginator = client.get_paginator("get_estimated_water_allocation")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetEstimatedCarbonEmissionsDimensionValuesRequestPaginateTypeDef,
    GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef,
    GetEstimatedCarbonEmissionsRequestPaginateTypeDef,
    GetEstimatedCarbonEmissionsResponseTypeDef,
    GetEstimatedWaterAllocationDimensionValuesRequestPaginateTypeDef,
    GetEstimatedWaterAllocationDimensionValuesResponseTypeDef,
    GetEstimatedWaterAllocationRequestPaginateTypeDef,
    GetEstimatedWaterAllocationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetEstimatedCarbonEmissionsDimensionValuesPaginator",
    "GetEstimatedCarbonEmissionsPaginator",
    "GetEstimatedWaterAllocationDimensionValuesPaginator",
    "GetEstimatedWaterAllocationPaginator",
)


if TYPE_CHECKING:
    _GetEstimatedCarbonEmissionsDimensionValuesPaginatorBase = AioPaginator[
        GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef
    ]
else:
    _GetEstimatedCarbonEmissionsDimensionValuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEstimatedCarbonEmissionsDimensionValuesPaginator(
    _GetEstimatedCarbonEmissionsDimensionValuesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissionsDimensionValues.html#Sustainability.Paginator.GetEstimatedCarbonEmissionsDimensionValues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedcarbonemissionsdimensionvaluespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedCarbonEmissionsDimensionValuesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissionsDimensionValues.html#Sustainability.Paginator.GetEstimatedCarbonEmissionsDimensionValues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedcarbonemissionsdimensionvaluespaginator)
        """


if TYPE_CHECKING:
    _GetEstimatedCarbonEmissionsPaginatorBase = AioPaginator[
        GetEstimatedCarbonEmissionsResponseTypeDef
    ]
else:
    _GetEstimatedCarbonEmissionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEstimatedCarbonEmissionsPaginator(_GetEstimatedCarbonEmissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissions.html#Sustainability.Paginator.GetEstimatedCarbonEmissions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedcarbonemissionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedCarbonEmissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEstimatedCarbonEmissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissions.html#Sustainability.Paginator.GetEstimatedCarbonEmissions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedcarbonemissionspaginator)
        """


if TYPE_CHECKING:
    _GetEstimatedWaterAllocationDimensionValuesPaginatorBase = AioPaginator[
        GetEstimatedWaterAllocationDimensionValuesResponseTypeDef
    ]
else:
    _GetEstimatedWaterAllocationDimensionValuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEstimatedWaterAllocationDimensionValuesPaginator(
    _GetEstimatedWaterAllocationDimensionValuesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocationDimensionValues.html#Sustainability.Paginator.GetEstimatedWaterAllocationDimensionValues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedwaterallocationdimensionvaluespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedWaterAllocationDimensionValuesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEstimatedWaterAllocationDimensionValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocationDimensionValues.html#Sustainability.Paginator.GetEstimatedWaterAllocationDimensionValues.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedwaterallocationdimensionvaluespaginator)
        """


if TYPE_CHECKING:
    _GetEstimatedWaterAllocationPaginatorBase = AioPaginator[
        GetEstimatedWaterAllocationResponseTypeDef
    ]
else:
    _GetEstimatedWaterAllocationPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetEstimatedWaterAllocationPaginator(_GetEstimatedWaterAllocationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocation.html#Sustainability.Paginator.GetEstimatedWaterAllocation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedwaterallocationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedWaterAllocationRequestPaginateTypeDef]
    ) -> AioPageIterator[GetEstimatedWaterAllocationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocation.html#Sustainability.Paginator.GetEstimatedWaterAllocation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/paginators/#getestimatedwaterallocationpaginator)
        """
