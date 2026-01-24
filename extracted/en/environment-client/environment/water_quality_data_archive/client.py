"""
An async client for the UK Environment Agency's Water Quality Data Archive API.

NOTE: This API will be replaced later this year (Spring/Summer 2025).
"""

import httpx
from .models import (
    SamplingPoint,
    Sample,
    Measurement,
    Determinand,
    Unit,
    DeterminandGroup,
    Purpose,
    EAArea,
    EASubArea,
    SampledMaterialType,
    SamplingPointType,
    SamplingPointTypeGroup,
)


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    # Avoid pre-reading body so VCR can capture content
    print(f"<<< Response: {response.status_code}")


class WaterQualityDataArchiveClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Water Quality Data Archive API.

    NOTE: The Water Quality Archive (WQA) APIs are being replaced. As of
    Spring/Summer 2025 the existing endpoints may return 404 and could stop
    working entirely. See: https://environment.data.gov.uk/apiportal/support
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
            base_url="https://environment.data.gov.uk/water-quality/view",
            timeout=timeout,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(log_request)
            self.event_hooks["response"].append(log_response)

        # Warn users that this API is being replaced and may be unavailable.
        try:
            import warnings

            warnings.warn(
                (
                    "WaterQualityDataArchiveClient: The Water Quality Archive (WQA) "
                    "APIs are being replaced in 2025. Existing endpoints may return 404 "
                    "and could stop working. See DEFRA support pages for updates."
                ),
                category=DeprecationWarning,
                stacklevel=2,
            )
        except Exception:
            # Best-effort warning only
            pass

    async def get_sampling_points(self, **params) -> list[SamplingPoint]:
        """
        Returns a list of sampling points.

        Returns:
            list[SamplingPoint]: A list of sampling points.
        """
        response = await self.get("/id/sampling-point", params=params)
        response.raise_for_status()
        return [SamplingPoint(**item) for item in response.json()["items"]]

    async def get_sampling_point_by_id(self, sampling_point_id: str) -> SamplingPoint:
        """
        Returns details of a single sampling point by ID.

        Args:
            sampling_point_id (str): The ID of the sampling point.

        Returns:
            SamplingPoint: Details of the sampling point.
        """
        response = await self.get(f"/id/sampling-point/{sampling_point_id}")
        response.raise_for_status()
        return SamplingPoint(**response.json()["items"][0])

    async def get_samples(self, **params) -> list[Sample]:
        """
        Returns a list of samples.

        Returns:
            list[Sample]: A list of samples.
        """
        response = await self.get("/data/sample", params=params)
        response.raise_for_status()
        return [Sample(**item) for item in response.json()["items"]]

    async def get_sample_by_id(self, sample_id: str) -> Sample:
        """
        Returns details of a single sample by ID.

        Args:
            sample_id (str): The ID of the sample.

        Returns:
            Sample: Details of the sample.
        """
        response = await self.get(f"/data/sample/{sample_id}")
        response.raise_for_status()
        return Sample(**response.json()["items"][0])

    async def get_measurements(self, **params) -> list[Measurement]:
        """
        Returns a list of measurements.

        Returns:
            list[Measurement]: A list of measurements.
        """
        response = await self.get("/data/measurement", params=params)
        response.raise_for_status()
        return [Measurement(**item) for item in response.json()["items"]]

    async def get_measurement_by_id(self, measurement_id: str) -> Measurement:
        """
        Returns details of a single measurement by ID.

        Args:
            measurement_id (str): The ID of the measurement.

        Returns:
            Measurement: Details of the measurement.
        """
        response = await self.get(f"/data/measurement/{measurement_id}")
        response.raise_for_status()
        return Measurement(**response.json()["items"][0])

    async def get_determinands(self, **params) -> list[Determinand]:
        """
        Returns a list of determinands.

        Returns:
            list[Determinand]: A list of determinands.
        """
        response = await self.get("/def/determinands", params=params)
        response.raise_for_status()
        return [Determinand(**item) for item in response.json()["items"]]

    async def get_units(self, **params) -> list[Unit]:
        """
        Returns a list of units.

        Returns:
            list[Unit]: A list of units.
        """
        response = await self.get("/def/units", params=params)
        response.raise_for_status()
        return [Unit(**item) for item in response.json()["items"]]

    async def get_determinand_groups(self, **params) -> list[DeterminandGroup]:
        """
        Returns a list of determinand groups.

        Returns:
            list[DeterminandGroup]: A list of determinand groups.
        """
        response = await self.get("/def/determinand-groups", params=params)
        response.raise_for_status()
        return [DeterminandGroup(**item) for item in response.json()["items"]]

    async def get_purposes(self, **params) -> list[Purpose]:
        """
        Returns a list of purposes.

        Returns:
            list[Purpose]: A list of purposes.
        """
        response = await self.get("/def/purposes", params=params)
        response.raise_for_status()
        return [Purpose(**item) for item in response.json()["items"]]

    async def get_ea_areas(self, **params) -> list[EAArea]:
        """
        Returns a list of EA areas.

        Returns:
            list[EAArea]: A list of EA areas.
        """
        response = await self.get("/id/ea-area", params=params)
        response.raise_for_status()
        return [EAArea(**item) for item in response.json()["items"]]

    async def get_ea_subareas(self, **params) -> list[EASubArea]:
        """
        Returns a list of EA subareas.

        Returns:
            list[EASubArea]: A list of EA subareas.
        """
        response = await self.get("/id/ea-subarea", params=params)
        response.raise_for_status()
        return [EASubArea(**item) for item in response.json()["items"]]

    async def get_sampled_material_types(self, **params) -> list[SampledMaterialType]:
        """
        Returns a list of sampled material types.

        Returns:
            list[SampledMaterialType]: A list of sampled material types.
        """
        response = await self.get("/def/sampled-material-types", params=params)
        response.raise_for_status()
        return [SampledMaterialType(**item) for item in response.json()["items"]]

    async def get_sampling_point_types(self, **params) -> list[SamplingPointType]:
        """
        Returns a list of sampling point types.

        Returns:
            list[SamplingPointType]: A list of sampling point types.
        """
        response = await self.get("/def/sampling-point-types", params=params)
        response.raise_for_status()
        return [SamplingPointType(**item) for item in response.json()["items"]]

    async def get_sampling_point_type_groups(
        self, **params
    ) -> list[SamplingPointTypeGroup]:
        """
        Returns a list of sampling point type groups.

        Returns:
            list[SamplingPointTypeGroup]: A list of sampling point type groups.
        """
        response = await self.get("/def/sampling-point-type-groups", params=params)
        response.raise_for_status()
        return [SamplingPointTypeGroup(**item) for item in response.json()["items"]]

    async def get_batch_measurements(self, **params) -> list[Measurement]:
        """
        Returns a list of measurements from a batch query.

        Returns:
            list[Measurement]: A list of measurements.
        """
        response = await self.get("/batch/measurement", params=params)
        response.raise_for_status()
        return [Measurement(**item) for item in response.json()["items"]]
