"""HTTP headers for a Mistral service that calls Vibe Agents directly, without the gateway."""

from typing import Final

from mistralai.vibe_agents.session_workflow import Principal

# Names the application that owns the Sessions a caller starts. Kong strips every `x-internal-*`
# header, so only a direct caller can set it; gateway callers get the server default.
APPLICATION_NAME_HEADER: Final = "x-internal-application-name"


def internal_caller_headers(
    principal: Principal,
    *,
    origin_service: str,
    application_name: str | None = None,
) -> dict[str, str]:
    """Return the caller headers for a client's ``extra_headers`` on a direct call."""

    headers = {
        "x-consumer-custom-id": str(principal.customer_id),
        "x-organization-id": str(principal.organization_id),
        "x-workspace-id": str(principal.workspace_id),
        "x-internal-service": origin_service,
    }
    if principal.user_id is not None:
        headers["x-user-id"] = str(principal.user_id)
    if application_name is not None:
        headers[APPLICATION_NAME_HEADER] = application_name
    return headers


__all__ = ["APPLICATION_NAME_HEADER", "internal_caller_headers"]
