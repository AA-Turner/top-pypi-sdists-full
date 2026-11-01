import subprocess
import sys

import pytest

from probe.analytics import report_policy


@pytest.mark.parametrize(
    ("env", "base_url", "reason"),
    [
        ({}, None, None),
        ({}, "https://api.research.prbe.ai", None),
        ({"PROBE_TELEMETRY": "off"}, None, "telemetry_off"),
        ({"PROBE_TELEMETRY": " False "}, None, "telemetry_off"),
        ({"PROBE_DIAGNOSTICS": "0"}, None, "diagnostics_off"),
        # Unlike SDK diagnostics, an explicit "on" does not override telemetry-off here.
        ({"PROBE_TELEMETRY": "off", "PROBE_DIAGNOSTICS": "on"}, None, "telemetry_off"),
        ({}, "https://probe.example.com", "not_hosted"),
        ({}, "http://api.research.prbe.ai", "not_hosted"),
        ({"PROBE_BASE_URL": "https://probe.example.com"}, "https://api.research.prbe.ai", "not_hosted"),
        ({"PROBE_BASE_URL": "https://api.research.prbe.ai"}, "https://probe.example.com", None),
    ],
)
def test_staff_reports_disabled(env, base_url, reason):
    assert report_policy.staff_reports_disabled(env, base_url) == reason
    assert report_policy.allowed(env, base_url) is (reason is None)


def test_import_stays_light():
    """Importing the policy loads the stdlib-only analytics package (whole, by design: a piece
    first loaded at exit would clear CPython's uncaught-Ctrl-C exit), never the CLI, a
    third-party library or the sender thread. The service's start path, which must not load
    even that, is pinned by tests/test_service_import_budget.py."""
    code = (
        "import sys, threading; import probe.analytics.report_policy; "
        "heavy = ('httpx', 'pydantic', 'typer', 'mcp', 'probe.cli', 'probe.sdk.client'); "
        "print(sorted(m for m in heavy if m in sys.modules), threading.active_count())"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "[] 1"
