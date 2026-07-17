"""
Main interface for sustainability service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sustainability/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sustainability import (
        Client,
        GetEstimatedCarbonEmissionsDimensionValuesPaginator,
        GetEstimatedCarbonEmissionsPaginator,
        GetEstimatedWaterAllocationDimensionValuesPaginator,
        GetEstimatedWaterAllocationPaginator,
        SustainabilityClient,
    )

    session = Session()
    client: SustainabilityClient = session.client("sustainability")

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
