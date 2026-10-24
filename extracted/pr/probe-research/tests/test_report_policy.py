import subprocess
import sys

import pytest

from probe._shared import report_policy


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
    """The service imports this on its start path: the telemetry core loads only when asked."""
    code = "import sys; import probe._shared.report_policy; print('probe.sdk._telemetry_core' in sys.modules)"
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "False"
