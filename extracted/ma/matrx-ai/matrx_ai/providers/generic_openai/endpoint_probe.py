"""The OpenAI-compatible client factory for reaching a RAW endpoint.

Why this exists in the provider layer rather than at the call site: an
OpenAI-compatible endpoint (HuggingFace TGI, llama.cpp, vLLM, any self-hosted
inference server) is reached with the ``openai`` SDK pointed at a different
``base_url``. Spelled at a call site that is an independent provider transport
boundary, and the mandate/provider scan is right to read ``from openai import
AsyncOpenAI`` there as a bypass — from the outside it is indistinguishable from
one. Spelled HERE it is what it is: provider access, in the provider layer,
where provider access belongs.

This is deliberately NOT a runtime path. ``GenericOpenAIChat`` /
``HuggingFaceChat`` are how the platform talks to these endpoints in anger —
they carry the translator, the capture client, key resolution and usage
accounting. This factory is for connectivity PROBES: a smoke test that has to
prove the endpoint itself answers, independent of our stack, and would prove
nothing if it went through the stack it is trying to rule out.
"""

from __future__ import annotations

from openai import AsyncOpenAI

__all__ = ["openai_compatible_probe_client"]


def openai_compatible_probe_client(*, base_url: str, api_key: str) -> AsyncOpenAI:
    """An ``AsyncOpenAI`` bound to a raw OpenAI-compatible endpoint.

    ``base_url`` is the server root; the ``/v1`` suffix is appended when it is
    not already there, because every one of these servers mounts the
    OpenAI-compatible surface at ``/v1`` and every call site was appending it
    by hand.
    """
    root = base_url.rstrip("/")
    if not root.endswith("/v1"):
        root = f"{root}/v1"
    return AsyncOpenAI(api_key=api_key, base_url=root)
