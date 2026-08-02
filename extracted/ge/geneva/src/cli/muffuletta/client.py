# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""REST client for Geneva Console API."""

import logging
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

import httpx
from .models import Cluster, Job, JobStatus, Manifest
from pydantic import ValidationError

log = logging.getLogger(__name__)


class GenevaClientError(Exception):
    """Geneva API client error."""


class GenevaClient:
    """Client for Geneva Console API."""

    def __init__(self, base_url: str, db_uri: str, timeout: float = 30.0) -> None:
        """
        Initialize the Geneva client.

        Args:
            base_url: Base URL of the console API (e.g., http://localhost:8000)
            db_uri: Database URI for the Geneva cluster
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        # The backend prepends ROOT_URI to the db_uri_encoded value, so we
        # must send just the relative path portion.
        # - db://data          → "data"
        # - s3://bucket/data   → "data"  (path after the bucket/netloc)
        if db_uri.startswith("db://"):
            self.db_uri_encoded = db_uri.removeprefix("db://")
        else:
            parsed = urlparse(db_uri)
            self.db_uri_encoded = parsed.path.lstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

        log.debug("GenevaClient initialized:")
        log.debug("  base_url: %s", self.base_url)
        log.debug("  db_uri: %s (encoded: %s)", db_uri, self.db_uri_encoded)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "GenevaClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an API request."""
        url = f"{self.base_url}{path}"

        if params is None:
            params = {}
        params["db_uri_encoded"] = self.db_uri_encoded

        log.debug("Request: %s %s", method, url)
        log.debug("  params: %s", params)
        if json:
            log.debug("  json: %s", json)

        try:
            response = self._client.request(
                method,
                url,
                params=params,
                json=json,
            )

            log.debug("Response: %s", response.status_code)
            log.debug("  url: %s", response.url)
            log.debug(
                "  body: %s", response.text[:1000] if response.text else "(empty)"
            )

            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_data = e.response.json()
                error_detail = error_data.get("detail", str(error_data))
            except Exception:
                error_detail = e.response.text

            log.debug("HTTP error: %s - %s", e.response.status_code, error_detail)
            raise GenevaClientError(
                f"API request failed: {e.response.status_code} - {error_detail}"
            ) from e
        except httpx.RequestError as e:
            log.debug("Request error: %s", e)
            raise GenevaClientError(f"Request failed: {e}") from e

    def list_clusters(self) -> list[Cluster]:
        """List all clusters."""
        data = self._request("GET", "/api/v1/clusters")
        # API returns "items" key
        items = data.get("items", data.get("clusters", []))
        try:
            clusters = [Cluster.model_validate(item) for item in items]
        except ValidationError as e:
            raise GenevaClientError(f"Failed to parse cluster response: {e}") from e
        return clusters

    def get_cluster(self, name: str) -> Cluster:
        """Get a specific cluster by name."""
        data = self._request("GET", f"/api/v1/clusters/{name}")
        return Cluster.model_validate(data)

    def list_manifests(self) -> list[Manifest]:
        """List all manifests."""
        data = self._request("GET", "/api/v1/manifests")
        # API returns "items" key
        items = data.get("items", data.get("manifests", []))
        try:
            manifests = [Manifest.model_validate(item) for item in items]
        except ValidationError as e:
            raise GenevaClientError(f"Failed to parse manifest response: {e}") from e
        return manifests

    def get_manifest(self, name: str) -> Manifest:
        """Get a specific manifest by name."""
        data = self._request("GET", f"/api/v1/manifests/{name}")
        return Manifest.model_validate(data)

    def list_jobs(
        self,
        status: JobStatus | None = None,
        launched_after: datetime | None = None,
        launched_before: datetime | None = None,
        limit: int | None = None,
    ) -> list[Job]:
        """
        List jobs with optional filters.

        Args:
            status: Filter by job status
            launched_after: Filter jobs launched after this time
            launched_before: Filter jobs launched before this time
            limit: Maximum number of jobs to return
        """
        params: dict[str, Any] = {}

        if status is not None:
            params["status"] = status.value

        if launched_after is not None:
            params["launched_after"] = launched_after.isoformat()

        if launched_before is not None:
            params["launched_before"] = launched_before.isoformat()

        if limit is not None:
            params["limit"] = limit

        data = self._request("GET", "/api/v1/jobs", params=params)

        # API returns "items" key
        items = data.get("items", data.get("jobs", []))
        try:
            jobs = [Job.model_validate(item) for item in items]
        except ValidationError as e:
            raise GenevaClientError(f"Failed to parse job response: {e}") from e
        return jobs

    def get_job(self, job_id: str) -> Job:
        """Get a specific job by ID."""
        data = self._request("GET", f"/api/v1/jobs/{job_id}")
        return Job.model_validate(data)
