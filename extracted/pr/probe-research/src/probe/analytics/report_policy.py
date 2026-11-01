"""Whether Probe may send the Probe team an automatic diagnostic report: either switch stops it.

Not ``probe.sdk.diagnostics.disabled()``; explicit sends skip it. Why: DESIGN.md (report_policy.py).
"""

from __future__ import annotations

from collections.abc import Mapping

_OFF = frozenset({"off", "0", "false", "no", "disabled"})


def staff_reports_disabled(env: Mapping[str, str], base_url: str | None = None) -> str | None:
    """Why automatic reports are off for ``env`` (a session's own variables), or None if allowed.

    ``PROBE_BASE_URL`` in ``env`` outranks ``base_url``, as everywhere in the client. A
    backend that is not Probe's hosted service never gets one (the self-host egress contract).
    """
    if (env.get("PROBE_TELEMETRY") or "").strip().lower() in _OFF:
        return "telemetry_off"
    if (env.get("PROBE_DIAGNOSTICS") or "").strip().lower() in _OFF:
        return "diagnostics_off"
    # Lazy: probe.sdk costs ~70 ms to import and the service start path has a budget.
    from probe.analytics.core import hosted_base_url

    if not hosted_base_url(env.get("PROBE_BASE_URL") or base_url):
        return "not_hosted"
    return None


def allowed(env: Mapping[str, str], base_url: str | None = None) -> bool:
    """Whether an automatic report may be sent for ``env``."""
    return staff_reports_disabled(env, base_url) is None
