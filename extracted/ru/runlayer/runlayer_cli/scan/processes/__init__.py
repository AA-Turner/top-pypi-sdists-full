"""Runtime / process-discovery channel for AI Watch Detect (scan PHASE 12).

Discovers *running* clients, MCP servers, and agents and joins them to the
static config scan. Two enumeration sources (process table + listening sockets)
are unioned by pid, scored for AI-relatedness, classified, redacted, and
submitted with the MCP scan payload. This is the runtime complement to the
filesystem-only config scan: it catches liveness and config-less runtime
shadows that no config file reveals.

``discover_processes`` is the single seam the scan calls; it is best-effort and
never raises into the scan. Standard-library only (fits the frozen ``aiwatch``
bundle).
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

import structlog

from runlayer_cli.scan.agents.install import runtime_signatures
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.processes.classify import (
    ClassifierContext,
    build_context,
    classify_processes,
    classify_processes_with_overrides,
)
from runlayer_cli.scan.processes.enumerate import (
    SUBPROCESS_TIMEOUT_S,
    enumerate_candidates,
    enumerate_wsl_process_tables,
)
from runlayer_cli.scan.processes.models import (
    DiscoveredProcess,
    ProcessCandidate,
    ProcessDiscoveryResult,
)
from runlayer_cli.scan.processes.probes import probe_agent_runtime

__all__ = [
    "ClassifierContext",
    "DiscoveredProcess",
    "ProcessCandidate",
    "ProcessDiscoveryResult",
    "build_context",
    "classify_processes",
    "discover_processes",
]

logger = structlog.get_logger(__name__)


def discover_processes(
    *,
    configurations,
    clients,
    agents=(),
    detect_agents: bool = True,
    usernames: Sequence[str] = (),
    wsl_distros: Iterable[DiscoveredWSLDistro] = (),
    timeout: int = SUBPROCESS_TIMEOUT_S,
    checkpoint: Callable[[], None] | None = None,
) -> ProcessDiscoveryResult:
    """Enumerate, score, classify, and redact running AI-related processes.

    The one entry point the scan flow (PHASE 12) calls. ``configurations``,
    ``clients``, and ``agents`` come from the at-rest channels and correlate
    runtime processes back to known identities. Best-effort: any failure is
    logged rather than aborting the scan.
    """
    try:
        candidates = enumerate_candidates(timeout=timeout)
    except Exception as exc:  # never raise into the scan
        logger.warning(
            "process_enumeration_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        candidates = []

    if detect_agents:
        try:
            candidates = probe_agent_runtime(
                candidates,
                runtime_signatures(),
                timeout=timeout,
            )
        except Exception as exc:  # preserve primary enumeration on probe failure
            logger.warning(
                "agent_runtime_probe_failed",
                error=str(exc),
                error_type=type(exc).__name__,
            )

    candidates.extend(
        enumerate_wsl_process_tables(
            wsl_distros,
            timeout=timeout,
            checkpoint=checkpoint,
        )
    )

    try:
        context = build_context(
            configurations,
            clients,
            agents,
            detect_agents=detect_agents,
        )
        return classify_processes_with_overrides(
            candidates,
            context,
            usernames=usernames,
        )
    except Exception as exc:  # never raise into the scan
        logger.warning(
            "process_classification_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        return ProcessDiscoveryResult()
