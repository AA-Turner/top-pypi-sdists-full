"""
cvc.adapters.vertex — Google Cloud Vertex AI adapter.

Uses Vertex AI's OpenAI-compatible REST endpoint, authenticated via
Google Cloud Application Default Credentials (ADC).  The user runs::

    gcloud auth application-default login

and CVC automatically discovers the GCP project and obtains short-lived
OAuth2 access tokens.  Tokens are refreshed transparently before each
request (they expire after ~1 hour).

CVC builds the base URL automatically:
    https://{location}-aiplatform.googleapis.com/v1/
        projects/{project_id}/locations/{location}/endpoints/openapi

Default model: ``gemini-2.5-flash`` — GA stable, best price-performance.

Vertex AI available models (April 2026):
  Gemini 3.x — Preview (billing-enabled; production-ready):
    gemini-3.1-pro-preview        — Most advanced reasoning + agentic coding, 1M ctx
    gemini-3-flash-preview        — Best multimodal & complex agentic tasks, Computer Use
    gemini-3.1-flash-lite-preview — Lowest cost, high-volume optimised

  Gemini 2.5 — GA stable channel:
    gemini-2.5-pro                — Complex reasoning, 1M context (GA)
    gemini-2.5-flash              — Best price-performance balance (GA)
    gemini-2.5-flash-lite         — Ultra-efficient for high volume (GA)

  Gemini 2.0 — GA legacy (still available; migrate to 3.x when ready):
    gemini-2.0-flash              — Reliable tool calling (GA)

  Third-party models (via Model Garden MaaS):
    mistral-large@latest          — Mistral Large (Vertex MaaS)
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from cvc.adapters.base import BaseAdapter
from cvc.core.models import (
    ChatCompletionChoice,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    UsageInfo,
)

logger = logging.getLogger("cvc.adapters.vertex")

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_LOCATION = "us-central1"
_VERTEX_SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

# Curated list of models available on Vertex AI (verified April 2026)
# Source: https://cloud.google.com/vertex-ai/generative-ai/docs/models (updated 2026-04-10)
VERTEX_MODELS: list[tuple[str, str, str]] = [
    # ── Gemini 3.x — Preview ────────────────────────────────────
    ("gemini-3.1-pro-preview", "3.1 Pro — advanced reasoning, 1M ctx", "Premium"),
    ("gemini-3-flash-preview", "3 Flash — multimodal & agentic tasks", "Standard"),
    ("gemini-3.1-flash-lite-preview", "3.1 Flash-Lite — lowest cost", "Economy"),
    # ── Gemini 2.5 — GA stable ──────────────────────────────────
    ("gemini-2.5-pro", "2.5 Pro — complex reasoning, 1M ctx (GA)", "Premium"),
    ("gemini-2.5-flash", "2.5 Flash — best price-performance (GA)", "Standard"),
    ("gemini-2.5-flash-lite", "2.5 Flash-Lite — ultra-efficient (GA)", "Economy"),
    # ── Gemini 2.0 — GA legacy ──────────────────────────────────
    ("gemini-2.0-flash", "2.0 Flash — reliable tool calling (GA)", "Standard"),
    # ── Third-party (Model Garden MaaS) ─────────────────────────
    ("mistral-large@latest", "Mistral Large — coding & reasoning", "Standard"),
]


def build_vertex_base_url(project_id: str, location: str = DEFAULT_LOCATION) -> str:
    """Construct the Vertex AI OpenAI-compatible base URL.

    Uses the ``/v1/`` API path (stable channel) which is what the OpenAI Python
    SDK expects — the SDK then appends ``/chat/completions`` directly.
    See: https://cloud.google.com/vertex-ai/generative-ai/docs/migrate/openai/auth-and-credentials
    """
    return (
        f"https://{location}-aiplatform.googleapis.com/v1/projects"
        f"/{project_id}/locations/{location}/endpoints/openapi"
    )


# ---------------------------------------------------------------------------
# ADC helpers — google-auth based credential management
# ---------------------------------------------------------------------------

def get_vertex_credentials() -> tuple[Any, str]:
    """Obtain ADC credentials and project ID.

    Returns ``(credentials, project_id)``.  Raises ``RuntimeError`` if ADC
    is not configured (user needs to run ``gcloud auth application-default login``).
    """
    try:
        import google.auth
        import google.auth.transport.requests
    except ImportError:
        raise RuntimeError(
            "google-auth is required for Vertex AI.  Install it with:\n"
            "  pip install google-auth"
        )

    try:
        credentials, project = google.auth.default(scopes=_VERTEX_SCOPES)
    except google.auth.exceptions.DefaultCredentialsError:
        raise RuntimeError(
            "No Google Cloud credentials found.  Run:\n"
            "  gcloud auth application-default login\n"
            "to authenticate, then retry."
        )

    return credentials, project or ""


def get_vertex_access_token(credentials: Any | None = None) -> tuple[str, Any]:
    """Return a valid OAuth2 access token, refreshing if needed.

    Returns ``(token, credentials)`` — callers should keep the credentials
    object around for subsequent refreshes.
    """
    import google.auth.transport.requests

    if credentials is None:
        credentials, _ = get_vertex_credentials()

    if not credentials.valid:
        credentials.refresh(google.auth.transport.requests.Request())

    return credentials.token, credentials


def fetch_vertex_models(
    project_id: str,
    location: str = DEFAULT_LOCATION,
    timeout: float = 10.0,
) -> list[tuple[str, str, str]] | None:
    """
    Attempt to fetch available models from Vertex AI using ADC credentials.

    Returns a list of (model_id, display_name, tier) tuples on success,
    or None if the request fails (caller should fall back to VERTEX_MODELS).
    """
    try:
        token, _ = get_vertex_access_token()
    except Exception as exc:
        logger.debug("Could not get Vertex AI token for model fetch: %s", exc)
        return None

    base_url = build_vertex_base_url(project_id, location)
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.get(
                f"{base_url}/models",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
            )
            if resp.status_code != 200:
                logger.debug("Vertex models fetch returned %d", resp.status_code)
                return None
            data = resp.json()
            models = []
            for m in data.get("data", []):
                mid = m.get("id", "")
                name = m.get("id", mid)
                if mid:
                    models.append((mid, name, "Vertex AI"))
            return models if models else None
    except Exception as exc:
        logger.debug("Vertex models fetch failed: %s", exc)
        return None


class VertexAIAdapter(BaseAdapter):
    """
    Adapter for Google Cloud Vertex AI via its OpenAI-compatible endpoint.

    Authentication uses Application Default Credentials (ADC) — the user
    runs ``gcloud auth application-default login`` once and CVC handles
    OAuth2 token refresh transparently.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        project_id: str = "",
        location: str = DEFAULT_LOCATION,
        api_key: str = "",  # Kept for interface compat; not used for auth
    ) -> None:
        self._model = model
        self._location = location or DEFAULT_LOCATION

        # Obtain ADC credentials
        self._credentials, adc_project = get_vertex_credentials()
        self._project_id = project_id or adc_project
        if not self._project_id:
            raise ValueError(
                "Could not determine GCP project ID from ADC. "
                "Set it with: gcloud config set project YOUR_PROJECT_ID"
            )

        # Get initial access token
        token, self._credentials = get_vertex_access_token(self._credentials)

        base_url = build_vertex_base_url(self._project_id, self._location)

        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=120.0,
        )

    # ------------------------------------------------------------------
    # Token management
    # ------------------------------------------------------------------

    def _refresh_auth(self) -> None:
        """Refresh the OAuth2 token if expired and update the client header."""
        if not self._credentials.valid:
            token, self._credentials = get_vertex_access_token(self._credentials)
            self._client.headers["Authorization"] = f"Bearer {token}"

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def complete(
        self,
        request: ChatCompletionRequest,
        *,
        committed_prefix_len: int = 0,
    ) -> ChatCompletionResponse:
        """Forward the request to Vertex AI via its OpenAI-compatible surface."""
        self._refresh_auth()
        messages = [self._convert_message(m) for m in request.messages]

        body: dict[str, Any] = {
            "model": request.model or self._model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        # Vertex AI OpenAI-compat endpoint requires "google/" prefix for Gemini models
        if not body["model"].startswith(("google/", "meta/", "mistral")):
            body["model"] = f"google/{body['model']}"

        if request.tools:
            body["tools"] = request.tools
        if request.tool_choice:
            body["tool_choice"] = request.tool_choice

        logger.debug(
            "Vertex AI request: model=%s messages=%d",
            body["model"],
            len(messages),
        )

        resp = await self._client.post("/chat/completions", json=body)
        resp.raise_for_status()
        data = resp.json()

        return self._to_response(data)

    async def close(self) -> None:
        await self._client.aclose()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_message(msg: ChatMessage) -> dict[str, Any]:
        """Convert a Pydantic ChatMessage to a plain dict."""
        entry: dict[str, Any] = {"role": msg.role}
        if msg.content is not None:
            entry["content"] = msg.content
        if msg.name:
            entry["name"] = msg.name
        if msg.tool_call_id:
            entry["tool_call_id"] = msg.tool_call_id
        if msg.tool_calls:
            entry["tool_calls"] = msg.tool_calls
        return entry

    @staticmethod
    def _to_response(data: dict[str, Any]) -> ChatCompletionResponse:
        """Convert a raw OpenAI-compat JSON response to our internal schema."""
        choices: list[ChatCompletionChoice] = []
        for c in data.get("choices", []):
            raw_msg = c.get("message", {})
            msg = ChatMessage(
                role=raw_msg.get("role", "assistant"),
                content=raw_msg.get("content"),
                tool_calls=raw_msg.get("tool_calls"),
            )
            choices.append(
                ChatCompletionChoice(
                    index=c.get("index", 0),
                    message=msg,
                    finish_reason=c.get("finish_reason", "stop"),
                )
            )

        usage_data = data.get("usage", {})
        usage = UsageInfo(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0),
            cache_read_tokens=usage_data.get("prompt_tokens_details", {}).get(
                "cached_tokens", 0
            ),
        )

        return ChatCompletionResponse(
            id=data.get("id", ""),
            model=data.get("model", ""),
            choices=choices,
            usage=usage,
        )
