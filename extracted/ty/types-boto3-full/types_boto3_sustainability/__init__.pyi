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
        SustainabilityClient,
    )

    session = Session()
    client: SustainabilityClient = session.client("sustainability")

    get_estimated_carbon_emissions_dimension_values_paginator: GetEstimatedCarbonEmissionsDimensionValuesPaginator = client.get_paginator("get_estimated_carbon_emissions_dimension_values")
    get_estimated_carbon_emissions_paginator: GetEstimatedCarbonEmissionsPaginator = client.get_paginator("get_estimated_carbon_emissions")
    ```
"""

from .client import SustainabilityClient
from .paginator import (
    GetEstimatedCarbonEmissionsDimensionValuesPaginator,
    GetEstimatedCarbonEmissionsPaginator,
)

Client = SustainabilityClient

__all__ = (
    "Client",
    "GetEstimatedCarbonEmissionsDimensionValuesPaginator",
    "GetEstimatedCarbonEmissionsPaginator",
    "SustainabilityClient",
)
