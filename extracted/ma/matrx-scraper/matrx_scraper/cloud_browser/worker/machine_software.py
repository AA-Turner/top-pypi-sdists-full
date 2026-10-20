"""Record a Cloud Computer person's system installs into their home (ruling 16).

The machine's root filesystem is new on every task; ``cloud-computer-software``
(the image's script) records apt packages and new system files into the home and
replays them at wake. The control plane calls this at save-before-stop so a
``pip install`` into /usr/local (no apt hook sees it) is kept too. Off a Cloud
Computer image the script is absent and the answer says so (never a fake yes).
"""

from __future__ import annotations

import asyncio
import os

SOFTWARE_SCRIPT = "/usr/local/bin/cloud-computer-software"
CARRYOVER_SCRIPT = "/usr/local/bin/cloud-computer-carryover"
SOFTWARE_STATUS = "/run/cloud-computer/software.json"


async def record_software(script: str = SOFTWARE_SCRIPT) -> dict[str, object]:
    if not os.access(script, os.X_OK):
        return {"recorded": False, "reason": "not a Cloud Computer image"}
    proc = await asyncio.create_subprocess_exec(
        "sudo", "-n", script, "record",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    _out, err = await proc.communicate()
    detail = err.decode(errors="replace").strip().splitlines()
    return {
        "recorded": proc.returncode == 0,
        "exit_code": proc.returncode,
        "detail": detail[-1][:300] if detail else "",
    }


def software_status(path: str = SOFTWARE_STATUS) -> dict[str, object]:
    """The wake-time replay's own progress file, or ``state: unknown``."""
    import json

    try:
        with open(path, encoding="utf-8") as f:
            return dict(json.load(f))
    except (OSError, ValueError):
        return {"state": "unknown"}


async def carryover_snapshot(auth_domains: list[str], script: str = CARRYOVER_SCRIPT) -> dict[str, object]:
    """The carry-over check's snapshot of this machine (counts, names, hashes;
    never cookie values). Run as root so system paths and the profile read alike."""
    import json

    if not os.access(script, os.X_OK):
        return {"available": False, "reason": "not a Cloud Computer image"}
    args = ["sudo", "-n", script, "snapshot"]
    for domain in auth_domains:
        args += ["--auth-domain", domain]
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    if proc.returncode != 0:
        return {"available": False, "reason": err.decode(errors="replace").strip()[-300:]}
    return {"available": True, "snapshot": json.loads(out)}
