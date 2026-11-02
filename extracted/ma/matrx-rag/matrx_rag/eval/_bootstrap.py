"""Host bootstrap seam for the eval CLIs.

The eval harnesses need SOMETHING to have called ``matrx_rag.configure(...)``
(and, in a host that has one, its sibling packages) before they run. That is a
HOST concern, not a matrx-rag concern — so the CLIs take the host's entry point
as an argument instead of importing one.

Both runners used to do ``from aidream.package_integration import
configure_packages`` inline, which hardwired the package to a single consumer
and was a standing package-boundary violation. Now:

    python -m matrx_rag.eval.runner --bootstrap aidream.package_integration:configure_packages ...

With ``--bootstrap`` omitted the CLI runs against whatever configuration is
already in the process (e.g. a standalone script that called
``matrx_rag.configure()`` itself). It never guesses a host.
"""

from __future__ import annotations

import importlib
import inspect
from typing import Annotated, Any

BOOTSTRAP_HELP = (
    "Dotted path to the host's package-wiring entry point, as 'module:callable' "
    "(e.g. 'aidream.package_integration:configure_packages'). Called before the "
    "eval runs. Omit it when the process is already configured."
)


async def run_bootstrap(spec: str | None) -> None:
    """Import and call ``spec`` ('module:callable'). Awaits it when it's async."""
    if not spec:
        return
    if ":" not in spec:
        raise SystemExit(
            f"--bootstrap must be 'module:callable', got {spec!r}. "
            "Example: aidream.package_integration:configure_packages"
        )
    module_name, _, attr = spec.partition(":")
    if not _is_public_dotted_module(module_name) or not attr.isidentifier():
        raise SystemExit(
            f"--bootstrap must be 'module:callable' with a dotted Python module and callable name, "
            f"got {spec!r}."
        )
    await _run_external_bootstrap(module_name, attr)


def _is_public_dotted_module(module_name: str) -> bool:
    """Keep the open bootstrap ABI syntactically precise without naming a host."""
    return bool(module_name) and all(part.isidentifier() for part in module_name.split("."))


async def _run_external_bootstrap(
    module_name: Annotated[str, "matrx.external_bootstrap_module"], attr: str
) -> None:
    """Run the caller-selected host bootstrap under the documented open ABI.

    The annotation is consumed by matrx-mandate-scan.  It identifies this one
    user-supplied extension boundary without disguising other computed imports.
    """
    fn: Any = getattr(importlib.import_module(module_name), attr)
    if not callable(fn):
        raise SystemExit(f"--bootstrap target {module_name}:{attr} is not callable")
    result = fn()
    if inspect.isawaitable(result):
        await result
