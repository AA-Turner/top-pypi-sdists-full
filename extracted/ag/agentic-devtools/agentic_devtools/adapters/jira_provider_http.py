"""Jira REST session and request helpers."""

from __future__ import annotations

from typing import Any

import requests as requests_lib

from agentic_devtools.adapters.jira_provider_config import _JiraProviderMixinProtocol
from agentic_devtools.adapters.retry import TransientError

_DEFAULT_TIMEOUT_SECONDS = 30


class _JiraProviderHttpMixin(_JiraProviderMixinProtocol):
    """Build Jira REST requests and classify response errors."""

    _epic_link_field: str | None

    @staticmethod
    def _contains_error_indicator(text: str, indicators: tuple[str, ...]) -> bool:
        return any(indicator in text for indicator in indicators)

    @staticmethod
    def _matches_field_error(text: str, field_name: str, indicators: tuple[str, ...]) -> bool:
        return field_name in text and _JiraProviderHttpMixin._contains_error_indicator(text, indicators)

    @staticmethod
    def _payload_has_inapplicable_field_error(
        payload: object,
        field_name: str,
        field_name_lower: str,
        indicators: tuple[str, ...],
    ) -> bool | None:
        """Return a payload classification, or None to fall back to response text."""
        if not isinstance(payload, dict):
            return None
        errors = payload.get("errors")
        if isinstance(errors, dict):
            field_error = errors.get(field_name)
            if isinstance(field_error, str):
                return _JiraProviderHttpMixin._contains_error_indicator(field_error.lower(), indicators)
        messages = payload.get("errorMessages")
        if isinstance(messages, list):
            for message in messages:
                if isinstance(message, str) and _JiraProviderHttpMixin._matches_field_error(
                    message.lower(), field_name_lower, indicators
                ):
                    return True
        return None

    def _api_url(self, path: str) -> str:
        """Build a full Jira REST API URL."""
        return f"{self._base_url}/rest/api/2{path}"

    def _request(self, method: str, url: str, **kwargs: Any) -> requests_lib.Response:
        """Make an HTTP request, raising on transient errors."""
        kwargs.setdefault("timeout", _DEFAULT_TIMEOUT_SECONDS)
        resp = self._session.request(method, url, **kwargs)
        if resp.status_code in (429, 502, 503):
            raise TransientError(
                f"Jira API returned {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )
        return resp

    def _get_epic_link_field(self) -> str:
        """Dynamically resolve the epic-link custom field ID.

        Queries ``GET /rest/api/2/field`` and searches for a field whose
        name or schema contains "epic link".
        """
        if self._epic_link_field:
            return self._epic_link_field

        url = self._api_url("/field")
        resp = self._request("GET", url)
        resp.raise_for_status()
        fields = resp.json()

        for f in fields:
            name = (f.get("name") or "").lower()
            schema = f.get("schema", {})
            custom_type = (schema.get("custom", "") or "").lower() if isinstance(schema, dict) else ""
            if "epic link" in name or "epiclink" in custom_type or "epic-link" in custom_type:
                self._epic_link_field = f["id"]
                return self._epic_link_field

        # Fallback to common field ID
        self._epic_link_field = "customfield_10008"
        return self._epic_link_field

    @staticmethod
    def _is_field_inapplicable_error(response: requests_lib.Response, field_name: str) -> bool:
        """Return True when a Jira validation error indicates a field is inapplicable."""
        field_name_lower = field_name.lower()
        field_error_indicators = (
            "not on the appropriate screen",
            "not applicable",
            "cannot be set",
            "does not exist",
        )
        try:
            payload = response.json()
        except ValueError:
            payload = None

        payload_result = _JiraProviderHttpMixin._payload_has_inapplicable_field_error(
            payload, field_name, field_name_lower, field_error_indicators
        )
        if payload_result is not None:
            return payload_result

        response_text = (response.text or "").lower()
        for line in response_text.splitlines():
            if _JiraProviderHttpMixin._matches_field_error(line, field_name_lower, field_error_indicators):
                return True
        return False
