"""Registry entry point for the OpenAI Agents SDK integration.

``aigie.init()`` already installs this integration through
:func:`aigie.integrations.install.install_framework_adapters`. This module
exposes the same install as a no-argument callable so the LiteLLM-style
registry (``aigie.patch("openai_agents")``) drives one code path rather than
its own copy of the emitter wiring.

Re-installing is safe: the adapter registers its ``TracingProcessor`` with the
Agents SDK once and merely re-binds the emitter on later calls.
"""

from __future__ import annotations

from aigie.client import get_aigie
from aigie.integrations.install import install_adapter

_FRAMEWORK = "openai_agents"


def install_openai_agents_patches() -> None:
    """Install the OpenAI Agents tracing processor against the live client.

    Raises:
        RuntimeError: If no client is initialized, or if the adapter failed to
            install. Either way nothing is tracing, and ``patch()`` only records
            FAILED if this raises — a quiet return would mark the integration
            patched and short-circuit the caller's later retry.
    """
    aigie = get_aigie()
    if aigie is None:
        raise RuntimeError(
            "aigie.init() must be called before patching openai_agents — "
            "there is no client to emit spans into. Note that init() installs "
            "this integration on its own, so an explicit patch() is not needed."
        )
    if not install_adapter(
        _FRAMEWORK,
        aigie=aigie,
        coordinator=getattr(aigie, "_rewind_coordinator", None),
    ):
        raise RuntimeError(
            "failed to install the openai_agents tracing adapter — "
            "see the preceding log record for the underlying cause"
        )


__all__ = ["install_openai_agents_patches"]
