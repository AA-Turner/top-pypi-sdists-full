"""Dynamic config service implementation."""

import requests
from requests.exceptions import HTTPError

from ..utils.http import ApiRequestHandler, TokenSource


class DynamicConfigService:
    """Service for managing dynamic configuration values via the admin endpoint."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the dynamic config service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates. Default: True
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def set(self, key: str, value: int | float | bool | str) -> dict:
        """Upsert a dynamic config value.

        Tries POST /v1/dynamic-config/ to create the key. If the key already
        exists (HTTP 409), falls back to PUT /v1/dynamic-config/{key} to update.
        ``value_type`` is inferred from the Python type of ``value``
        (``bool`` before ``int`` since ``bool`` is an ``int`` subclass) and
        sent alongside the string-serialised value, as required by the API.

        A string value is stored as-is — no int/float/bool coercion is
        applied server-side (DynamicConfigService.convert_value passes
        ConfigValueType.STRING straight through). Unlike the declared
        customer-config endpoint (``PUT /v1/config/declarations/{component_id}``,
        wrapped by ``CustomerConfigService.save_setting``), this generic admin
        endpoint does not validate the value against any field declaration —
        it is the only way to write a raw value that a declaration's own
        completeness check would reject, e.g. a customer-config override
        JSON blob missing one of its currently-declared fields.

        Args:
            key: Config key name (e.g. "SKILL_MAX_CONTENT_LENGTH")
            value: Value to set — int, float, bool, or str (e.g. a
                JSON-encoded override payload)

        Returns:
            Response dict from the admin endpoint

        Raises:
            ValueError: If key is empty or contains a path separator
        """
        if not key or "/" in key:
            raise ValueError(f"Invalid config key: {key!r}")
        if isinstance(value, bool):
            value_type = "bool"
        elif isinstance(value, int):
            value_type = "int"
        elif isinstance(value, float):
            value_type = "float"
        else:
            value_type = "string"
        value_str = value if isinstance(value, str) else str(value)
        # Try to create first; use raw Response so we can inspect the status code
        response = self._api.post(
            "/v1/dynamic-config/",
            requests.Response,
            json_data={"key": key, "value": value_str, "value_type": value_type},
            wrap_response=False,
            raise_on_error=False,
        )
        if response.status_code == 409:
            # Key already exists — update it via PUT
            return self._api.put(
                f"/v1/dynamic-config/{key}",
                dict,
                json_data={"value": value_str},
                wrap_response=False,
            )
        response.raise_for_status()
        return response.json()

    def delete(self, key: str) -> None:
        """Delete a dynamic config key, restoring the system to its built-in default.

        Silently succeeds when the key does not exist (404 is treated as already
        absent — the operation is idempotent).

        Args:
            key: Config key name (e.g. "SKILL_MAX_CONTENT_LENGTH")

        Raises:
            ValueError: If key is empty or contains a path separator
            requests.HTTPError: On non-2xx / non-404 response
        """
        if not key or "/" in key:
            raise ValueError(f"Invalid config key: {key!r}")
        try:
            self._api.delete(f"/v1/dynamic-config/{key}", dict, wrap_response=False)
        except HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                return  # Key did not exist — already at default state
            raise
