"""The pause keeper: lift an outbox pause that no longer holds and start its drainer with the login shell's environment."""

from __future__ import annotations

import asyncio
import os
import sys

from ..actions import caller
from ...foundation.service_api import paths
from ...foundation.service_api.vocabularies import BackgroundRefusal
from ...foundation.service_api.env import BASE_URL_ENV
from probe.service.server.policy import log


class OutboxMixin:
    """Part of Service: its methods run with `self` the Service; compose() folds them into Service."""

    async def _keep_outbox(self) -> None:
        """At start and every OUTBOX_LOOK_S: lift an outbox pause that no longer holds and start the drainer for
        what it held (jobs/background/DESIGN.md, Traps: "The pause keeper")."""
        period = _get_outbox_look_s()
        if period <= 0:
            return
        while self.stop_reason is None:
            try:
                lifted, root, held = await asyncio.to_thread(_lift_outbox_pause, None)
                if lifted:
                    log(f"lifted an outbox pause that no longer held ({held} write(s) queued)")
                    env = await _build_drainer_env() if held else None
                    if env is not None:
                        request = {"dir": root, "python": sys.executable, "cwd": None, "env": env}
                        answer = await asyncio.to_thread(
                            lambda: self.background.drain(request) if _is_base_url_allowed(env)
                            else {"accepted": False, "reason": BackgroundRefusal.UNKNOWN_ENDPOINT})
                        log(f"outbox drainer: {answer.get('state') or answer.get('reason')}")
            except Exception as exc:  # noqa: BLE001 -- the next look tries again
                log(f"outbox look failed: {type(exc).__name__}")
            try:
                await _restore_outbox()
            except Exception as exc:  # noqa: BLE001 -- the next look tries again
                log(f"outbox restore look failed: {type(exc).__name__}")
            await asyncio.sleep(period)


#: How often the service looks for an outbox pause that no longer holds: one stat.
OUTBOX_LOOK_S = 60.0
#: Test-only: the look's period in seconds, "0" off (the suite's services).
OUTBOX_LOOK_ENV = "PROBE_SERVICE_OUTBOX_S"


def _get_outbox_look_s() -> float:
    try:
        return float(os.environ.get(OUTBOX_LOOK_ENV) or OUTBOX_LOOK_S)
    except ValueError:
        return OUTBOX_LOOK_S


async def _build_drainer_env() -> dict | None:
    """The outbox drainer's environment, from the login shell as every other
    network child of this service gets it (`loginenv`): PATH, where the outbox
    and the stored login are, the proxies and CAs, and the person's report
    switches (`watch.CONSENT_VARS`), by `runtime_env_name` (never a
    credential). None when the login shell cannot be read."""
    from ..actions import loginenv
    from .. import watch
    from ...foundation.service_api.env import runtime_env_name

    names = tuple(sorted({*loginenv.NAMES, *watch.CONSENT_VARS, "PROBE_OUTBOX_DIR", "PROBE_OUTBOX_RESCUE"}))
    read = await loginenv.read(names=names)
    if read is None:
        return None
    login_path, values = read
    env = {"PATH": loginenv.build_path(login_path, os.environ.get("PATH"), paths.home())}
    env.update({name: value for name, value in values.items() if value and runtime_env_name(name)})
    return env


def _is_base_url_allowed(env: dict) -> bool:
    """May a drainer run with `env`'s PROBE_BASE_URL (plan D10: the stored
    login follows it)? Unset, or https and an endpoint that login may go to
    (`caller.known_endpoint`). Blocking (reads the CLI config): a thread."""
    url = env.get(BASE_URL_ENV) or None  # empty is unset, as `config.resolve` reads it
    return url is None or (url.startswith("https://") and caller.known_endpoint(url, env))


# -- ONE-TIME (`sdk/delivery/journal/failures/restores.py`; delete with it) -------------


async def _restore_outbox() -> None:
    """The one-time restore of set-aside writes, with no command run: while this service's
    outbox root has no `.restore-done` marker, start the rescuer at most every 10 minutes
    (`claim_restore`) with the login shell's variables, as the drainer gets them (the person's
    report switches and `PROBE_OUTBOX_RESCUE` included). One stat once the marker is there."""
    root = await asyncio.to_thread(_claim_outbox_restore)
    if root is None:
        return
    env = await _build_drainer_env()
    if env is None:
        return
    started = await asyncio.to_thread(lambda: _is_base_url_allowed(env) and _start_outbox_restore(root, env))
    log(f"outbox restore: rescuer {'started' if started else 'not started'}")


def _claim_outbox_restore() -> str | None:
    """This service's outbox root when its restore is due (`claim_restore`), else None: not
    while paused or with the rescue switched off here. Blocking: a thread."""
    from probe.sdk.delivery import outbox as outbox_worker
    from probe.sdk.delivery.journal.journal import Journal
    from probe.sdk.delivery.journal.paths import default_root

    root = default_root(None)
    if not outbox_worker.rescue_enabled() or os.path.lexists(root / "paused"):
        return None
    return str(root) if outbox_worker.claim_restore(Journal(str(root))) else None


def _start_outbox_restore(root: str, env: dict) -> bool:
    """Start the rescuer for ``root`` with ``env`` (the login shell's), unless its
    `PROBE_OUTBOX_RESCUE` is off. Blocking: a thread."""
    from probe.sdk.delivery import outbox as outbox_worker
    from probe.sdk.delivery.journal.journal import Journal

    if not outbox_worker.rescue_enabled(env):
        return False
    return outbox_worker.spawn_rescuer(Journal(root), env=env)


def _lift_outbox_pause(env: dict | None) -> tuple[bool, str, int]:
    """Lift the pause of the outbox `env` names (the login shell's variables;
    None: this service's own) when it no longer holds, reporting nothing:
    `(lifted, outbox root, writes it held)`. One stat when there is no marker."""
    from probe.sdk.delivery import outbox as outbox_worker
    from probe.sdk.delivery.journal.journal import Journal
    from probe.sdk.delivery.journal.paths import default_root

    root = default_root(env)
    if not os.path.lexists(root / "paused"):
        return False, str(root), 0
    status = Journal.read_status(str(root)) or {}
    lifted = outbox_worker.lift_stale_pause(Journal(str(root)), status, base_url=None, wait=False)
    return lifted, str(root), int(status.get("pending") or 0) + int(status.get("waiting") or 0)
