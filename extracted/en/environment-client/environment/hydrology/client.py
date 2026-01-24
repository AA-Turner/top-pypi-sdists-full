"""
An async client for the UK Environment Agency's Hydrology API.
"""

import httpx
from .models import Station, Measure, Reading


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    # Avoid pre-reading body so VCR can capture content
    print(f"<<< Response: {response.status_code}")


class HydrologyClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Hydrology API.
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
            base_url="https://environment.data.gov.uk/hydrology",
            timeout=timeout,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(log_request)
            self.event_hooks["response"].append(log_response)

    async def get_stations(self, **params) -> list[Station]:
        """
        Returns a list of monitoring stations.

        Returns:
            list[Station]: A list of monitoring stations.
        """
        response = await self.get("/id/stations", params=params)
        response.raise_for_status()
        items = response.json()["items"]
        normalised = []
        for item in items:
            data = dict(item)
            if isinstance(data.get("status"), list) and data["status"]:
                first = data["status"][0]
                if isinstance(first, dict):
                    data["status"] = first.get("label") or first.get("@id")
            if isinstance(data.get("riverName"), list) and data["riverName"]:
                # Prefer the first provided river name
                data["riverName"] = data["riverName"][0]
            normalised.append(data)
        return [Station(**data) for data in normalised]

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
        if isinstance(data.get("status"), list) and data["status"]:
            first = data["status"][0]
            if isinstance(first, dict):
                data["status"] = first.get("label") or first.get("@id")
        return Station(**data)

    async def get_measures(self, **params) -> list[Measure]:
        """
        Returns a list of measures.

        Returns:
            list[Measure]: A list of measures.
        """
        response = await self.get("/id/measures", params=params)
        response.raise_for_status()
        items = response.json()["items"]
        normalised = []
        for item in items:
            data = dict(item)
            if isinstance(data.get("station"), dict):
                data["station"] = data["station"].get("@id")
            if isinstance(data.get("unit"), dict):
                data["unit"] = data["unit"].get("@id")
            normalised.append(data)
        return [Measure(**data) for data in normalised]

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
        data = response.json()["items"]
        if isinstance(data, list):
            data = data[0]
        if isinstance(data.get("station"), dict):
            data["station"] = data["station"].get("@id")
        if isinstance(data.get("unit"), dict):
            data["unit"] = data["unit"].get("@id")
        return Measure(**data)

    async def get_readings(
        self, measure_id: str | None = None, **params
    ) -> list[Reading]:
        """
        Returns a list of readings.

        Returns:
            list[Reading]: A list of readings.
        """
        # Hydrology readings are exposed per-measure
        if not measure_id:
            # Fallback: fetch the first measure and use it
            measures = await self.get_measures(_limit=1)
            if not measures:
                return []
            measure_id = measures[0].id.split("/")[-1]
        response = await self.get(f"/id/measures/{measure_id}/readings", params=params)
        response.raise_for_status()
        items = response.json()["items"]
        normalised = []
        for item in items:
            data = dict(item)
            if isinstance(data.get("measure"), dict):
                data["measure"] = data["measure"].get("@id")
            normalised.append(data)
        return [Reading(**data) for data in normalised]

    async def get_reading_by_id(self, reading_id: str) -> Reading:
        """
        Returns details of a single reading by ID.

        Args:
            reading_id (str): The ID of the reading.

        Returns:
            Reading: Details of the reading.
        """
        response = await self.get(f"/id/readings/{reading_id}")
        response.raise_for_status()
        data = response.json()["items"]
        if isinstance(data, list):
            data = data[0]
        return Reading(**data)
