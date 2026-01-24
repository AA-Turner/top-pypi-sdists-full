"""
An async client for the UK Environment Agency's Rainfall API.
"""

import httpx
from .models import Station, Measure, Reading


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    # Avoid pre-reading body so VCR can capture content
    print(f"<<< Response: {response.status_code}")


class RainfallClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Rainfall API.
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

    async def get_stations(self, **params) -> list[Station]:
        """
        Returns a list of rainfall monitoring stations.

        Returns:
            list[Station]: A list of rainfall monitoring stations.
        """
        params = {"parameter": "rainfall", **params}
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
        data = response.json()["items"]
        if isinstance(data, list):
            data = data[0]
        # Normalise measures field to a list if a single object is returned
        if isinstance(data.get("measures"), dict):
            data["measures"] = [data["measures"]]
        return Station(**data)

    async def get_measures(self, **params) -> list[Measure]:
        """
        Returns a list of rainfall measures.

        Returns:
            list[Measure]: A list of rainfall measures.
        """
        params = {"parameter": "rainfall", **params}
        response = await self.get("/id/measures", params=params)
        response.raise_for_status()
        return [Measure(**item) for item in response.json()["items"]]

    async def get_measure_by_id(self, measure_id: str) -> Measure:
        """
        Returns details of a single rainfall measure by ID.

        Args:
            measure_id (str): The ID of the measure.

        Returns:
            Measure: Details of the measure.
        """
        response = await self.get(f"/id/measures/{measure_id}")
        response.raise_for_status()
        data = response.json()["items"]
        if isinstance(data, list):
            data = data[0]
        return Measure(**data)

    async def get_readings(self, **params) -> list[Reading]:
        """
        Returns a list of rainfall readings.

        Returns:
            list[Reading]: A list of rainfall readings.
        """
        params = {"parameter": "rainfall", **params}
        response = await self.get("/data/readings", params=params)
        response.raise_for_status()
        return [Reading(**item) for item in response.json()["items"]]

    async def get_reading_by_id(self, reading_id: str) -> Reading:
        """
        Returns details of a single rainfall reading by ID.

        Args:
            reading_id (str): The ID of the reading.

        Returns:
            Reading: Details of the reading.
        """
        response = await self.get(f"/data/readings/{reading_id}")
        response.raise_for_status()
        data = response.json()["items"]
        if isinstance(data, list):
            data = data[0]
        # Ensure measure field is a string ID
        if isinstance(data.get("measure"), dict):
            data["measure"] = data["measure"].get("@id")
        return Reading(**data)
