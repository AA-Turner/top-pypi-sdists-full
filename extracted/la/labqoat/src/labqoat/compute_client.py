"""Workspace compute limits, usage, offerings, location policy, connected-host and site management."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import TYPE_CHECKING

from labqoat.base_client import BaseClient
from labqoat.errors.revision_conflict_error import RevisionConflictError
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.net.response import Response


class ComputeClient(BaseClient):
    """Read and update shared compute policy using revision-checked JSON Merge Patch."""

    SETTINGS = "/api/v1/compute/settings"
    MERGE_PATCH = "application/merge-patch+json"

    def settings(self) -> JsonDocument:
        """Read workload limits, rate ceiling, idle delays and the current policy revision."""
        return self._read(self.SETTINGS)

    def update_settings(self, patch: Mapping[str, JsonValue], revision: int | str) -> JsonDocument:
        """Merge-patch settings; null removes an optional limit and a supplied family list replaces it."""
        return self._conditional_patch(self.SETTINGS, patch, revision)

    def usage(self) -> JsonDocument:
        """Read held, draining and lifecycle usage by workload, GPU family and elastic rate."""
        return self._read("/api/v1/compute/usage")

    def offerings(self) -> JsonDocument:
        """Read the observed hardware catalog with prices and purchase eligibility."""
        return self._read("/api/v1/compute/offerings")

    def location(self, location_id: str) -> JsonDocument:
        """Read one location's allowed hardware and scheduling controls."""
        return self._read(self._location_path(location_id))

    def update_location(self, location_id: str, patch: Mapping[str, JsonValue], revision: int | str) -> JsonDocument:
        """Merge-patch allowed instance types or the paused state of one location."""
        return self._conditional_patch(self._location_path(location_id), patch, revision)

    def hosts(self) -> JsonDocument:
        """List enrolled connected hosts and their enforced resource shares."""
        return self._read("/api/v1/compute/hosts")

    def host(self, host_id: str) -> JsonDocument:
        """Read one connected host's state, capacity, devices and share."""
        return self._read(self._host_path(host_id))

    def enroll_host(self, site: str) -> JsonDocument:
        """Create a host enrollment and receive one-time agent bootstrap settings."""
        path = "/api/v1/compute/hosts"
        return self._document(self.send_json("POST", path, {"site": site}), path)

    def update_host_share(self, host_id: str, share: Mapping[str, JsonValue]) -> JsonDocument:
        """Merge-patch the CPU, memory and GPU devices Labqoat may use on a connected host."""
        path = self._host_path(host_id)
        body = json.dumps({"share": dict(share)}).encode()
        return self._document(self.send_content("PATCH", path, body, self.MERGE_PATCH), path)

    def unenroll_host(self, host_id: str) -> JsonDocument:
        """Stop scheduling on a connected host; the machine itself keeps running."""
        path = self._host_path(host_id)
        return self._document(self.send("DELETE", path), path)

    def remove_site(self, site_id: str) -> None:
        """Remove an existing-machine site such as ``site-rack-1`` once every host there is unenrolled."""
        self.send("DELETE", f"/api/v1/compute/sites/{self._segment(site_id)}")

    def _read(self, path: str) -> JsonDocument:
        """Read one JSON document, filling its revision from the entity tag when omitted."""
        return self._document(self.send("GET", path), path)

    def _conditional_patch(self, path: str, patch: Mapping[str, JsonValue], revision: int | str) -> JsonDocument:
        """Send If-Match with a merge patch and map precondition failures to a typed conflict."""
        from labqoat.errors.transport_error import TransportError
        from labqoat.net.http_error import HttpError
        from labqoat.net.http_timeout_error import HttpTimeoutError

        body = json.dumps(dict(patch)).encode()
        try:
            response = self._transport.request(
                "PATCH", path, content=body, content_type=self.MERGE_PATCH, headers={"if-match": self._tag(revision)}
            )
        except HttpTimeoutError as error:
            raise TransportError(f"Request to {path} exceeded its deadline.", timed_out=True) from error
        except HttpError as error:
            raise TransportError(f"Could not reach the API at {path}.") from error
        if response.status_code in (412, 428):
            problem = BaseClient.problem_document(response)
            raise RevisionConflictError(path, response.status_code, problem, response.headers.get("x-request-id"))
        BaseClient.raise_for_status(path, response)
        return self._document(response, path)

    @staticmethod
    def _tag(revision: int | str) -> str:
        """Quote the revision as a strong entity tag."""
        if isinstance(revision, bool) or not str(revision).strip() or '"' in str(revision):
            raise ValueError("revision must be a nonempty value without quotes")
        return f'"{revision}"'

    def _document(self, response: Response, path: str) -> JsonDocument:
        """Decode an object body; empty success bodies become an empty document."""
        document = self.decode(response, path, JsonDocument.expect_dict)
        tag = response.headers.get("etag")
        if tag and "revision" not in document:
            document["revision"] = tag.removeprefix("W/").strip('"')
        return document

    def _location_path(self, location_id: str) -> str:
        """Encode a location identifier such as ``location:us-east-2`` as one path segment."""
        return f"/api/v1/compute/locations/{self._segment(location_id)}"

    def _host_path(self, host_id: str) -> str:
        """Encode a host identifier as one path segment."""
        return f"/api/v1/compute/hosts/{self._segment(host_id)}"

    @staticmethod
    def _segment(value: str) -> str:
        """Reject empty identifiers before they could address the collection."""
        if not value:
            raise ValueError("identifier must be nonempty")
        return BaseClient.encode_ref(value)
