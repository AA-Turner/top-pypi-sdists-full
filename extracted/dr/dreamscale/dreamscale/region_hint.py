"""After connecting to a deployment: one line when another live region is much closer to this
machine than the deployment's own (DSL-367).

It measures the region record's probes (``region_choice.measure_regions``, about a second) while
the session opens, so connect never waits for it: a measurement not finished by then is dropped.
Each deployment is checked once per machine (``region-hints.json`` in the SDK directory),
whether or not a hint came of it. Never raises.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dreamscale.region_probe import RegionProbeResult

STATE_FILE = "region-hints.json"
# Much closer: at least 40 ms less round trip, and at most half of the deployment region's.
MIN_GAIN_MS = 40.0
MAX_FRACTION = 0.5


def _state_path() -> Path:
    from dreamscale.config import dreamscale_home

    return dreamscale_home() / STATE_FILE


def _checked(path: Path) -> list[str]:
    try:
        checked = json.loads(path.read_text()).get("checked")
    except (OSError, ValueError, AttributeError):
        return []
    return [c for c in checked if isinstance(c, str)] if isinstance(checked, list) else []


def _remember(path: Path, deployment_id: str) -> None:
    with contextlib.suppress(OSError):
        checked = [c for c in _checked(path) if c != deployment_id][-199:] + [deployment_id]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"checked": checked}))


def hint_line(result: RegionProbeResult, home: str, labels: dict[str, str]) -> str | None:
    """The hint for a deployment in ``home``, or None when no measured region is much closer
    (or ``home`` itself wasn't measured, or a proxy answered for every region)."""
    if result.intercepted:
        return None
    medians = {m.region: m.median_ms for m in result.measurements if m.median_ms is not None}
    here = medians.get(home)
    others = {r: ms for r, ms in medians.items() if r != home}
    if here is None or not others:
        return None
    best, ms = min(others.items(), key=lambda item: item[1])
    if here - ms < MIN_GAIN_MS or ms > here * MAX_FRACTION:
        return None
    name, home_name = labels.get(best, best), labels.get(home, home)
    return (f"Region: {name} is about {here - ms:.0f} ms closer to this machine than {home_name}, "
            f"where this deployment runs ({ms:.0f} ms against {here:.0f} ms). A deployment "
            f"created with --region {best} would answer faster.")


async def measure(client: Any, deployment_id: str) -> tuple[RegionProbeResult, str,
                                                              dict[str, str]] | None:
    """The live regions measured from here, with the deployment's region and the regions'
    labels; None when it was checked before, or there is nothing to compare."""
    from dreamscale.region_choice import measure_regions

    path = _state_path()
    if deployment_id in _checked(path):
        return None
    deployment = await client.get_checkpoint(deployment_id)
    home = deployment.get("region") if isinstance(deployment, dict) else None
    listed = await client.list_regions()
    live = [r for r in (listed or {}).get("regions") or ()
            if isinstance(r, dict) and r.get("live") and isinstance(r.get("id"), str)]
    candidates = [{"region": r["id"], "url": r["probe_url"]} for r in live if r.get("probe_url")]
    if not isinstance(home, str) or len(candidates) < 2 or home not in {
        c["region"] for c in candidates
    }:
        _remember(path, deployment_id)
        return None
    result = await measure_regions(candidates)
    _remember(path, deployment_id)
    return result, home, {r["id"]: str(r.get("label") or r["id"]) for r in live}


def start(deployment_id: str | None, api_key: str | None,
          client_factory: Callable[..., Any] | None) -> asyncio.Task | None:
    """Measure in the background while the session opens (None: nothing to check)."""
    if deployment_id in (None, "base"):
        return None

    async def run() -> tuple[RegionProbeResult, str, dict[str, str]] | None:
        from dreamscale.config import load_config
        from dreamscale.control import ControlPlaneClient

        config = load_config()
        key = (api_key.strip() if api_key is not None else config.api_key) or None
        if key is None:
            return None
        client = (client_factory or ControlPlaneClient)(config.control_plane_url, key)
        try:
            return await measure(client, deployment_id)
        finally:
            await client.close()

    with contextlib.suppress(Exception):
        return asyncio.ensure_future(run())
    return None


def finish(task: asyncio.Task | None, progress: Callable[[str], None] | None) -> None:
    """Say the hint if the measurement is done and found one; otherwise drop it."""
    if task is None:
        return
    if not task.done():
        task.cancel()
        return
    with contextlib.suppress(Exception):
        found = task.result()
        line = hint_line(*found) if found is not None else None
        if line is not None and progress is not None:
            progress(line)
