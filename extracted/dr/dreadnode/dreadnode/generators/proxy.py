"""Helpers for routing a model through a Dreadnode LiteLLM proxy gateway.

A task environment that declares ``models`` in its ``task.yaml`` is provisioned
with ``DREADNODE_LLM_BASE`` + ``DREADNODE_LLM_API_KEY`` and a ``MODEL`` set to a
platform model id. Task code routes through the gateway with
:func:`get_proxied_generator` — prefix-agnostic, so it works for any platform
model id without depending on the agent runtime's ``dn/`` convention.
"""

import os
import typing as t

if t.TYPE_CHECKING:
    from dreadnode.generators.generator import Generator

DREADNODE_LLM_BASE_ENV = "DREADNODE_LLM_BASE"
DREADNODE_LLM_API_KEY_ENV = "DREADNODE_LLM_API_KEY"


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
    api_base = os.environ.get(DREADNODE_LLM_BASE_ENV, "").strip() or None
    api_key = os.environ.get(DREADNODE_LLM_API_KEY_ENV, "").strip() or None
    if not api_base or not api_key:
        return model
    return build_proxy_generator(model, api_base=api_base, api_key=api_key)
