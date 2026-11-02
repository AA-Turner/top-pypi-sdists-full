"""uv tool install: update in place under the lock, or side by side beside the running version."""

from __future__ import annotations

import contextlib
import os
import subprocess
import dataclasses
from pathlib import Path

from probe.shared.updates import handoff, installs
from probe.core import adopt as _adopt


def _side_by_side_machine() -> bool:
    """Does this uv tool install update beside the running version (the
    layout is usable here, the receipt names probe-research from its index),
    unless a person asked for in place (IN_PLACE_ENV)?"""
    if os.environ.get(IN_PLACE_ENV) == "1":
        return False
    try:
        return kept_from_uv_receipt() is not None and installs.usable(installs.tool_dir())
    except Exception:  # noqa: BLE001 -- unknown: as before
        return False


def _upgrade_in_place(current: str | None, target: str | None) -> CliResult:
    """The uv tool update before side-by-side installs, under the install lock."""
    # `[all]` is restated FIRST (plan 2.11): `uv tool upgrade` re-resolves the
    # requirement the tool was first installed with, so upgrading a bare
    # receipt onto the release that drops these dependencies from core would
    # strip `probe` -- restating after that upgrade left exactly that window
    # (#2043 review). `uv tool install` REPLACES the receipt, so everything
    # else it records (`--with` packages, extras, the Python) is restated too.
    # In place there is no version to switch back to: a receipt it cannot
    # restate whole is left alone (`faithful_kept_from_uv_receipt`).
    kept = faithful_kept_from_uv_receipt()
    unrecorded = ""
    if kept is not None:
        restated = _run(uv_tool_install_command(kept), _UPGRADE_TIMEOUT_S)
        if restated is None:
            return CliResult(
                False, False, False, current, current, "`uv` not found on PATH",
                missing_binary=True,
            )
        if restated.returncode != 0:
            return CliResult(
                True, False, False, current, current,
                "could not record `probe-research[all]` in this uv tool install "
                f"(`uv tool install` exited {restated.returncode}); the CLI was not upgraded",
            )
    else:
        # A receipt this cannot restate faithfully (an editable `--with`,
        # constraints, probe-research itself from a path) is left alone rather
        # than stripped -- but then `[all]` is not recorded, and the release
        # after this one needs it.
        unrecorded = (
            "; `probe-research[all]` is NOT recorded in this install's uv receipt, which "
            "has entries the wizard's Update cannot restate. Before the next release, run "
            f"`uv tool install '{_dist()}'` with your own `--with` packages"
        )
    if _run(["uv", "tool", "upgrade", DIST], _UPGRADE_TIMEOUT_S) is None:
        return CliResult(
            False, False, False, current, current, "`uv` not found on PATH",
            missing_binary=True,
        )
    result = _finalize(current, target, "uv")
    if not result.ok:
        # `uv tool upgrade` no-ops on a version-pinned install (exits 0, changes
        # nothing), and on uv's cached index when that predates the release
        # (`uv tool upgrade` takes no refresh flag): install the latest from a
        # FRESH index, then re-verify (R9). Not `--force`: a plain install of a
        # new requirement upgrades the environment in place, while `--force`
        # deletes and rebuilds it -- on the newest Python uv has, unless told --
        # under every running `probe` (2026-10-12: a daemon worker crashed
        # reading its own files from the deleted lib/python3.13).
        _run(
            uv_tool_install_command(kept or KeptInstall(), version="@latest", refresh=True),
            _UPGRADE_TIMEOUT_S,
        )
        result = _finalize(current, target, "uv")
    if unrecorded:
        result = dataclasses.replace(result, message=result.message + unrecorded)
    return result


#: Set to 1 to update the uv tool env in place, as before side-by-side installs.
IN_PLACE_ENV = "PROBE_UPDATE_IN_PLACE"


def upgrade_side_by_side(current: str | None, target: str | None) -> CliResult | None:
    """The uv tool update of plan D6: install `target` as its own environment
    beside the running one, check it starts (the service's start path, the
    CLI's import), then switch the tool path to it in one rename and point
    `runtime.json` at it. The running version stays, for the switch back (D5).
    Nothing is changed unless all of that worked: a failed install leaves the
    machine on `current`.

    None when this layout cannot be used here (no target version known,
    probe-research itself installed from a path or URL, another filesystem,
    or IN_PLACE_ENV): the caller decides (`upgrade_cli`: never in place on a
    machine that updates side by side, when it is only the target that is
    unknown). A receipt entry it cannot restate is left out and said
    (`KeptInstall.dropped`); a pinned Python uv cannot use, and `--with`
    packages that will not resolve, are retried without (plan A4)."""
    if not target or os.environ.get(IN_PLACE_ENV) == "1":
        return None
    kept = kept_from_uv_receipt()
    if kept is None:
        return None
    try:
        tools = installs.tool_dir()
        if not installs.usable(tools):
            return None
    except Exception:  # noqa: BLE001 -- unknown: update in place, as before
        return None
    if current and not is_newer(target, current):
        return CliResult(True, True, False, current, current, f"CLI already at the latest ({current})")
    if target in installs.rejected(tools):
        return CliResult(
            True, False, False, current, current,
            f"CLI {target} failed its check on this machine and was switched back; staying on "
            f"{current} for up to {installs.REJECT_TTL_S // 3600} h, or until a newer release",
        )
    handed = _stage1_said(target)
    if handed is not None:
        return dataclasses.replace(handed, before=current, after=current)
    spec = _dist(kept.extras) + f"=={target}"
    try:
        env, dropped = _install_with_fallbacks(target, spec, kept, tools)
    except subprocess.TimeoutExpired as exc:
        return CliResult(True, False, False, current, current,
                         f"could not install CLI {target}: `uv tool install` timed out after {exc.timeout:.0f} s; "
                         "nothing changed, and the next update tries again")
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        return CliResult(True, False, False, current, current, f"could not install CLI {target}; nothing changed: {exc}")
    problem = installs.selftest(env)
    if problem:
        installs.discard(env)
        return CliResult(
            True, False, False, current, current, f"CLI {target} installed but does not start ({problem}); nothing changed"
        )
    try:
        installs.activate(env, tools=tools)
    except (RuntimeError, OSError) as exc:
        return CliResult(True, False, False, current, current, f"could not switch to CLI {target}; nothing changed: {exc}")
    try:
        from probe.foundation import service_api as client

        client.write_runtime(str(installs.env_python(env)), target)
    except Exception:  # noqa: BLE001 -- the service falls back to the tool path, which is this version now
        pass
    missing, pin = [], None
    with contextlib.suppress(Exception):
        missing, pin = record_left_out(kept, env, tools, list(dropped))
    installs.prune(tools)
    note = dropped_note(kept)
    if missing or pin:
        left = [*(f"--with {item}" for item in missing), *([f"--python {pin}"] if pin else [])]
        note += (f"; left out {', '.join(left)}, which would not install beside it "
                 "(`probe doctor` shows how to add them back)")
    return CliResult(
        True, True, True, current, target,
        f"CLI upgraded {current} → {target} (beside {current}, which stays for a switch back){note}",
    )


def _stage1_said(target: str) -> CliResult | None:
    """The hand-off's stage 1 already tried this update in this process
    (`probe.core.adopt`) and could not: its reason, rather than a second
    install that fails the same way. None when it did not, or went fine."""
    try:
        answer = _adopt.stage1_answer() or {}
    except Exception:  # noqa: BLE001
        return None
    result = answer.get("result")
    if result == handoff.Result.BUSY:
        return CliResult(True, False, False, None, None, LOCK_BUSY_MESSAGE)
    if result == handoff.Result.UNCHECKED and answer.get("latest") == target:
        # Installed; its check timed out (a loaded machine). Never switched to
        # by this (old) code: the next update checks it again and hands over.
        return CliResult(
            True, False, False, None, None,
            f"CLI {target} is installed, but its check timed out; nothing changed, and the next update "
            f"tries again ({clean_reason(answer.get('detail'))})",
        )
    if result == handoff.Result.INSTALL_FAILED and answer.get("latest") == target:
        return CliResult(
            True, False, False, None, None,
            f"could not install CLI {target}; nothing changed: {clean_reason(answer.get('detail'))}",
        )
    return None


def _install_with_fallbacks(target: str, spec: str, kept: KeptInstall, tools: Path, *,
                            rebuild: bool = False) -> tuple[Path, tuple]:
    """`installs.install` tried in the hand-off's order (`handoff.attempts`,
    plan A4): as recorded with the `--with` packages an earlier install left
    out (`installs.dropped_with`) again first, then without the Python pin (a
    new env needs none), then without those, then without any `--with` --
    the last resort on any failure -- within `handoff.INSTALL_BUDGET_S`. A uv
    that times out ends it at once (`subprocess.TimeoutExpired` rises: the
    machine or the network, not the package set). `rebuild`: the version's
    env there is broken (`installs.install`). `(env, the --with packages left
    out)`; the last failure raises."""
    import time

    tries = handoff.attempts(list(kept.with_packages), installs.dropped_with(tools), kept.python)
    every = tries[0][0]
    budget_ends = time.monotonic() + handoff.INSTALL_BUDGET_S
    failure: Exception | None = None
    for packages, python in tries:
        left = min(_UPGRADE_TIMEOUT_S, budget_ends - time.monotonic())
        if left <= 0:
            break
        try:
            env = installs.install(target, spec, with_packages=tuple(packages), python=python, tools=tools,
                                   timeout=left, **({"rebuild": True} if rebuild else {}))
        except (handoff.LockBusy, subprocess.TimeoutExpired):
            raise
        except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
            failure = exc
            continue
        return env, tuple(item for item in every if item not in packages)
    raise failure or RuntimeError(f"the install ran out of its {handoff.INSTALL_BUDGET_S:g} s")
from probe.cli.install.updater.cli_install import LOCK_BUSY_MESSAGE, _UPGRADE_TIMEOUT_S, _dist  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.cli_versions import CliResult, _finalize, _run  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.updater import DIST  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.updater.uv_receipt import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    KeptInstall,
    dropped_note,
    faithful_kept_from_uv_receipt,
    kept_from_uv_receipt,
    record_left_out,
    uv_tool_install_command,
)
from probe.shared.harness.plugin_update import clean_reason, is_newer  # noqa: E402 -- pieces need each other; the front door loads this one first
