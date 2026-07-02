"""
cvc.adapters.copilot — GitHub Copilot API adapter for CVC.

EXACT REPLICA of the upstream Copilot integration pattern:

1. Resolve a raw GitHub token (gho_/github_pat_/ghu_) from env vars or
   `gh auth token`. If absent, the caller must run `cvc auth login copilot`
   to trigger the OAuth device-code flow (see cvc.auth.copilot_auth).
2. Exchange that raw token for a short-lived Copilot API token via
   ``GET https://api.github.com/copilot_internal/v2/token``. The exchanged
   token is cached in-process with a 2-minute refresh margin.
3. Send chat requests to ``https://api.githubcopilot.com/chat/completions``
   with VSCode-impersonating headers (``Editor-Version``,
   ``Copilot-Integration-Id: vscode-chat``, ``Openai-Intent``,
   ``x-initiator``). These headers route the request through the IDE
   quota (effectively unlimited for Copilot Pro) instead of the Premium
   Chat quota — yielding 0% premium burn.

No CLI dependency. No ACP subprocess. Pure HTTP, exactly like upstream.

Default model: claude-sonnet-4.6 (best quality for agentic work)
Env vars:      COPILOT_GITHUB_TOKEN, GH_TOKEN, GITHUB_TOKEN
"""

from __future__ import annotations

import logging
import re
import time

import httpx

from cvc.adapters.openai import OpenAIAdapter
from cvc.auth.copilot_auth import (
    copilot_request_headers,
    exchange_copilot_token,
    list_copilot_models,
    pick_closest_copilot_model,
    resolve_copilot_token,
)

logger = logging.getLogger("cvc.adapters.copilot")

DEFAULT_MODEL = "claude-sonnet-4.6"
COPILOT_BASE_URL = "https://api.githubcopilot.com"

# Token-refresh safety margin: re-exchange when within this many seconds of expiry.
_TOKEN_REFRESH_MARGIN_SECONDS = 120

# Pattern matching the Copilot "model not available" error message.
# Example: "The requested model is not available for integrator
# 'copilot-language-server'. Available models: [gpt-4.1 claude-opus-4.7 ...]"
_MODEL_NOT_AVAILABLE_RE = re.compile(
    r"model is not available.*?Available models:\s*\[([^\]]+)\]",
    re.IGNORECASE | re.DOTALL,
)


class CopilotAdapter(OpenAIAdapter):
    """
    GitHub Copilot adapter — upstream-equivalent path.

    Reuses the OpenAI wire format (chat completions) since the Copilot
    endpoint is OpenAI-compatible. Overrides only the transport layer to
    inject Copilot-specific authentication and VSCode-impersonating
    headers, plus per-request token refresh.
    """

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL) -> None:
        # Resolve a raw GitHub token. Order of precedence:
        # 1. Explicit api_key passed by the caller (e.g. setup wizard).
        # 2. COPILOT_GITHUB_TOKEN / GH_TOKEN / GITHUB_TOKEN env vars.
        # 3. `gh auth token` (GitHub CLI).
        raw_token = (api_key or "").strip()
        token_source = "explicit"
        if not raw_token:
            raw_token, token_source = resolve_copilot_token()

        if not raw_token:
            raise ValueError(
                "No GitHub token available for Copilot. Set COPILOT_GITHUB_TOKEN "
                "or run `cvc auth login copilot` to authenticate via the browser."
            )

        # Exchange the raw token for the Copilot API token. We store the
        # raw token (so we can re-exchange when the API token expires) and
        # the exchanged token + expiry for fast path on subsequent calls.
        try:
            api_token, expires_at, api_url = exchange_copilot_token(raw_token)
        except ValueError as exc:
            raise ValueError(
                f"Copilot token exchange failed ({exc}). "
                "Verify the token is gho_*/github_pat_*/ghu_* (not ghp_*) and "
                "that the account has GitHub Copilot enabled."
            ) from exc

        self._raw_token = raw_token
        self._token_source = token_source
        self._api_token = api_token
        self._token_expires_at = expires_at
        self._api_url = api_url
        self._model = model

        # Build the httpx client with VSCode-impersonating default headers.
        # The Bearer token is injected per request so we can refresh it
        # transparently without rebuilding the client.
        self._client = httpx.AsyncClient(
            base_url=api_url,
            headers={
                "Content-Type": "application/json",
                **copilot_request_headers(is_agent_turn=True),
            },
            timeout=120.0,
        )

        # OpenAIAdapter base relies on these attributes for `complete()`.
        self._api_key = api_token

        logger.info(
            "CopilotAdapter initialised (model=%s, endpoint=%s, token_source=%s)",
            model,
            api_url,
            token_source,
        )

    # ------------------------------------------------------------------
    # Transport overrides
    # ------------------------------------------------------------------

    def _ensure_fresh_token(self) -> None:
        """Re-exchange the raw token if the cached API token is near expiry."""
        if time.time() < self._token_expires_at - _TOKEN_REFRESH_MARGIN_SECONDS:
            return
        try:
            api_token, expires_at, api_url = exchange_copilot_token(self._raw_token)
        except ValueError as exc:
            logger.warning("Copilot token refresh failed: %s", exc)
            return
        self._api_token = api_token
        self._token_expires_at = expires_at
        self._api_key = api_token
        # If GitHub starts routing this account to a different endpoint
        # (rare, but Business/Enterprise upgrades can flip it), follow it.
        if api_url and api_url != getattr(self, "_api_url", None):
            self._api_url = api_url
            self._client.base_url = httpx.URL(api_url)

    async def complete(self, request, *, committed_prefix_len: int = 0):  # type: ignore[override]
        """Override to refresh the Bearer token before every request AND
        gracefully fall back to an available model when the requested one
        isn't enabled on the user's plan.

        The fallback path is critical: GitHub Copilot's "individual",
        "business" and "enterprise" hostnames serve different model sets,
        and orgs can enable/disable specific models at any time. Without
        the fallback, picking a model that your org hasn't yet enabled
        surfaces as HTTP 400 with a confusing message in the chat UI
        (the user sees "HTTP 400: The requested model is not available...").
        With the fallback, we silently retry with the closest available
        model and the chat just works.
        """
        self._ensure_fresh_token()
        # Inject the (possibly refreshed) Bearer header for this call.
        # We pass it via per-request headers rather than mutating client
        # defaults to avoid races across concurrent requests.
        # OpenAIAdapter.complete() builds the httpx call internally, so we
        # set the Authorization on the client's default headers — Copilot
        # tokens are valid for ~30 min, refresh is rare.
        self._client.headers["Authorization"] = f"Bearer {self._api_token}"

        # Try the original request first.
        try:
            return await super().complete(request, committed_prefix_len=committed_prefix_len)
        except httpx.HTTPStatusError as exc:
            fallback_model = await self._maybe_pick_fallback_model(exc, request)
            if not fallback_model:
                # Not a model-availability error, or no fallback found —
                # re-raise so the caller sees the original error.
                raise

            logger.warning(
                "Copilot: model %r not available on this account — "
                "auto-falling back to %r",
                request.model or self._model,
                fallback_model,
            )
            # Retry once with the fallback model. Build a shallow copy
            # of the request so we don't mutate the caller's object.
            try:
                from copy import copy
                new_request = copy(request)
                new_request.model = fallback_model
                # Persist the swap so subsequent turns on the same
                # adapter instance keep using the working model.
                self._model = fallback_model
                return await super().complete(new_request, committed_prefix_len=committed_prefix_len)
            except Exception:
                # If the fallback also fails, raise the original error
                # so the caller sees a clean failure mode.
                raise

    async def _maybe_pick_fallback_model(
        self, exc: httpx.HTTPStatusError, request
    ) -> str | None:
        """Inspect a Copilot 400 error and return a fallback model id, if any.

        Returns None when:
          - the status code isn't 400
          - the error body doesn't match the "model not available" pattern
          - no reasonable fallback exists in the available list

        Strategy:
          1. Parse the available list from the error body (preferred — no
             extra round-trip).
          2. If parsing fails, call /models to discover what's available.
          3. Score each candidate against the requested model using
             pick_closest_copilot_model and return the best match.
        """
        if exc.response.status_code != 400:
            return None
        try:
            body = exc.response.text or ""
        except Exception:
            body = ""

        available_ids: list[str] = []

        # Path 1: extract from error body
        m = _MODEL_NOT_AVAILABLE_RE.search(body)
        if m:
            raw = m.group(1)
            available_ids = [
                tok.strip().strip("`'\"")
                for tok in raw.split()
                if tok.strip() and not tok.strip() in (",", ";")
            ]
            # Drop obvious non-model tokens (sometimes the list contains
            # punctuation or "and")
            available_ids = [
                x for x in available_ids
                if re.match(r"^[a-z0-9][a-z0-9._-]*$", x, re.IGNORECASE)
            ]

        # Path 2: fall back to /models if body parsing failed
        if not available_ids:
            try:
                models = list_copilot_models(self._raw_token, force_refresh=False)
                available_ids = [m_["id"] for m_ in models if isinstance(m_, dict) and m_.get("id")]
            except Exception as e:  # pragma: no cover — best-effort
                logger.debug("copilot fallback: /models lookup failed: %s", e)
                return None

        if not available_ids:
            return None

        requested = request.model or self._model
        fallback = pick_closest_copilot_model(requested, available_ids)
        # Don't loop on the same model
        if fallback and fallback.lower() == (requested or "").lower():
            return None
        return fallback


# Backwards-compat alias for any code still importing HermesAdapter.
# Remove after one release cycle.
HermesAdapter = CopilotAdapter
