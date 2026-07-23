"""Helpers for routing a model through a Dreadnode LiteLLM proxy gateway.

A task environment that declares ``models`` in its ``task.yaml`` is provisioned
with ``DREADNODE_LLM_BASE`` + ``DREADNODE_LLM_API_KEY`` and a ``MODEL`` set to a
platform model id. Task code routes through the gateway with
:func:`get_proxied_generator` — prefix-agnostic, so it works for any platform
model id without depending on the agent runtime's ``dn/`` convention.
"""

import logging
import os
import typing as t

if t.TYPE_CHECKING:
    from dreadnode.app.api.client import ApiClient
    from dreadnode.generators.generator import Generator

logger = logging.getLogger("dreadnode")

DREADNODE_LLM_BASE_ENV = "DREADNODE_LLM_BASE"
DREADNODE_LLM_API_KEY_ENV = "DREADNODE_LLM_API_KEY"

# A process-wide hook, registered by dn.configure(), that provisions the platform
# LiteLLM proxy on demand: it mints a short-lived *virtual* key (no provider keys
# ever leave the platform) and sets the two env vars below. Kept in-memory only.
# Held in a dict (mutated, never rebound) so no `global` statement is needed.
_proxy_state: "dict[str, t.Any]" = {"provisioner": None, "attempted": False}


def register_proxy_provisioner(provisioner: "t.Callable[[], bool] | None") -> None:
    """Register (or clear) the lazy proxy provisioner. Called by dn.configure()."""
    _proxy_state["provisioner"] = provisioner
    _proxy_state["attempted"] = False


def _proxy_env_present() -> bool:
    return bool(
        os.environ.get(DREADNODE_LLM_BASE_ENV, "").strip()
        and os.environ.get(DREADNODE_LLM_API_KEY_ENV, "").strip()
    )


def _ensure_proxy_env() -> bool:
    """Provision the proxy lazily on first ``dn/`` use if a provisioner is
    registered and the env isn't already set. Idempotent per process."""
    if _proxy_env_present():
        return True
    if _proxy_state["provisioner"] is None or _proxy_state["attempted"]:
        return _proxy_env_present()
    _proxy_state["attempted"] = True
    try:
        _proxy_state["provisioner"]()
    except Exception as exc:
        logger.debug("Proxy provisioning failed: %s", exc)
    return _proxy_env_present()


def provision_platform_proxy(api: "ApiClient", org: str, client_id: str) -> bool:
    """Mint a short-lived LiteLLM *virtual* key for ``org`` and set the proxy env
    vars in-memory for this process. Returns True on success.

    The virtual key only fronts the Dreadnode gateway (never a provider key) and
    every call is metered to the org's credits, so it is safe to hold locally -
    the same mechanism the TUI uses. Never written to disk or logged."""
    result = api.provision_inference_key(org, client_id)
    base_url = result.get("base_url") or result.get("url")
    api_key = result.get("api_key") or result.get("key")
    if isinstance(base_url, str) and isinstance(api_key, str) and base_url and api_key:
        os.environ[DREADNODE_LLM_BASE_ENV] = base_url
        os.environ[DREADNODE_LLM_API_KEY_ENV] = api_key
        return True
    return False


def build_proxy_generator(
    model: str,
    *,
    api_base: str | None,
    api_key: str | None,
) -> "Generator":
    """Build a generator that routes ``model`` through a LiteLLM proxy gateway.

    The model id is passed through verbatim and tagged with the
    ``litellm_proxy`` provider so the gateway — not the local environment —
    resolves the upstream deployment.
    """
    from dreadnode.generators.generator import GenerateParams, get_generator

    generator = get_generator(
        model,
        params=GenerateParams(
            api_base=api_base,
            extra={"custom_llm_provider": "litellm_proxy"},
        ),
    )
    generator.api_key = api_key
    return generator


def get_proxied_generator(model: str) -> "str | Generator":
    """Return a gateway-routed generator for ``model`` when platform inference
    env is present, otherwise return ``model`` unchanged for normal resolution.

    Routing engages only when both ``DREADNODE_LLM_BASE`` and
    ``DREADNODE_LLM_API_KEY`` are set (as the platform injects into a task
    environment that declared ``models``); the model id is routed regardless of
    prefix. Without them, the call is a no-op and ``model`` resolves through the
    usual provider lookup.
    """
    _ensure_proxy_env()
    api_base = os.environ.get(DREADNODE_LLM_BASE_ENV, "").strip() or None
    api_key = os.environ.get(DREADNODE_LLM_API_KEY_ENV, "").strip() or None
    if not api_base or not api_key:
        return model
    return build_proxy_generator(model, api_base=api_base, api_key=api_key)


def resolve_dn_model_to_generator(model: "str | Generator") -> "str | Generator":
    """Resolve ``dn/*`` model IDs to a configured proxy generator.

    Non-``dn/*`` values are returned unchanged.
    """
    if not isinstance(model, str) or not model.startswith("dn/"):
        return model

    _ensure_proxy_env()
    api_base = os.environ.get(DREADNODE_LLM_BASE_ENV, "").strip() or None
    api_key = os.environ.get(DREADNODE_LLM_API_KEY_ENV, "").strip() or None
    missing: list[str] = []
    if not api_base:
        missing.append(DREADNODE_LLM_BASE_ENV)
    if not api_key:
        missing.append(DREADNODE_LLM_API_KEY_ENV)
    if missing:
        keys = ", ".join(missing)
        raise RuntimeError(f"Missing proxy configuration — set {keys} to use {model}")

    return build_proxy_generator(model, api_base=api_base, api_key=api_key)
