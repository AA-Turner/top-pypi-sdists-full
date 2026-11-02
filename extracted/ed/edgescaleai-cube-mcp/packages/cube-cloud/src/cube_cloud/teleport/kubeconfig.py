"""kubectl execution via tbot oneshot (on-demand kube certs).

Uses tbot in oneshot mode to generate role-scoped kubernetes certs
for each (profile, cluster) pair. Certs are cached for ~23h.
"""

from __future__ import annotations

import asyncio
import logging
import shlex

from cube_cloud.teleport.tbot_manager import tbot

logger = logging.getLogger(__name__)

MAX_OUTPUT = 512 * 1024  # 512 KB
# Appended to output cut at MAX_OUTPUT. The return code stays the child's, so a caller
# that parses the output must check for this to tell a partial list from a whole one.
TRUNCATION_MARKER = "\n\n... (truncated)"


async def run_kubectl(
    args: list[str], cluster: str | None = None, profile: str = "admin", timeout: float = 60
) -> tuple[str, int]:
    """Run a kubectl command using a tbot-generated kubeconfig for the given cluster.

    Returns (output, return_code).
    """
    if not tbot.is_ready:
        return "tbot credentials not ready. kubectl is not available.", 1

    if not cluster:
        return "Error: cluster name is required.", 1

    logger.info("kubectl %s (cluster=%s)", " ".join(shlex.quote(a) for a in args), cluster)

    kc_path, err = await tbot.get_kube_kubeconfig(cluster, profile)
    if err:
        return f"Failed to get credentials for '{cluster}': {err}", 1

    proc = None
    try:
        cmd = ["kubectl", "--kubeconfig", kc_path] + args
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=tbot.tsh_env(),
        )

        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        output = stdout.decode("utf-8", errors="replace")

        if len(output) > MAX_OUTPUT:
            output = output[:MAX_OUTPUT] + TRUNCATION_MARKER

        return output, proc.returncode or 0

    except asyncio.TimeoutError:
        # `wait_for` cancels the WAIT, not the process: without this the child keeps
        # running (and holding a Teleport connection) after the caller has given up.
        # That mattered little while every caller allowed 60s; the console's services
        # read now runs on every cube-page load with a shorter bound, so an unreachable
        # cube would otherwise leave one orphaned kubectl behind per timed-out load.
        if proc is not None and proc.returncode is None:
            try:
                proc.kill()
                await asyncio.wait_for(proc.wait(), timeout=5)
            except (ProcessLookupError, asyncio.TimeoutError):
                pass
        return f"kubectl command timed out after {timeout}s", 1
    except asyncio.CancelledError:
        # A caller's own deadline (an outer `wait_for`, a gather that gave up) cancels
        # this task rather than timing out the wait above, so the branch above never runs
        # and the child would outlive the request. Kill it without awaiting: a cancelled
        # task should not block, and the event loop's child watcher reaps it.
        if proc is not None and proc.returncode is None:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        raise
    except FileNotFoundError:
        return "kubectl not found in container.", 1
