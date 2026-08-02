"""Integration tests for Jobs API - basic smoke tests to verify 200 responses."""

import os

import pytest

from pipebio.models.job_filter import JobFilter
from pipebio.pipebio_client import PipebioClient


class TestJobsIntegration:

    def setup_method(self):
        self.api_url = os.environ.get("PIPE_API_URL")
        if not self.api_url:
            pytest.skip("PIPE_API_URL not set - skipping integration test")

    def test_list_jobs(self):
        """List jobs returns 200 and valid response structure."""
        client = PipebioClient(url=self.api_url)
        response = client.jobs.list(page_limit=10)
        assert "data" in response
        assert isinstance(response["data"], list)

    def test_list_jobs_with_pagination(self):
        """List jobs with pagination returns 200."""
        client = PipebioClient(url=self.api_url)
        response = client.jobs.list(page_offset=0, page_limit=10)
        assert "data" in response
        assert isinstance(response["data"], list)
        assert len(response["data"]) <= 10

    def test_list_jobs_with_sort(self):
        """List jobs with sort returns 200."""
        client = PipebioClient(url=self.api_url)
        response = client.jobs.list(sort="-created_at", page_limit=10)
        assert "data" in response
        assert isinstance(response["data"], list)

    def test_list_jobs_with_filters(self):
        """List jobs with filters (POST _search) returns 200."""
        client = PipebioClient(url=self.api_url)
        filters = [
            JobFilter(key="status", comparator="=", value="COMPLETE"),
        ]
        response = client.jobs.list(filters=filters, page_limit=10)
        assert "data" in response
        assert isinstance(response["data"], list)
        assert len(response["data"]) <= 10

    def test_list_jobs_with_include_total_count(self):
        """List jobs with include_total_count returns 200 and optional total."""
        client = PipebioClient(url=self.api_url)
        response = client.jobs.list(include_total_count=True, page_limit=10)
        assert "data" in response
        assert isinstance(response["data"], list)
        if "total" in response:
            assert isinstance(response["total"], int)

    def test_get_job_from_list(self):
        """Get single job returns 200 when job exists."""
        client = PipebioClient(url=self.api_url)
        list_response = client.jobs.list(page_limit=1)
        jobs = list_response.get("data", [])
        if not jobs:
            pytest.skip("No jobs in org - cannot test get")
        job_id = jobs[0]["id"]
        job = client.jobs.get(job_id)
        assert "id" in job
        assert job["id"] == job_id
