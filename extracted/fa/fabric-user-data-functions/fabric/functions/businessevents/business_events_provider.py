# flake8: noqa: I003

import json
import logging
from azure.functions import HttpRequest

from fabric.functions.providers.base_fabricitem_provider import BaseFabricItemProvider
from fabric.functions.businessevents.fabric_business_events import FabricBusinessEventsClient
from fabric.internal.decorators.function_parameter_keywords import ADDITIONAL_PARAMETERS_HEADER


class BusinessEventsClientProvider(BaseFabricItemProvider):
    """Provider that transforms a FabricItem into a FabricBusinessEventsClient."""

    def create(self, item, req: HttpRequest = None, **kwargs) -> FabricBusinessEventsClient:
        """Create a FabricBusinessEventsClient from a FabricItem or existing client.
        
        Args:
            item: The FabricItem or FabricBusinessEventsClient containing endpoint info
            req: The HTTP request containing additional parameters in headers
            **kwargs: Contains decorator kwargs (e.g., allowedEvents)
            
        Returns:
            FabricBusinessEventsClient: An initialized client ready to publish events
        """
        # Parse header parameters specific to this provider
        header_params = {}
        if req and ADDITIONAL_PARAMETERS_HEADER in req.headers:
            try:
                additional_params_json = req.headers.get(ADDITIONAL_PARAMETERS_HEADER)
                additional_params = json.loads(additional_params_json)
                if isinstance(additional_params, dict):
                    header_params = additional_params
            except (json.JSONDecodeError, TypeError) as e:
                logging.warning(f"Failed to parse {ADDITIONAL_PARAMETERS_HEADER} header: {e}")

        # Construct client from item's endpoints — works uniformly for both
        # FabricItem and FabricBusinessEventsClient since both expose
        # .alias_name and .endpoints properties
        return FabricBusinessEventsClient(
            alias_name=item.alias_name,
            endpoints=item.endpoints,
            **{**kwargs, **header_params}
        )
