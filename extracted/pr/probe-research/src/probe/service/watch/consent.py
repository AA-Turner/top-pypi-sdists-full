"""may a report be sent: a session family's consent from its own environment, a machine family's from every live session."""

from __future__ import annotations

import asyncio
from collections.abc import Mapping
from dataclasses import dataclass
from probe.service.watch.incident import Incident, SESSION_FAMILIES
from probe.service.watch.loop import _on_daemon_thread
from probe.service.watch.settings import CREDENTIAL_TIMEOUT_S, LOGIN_CACHE_S
#: The variables a report's consent reads (`report_policy`), never more of an environment.
CONSENT_VARS = ("PROBE_TELEMETRY", "PROBE_DIAGNOSTICS", "PROBE_BASE_URL")


# -- consent ------------------------------------------------------------------


def consent_env(env: object) -> dict:
    """The variables of `env` the consent reads (CONSENT_VARS), and nothing else."""
    if not isinstance(env, Mapping):
        return {}
    return {name: env[name] for name in CONSENT_VARS if isinstance(env.get(name), str)}


def config_base_url() -> str | None:
    """The CLI config's backend (its active context), or None. Blocking (a file
    read, and `probe.sdk`'s telemetry core: ~70 ms the first time): a thread."""
    try:
        from probe.analytics.core import read_cli_config

        value = read_cli_config().get("base_url")
    except Exception:  # noqa: BLE001 -- no config: the hosted default
        return None
    return value if isinstance(value, str) and value else None


def env_allows(env: Mapping | None, base_url: str | None) -> bool:
    """`report_policy.allowed` for `env`'s consent variables; False when it
    cannot be asked (fail closed). Blocking the first time (its lazy import)."""
    try:
        from probe.analytics import report_policy

        return report_policy.allowed(consent_env(env or {}), base_url)
    except Exception:  # noqa: BLE001
        return False


@dataclass
class Live:
    """A session whose agent runs, as consent sees it: the environment its
    recorder runs with (hosted), else what its registrant said (`report_env`)."""

    sid: str
    hosted_env: dict | None = None
    report_env: bool | None = None


def decide_session(live: Live | None, env: dict | None, base_url: str | None) -> tuple[bool, str, dict]:
    """A session family's consent: `(allowed, why, the env the child gets)`.
    `env`: the consent variables noted with the incident (the recorder's or
    worker's own environment), which come first."""
    if env is None and live is not None and live.hosted_env is not None:
        env = consent_env(live.hosted_env)
    if env is not None:
        ok = env_allows(env, base_url)
        return ok, "its environment allows reports" if ok else "its environment turns reports off", env
    if live is not None and live.report_env is not None:
        return live.report_env, f"its registrant said report_env {str(live.report_env).lower()}", {}
    return False, "nothing says this session allows reports", {}


def decide_machine(live: list, base_url: str | None, login: dict | None) -> tuple[bool, str]:
    """A machine family's consent: every session whose agent runs allows it;
    with none, `login` (the login shell's variables) and the CLI config's
    backend; unknown is no."""
    if live:
        for session in live:
            ok, _, _ = decide_session(session, None, base_url)
            if not ok:
                return False, f"session {session.sid} does not allow reports"
        return True, f"every session ({len(live)}) allows reports"
    if login is None:
        return False, "no session, and the login environment could not be read"
    if env_allows(login, base_url):
        return True, "no session; the login environment allows reports"
    return False, "no session; the login environment turns reports off"


async def login_env() -> dict | None:
    """The login shell's consent variables (`loginenv`), or None when it cannot
    be asked (no shell, Windows)."""
    from ..actions import loginenv

    found = await loginenv.read(names=CONSENT_VARS)
    return None if found is None else consent_env(found[1])


def _unknown(live: Live) -> bool:
    """Says nothing yet: no environment of its recorder's, no `report_env`."""
    return live.hosted_env is None and live.report_env is None


def merge_voters(then: list, now: list) -> list:
    """Every session of either moment: one that ran then counts as it was
    (it ended or not); one whose consent was not yet known then (a hosted
    session restored before its recorder resumed) is asked as it is now."""
    merged = {v.sid: v for v in then}
    for live in now:
        if live.sid not in merged or _unknown(merged[live.sid]):
            merged[live.sid] = live
    return list(merged.values())


class ConsentMixin:
    """Part of Watch: its methods run with `self` the Watch; compose() folds them into Watch."""

    async def _may_ask_keys(self) -> bool:
        """The consent a `credential_refused` report would need, asked before
        the keys are: a check whose answer could not be reported is not made."""
        try:
            allowed, _ = await self.machine_consent()
        except (asyncio.TimeoutError, RuntimeError):
            return False  # the config cannot be read: no
        return allowed

    async def machine_consent(self) -> tuple[bool, str | None]:
        """A machine family's consent as it stands (every session whose agent
        runs, else the login shell, and the CLI config's backend), and that
        backend (None: unset, the hosted default). Raises when the config
        cannot be read in time."""
        # A daemon thread of its own: a hung home mount is left behind, never
        # joined at exit. Raises (TimeoutError, RuntimeError) when the config
        # cannot be read: "unread" is not "unset" (None, the hosted default).
        base_url = await _on_daemon_thread(config_base_url, CREDENTIAL_TIMEOUT_S)
        voters = list(self.voters())
        login = None if voters else await self._login_env()
        allowed, _ = await asyncio.to_thread(decide_machine, voters, base_url, login)
        return bool(allowed), base_url

    async def _consent(self, incident: Incident, base_url: str | None) -> tuple[bool, str, dict]:
        """From what it was noted with: the environments it happened in, and
        the sessions whose agent ran then (or, with none, the login shell).
        Looked at while discovering, or tried again after a failed try: the
        sessions of THIS moment are asked too (`merge_voters`)."""
        voters = list(incident.voters or [])
        if incident.partial or incident.first_try is not None:
            voters = merge_voters(voters, list(self.voters()))
        for env in incident.envs:
            if not await asyncio.to_thread(env_allows, env, base_url):
                return False, "the environment it happened in turns reports off", {}
        if incident.family in SESSION_FAMILIES:
            if incident.envs:
                return True, "its environment allows reports", dict(incident.envs[-1])
            own = next((v for v in voters if v.sid == incident.sid), None)
            return await asyncio.to_thread(decide_session, own, None, base_url)
        login = None
        if not voters:
            login = await self._login_env()
        allowed, why = await asyncio.to_thread(decide_machine, voters, base_url, login)
        return allowed, why, {}

    async def _login_env(self) -> dict | None:
        cached = self._login_cache
        if cached is not None and self.monotonic() - cached[0] < LOGIN_CACHE_S:
            return cached[1]
        try:
            found = await self.login()
        except Exception:  # noqa: BLE001 -- unknown: no
            found = None
        self._login_cache = (self.monotonic(), found if isinstance(found, dict) else None)
        return self._login_cache[1]
