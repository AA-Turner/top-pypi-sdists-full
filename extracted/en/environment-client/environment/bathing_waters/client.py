"""
An async client for the UK Environment Agency's Bathing Water Quality API.

This client provides access to information about bathing waters in England.
"""

import httpx
from .models import (
    BathingWater,
    SamplingPoint,
    SampleAssessment,
    ComplianceAssessment,
    PollutionIncident,
)


async def log_request(request):
    print(f">>> Request: {request.method} {request.url}")


async def log_response(response):
    # Avoid pre-reading body so VCR can capture content
    print(f"<<< Response: {response.status_code}")


class BathingWatersClient(httpx.AsyncClient):
    """
    An async client for the UK Environment Agency's Bathing Water Quality API.
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
            base_url="https://environment.data.gov.uk",
            timeout=timeout,
            follow_redirects=True,
            **kwargs,
        )
        if verbose:
            self.event_hooks["request"].append(log_request)
            self.event_hooks["response"].append(log_response)

    async def get_bathing_waters(self, **params) -> list[BathingWater]:
        """
        Returns a list of bathing waters.

        Returns:
            list[BathingWater]: A list of bathing waters.
        """
        response = await self.get("/doc/bathing-water.json", params=params)
        response.raise_for_status()
        return [BathingWater(**item) for item in response.json()["result"]["items"]]

    async def get_bathing_water_by_id(self, bathing_water_id: str) -> BathingWater:
        """
        Returns details of a single bathing water by ID.

        Args:
            bathing_water_id (str): The ID of the bathing water.

        Returns:
            BathingWater: Details of the bathing water.
        """
        response = await self.get(f"/id/bathing-water/{bathing_water_id}")
        response.raise_for_status()
        return BathingWater(**response.json()["items"][0])

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

    async def get_sample_assessments(self, **params) -> list[SampleAssessment]:
        """
        Returns a list of sample assessments.

        Returns:
            list[SampleAssessment]: A list of sample assessments.
        """
        response = await self.get("/id/sample-assessment", params=params)
        response.raise_for_status()
        return [SampleAssessment(**item) for item in response.json()["items"]]

    async def get_sample_assessment_by_id(
        self, sample_assessment_id: str
    ) -> SampleAssessment:
        """
        Returns details of a single sample assessment by ID.

        Args:
            sample_assessment_id (str): The ID of the sample assessment.

        Returns:
            SampleAssessment: Details of the sample assessment.
        """
        response = await self.get(f"/id/sample-assessment/{sample_assessment_id}")
        response.raise_for_status()
        return SampleAssessment(**response.json()["items"][0])

    async def get_compliance_assessments(self, **params) -> list[ComplianceAssessment]:
        """
        Returns a list of compliance assessments.

        Returns:
            list[ComplianceAssessment]: A list of compliance assessments.
        """
        response = await self.get("/id/compliance-assessment", params=params)
        response.raise_for_status()
        return [ComplianceAssessment(**item) for item in response.json()["items"]]

    async def get_compliance_assessment_by_id(
        self, compliance_assessment_id: str
    ) -> ComplianceAssessment:
        """
        Returns details of a single compliance assessment by ID.

        Args:
            compliance_assessment_id (str): The ID of the compliance assessment.

        Returns:
            ComplianceAssessment: Details of the compliance assessment.
        """
        response = await self.get(
            f"/id/compliance-assessment/{compliance_assessment_id}"
        )
        response.raise_for_status()
        return ComplianceAssessment(**response.json()["items"][0])

    async def get_pollution_incidents(self, **params) -> list[PollutionIncident]:
        """
        Returns a list of pollution incidents.

        Returns:
            list[PollutionIncident]: A list of pollution incidents.
        """
        response = await self.get("/id/pollution-incident", params=params)
        response.raise_for_status()
        return [PollutionIncident(**item) for item in response.json()["items"]]

    async def get_pollution_incident_by_id(
        self, pollution_incident_id: str
    ) -> PollutionIncident:
        """
        Returns details of a single pollution incident by ID.

        Args:
            pollution_incident_id (str): The ID of the pollution incident.

        Returns:
            PollutionIncident: Details of the pollution incident.
        """
        response = await self.get(f"/id/pollution-incident/{pollution_incident_id}")
        response.raise_for_status()
        return PollutionIncident(**response.json()["items"][0])
