"""
Type annotations for sustainability service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_sustainability.client import SustainabilityClient
    from types_boto3_sustainability.paginator import (
        GetEstimatedCarbonEmissionsDimensionValuesPaginator,
        GetEstimatedCarbonEmissionsPaginator,
        GetEstimatedWaterAllocationDimensionValuesPaginator,
        GetEstimatedWaterAllocationPaginator,
    )

    session = Session()
    client: SustainabilityClient = session.client("sustainability")

    get_estimated_carbon_emissions_dimension_values_paginator: GetEstimatedCarbonEmissionsDimensionValuesPaginator = client.get_paginator("get_estimated_carbon_emissions_dimension_values")
    get_estimated_carbon_emissions_paginator: GetEstimatedCarbonEmissionsPaginator = client.get_paginator("get_estimated_carbon_emissions")
    get_estimated_water_allocation_dimension_values_paginator: GetEstimatedWaterAllocationDimensionValuesPaginator = client.get_paginator("get_estimated_water_allocation_dimension_values")
    get_estimated_water_allocation_paginator: GetEstimatedWaterAllocationPaginator = client.get_paginator("get_estimated_water_allocation")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _GetEstimatedCarbonEmissionsDimensionValuesPaginatorBase = Paginator[
        GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef
    ]
else:
    _GetEstimatedCarbonEmissionsDimensionValuesPaginatorBase = Paginator  # type: ignore[assignment]

class GetEstimatedCarbonEmissionsDimensionValuesPaginator(
    _GetEstimatedCarbonEmissionsDimensionValuesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissionsDimensionValues.html#Sustainability.Paginator.GetEstimatedCarbonEmissionsDimensionValues)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedcarbonemissionsdimensionvaluespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedCarbonEmissionsDimensionValuesRequestPaginateTypeDef]
    ) -> PageIterator[GetEstimatedCarbonEmissionsDimensionValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissionsDimensionValues.html#Sustainability.Paginator.GetEstimatedCarbonEmissionsDimensionValues.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedcarbonemissionsdimensionvaluespaginator)
        """

if TYPE_CHECKING:
    _GetEstimatedCarbonEmissionsPaginatorBase = Paginator[
        GetEstimatedCarbonEmissionsResponseTypeDef
    ]
else:
    _GetEstimatedCarbonEmissionsPaginatorBase = Paginator  # type: ignore[assignment]

class GetEstimatedCarbonEmissionsPaginator(_GetEstimatedCarbonEmissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissions.html#Sustainability.Paginator.GetEstimatedCarbonEmissions)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedcarbonemissionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedCarbonEmissionsRequestPaginateTypeDef]
    ) -> PageIterator[GetEstimatedCarbonEmissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedCarbonEmissions.html#Sustainability.Paginator.GetEstimatedCarbonEmissions.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedcarbonemissionspaginator)
        """

if TYPE_CHECKING:
    _GetEstimatedWaterAllocationDimensionValuesPaginatorBase = Paginator[
        GetEstimatedWaterAllocationDimensionValuesResponseTypeDef
    ]
else:
    _GetEstimatedWaterAllocationDimensionValuesPaginatorBase = Paginator  # type: ignore[assignment]

class GetEstimatedWaterAllocationDimensionValuesPaginator(
    _GetEstimatedWaterAllocationDimensionValuesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocationDimensionValues.html#Sustainability.Paginator.GetEstimatedWaterAllocationDimensionValues)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedwaterallocationdimensionvaluespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedWaterAllocationDimensionValuesRequestPaginateTypeDef]
    ) -> PageIterator[GetEstimatedWaterAllocationDimensionValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocationDimensionValues.html#Sustainability.Paginator.GetEstimatedWaterAllocationDimensionValues.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedwaterallocationdimensionvaluespaginator)
        """

if TYPE_CHECKING:
    _GetEstimatedWaterAllocationPaginatorBase = Paginator[
        GetEstimatedWaterAllocationResponseTypeDef
    ]
else:
    _GetEstimatedWaterAllocationPaginatorBase = Paginator  # type: ignore[assignment]

class GetEstimatedWaterAllocationPaginator(_GetEstimatedWaterAllocationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocation.html#Sustainability.Paginator.GetEstimatedWaterAllocation)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedwaterallocationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetEstimatedWaterAllocationRequestPaginateTypeDef]
    ) -> PageIterator[GetEstimatedWaterAllocationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sustainability/paginator/GetEstimatedWaterAllocation.html#Sustainability.Paginator.GetEstimatedWaterAllocation.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/paginators/#getestimatedwaterallocationpaginator)
        """
