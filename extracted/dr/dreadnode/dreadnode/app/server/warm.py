"""Warm the first chat turn's code path so an E2B snapshot carries it in page cache.

The agent E2B templates run this once, at build time, as the template's start
command (``platform/e2b/template_base.py``). The VM is snapshotted after it
exits, and every sandbox created from the template resumes with the files this
process read already in the guest page cache. Only the page cache survives: the
API starts a fresh ``dreadnode serve`` with creation-time environment variables.

An import list trails the code, so this does not name modules. It executes
what the first turn executes: import the serve graph, build an agent, then
drive one gateway-routed generation against a loopback address that refuses
the connection. That runs litellm's first-call setup and loads the ``openai``
client it uses for the ``litellm_proxy`` provider (446 modules on 2026-09-22,
the largest cold cost left on the first turn) without touching the network.
The trace object store's import stack is loaded alongside.

The dry generation is expected to fail with a connection error. Only an import
failure is fatal, which is what lets the build gate its snapshot marker on this
process's exit code.
"""

import asyncio
import importlib
import json
import os
import sys
import time
import typing as t

# The discard port: the kernel refuses the connection immediately, so the
# generation fails after the full request path has been exercised.
LOOPBACK_GATEWAY = "http://127.0.0.1:9"
WARM_MODEL = "dn/gpt-4o-mini"


def _import_first_turn_graph() -> None:
    """Modules the first turn needs that nothing before it imports."""
    import aiobotocore  # noqa: F401
    import botocore  # noqa: F401
    import litellm
    import litellm.exceptions  # noqa: F401
    import openai  # noqa: F401  # litellm loads it for the litellm_proxy provider
    import s3fs  # noqa: F401  # trace object store


async def _dry_generation() -> str:
    """Run one gateway-routed generation the way a chat turn does, offline."""
    from dreadnode.generators.generator import GenerateParams
    from dreadnode.generators.message import Message
    from dreadnode.generators.proxy import build_proxy_generator

    generator = build_proxy_generator(WARM_MODEL, api_base=LOOPBACK_GATEWAY, api_key="warm")
    try:
        results = await generator.generate_messages(
            [[Message(role="user", content="warm")]],
            [GenerateParams(max_tokens=1)],
        )
    except Exception as exc:  # a refused connection is the expected outcome
        return type(exc).__name__
    for result in results:
        if isinstance(result, BaseException):
            return type(result).__name__
    return "completed"


def warm() -> dict[str, t.Any]:
    """Execute the first-turn path and return what it cost."""
    os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")
    started = time.perf_counter()
    _import_first_turn_graph()
    server = importlib.import_module("dreadnode.app.server.app")
    imported = time.perf_counter()
    server.create_agent("openai/gpt-4o-mini")
    agent_built = time.perf_counter()
    outcome = asyncio.run(_dry_generation())
    generated = time.perf_counter()
    return {
        "import_sec": round(imported - started, 2),
        "agent_sec": round(agent_built - imported, 2),
        "generation_sec": round(generated - agent_built, 2),
        "generation_outcome": outcome,
        "modules": len(sys.modules),
    }


def main(argv: t.Sequence[str] | None = None) -> int:
    """``python -m dreadnode.app.server.warm [--report]``.

    ``--report`` adds the loaded module names so a test can check coverage.
    """
    args = list(sys.argv[1:] if argv is None else argv)
    summary = warm()
    if "--report" in args:
        summary["module_names"] = sorted(sys.modules)
    sys.stdout.write(json.dumps(summary) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
