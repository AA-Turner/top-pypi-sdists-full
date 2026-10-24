"""Whether Probe may send the Probe team an automatic diagnostic report.

Light and stdlib-only at import: the Probe service imports it on its start path. The
environment is an argument because the service decides for each session from that
session's own variables (handed over at registration), never from its own clean
environment.

These reports go to the Probe team, not to the customer's backend, so this is NOT
``probe.sdk.diagnostics.disabled()``: there ``PROBE_DIAGNOSTICS=on`` may override
``PROBE_TELEMETRY=off`` because the data stays in the customer's own tenant. Here
either switch stops the report and neither overrides the other.

An explicit send (``probe doctor --send``, the app's Send log) is the person's own
choice and does not consult this.
"""

from __future__ import annotations

from collections.abc import Mapping

_OFF = frozenset({"off", "0", "false", "no", "disabled"})


def staff_reports_disabled(env: Mapping[str, str], base_url: str | None = None) -> str | None:
    """Why automatic reports are off for ``env``, or None when they may be sent.

    ``base_url`` is the configured backend; ``PROBE_BASE_URL`` in ``env`` outranks it,
    as it does everywhere else in the client. A backend that is not Probe's hosted
    service never gets a report (the self-host egress contract).
    """
    if (env.get("PROBE_TELEMETRY") or "").strip().lower() in _OFF:
        return "telemetry_off"
    if (env.get("PROBE_DIAGNOSTICS") or "").strip().lower() in _OFF:
        return "diagnostics_off"
    # Lazy: probe.sdk costs ~70 ms to import and the service start path has a budget.
    from probe.sdk._telemetry_core import hosted_base_url

    if not hosted_base_url(env.get("PROBE_BASE_URL") or base_url):
        return "not_hosted"
    return None


def allowed(env: Mapping[str, str], base_url: str | None = None) -> bool:
    """Whether an automatic report may be sent for ``env``."""
    return staff_reports_disabled(env, base_url) is None
