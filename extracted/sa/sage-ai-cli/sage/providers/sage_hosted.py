"""sage-hosted provider — paid-tier cloud models served from our GCP infra.

Architecture:

  sage CLI (this file)
       │
       │ POST /chat  (Bearer token from `sage login`)
       ▼
  sage backend (FastAPI)
       │
       │ tier check + anonymizer + usage counter
       ▼
  Cloud Run GPU service (vLLM, scale-to-zero)
       │
       │ OpenAI-compatible /v1/chat/completions
       ▼
  Response streamed back through both hops

Free users hit a 403 with `upgrade_required=true` — we surface that as a
typed error so the REPL can render a clean upgrade pitch instead of a
generic HTTPError stack trace.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Optional

import httpx

from ..core.cli_auth import SAGE_API_BASE, load_auth
from .anonymizer import anonymize_payload
from .base import Message, ModelInfo, ProviderBase


# Catalog of sage-hosted models — slot IDs renamed 2026-05-17 to match what
# each service actually serves. Old IDs stay registered as ALIAS_REDIRECTS
# below so existing user config (sage config set default_model cloud:...,
# cached frontend selections, etc.) keeps working without a breaking change.
_HOSTED_MODELS: tuple[ModelInfo, ...] = (
    ModelInfo(
        id="cloud:qwen3-coder",
        provider="cloud",
        name="Qwen3 Coder",
        description="Latest Qwen3 coding model — top-tier code generation. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:llama-3-2",
        provider="cloud",
        name="Llama 3.2",
        description="Meta's latest small Llama, multimodal-ready. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:deepseek-r1-7b",
        provider="cloud",
        name="DeepSeek R1 7B",
        description="Reasoning + chain-of-thought specialist. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:gemma-4",
        provider="cloud",
        name="Gemma 4",
        description="Google's latest multimodal Gemma — text + vision + audio + tools. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:phi-4-reasoning",
        provider="cloud",
        name="Phi-4 Reasoning",
        description="Microsoft's Phi-4 reasoning variant — 14B with chain-of-thought. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:mistral-small",
        provider="cloud",
        name="Mistral Small",
        description="Mistral's latest small instruct model — reliable + fast. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:llava-llama-3",
        provider="cloud",
        name="LLaVA Llama 3 (Vision)",
        description="Vision-capable Llama 3 — image + text input → text output. Paid tier — sage-hosted on GCP.",
    ),
    ModelInfo(
        id="cloud:yi-coder-9b",
        provider="cloud",
        name="Yi Coder 9B",
        description="Yi's 9B coding specialist with extended context. Paid tier — sage-hosted on GCP.",
    ),
)


# Backward-compat: old `cloud:<id>` strings users may have saved in their
# config or selected in the frontend redirect to the new slot. Updated
# whenever a slot ID changes — drop entries once the deprecation window
# has passed (recommend 1 release cycle minimum).
_LEGACY_ID_ALIASES: dict[str, str] = {
    "cloud:qwen-coder-7b":  "cloud:qwen3-coder",
    "cloud:llama-3-1-8b":   "cloud:llama-3-2",
    "cloud:gemma-2-9b":     "cloud:gemma-4",
    "cloud:phi-4-14b":      "cloud:phi-4-reasoning",
    "cloud:mistral-7b":     "cloud:mistral-small",
    "cloud:llava-next-7b":  "cloud:llava-llama-3",
    "cloud:yi-1-5-9b":      "cloud:yi-coder-9b",
}


def resolve_legacy_id(model_id: str) -> str:
    """Translate old-style cloud slot IDs to their current canonical form.

    Safe no-op for anything not in the alias table. Called by the
    backend's `/chat` route + the CLI router so old IDs route to the
    right Cloud Run service without an explicit migration step.
    """
    return _LEGACY_ID_ALIASES.get(model_id, model_id)


def _deployed_model_tags() -> set[str] | None:
    """Return the set of model tags with a non-null Cloud Run URL.

    Returns None if the registry can't be read — caller should fall back
    to the full hardcoded catalog so dev builds without model_servers/
    still surface every model.
    """
    # Resolve path relative to this file: sage/providers/sage_hosted.py
    # → ../../model_servers/model_registry.json
    from pathlib import Path as _Path
    registry_path = (
        _Path(__file__).resolve().parent.parent.parent
        / "model_servers" / "model_registry.json"
    )
    if not registry_path.exists():
        return None
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return {
        k for k, v in data.items()
        if not k.startswith("_") and isinstance(v, str) and v.startswith("http")
    }


class UpgradeRequired(RuntimeError):
    """403 from the backend — the user's tier is too low for this model.

    Carries the upgrade_url so the REPL can render an actionable message.
    """

    def __init__(self, message: str, upgrade_url: str = "https://sageworksai.com/#billing"):
        super().__init__(message)
        self.upgrade_url = upgrade_url


class DailyQuotaExceeded(RuntimeError):
    """429 from the backend — user is paid but hit their daily/burst cap."""

    def __init__(self, message: str, retry_after: int | None = None):
        super().__init__(message)
        self.retry_after = retry_after


@dataclass
class _AuthHeaders:
    """Bundle of Bearer token + tier hint, computed once per call."""
    bearer: str
    tier: str


class SageHostedProvider(ProviderBase):
    """sage's paid-tier cloud models. Routes via the backend.

    Provider name is "cloud" so model IDs like `cloud:qwen-coder-7b` resolve
    cleanly via the standard `provider:model` split in ProviderRouter.
    """

    name = "cloud"

    def __init__(self, *, api_base: str | None = None, timeout_seconds: int = 180):
        # Allow override for local dev (point at localhost:8000) without
        # changing the user's `sage login` state.
        self._api_base = (api_base or SAGE_API_BASE).rstrip("/")
        # 180s default covers worst-case cold start (60s) + a few seconds of
        # actual inference. Streaming has no read timeout, see below.
        self._timeout = timeout_seconds

    # ── Capability discovery ──────────────────────────────────────────────────

    def list_models(self) -> list[ModelInfo]:
        """Return only models with a deployed Cloud Run URL.

        Source of truth: `model_servers/model_registry.json`. Entries with
        `null` URLs are not yet deployed — showing them as bookable would
        produce a 500 RUNTIME_ERROR every time a user picks one, which is
        what the 2026-05-16 probe surfaced. Hiding them is the honest UX:
        users only see what actually works.

        Falls back to the full hardcoded catalog if the registry can't be
        read (e.g. when the CLI is shipped without model_servers/).
        """
        deployed = _deployed_model_tags()
        if deployed is None:
            return list(_HOSTED_MODELS)  # registry not available — fail open
        return [m for m in _HOSTED_MODELS if m.id.removeprefix("cloud:") in deployed]

    def is_available(self) -> bool:
        """sage-hosted is "available" if the user is logged in. Free users
        can SEE the models in `sage models` (so they know the upgrade path
        exists) but get the 403 + upgrade prompt on actual call."""
        auth = load_auth()
        return auth is not None and bool(auth.get("id_token"))

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _auth_or_raise(self) -> _AuthHeaders:
        auth = load_auth()
        if not auth or not auth.get("id_token"):
            raise RuntimeError(
                "sage-hosted models require login. Run `sage login` first."
            )
        return _AuthHeaders(
            bearer=auth["id_token"],
            tier=auth.get("tier", "free"),
        )

    def _build_request_payload(
        self,
        messages: list[Message],
        model_name: str,
        temperature: float,
        max_tokens: int,
        stream: bool,
    ) -> dict:
        """Build the body for sage backend's /chat endpoint.

        The backend expects `model_id` prefixed with `cloud:` so its router
        sends the call to CloudRuntime. Anonymizer runs here too as
        defense-in-depth — the backend also anonymizes, but if a future
        deploy ever skips that step, this catches it.
        """
        # The list_models() entries already include the cloud: prefix. If
        # someone calls us with just "qwen-coder-7b", re-prefix.
        full_id = model_name if model_name.startswith("cloud:") else f"cloud:{model_name}"

        payload = {
            "model_id": full_id,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }
        return anonymize_payload(payload, provider_name="sage")

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Translate backend error responses into typed sage exceptions.

        403 → UpgradeRequired (frontend shows the upgrade modal)
        429 → DailyQuotaExceeded (frontend shows "you've used X/Y today")
        other → generic RuntimeError
        """
        if response.is_success:
            return

        # Streaming responses don't have a body until we call read(). Even
        # for errors, .json() and .text would fail with
        # "Attempted to access streaming response content, without having
        # called read()". Read explicitly so the error path is robust.
        try:
            response.read()
        except Exception:
            pass

        # Try to parse the structured error body from FastAPI's HTTPException.
        detail: dict = {}
        try:
            body = response.json()
            detail = body.get("detail", {}) if isinstance(body, dict) else {}
            if not isinstance(detail, dict):
                detail = {"error": str(detail)}
        except Exception:
            try:
                detail = {"error": response.text[:200]}
            except Exception:
                detail = {"error": f"HTTP {response.status_code}"}

        # APIError emits `detail = {"error": "<CODE>", "message": "...", "details": {}}`.
        # `error` is the taxonomy code (RUNTIME_ERROR, NOT_FOUND, ...) — useful
        # to programmatic callers; `message` is the human reason. The user-
        # facing string MUST be the message; surfacing only the code leaves
        # the user with "sage backend error (500): RUNTIME_ERROR", which
        # tells them nothing about what to do.
        msg = (
            detail.get("message")
            or detail.get("error")
            or f"HTTP {response.status_code}"
        )

        if response.status_code == 403 and detail.get("upgrade_required"):
            raise UpgradeRequired(
                msg, upgrade_url=detail.get("upgrade_url", "https://sageworksai.com/#billing"),
            )
        if response.status_code == 429:
            retry = response.headers.get("Retry-After")
            raise DailyQuotaExceeded(
                msg, retry_after=int(retry) if retry and retry.isdigit() else None,
            )
        raise RuntimeError(f"sage backend error ({response.status_code}): {msg}")

    # ── Generation ────────────────────────────────────────────────────────────

    def generate(
        self,
        messages: list[Message],
        model_name: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        auth = self._auth_or_raise()
        payload = self._build_request_payload(
            messages, model_name, temperature, max_tokens, stream=False,
        )
        with httpx.Client(timeout=self._timeout) as client:
            response = client.post(
                f"{self._api_base}/chat",
                json=payload,
                headers={
                    "Authorization": f"Bearer {auth.bearer}",
                    "X-CLI": "true",
                },
            )
            self._raise_for_status(response)
            data = response.json()

        # Backend's non-streaming /chat returns: `{"ok": True, "output": "<text>"}`.
        # Also handle OpenAI-shaped responses for forward-compat with future
        # backend changes, and a few alternate keys we've seen in older revisions.
        if isinstance(data, dict):
            if data.get("ok") is True and "output" in data:
                return data["output"]
            if "choices" in data:
                try:
                    return data["choices"][0]["message"]["content"]
                except (KeyError, IndexError):
                    pass
            for key in ("output", "response", "content"):
                if key in data and isinstance(data[key], str):
                    return data[key]
        return str(data)

    def stream(
        self,
        messages: list[Message],
        model_name: str,
        temperature: float,
        max_tokens: int,
    ) -> Iterator[str]:
        auth = self._auth_or_raise()
        payload = self._build_request_payload(
            messages, model_name, temperature, max_tokens, stream=True,
        )
        # Streaming uses an unbounded read timeout because generation can
        # legitimately take 5+ minutes on long outputs from a cold model.
        with httpx.Client(timeout=httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)) as client:
            with client.stream(
                "POST",
                f"{self._api_base}/chat",
                json=payload,
                headers={
                    "Authorization": f"Bearer {auth.bearer}",
                    "X-CLI": "true",
                },
            ) as response:
                self._raise_for_status(response)
                for line in response.iter_lines():
                    if not line:
                        continue
                    # The backend streams SSE; lines look like "data: {...}".
                    if line.startswith("data:"):
                        chunk = line[len("data:"):].strip()
                        if not chunk or chunk == "[DONE]":
                            continue
                        try:
                            parsed = json.loads(chunk)
                        except json.JSONDecodeError:
                            # Non-JSON SSE payload — assume it's already raw text.
                            yield chunk
                            continue
                        # Sage backend streams SSE events with several shapes:
                        #   {"token": "<piece>"}        — actual response token (most common)
                        #   {"step": "...", "message"}  — UI status (ignore)
                        #   {"done": true}              — completion sentinel (ignore)
                        #   {"error": ...}              — stream error (raise)
                        # OpenAI-shaped responses also handled for forward-compat.
                        if isinstance(parsed, dict):
                            if parsed.get("error"):
                                raise RuntimeError(
                                    f"backend stream error: {parsed.get('message', parsed['error'])}"
                                )
                            if parsed.get("done"):
                                return
                            # Skip status events
                            if "step" in parsed and "token" not in parsed:
                                continue
                            token = parsed.get("token")
                            if token is None:
                                # OpenAI-shaped fallback
                                token = (
                                    parsed.get("choices", [{}])[0].get("delta", {}).get("content")
                                    if parsed.get("choices") else None
                                )
                            if token is None:
                                token = parsed.get("content") or parsed.get("response")
                            if token:
                                yield token
                    else:
                        # Non-SSE backend (e.g. local dev) — yield raw lines.
                        yield line


__all__ = [
    "SageHostedProvider",
    "UpgradeRequired",
    "DailyQuotaExceeded",
]
