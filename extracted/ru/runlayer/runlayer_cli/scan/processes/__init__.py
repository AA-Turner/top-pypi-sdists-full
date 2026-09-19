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

from runlayer_cli.scan.completeness import ScanCompletionStatus
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
    ExtensionRootRef,
    OverrideConfigRef,
    ProcessCandidate,
    ProcessDiscoveryResult,
)
from runlayer_cli.scan.processes.probes import probe_agent_runtime
from runlayer_cli.scan.processes.windows_owner import windows_process_owner_sid

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


def _has_profile_attribution(
    item: DiscoveredProcess | OverrideConfigRef | ExtensionRootRef,
) -> bool:
    return item.owner_sid is not None or item.wsl_distro is not None


def discover_processes(
    *,
    configurations,
    clients,
    agents=(),
    detect_agents: bool = True,
    usernames: Sequence[str] = (),
    wsl_distros: Iterable[DiscoveredWSLDistro] = (),
    windows_user_sid: str | None = None,
    timeout: int = SUBPROCESS_TIMEOUT_S,
    checkpoint: Callable[[], None] | None = None,
) -> ProcessDiscoveryResult:
    """Enumerate, score, classify, and redact running AI-related processes.

    The one entry point the scan flow (PHASE 12) calls. ``configurations``,
    ``clients``, and ``agents`` come from the at-rest channels and correlate
    runtime processes back to known identities. Best-effort: any failure is
    logged rather than aborting the scan.
    """
    completion = ScanCompletionStatus()
    try:
        candidates = enumerate_candidates(timeout=timeout, scan_status=completion)
    except Exception as exc:  # never raise into the scan
        logger.warning(
            "process_enumeration_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        candidates = []
        completion.mark_incomplete("process_enumeration_failed")

    if detect_agents:
        try:
            candidates = probe_agent_runtime(
                candidates,
                runtime_signatures(),
                timeout=timeout,
                scan_status=completion,
            )
        except Exception as exc:  # preserve primary enumeration on probe failure
            logger.warning(
                "agent_runtime_probe_failed",
                error=str(exc),
                error_type=type(exc).__name__,
            )
            completion.mark_incomplete("agent_runtime_probe_failed")

    if windows_user_sid is not None:
        profile_candidates: list[ProcessCandidate] = []
        for candidate in candidates:
            if candidate.pid <= 0:
                profile_candidates.append(candidate)
                continue
            if checkpoint is not None:
                checkpoint()
            try:
                owner_sid = windows_process_owner_sid(candidate.pid)
            except Exception as exc:
                logger.debug(
                    "process_owner_lookup_failed",
                    pid=candidate.pid,
                    error=str(exc),
                )
                owner_sid = None
            candidate.owner_sid = owner_sid
            if owner_sid is None or owner_sid.casefold() == windows_user_sid.casefold():
                profile_candidates.append(candidate)
        candidates = profile_candidates

    candidates.extend(
        enumerate_wsl_process_tables(
            wsl_distros,
            timeout=timeout,
            checkpoint=checkpoint,
            scan_status=completion,
        )
    )

    try:
        context = build_context(
            configurations,
            clients,
            agents,
            detect_agents=detect_agents,
        )
        result = classify_processes_with_overrides(
            candidates,
            context,
            usernames=usernames,
        )
        if not result.complete:
            completion.mark_incomplete("process_classification_capped")
        if windows_user_sid is not None:
            # Unattributable host candidates intentionally reach classification
            # only to detect whether they would surface. If so, revoke absence
            # authority, then drop them from every output. See
            # docs-internal/decision-records/
            # 2026-09-03-ai-watch-evasion-launcher-inspection.md.
            reportable_owner_gap = any(
                not _has_profile_attribution(process) for process in result.processes
            )
            if reportable_owner_gap:
                completion.mark_incomplete("process_owner_lookup_failed")
            result.processes = [
                process
                for process in result.processes
                if _has_profile_attribution(process)
            ]
            result.override_config_refs = [
                ref
                for ref in result.override_config_refs
                if _has_profile_attribution(ref)
            ]
            result.extension_root_refs = [
                ref
                for ref in result.extension_root_refs
                if _has_profile_attribution(ref)
            ]
        result.complete = completion.complete
        result.incomplete_reasons = completion.reasons
    except Exception as exc:  # never raise into the scan
        logger.warning(
            "process_classification_failed",
            error=str(exc),
            error_type=type(exc).__name__,
        )
        completion.mark_incomplete("process_classification_failed")
        result = ProcessDiscoveryResult(
            complete=False,
            incomplete_reasons=list(completion.reasons),
        )
    return result
