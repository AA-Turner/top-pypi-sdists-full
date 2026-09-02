"""Report rendering for discovered agents.

Turns a list of :class:`~runlayer_cli.scan.agents.detect.DiscoveredAgent` into a
compact human-readable summary for ``scan`` output. Supports a ``min_confidence``
threshold; locations with no framework signal are reported as ``unknown``
(skipped) rather than guessed.

For a machine-readable aggregate, use each agent's :meth:`DiscoveredAgent.to_dict`
(see ``ScanResult.to_full_payload``); this module is the human-facing surface.

Standard-library only.
"""

from __future__ import annotations

from collections import Counter

from runlayer_cli.scan.agents.detect import DiscoveredAgent


def _evidence_brief(detection: DiscoveredAgent) -> str:
    """One-line evidence summary: counts plus the discriminating dependency."""
    counts: Counter[str] = Counter(e.kind for e in detection.evidence)
    parts = [
        f"{kind.replace('_', ' ')}:{counts[kind]}"
        for kind in ("package_dep", "shared_dep", "import", "symbol")
        if counts[kind]
    ]
    key_dep = next(
        (e.value for e in detection.evidence if e.kind == "package_dep"), None
    )
    brief = ", ".join(parts)
    if key_dep:
        brief += f"  [{key_dep}]"
    return brief or detection.detection_method


def format_summary(
    detections: list[DiscoveredAgent],
    *,
    min_confidence: float = 0.0,
    verbose: bool = False,
) -> str:
    """Render a compact human-readable summary of detected agents."""
    agents = [d for d in detections if d.is_agent and d.confidence >= min_confidence]
    lines: list[str] = [
        f"Agent detection: {len(agents)} agent(s) across {len(detections)} location(s)"
    ]
    if not agents:
        lines.append("  (no agents detected)")
        return "\n".join(lines)

    name_w = max(max(len(a.name) for a in agents), len("LOCATION"))
    fw_w = max(max(len(a.display_name or "") for a in agents), len("FRAMEWORK"))
    lang_w = max(max(len(a.language or "") for a in agents), len("LANGUAGE"))
    header = (
        f"  {'LOCATION':<{name_w}}  {'FRAMEWORK':<{fw_w}}  "
        f"{'LANGUAGE':<{lang_w}}  {'CONF':>5}  {'MARGIN':>6}  EVIDENCE"
    )
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))
    for a in agents:
        lines.append(
            f"  {a.name:<{name_w}}  {a.display_name or '':<{fw_w}}  "
            f"{a.language or '':<{lang_w}}  {a.confidence:>5.2f}  "
            f"{a.margin:>6.2f}  {_evidence_brief(a)}"
        )

    if verbose:
        lines.append("")
        lines.append("Evidence detail:")
        for a in agents:
            lines.append(f"  {a.name} -> {a.display_name} ({a.detection_method})")
            for e in a.evidence:
                lines.append(f"      [{e.kind}] {e.value}  ({e.source})")
            if a.runner_up:
                lines.append(
                    f"      runner-up: {a.runner_up} "
                    f"(score {a.runner_up_score:.1f} vs {a.score:.1f})"
                )

    return "\n".join(lines)
