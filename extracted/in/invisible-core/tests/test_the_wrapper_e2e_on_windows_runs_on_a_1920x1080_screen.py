"""The Windows legs of `wrapper-on-this-core` declare the runner's screen before they run the wrapper's e2e.

The runner's screen is 1024x768 by default, smaller than the browser window the wrapper's e2e open (1936x1048 for a 1920x1080 identity).
The wrapper's e2e park the OS cursor outside that window before every Windows test (its tests/_os_cursor.py), and the gestures that judge
recorded pointer events require it: a native mouse move for the runner's cursor reaches the page otherwise (wrapper-on-this-core of core
#327, run 45691826441: `mousemove 512,299 buttons=0` in the middle of a drag). 1920x1080 is the largest mode the runner's video device
accepts (run 45730213378 of oss-invisible/playwright) and it leaves the strip below the window free.

The step is the same, byte for byte, as the one in the wrapper's e2e.yml and the engine's gate.yml (one text in three repositories), so its
body is pinned here.
"""
from __future__ import annotations

import pathlib
import re

CI = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"

STEP = """      - name: The runner's screen is 1920x1080, larger than the browser window is tall (read back)
        if: matrix.os == 'windows'
        shell: pwsh
        run: |
          Set-DisplayResolution -Width 1920 -Height 1080 -Force
          Add-Type -AssemblyName System.Windows.Forms
          $b = [System.Windows.Forms.SystemInformation]::VirtualScreen
          "the runner's screen: $($b.Width)x$($b.Height) at $($b.X),$($b.Y)"
          if ($b.Width -lt 1920 -or $b.Height -lt 1080) { Write-Error "the runner's screen is $($b.Width)x$($b.Height), not 1920x1080: the OS cursor could not be parked outside the browser window"; exit 1 }
"""


def _job(text: str, name: str) -> str:
    match = re.search(r"\n  %s:\n(.*?)(?=\n  [a-z0-9-]+:\n|\Z)" % re.escape(name), text, re.S)
    assert match, "ci.yml has no job %r: the check reads nothing" % name
    return match.group(1)


def test_the_wrapper_e2e_on_windows_declare_the_runners_screen_first():
    job = _job(CI.read_text(encoding="utf-8"), "wrapper-on-this-core")
    assert "windows" in job, "wrapper-on-this-core has no Windows leg: the check reads nothing"
    at = job.find(STEP)
    assert at >= 0, "wrapper-on-this-core does not carry the screen step, byte for byte as the wrapper's e2e.yml and the engine's gate.yml have it"
    e2e_at = job.find("the wrapper, then THIS core over its pin")
    assert e2e_at > 0 and at < e2e_at, "the screen step comes after the wrapper is installed and run: the e2e would start on the 1024x768 screen"


def test_the_check_sees_a_missing_or_late_step():
    """The control: the same reading on a job without the step, and with it after the e2e, says so."""
    text = CI.read_text(encoding="utf-8")
    job = _job(text, "wrapper-on-this-core")
    assert job.replace(STEP, "").find(STEP) < 0
    late = job.replace(STEP, "")
    marker = "the wrapper, then THIS core over its pin"
    late = late.replace(marker, marker + "\n" + STEP, 1)
    assert late.find(STEP) > late.find(marker)
