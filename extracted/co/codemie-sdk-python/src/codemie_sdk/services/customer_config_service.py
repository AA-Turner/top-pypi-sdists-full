"""Customer config service implementation.

Wraps four endpoints introduced in EPMCDME-13983:
  GET  /v1/config/declarations            — list dynamic-config declarations (admin/maintainer)
  PUT  /v1/config/declarations/{id}       — save override settings for a component
  DELETE /v1/config/declarations/{id}     — reset component to YAML default (idempotent)
  GET  /v1/config                         — merged component values (anonymous)
"""

from ..utils.http import ApiRequestHandler, TokenSource


class CustomerConfigService:
    """Service for managing customer configuration overrides via the admin endpoint."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the customer config service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token source
            verify_ssl: Whether to verify SSL certificates. Default: True
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def list_declarations(self) -> list[dict]:
        """GET /v1/config/declarations — list all registered setting declarations.

        Requires admin or maintainer role.  Read path bypasses the TTL cache so
        the response always reflects the current DB state.

        Returns:
            List of declaration dicts, each containing:
            ``component_id``, ``label``, ``description``, ``overridden``,
            ``value`` (current merged value), ``fields`` (field metadata).

        Raises:
            requests.HTTPError: On non-2xx response (e.g. 403 for non-admin).
        """
        return self._api.get(
            "/v1/config/declarations",
            list[dict],
            wrap_response=False,
        )

    def get_config(self) -> list[dict]:
        """GET /v1/config — merged component values (anonymous access).

        Returns the merged list of all active components with their current
        settings (YAML defaults merged with any dynamic overrides).  The
        writing pod invalidates its own cache immediately after a PUT or
        DELETE, so a same-pod GET reflects the change right away (AC-20).

        Returns:
            List of component dicts, each with ``id`` and ``settings``.
        """
        return self._api.get(
            "/v1/config",
            list[dict],
            wrap_response=False,
        )

    def save_setting(self, component_id: str, settings: dict) -> dict:
        """PUT /v1/config/declarations/{component_id} — persist a settings override.

        Validates and sanitises the payload on the server side; rejects block-level
        Markdown and ``javascript:`` URLs.  Audits the change to the activity log.
        Invalidates the writing-pod TTL cache immediately.

        Args:
            component_id: Component identifier, e.g. ``"chatDisclaimer"``.
            settings: Key/value map of field names to new values,
                e.g. ``{"enabled": True, "text": "Notice [link](https://...)"}``.

        Returns:
            Response dict with ``component_id`` and ``settings`` as persisted.

        Raises:
            requests.HTTPError: 400 on validation failure, 403 for non-admin callers.
        """
        return self._api.put(
            f"/v1/config/declarations/{component_id}",
            dict,
            json_data={"settings": settings},
            wrap_response=False,
        )

    def reset_setting(self, component_id: str) -> None:
        """DELETE /v1/config/declarations/{component_id} — reset to YAML default.

        Removes the dynamic-config override row; the component reverts to its
        YAML default on the next config read.  Idempotent — 204 even when no
        override row exists.  Audits the reset to the activity log.

        Args:
            component_id: Component identifier, e.g. ``"chatDisclaimer"``.

        Raises:
            requests.HTTPError: On non-2xx / non-204 response.
        """
        self._api.delete(
            f"/v1/config/declarations/{component_id}",
            dict,
            wrap_response=False,
        )
