"""
An async client for the UK Environment Agency's Catchment Data API.
"""

import httpx
from .models import CatchmentData


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    await response.aread()
    print(f"<<< Response: {response.status_code}")
    print(response.text)


class CatchmentDataClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Catchment Data API.
    """

    def __init__(self, timeout=30.0, verbose=False, **kwargs):
        """
        Initializes the client.

        Args:
            timeout (float, optional): The timeout for requests in seconds. Defaults to 30.0.
            verbose (bool, optional): If True, logs requests and responses. Defaults to False.
            **kwargs: Additional keyword arguments to pass to the httpx.AsyncClient constructor.
        """
        super().__init__(
            base_url="https://environment.data.gov.uk/catchment-planning",
            timeout=timeout,
            follow_redirects=True,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(log_request)
            self.event_hooks["response"].append(log_response)

    async def get_catchment_data(self, **params) -> list[CatchmentData]:
        """
        Returns a list of catchment data.

        NOTE: The actual API endpoint for Catchment Data could not be determined from the available documentation.
        This method currently returns an empty list as a placeholder.

        Returns:
            list[CatchmentData]: A list of catchment data.
        """
        # TODO: Determine the correct API endpoint for Catchment Data
        # response = await self.get("/data.json", params=params)
        # response.raise_for_status()
        # return [CatchmentData(**item) for item in response.json()["items"]]
        return []
