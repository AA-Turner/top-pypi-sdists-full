"""Per-context kubeconfig files for tools that only honor the current-context.

``mcp-server-kubernetes`` (4.0.4) ignores ``K8S_CONTEXT`` and always targets
the kubeconfig current-context. Two servers sharing ``~/.kube/config`` therefore
both hit whichever context happens to be current — the read/write ``dev`` server
silently operating on prod. Giving each server its own single-context kubeconfig
(via ``KUBECONFIG``) makes the current-context unambiguous regardless of that bug.
"""

import os
import subprocess
from pathlib import Path

from . import binary


def dedicated_kubeconfig_path(context: str) -> Path:
    return Path.home() / ".kube" / f"{context}.kubeconfig"


def write_dedicated_kubeconfig(context: str) -> str:
    """Write a standalone kubeconfig minified down to ``context``.

    The written file's current-context is ``context``, so a tool that reads only
    the current-context lands on the right cluster. Returns an empty string on
    success, else a short reason; never raises for the caller.
    """
    if not binary.which("kubectl"):
        return "kubectl not installed"
    try:
        result = subprocess.run(
            ["kubectl", "--context", context, "config", "view", "--minify", "--flatten"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"kubectl not runnable: {exc}"
    if result.returncode != 0 or not (result.stdout or "").strip():
        err = (result.stderr or "").strip().splitlines()
        return err[-1] if err else f"context {context} not found"

    path = dedicated_kubeconfig_path(context)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(result.stdout)
    except OSError as exc:
        return f"write failed: {exc}"
    return ""
