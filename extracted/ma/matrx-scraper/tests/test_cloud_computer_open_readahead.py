"""A cold open's first Chrome launch reads Chrome from the page cache, not ECR.

The Cloud Computer image is lazily loaded (SOCI): every file is fetched the first
time it is read. Chrome's launch inside /bootstrap took 8.7-9.2 s on a just-woken
machine and 2.5-3 s on a warm one (FIX-COLD-OPEN 2026-10-18). The image now lists
Chrome, the Playwright driver and the stream page at build time and the entrypoint
reads them right after the worker's boot files. Each check failed before the change.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "docker" / "cloud-computer"
DOCKERFILE = (ROOT / "Dockerfile").read_text()
ENTRYPOINT = ROOT / "cloud-computer-entrypoint.sh"


def test_the_image_lists_what_the_first_picture_waits_on() -> None:
    assert "/usr/local/share/cloud-computer/open-files" in DOCKERFILE
    block = DOCKERFILE.split("list=/usr/local/share/cloud-computer/open-files", 1)[1].split("\n\n", 1)[0]
    for path in ("/opt/google/chrome", "$driver", "/opt/selkies-gstreamer/share/selkies-web"):
        assert path in block, f"{path} is not read ahead"
    assert "playwright" in block and "ldd /opt/google/chrome/chrome" in block
    assert 'test "$(wc -l < "$list")" -gt 100' in block  # an empty list fails the build


def test_the_entrypoint_reads_them_after_the_boot_files_in_the_background(tmp_path: Path) -> None:
    text = ENTRYPOINT.read_text()
    assert subprocess.run(["bash", "-n", str(ENTRYPOINT)]).returncode == 0
    boot, opened = text.index('< "${boot_files}" | xargs'), text.index('< "${open_files}" | xargs')
    assert boot < opened, "Chrome must not crowd out the worker's own imports"
    block = text[text.index("open_files=") : text.index("} &") + 3]
    # Run the real block against stand-in lists: both are read, and a missing
    # list or unreadable file never stops the machine from booting.
    seen = tmp_path / "seen"
    a, b = tmp_path / "a", tmp_path / "b"
    a.write_text("x")
    b.write_text("y")
    (tmp_path / "boot").write_text(f"{a}\n{tmp_path / 'missing'}\n")
    (tmp_path / "open").write_text(f"{b}\n")
    script = (
        "set -euo pipefail\n"
        f"boot_files={tmp_path / 'boot'}\n"
        + block.replace("open_files=/usr/local/share/cloud-computer/open-files", f"open_files={tmp_path / 'open'}")
        .replace("cat >/dev/null 2>&1", f"cat >>{seen} 2>/dev/null")
        + "\nwait\necho booted\n"
    )
    out = subprocess.run(["bash", "-c", script], capture_output=True, text=True, timeout=30)
    assert out.returncode == 0 and out.stdout.strip() == "booted", out.stderr
    assert seen.read_text() == "xy"
