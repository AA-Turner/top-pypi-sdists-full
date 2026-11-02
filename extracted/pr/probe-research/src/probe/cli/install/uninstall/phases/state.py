"""state: remove Probe's files and saved accounts, never through a symlink, pruning emptied parents."""

from __future__ import annotations

import contextlib
import json
import os
import shutil
import sys
from pathlib import Path


# -- state (U-T8) --------------------------------------------------------------------------------


def _remove_path(path: Path) -> bool:
    """Remove one path, never through a symlink. True when it is gone."""
    if not os.path.lexists(path):
        return True
    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    return True


def standard_folders() -> set:
    """Folders an uninstall never removes, empty or not: HOME, its XDG and
    `~/.local` folders, and every coding agent's home."""
    home = Path.home()
    found = {home, home / ".config", home / ".cache", home / ".local", home / ".local" / "state",
             home / ".local" / "share", home / ".local" / "bin"}
    for name in ("XDG_CONFIG_HOME", "XDG_CACHE_HOME", "XDG_STATE_HOME", "XDG_DATA_HOME", "XDG_BIN_HOME"):
        if os.environ.get(name):
            found.add(Path(os.environ[name]))
    with contextlib.suppress(Exception):
        from probe.foundation.harness_registry import get_registry

        found.update(h.home_dir() for h in get_registry().all() if h.home_dir() is not None)
    return found


def prune_empty_parents(path: Path, stop: Path | None = None) -> None:
    """rmdir `path`'s parents while they are empty: the folders Probe's files
    were the only reason for (`.../plugins/marketplaces/` around Probe's clone).
    Never a standard folder (`standard_folders`), never `stop`, never above
    HOME; a folder with anything in it stays."""
    keep = standard_folders()
    if stop is not None:
        keep.add(Path(stop))
    home = Path.home()
    for parent in Path(path).parents:
        if parent in keep or home not in parent.parents:
            return
        try:
            parent.rmdir()
        except OSError:
            return


def _clear_config(lines: list[str]) -> None:
    """Every saved account goes; the file too when it holds nothing else of
    the researcher's (and is not a dotfile manager's symlink)."""
    from probe.sdk.settings import settings as config_mod

    path = config_mod.config_path()
    try:
        raw = json.loads(Path(os.path.realpath(path)).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return
    except (OSError, ValueError) as exc:
        lines.append(f"! could not read {path} ({exc}); delete the saved Probe accounts in it by hand.")
        return
    probe_keys = {"version", "current_context", "contexts", *config_mod._CONTEXT_KEYS}  # noqa: SLF001
    others = {k: v for k, v in raw.items() if k not in probe_keys} if isinstance(raw, dict) else {}
    if not others and not path.is_symlink():
        _remove_path(path)
        prune_empty_parents(path)
        lines.append(f"Removed {path} (every saved Probe account).")
        return
    kept = {**others, "version": raw.get("version", config_mod.CONFIG_VERSION), "contexts": {}}
    try:
        config_mod.save_file(kept)
        lines.append(f"Removed every saved Probe account from {path}; kept the rest of the file.")
    except Exception as exc:  # noqa: BLE001
        lines.append(f"! could not clear {path} ({exc}); delete the saved Probe accounts in it by hand.")


def _runs_from_plan(plan: dict) -> bool:
    """Is this interpreter one of the env generations the finisher deletes?"""
    here = os.path.realpath(sys.prefix)
    if any(part in here.replace(os.sep, "/") for part in ("/.cache/uv/", "/Caches/uv/", "/uv/archive-")):
        return True  # `npx probe-research uninstall`'s throwaway env: uv's cache, uv's to clean
    for env in plan.get("env_generations", []):
        real = os.path.realpath(env)
        if here == real or here.startswith(real.rstrip(os.sep) + os.sep):
            return True
    return False


def _phase_state(run: Run) -> list[str]:
    from probe.cli.install.uninstall import plan as uninstall_plan
    from probe.core import events

    lines = run.out
    _recount_unsent(run)
    with contextlib.suppress(Exception):
        from probe.cli.install.uninstall import agent_traces as uninstall_agents

        lines.extend(uninstall_agents.remove_hollow())  # again: a run resumed at "state" skipped integrations
    _telemetry_done(run)
    # Nothing in this process writes Probe's files again from here.
    os.environ["PROBE_TELEMETRY"] = "off"
    with contextlib.suppress(Exception):
        from probe.cli.imports import jobs as import_jobs

        if import_jobs.clear_all():
            lines.append("Cleared Probe's import jobs.")
    _clear_config(lines)
    fresh = uninstall_plan.state_layout()
    planned = [p for p in run.plan.get("paths", []) if p.get("stage") == uninstall_plan.STAGE_STATE]
    by_path = {p["path"]: p for p in planned}
    for item in fresh["paths"]:
        by_path.setdefault(item["path"], item)
    from probe.shared.updates import finisher

    left = []
    for item in finisher.ordered(list(by_path.values())):
        path = Path(item["path"])
        if item.get("empty_only"):
            with contextlib.suppress(OSError):
                path.rmdir()
                prune_empty_parents(path)
            continue
        if not _remove_path(path):
            left.append(str(path))
        else:
            prune_empty_parents(path)
    for line in fresh["kept"]:
        lines.append(f"Kept {line}.")
    if not _runs_from_plan(run.plan):
        lines.append(f"Kept the `probe` this runs from ({sys.prefix}): it is not Probe's managed install. Remove it "
                     "with what installed it (`pipx uninstall probe-research`, or `pip uninstall probe-research`).")
    for path in left:
        lines.append(f"! could not remove {path}")
    from probe.sdk.settings.settings import load_context

    try:
        signed_in = bool((load_context() or {}).get("token"))
    except Exception:  # noqa: BLE001 - an unreadable config holds no credential
        signed_in = False
    offline = run.options.offline or bool((run.plan.get("server") or {}).get("offline"))
    if not run.options.embedded:
        events.agent_result(None, requested={"signed_in": False}, actual={"signed_in": signed_in},
                            ok=not signed_in,
                            message=f"offline: revoke this computer's keys in {_dashboard_hint()}" if offline else "")
    _step(events.Step.UNINSTALL_STATE, events.Status.FAILED if left else events.Status.DONE,
          f"{len(left)} path(s) left" if left else "Probe's files for this user removed")
    if left:
        raise Stop(EXIT_PARTIAL, (
            f"probe uninstall: {len(left)} of Probe's files could not be removed (above). Fix that, then run "
            "`probe uninstall` again to finish."))
    return lines
from probe.cli.install.uninstall.phases.draining import _recount_unsent  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.phases.server import _dashboard_hint  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.state import Run, Stop, _step  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.telemetry import _telemetry_done  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_PARTIAL, run  # noqa: E402 -- pieces need each other; the front door loads this one first
