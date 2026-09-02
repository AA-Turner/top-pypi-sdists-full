"""The client-host import surface: everything matrx-local touches must import
with ZERO configuration.

Each module is imported in a SUBPROCESS with a scrubbed environment (the
pytest process itself has stub DB configs installed, which would mask a
regression). A failure here means some module resolves host-injected DB
models/bases at import time again — config errors must surface at CALL time,
never import time.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

# The modules the matrx-local desktop host imports (directly or via its
# engine bootstrap) — the 0.3.0 equivalents of its 0.1.26 import list.
_CLIENT_HOST_IMPORTS = [
    "matrx_ai",
    "matrx_ai.client_host",
    "matrx_ai.client_host.store",
    "matrx_ai.client_host.validate",
    "matrx_ai.catalog",
    "matrx_ai.catalog.host_catalog",
    "matrx_ai.providers",
    "matrx_ai.providers.unified_client",
    "matrx_ai.providers.generic_openai",
    "matrx_ai.providers.keys",
    "matrx_ai.db.ai_models.ai_model_manager",
    "matrx_ai.db.conversation_gate",
    "matrx_ai.db.persistence",
    "matrx_ai.orchestrator",
    "matrx_ai.orchestrator.executor",
    "matrx_ai.tools",
    "matrx_ai.tools.models",
    "matrx_ai.tools.registry",
    "matrx_ai.tools.handle_tool_calls",
    "matrx_ai.tools.external_handlers",
    "matrx_ai.tools.lifecycle",
    "matrx_ai.agents.resolver",
]


def _clean_env() -> dict[str, str]:
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }
    if "VIRTUAL_ENV" in os.environ:
        env["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV"]
    return env


@pytest.mark.parametrize("module", _CLIENT_HOST_IMPORTS)
def test_client_host_import_without_configure(module: str) -> None:
    proc = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        capture_output=True,
        text=True,
        env=_clean_env(),
        cwd=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        timeout=120,
    )
    assert proc.returncode == 0, (
        f"`import {module}` failed in an unconfigured environment — the "
        f"client-host import surface regressed.\nstderr:\n{proc.stderr}"
    )


def test_generic_openai_chat_constructible_without_config() -> None:
    """The matrx-local local-LLM bridge constructs GenericOpenAIChat and
    registers it with the unified-client registry before ANY configure()."""
    code = (
        "from matrx_ai.providers.generic_openai import GenericOpenAIChat\n"
        "from matrx_ai.providers.unified_client import (\n"
        "    register_generic_openai_instance,\n"
        "    get_generic_openai_instance,\n"
        "    unregister_generic_openai_instance,\n"
        ")\n"
        "inst = GenericOpenAIChat(base_url='http://127.0.0.1:1/', api_key='none',\n"
        "                         provider_name='local_llama')\n"
        "register_generic_openai_instance('local/test', inst)\n"
        "assert get_generic_openai_instance('local/test') is inst\n"
        "unregister_generic_openai_instance('local/test')\n"
        "assert get_generic_openai_instance('local/test') is None\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=_clean_env(),
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
