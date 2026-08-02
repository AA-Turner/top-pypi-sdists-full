"""
Main interface for sustainability service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sustainability/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sustainability import (
        Client,
        GetEstimatedCarbonEmissionsDimensionValuesPaginator,
        GetEstimatedCarbonEmissionsPaginator,
        GetEstimatedWaterAllocationDimensionValuesPaginator,
        GetEstimatedWaterAllocationPaginator,
        SustainabilityClient,
    )

    session = get_session()
    async with session.create_client("sustainability") as client:
        client: SustainabilityClient
        ...


    get_estimated_carbon_emissions_dimension_values_paginator: GetEstimatedCarbonEmissionsDimensionValuesPaginator = client.get_paginator("get_estimated_carbon_emissions_dimension_values")
    get_estimated_carbon_emissions_paginator: GetEstimatedCarbonEmissionsPaginator = client.get_paginator("get_estimated_carbon_emissions")
    get_estimated_water_allocation_dimension_values_paginator: GetEstimatedWaterAllocationDimensionValuesPaginator = client.get_paginator("get_estimated_water_allocation_dimension_values")
    get_estimated_water_allocation_paginator: GetEstimatedWaterAllocationPaginator = client.get_paginator("get_estimated_water_allocation")
    ```
"""

from .client import SustainabilityClient
from .paginator import (
    GetEstimatedCarbonEmissionsDimensionValuesPaginator,
    GetEstimatedCarbonEmissionsPaginator,
    GetEstimatedWaterAllocationDimensionValuesPaginator,
    GetEstimatedWaterAllocationPaginator,
)

Client = SustainabilityClient

__all__ = (
    "Client",
    "GetEstimatedCarbonEmissionsDimensionValuesPaginator",
    "GetEstimatedCarbonEmissionsPaginator",
    "GetEstimatedWaterAllocationDimensionValuesPaginator",
    "GetEstimatedWaterAllocationPaginator",
    "SustainabilityClient",
)
