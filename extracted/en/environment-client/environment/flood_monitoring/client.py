"""
An async client for the UK Environment Agency's Real-time flood-monitoring API.

This client provides access to near real-time information about flood warnings, flood areas,
water levels, and monitoring stations.

The API is provided as open data under the Open Government Licence with no requirement for registration.

For more information, see the official documentation:
https://environment.data.gov.uk/flood-monitoring/doc/reference
"""

import httpx
from .models import FloodWarning, FloodArea, Station, Measure, Reading


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    # Avoid pre-reading body so VCR can capture content
    print(f"<<< Response: {response.status_code}")


class FloodClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Real-time flood-monitoring API.
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
            base_url="https://environment.data.gov.uk/flood-monitoring",
            timeout=timeout,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(log_request)
            self.event_hooks["response"].append(log_response)

    async def get_flood_warnings(self, **params) -> list[FloodWarning]:
        """
        Returns a list of current flood warnings.

        For a list of available parameters, see the API documentation:
        https://environment.data.gov.uk/flood-monitoring/doc/reference#/paths/~1floods/get

        Args:
            **params: Query parameters to filter the results.

        Returns:
            list[FloodWarning]: A list of flood warnings.
        """
        response = await self.get("/id/floods", params=params)
        response.raise_for_status()
        return [FloodWarning(**item) for item in response.json()["items"]]

    async def get_flood_warning_by_id(self, warning_id: str) -> FloodWarning:
        """
        Returns details of a single flood warning by ID.

        Args:
            warning_id (str): The ID of the flood warning.

        Returns:
            FloodWarning: Details of the flood warning.
        """
        response = await self.get(f"/id/floods/{warning_id}")
        response.raise_for_status()
        return FloodWarning(**response.json()["items"][0])

    async def get_flood_areas(self, **params) -> list[FloodArea]:
        """
        Returns a list of flood areas.

        For a list of available parameters, see the API documentation:
        https://environment.data.gov.uk/flood-monitoring/doc/reference#/paths/~1flood-areas/get

        Args:
            **params: Query parameters to filter the results.

        Returns:
            list[FloodArea]: A list of flood areas.
        """
        # Flood areas are identifiable resources under the /id namespace
        # See: https://environment.data.gov.uk/flood-monitoring/doc/reference#flood-areas
        response = await self.get("/id/floodAreas", params=params)
        response.raise_for_status()
        return [FloodArea(**item) for item in response.json()["items"]]

    async def get_flood_area_by_id(self, area_id: str) -> FloodArea:
        """
        Returns details of a single flood area by ID.

        Args:
            area_id (str): The ID of the flood area.

        Returns:
            FloodArea: Details of the flood area.
        """
        # Flood area details endpoint follows the same /id/floodAreas pattern
        response = await self.get(f"/id/floodAreas/{area_id}")
        response.raise_for_status()
        return FloodArea(**response.json()["items"][0])

    async def get_stations(self, **params) -> list[Station]:
        """
        Returns a list of monitoring stations.

        For a list of available parameters, see the API documentation:
        https://environment.data.gov.uk/flood-monitoring/doc/reference#/paths/~1stations/get

        Args:
            **params: Query parameters to filter the results.

        Returns:
            list[Station]: A list of monitoring stations.
        """
        response = await self.get("/id/stations", params=params)
        response.raise_for_status()
        return [Station(**item) for item in response.json()["items"]]

    async def get_station_by_id(self, station_id: str) -> Station:
        """
        Returns details of a single monitoring station by ID.

        Args:
            station_id (str): The ID of the monitoring station.

        Returns:
            Station: Details of the monitoring station.
        """
        response = await self.get(f"/id/stations/{station_id}")
        response.raise_for_status()
        return Station(**response.json()["items"][0])

    async def get_measures(self, **params) -> list[Measure]:
        """
        Returns a list of measures.

        For a list of available parameters, see the API documentation:
        https://environment.data.gov.uk/flood-monitoring/doc/reference#/paths/~1measures/get

        Args:
            **params: Query parameters to filter the results.

        Returns:
            list[Measure]: A list of measures.
        """
        response = await self.get("/id/measures", params=params)
        response.raise_for_status()
        return [Measure(**item) for item in response.json()["items"]]

    async def get_measure_by_id(self, measure_id: str) -> Measure:
        """
        Returns details of a single measure by ID.

        Args:
            measure_id (str): The ID of the measure.

        Returns:
            Measure: Details of the measure.
        """
        response = await self.get(f"/id/measures/{measure_id}")
        response.raise_for_status()
        return Measure(**response.json()["items"][0])

    async def get_readings(self, **params) -> list[Reading]:
        """
        Returns a list of readings.

        For a list of available parameters, see the API documentation:
        https://environment.data.gov.uk/flood-monitoring/doc/reference#/paths/~1data~1readings/get

        Args:
            **params: Query parameters to filter the results.

        Returns:
            list[Reading]: A list of readings.
        """
        response = await self.get(
            "/data/readings",
            params=params,
        )
        response.raise_for_status()
        return [Reading(**item) for item in response.json()["items"]]

    async def get_reading_by_id(self, reading_id: str) -> Reading:
        """
        Returns details of a single reading by ID.

        Args:
            reading_id (str): The ID of the reading.

        Returns:
            Reading: Details of the reading.
        """
        response = await self.get(f"/data/readings/{reading_id}")
        response.raise_for_status()
        return Reading(**response.json()["items"][0])
