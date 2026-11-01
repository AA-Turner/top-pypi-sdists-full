"""Old entry paths other releases run: `python -m probe.sdk.outputs` (every log helper's call after a
hard kill) and the `sdk/logcapture.py` file an older release's process starts its log helper from."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import probe.sdk.capture.logs.logs as logs

PY = sys.executable
#: The old file: an older release's `logcapture` module, upgraded under it, still names this path.
OLD_HELPER_FILE = Path(logs.__file__).resolve().parents[2] / "logcapture.py"


def test_the_output_entry_runs_its_recovery_under_w_error(tmp_path):
    # -W error makes runpy's "found in sys.modules" warning fatal: the shim must call the loaded piece.
    entry = tmp_path / "entry.json"
    proc = subprocess.run(
        [PY, "-W", "error", "-m", "probe.sdk.outputs", "--writer-gone", str(entry)],
        capture_output=True, text=True, timeout=60, cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    assert (tmp_path / "entry.json.gone").exists(), "the writer-gone reporter never claimed its entry"


def test_a_helper_started_from_the_old_file_still_tees_the_log(tmp_path):
    # The helper runs `python -I -S <its module's __file__>`: no site-packages, so the stub must
    # run the moved file by path, never import probe.
    script = tmp_path / "older_release.py"
    script.write_text(
        "import json, os\n"
        "from probe.sdk.capture.logs import logs\n"
        f"logs.__file__ = {str(OLD_HELPER_FILE)!r}\n"
        f"tee = logs.InProcessTee({str(tmp_path / 'run.log')!r})\n"
        "tee.start()\n"
        "print('through the old file', flush=True); os.write(2, b'fd2\\n')\n"
        "print('stats ' + json.dumps(tee.stop()))\n"
    )
    proc = subprocess.run([PY, str(script)], capture_output=True, timeout=60)
    assert proc.returncode == 0, proc.stderr
    log = (tmp_path / "run.log").read_bytes()
    assert b"through the old file\n" in log and b"fd2\n" in log
    assert b'"omitted_bytes": 0' in proc.stdout
