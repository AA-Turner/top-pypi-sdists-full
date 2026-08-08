"""Wire the registry credential socle to the env resolver and the install tools.

This is the layer the socle deliberately leaves out: resolving the token's
*value* (process environment, on-disk cache, user prompt) goes through
the ``env`` group, which ``common/`` cannot import.

Everything here is resolved **once per process** and shared by the three tools
(``uv``, ``node``, ``docker``). That is not an optimisation but the correctness
requirement behind AC-4: rotating invalidates the old token, so three tools each
rotating on their own would leave two of them holding a dead credential. The
first one to need it rotates, re-poses the new value in every ecosystem that
already held one, and the others reuse it.
"""

import os
from dataclasses import dataclass, field
from datetime import UTC, datetime

import typer

from ..common.registry_auth import docker as docker_writer
from ..common.registry_auth import journal, pat
from ..common.registry_auth import npm as npm_writer
from ..common.registry_auth import uv as uv_writer
from ..common.registry_auth.consumer import ApplyResult, RegistryConsumer
from ..common.registry_auth.targets import RegistryTargets, detect_targets
from ..env import cache
from ..env.resolve import try_auto_resolve
from .common.base import InstallReport, ToolState

TOKEN_VAR = "GITLAB_REGISTRY_TOKEN"

# One entry per ecosystem the credential is posed in. Order is the order a
# post-rotation re-pose walks them in.
CONSUMERS: tuple[RegistryConsumer, ...] = (uv_writer.consumer, npm_writer.consumer, docker_writer.consumer)

CONSUMERS_BY_NAME: dict[str, RegistryConsumer] = {c.name: c for c in CONSUMERS}


@dataclass
class Credential:
    """The token in use for this process, plus what GitLab says about it."""

    token: str
    targets: RegistryTargets
    info: pat.TokenInfo | None = None
    rotated: bool = False
    reposed: tuple[str, ...] = field(default_factory=tuple)
    # False for a credential merely read to report state: `state_of` builds one
    # without arbitrating rotation, and it must not be mistaken for a credential
    # the rotation pipeline has already cleared (see `credential`).
    rotation_arbitrated: bool = False

    @property
    def usable(self) -> bool:
        """True when GitLab confirmed the token authenticates with every scope.

        ``info is None`` means GitLab could not be reached or rejected it — we
        do not assume a token is good just because we hold one.
        """
        return self.info is not None and self.info.usable


# Per-process memo. A dict rather than a module global so mutation needs no
# ``global`` statement; the key is fixed — there is only ever one credential.
_MEMO: dict[str, object] = {}
_TARGETS_KEY = "targets"
_CREDENTIAL_KEY = "credential"
_JOURNAL_KEY = "journal"


def reset() -> None:
    """Drop the per-process memo (tests, and any caller that changed the repo)."""
    _MEMO.clear()


def targets() -> RegistryTargets:
    """The resolved targets, detected once per process."""
    cached = _MEMO.get(_TARGETS_KEY)
    if isinstance(cached, RegistryTargets):
        return cached
    resolved = detect_targets()
    _MEMO[_TARGETS_KEY] = resolved
    return resolved


def creation_hint() -> str:
    """Pre-filled creation link for the resolved host — the prompt's help text."""
    return pat.creation_url(targets().host)


def resolve_token() -> str:
    """Resolve the PAT: the environment first, then the resolver chain and cache.

    The environment wins — that is the CI and troubleshooting path. It is used to
    *obtain* the token, never handed to the package managers as a variable they
    would interpolate.

    No prompt here. Asking the user is the install framework's job: the tools
    declare the variable as ``env_optional``, and the orchestrator's env phase
    prompts for it (with the pre-filled creation link, from ``ENV_CONFIG``)
    before any tool is configured. By the time this runs, the answer is already
    in the environment or the cache.
    """
    existing = os.environ.get(TOKEN_VAR)
    if existing:
        return existing

    return try_auto_resolve(TOKEN_VAR) or ""


def _persist(token: str) -> None:
    """Make ``token`` the value later resolutions see, in this process and on disk."""
    os.environ[TOKEN_VAR] = token
    cache.write(TOKEN_VAR, token)


def _persist_resolved(cred: Credential) -> None:
    """Cache a token GitLab has just validated, so the next run need not ask again.

    The environment is a legitimate way in — the installer resolves the credential
    before this package exists on the machine, then hands it over that way — but
    :func:`resolve_token` returns an environment value untouched, and
    ``try_auto_resolve`` only writes back what its *own* resolvers produced. Left
    alone, a token that arrived through the environment would be prompted for
    again on the very next command.

    Three cases are deliberately skipped: a rotation has already written its
    replacement, a credential GitLab rejected would serve a dead value to every
    later run while hiding the real failure, and CI is excluded for the reason
    :func:`rotation_blocked_reason` spells out — the value there is a shared
    pipeline variable, which a persistent shell runner would end up keeping in its
    own user cache.
    """
    if cred.rotated or not cred.usable or _in_ci():
        return
    if cred.token != _cached_token():
        _persist(cred.token)


def _journal_snapshot() -> journal.Journal:
    """The recorded instants as they stood when this process started working.

    Snapshotted rather than re-read, so what the user is shown is the *previous*
    pass: this very run's own check and rotation are reported as the events they
    are (``configure``'s ``rotated`` flag), not as a timestamp reading "now".
    """
    cached = _MEMO.get(_JOURNAL_KEY)
    if isinstance(cached, journal.Journal):
        return cached
    snapshot = journal.read()
    _MEMO[_JOURNAL_KEY] = snapshot
    return snapshot


def _introspect(token: str, host: str) -> pat.TokenInfo | None:
    """Ask GitLab about ``token``, journalling the check when it answers.

    The single introspection path, so every command that verifies the credential
    — including a plain ``tools status`` — dates the check the user is shown.
    Only a conclusive answer counts: a rejected or unreachable token leaves the
    last known-good check in place rather than claiming a verification.
    """
    _journal_snapshot()  # Freeze what the previous pass recorded before overwriting it.
    info = pat.token_info(token, host)
    if info is not None:
        journal.record_check()
    return info


def credential() -> Credential | None:
    """The process-wide credential: resolved, introspected, rotated if due.

    Returns ``None`` when no token could be obtained at all. A token that
    resolves but that GitLab rejects is still returned, with ``usable`` False —
    the caller reports it rather than silently doing nothing.

    A memo entry left by :func:`state_of` is reused but **not** trusted to have
    been through rotation: the install pipeline calls ``get_state`` before
    ``do_configure``, so without this distinction the state read would silently
    cancel the rotation for the whole run.
    """
    cached = _MEMO.get(_CREDENTIAL_KEY)
    if isinstance(cached, Credential) and cached.rotation_arbitrated:
        return cached

    if isinstance(cached, Credential):
        result = cached
    else:
        token = resolve_token()
        if not token:
            return None
        resolved_targets = targets()
        result = Credential(token=token, targets=resolved_targets, info=_introspect(token, resolved_targets.host))
        if result.info is None:
            result = _fall_back_to_cache(result)
        _MEMO[_CREDENTIAL_KEY] = result

    result.rotation_arbitrated = True
    if _rotation_due(result) and rotation_blocked_reason() is None:
        _rotate_and_repose(result)
    _persist_resolved(result)

    return result


def _rotation_due(cred: Credential) -> bool:
    return cred.info is not None and cred.info.needs_rotation() and cred.info.can_rotate


def _in_ci() -> bool:
    """True inside a pipeline, where the token is a shared variable we do not own."""
    return bool(os.environ.get("CI"))


def rotation_blocked_reason() -> str | None:
    """Why rotation must not be attempted at all, or ``None`` when it may run.

    CI is the one hard veto, and it belongs here rather than in the callers: in a
    pipeline the token comes from a **shared** GitLab variable that no job can
    write back, so rotating it would revoke the credential for every other job
    and every other project using it. Any command reaching a rotation — including
    a plain ``tools install`` on a runner — is covered by this single check.
    """
    if _in_ci():
        return "running in CI: the token comes from a shared pipeline variable this job cannot write back"
    return None


def _fall_back_to_cache(rejected: Credential) -> Credential:
    """Retry with the cached token when the resolved one is rejected by GitLab.

    Rotation writes the new token to ``os.environ`` and to the cache, but it
    cannot reach the **parent shell**. So a developer who exported the variable
    by hand keeps re-exporting the value our own rotation revoked — and since the
    environment takes precedence over the cache, that dead token would win on
    every subsequent run while the good one sat in the cache unused.

    Only reached when GitLab rejected the token outright, so a working credential
    is never second-guessed.
    """
    fallback = _cached_token()
    if not fallback or fallback == rejected.token:
        return rejected

    info = _introspect(fallback, rejected.targets.host)
    if info is None:
        return rejected

    typer.secho(
        f"  ↻ ${TOKEN_VAR} from the environment was rejected — using the rotated value from the cache instead.",
        fg=typer.colors.YELLOW,
        err=True,
    )
    os.environ[TOKEN_VAR] = fallback
    return Credential(token=fallback, targets=rejected.targets, info=info)


def _rotate_and_repose(current: Credential) -> None:
    """Rotate the token, then re-pose it wherever the old one was already posed.

    Order matters: the ecosystems holding the credential are listed *before*
    rotating, because rotation is what makes the copies they hold stale.

    The replacement is asked for the window the current token was issued with,
    so a renewal never shortens the credential's life (nor lands it back under
    the rotation threshold — see :mod:`pysae_ai_tools.common.registry_auth.pat`).
    """
    holders = [c for c in CONSUMERS if c.state(current.targets).configured]

    expiry = current.info.rotation_expiry() if current.info is not None else None
    rotated = pat.rotate(current.token, current.targets.host, expires_at=expiry)
    if not rotated:
        return

    current.token = rotated
    current.rotated = True
    journal.record_rotation()
    current.info = _introspect(rotated, current.targets.host)
    _persist(rotated)

    reposed: list[str] = []
    for consumer in holders:
        if consumer.apply(rotated, current.targets).ok:
            reposed.append(consumer.name)
    current.reposed = tuple(reposed)
    _announce_rotation(current)


def _announce_rotation(current: Credential) -> None:
    """Tell the user their credential was just replaced.

    Rotation revokes the value their shell may still hold, so it is never a
    silent operation — even when the command that triggered it was doing
    something else entirely. On stderr, like every other progress line.
    """
    expiry = current.info.expires_at if current.info is not None else None
    detail = f", expires {expiry.isoformat()}" if expiry is not None else ""
    where = f" — re-posed in {', '.join(current.reposed)}" if current.reposed else ""
    typer.secho(
        f"  ↻ ${TOKEN_VAR} rotated on {current.targets.host}{detail}{where}",
        fg=typer.colors.YELLOW,
        err=True,
    )


@dataclass(frozen=True)
class Sweep:
    """What a rotation pass verified and did — the report ``rotate-tokens`` renders."""

    host: str
    token_found: bool
    checked: bool
    usable: bool
    rotated: bool
    reposed: tuple[str, ...] = ()
    expires_in_days: int | None = None
    missing_scopes: tuple[str, ...] = ()
    blocked: str | None = None

    @property
    def needs_user_action(self) -> bool:
        """True when only the developer can fix what the pass found.

        A blocked pass is not their problem (CI vetoes rotation by design), and
        neither is an unreachable GitLab — but a missing, rejected or unrenewable
        token is: each needs a token created or re-scoped by hand.
        """
        if self.blocked is not None or self.unreachable:
            return False
        return not self.token_found or not self.usable or not self.can_renew

    @property
    def unreachable(self) -> bool:
        """True when a token is at hand but GitLab said nothing about it.

        Its own category because it is transient — an outage, a timeout, a 500,
        all indistinguishable in ``pat.token_info`` — and calls for a retry, not
        for the developer to go create a token.
        """
        return self.blocked is None and self.token_found and not self.checked

    @property
    def can_renew(self) -> bool:
        """True when the token carries the scope its own renewal requires."""
        return "self_rotate" not in self.missing_scopes

    def to_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "variable": TOKEN_VAR,
            "host": self.host,
            "token_found": self.token_found,
            "checked": self.checked,
            "usable": self.usable,
            "rotated": self.rotated,
        }
        if self.reposed:
            payload["reposed"] = list(self.reposed)
        if self.expires_in_days is not None:
            payload["expires_in_days"] = self.expires_in_days
        if self.missing_scopes:
            payload["missing_scopes"] = list(self.missing_scopes)
        if self.blocked:
            payload["blocked"] = self.blocked
        return payload


def sweep(*, force: bool = False) -> Sweep:
    """Verify the credential and renew it when due. The rotation entry point.

    ``force`` rotates a token that is still far from expiry — for a credential
    believed leaked, or to exercise the path. It overrides the expiry threshold,
    never :func:`rotation_blocked_reason`.

    Always journals the pass, even when there was no token to check: the hourly
    tick throttles on that instant, and a developer without a credential must not
    have it respawned by every command they run.
    """
    blocked = rotation_blocked_reason()
    cred = credential()
    journal.record_sweep()

    if cred is None:
        return Sweep(
            host=targets().host, token_found=False, checked=False, usable=False, rotated=False, blocked=blocked
        )

    if force and not cred.rotated and blocked is None and cred.info is not None and cred.info.can_rotate:
        _rotate_and_repose(cred)

    info = cred.info
    return Sweep(
        host=cred.targets.host,
        token_found=True,
        checked=info is not None,
        usable=cred.usable,
        rotated=cred.rotated,
        reposed=cred.reposed,
        expires_in_days=info.days_left() if info is not None else None,
        missing_scopes=info.missing_scopes if info is not None else (),
        blocked=blocked,
    )


def apply_to(name: str) -> tuple[ApplyResult, Credential | None]:
    """Pose the credential in the ``name`` ecosystem.

    Returns the outcome plus the credential in use, so the caller can report
    both what it wrote and whether a rotation happened along the way.
    """
    consumer = CONSUMERS_BY_NAME[name]
    cred = credential()
    if cred is None:
        return ApplyResult(error=f"{TOKEN_VAR} unavailable — create one at {creation_hint()}"), None
    if not cred.usable:
        return ApplyResult(error=_unusable_reason(cred)), cred
    return consumer.apply(cred.token, cred.targets), cred


def _unusable_reason(cred: Credential) -> str:
    if cred.info is None:
        return f"{TOKEN_VAR} was rejected by {cred.targets.host} (revoked, expired, or missing read_api)"
    return f"{TOKEN_VAR} is revoked or expired on {cred.targets.host} — create a new one at {creation_hint()}"


def state_of(name: str) -> dict[str, object]:
    """Credential state for one ecosystem, as ``tools status --json`` reports it.

    Reads the on-disk configuration and — only when a token is already at hand —
    what GitLab says about it. Never resolves interactively and never surfaces
    the token itself.
    """
    consumer = CONSUMERS_BY_NAME[name]
    resolved_targets = targets()
    payload = consumer.state(resolved_targets).to_dict()
    payload["host"] = resolved_targets.host

    recorded = _journal_snapshot()
    for key, instant in (("checked_at", recorded.checked_at), ("rotated_at", recorded.rotated_at)):
        if instant is not None:
            payload[key] = instant.isoformat()

    cached = _MEMO.get(_CREDENTIAL_KEY)
    cred = cached if isinstance(cached, Credential) else None
    if cred is None:
        token = os.environ.get(TOKEN_VAR) or _cached_token()
        if token:
            cred = Credential(token=token, targets=resolved_targets, info=_introspect(token, resolved_targets.host))
            _MEMO[_CREDENTIAL_KEY] = cred

    if cred is None:
        payload["credential"] = "unknown"
        return payload

    payload["credential"] = "usable" if cred.usable else "unusable"
    if cred.info is not None:
        days = cred.info.days_left()
        if days is not None:
            payload["expires_in_days"] = days
        if cred.info.missing_scopes:
            payload["missing_scopes"] = list(cred.info.missing_scopes)
    return payload


def _cached_token() -> str:
    return cache.read(TOKEN_VAR) or ""


def remove_from(name: str) -> tuple[str, ...]:
    """Strip the credential from one ecosystem. Returns the locations cleaned."""
    return CONSUMERS_BY_NAME[name].remove(targets())


def remove_everywhere() -> dict[str, tuple[str, ...]]:
    """Strip the credential from every ecosystem the CLI posed it in.

    Its lifecycle record goes with it: nothing is left holding the token, so
    dating the checks and rotations of a credential no longer in use would only
    mislead the next status read.
    """
    removed = {consumer.name: consumer.remove(targets()) for consumer in CONSUMERS}
    journal.clear()
    _MEMO.pop(_JOURNAL_KEY, None)
    return removed


# ---------------------------------------------------------------------------
# Install-framework adapters — the same three hooks for each of the three tools
# ---------------------------------------------------------------------------


def configure_report(name: str) -> InstallReport:
    """``do_configure`` body for the ``name`` ecosystem.

    **Never returns an error and never raises.** A developer with no registry
    PAT — or one whose login fails, or whose machine has no ``git`` yet — must
    still end up with a working uv, Node and Docker, so the outcome is reported
    under ``extra['registry']`` and the install carries on. Same rule ArgoCD
    applies to its missing tokens.

    The blanket catch is the point rather than defensive habit: ``uv`` and
    ``node`` are REQUIRED tools, and an exception escaping here fails them
    outright — which is exactly what happened on a bare CI runner where ``git``
    was not yet installed when the target detection ran.
    """
    try:
        result, cred = apply_to(name)
    except Exception as exc:  # noqa: BLE001
        return InstallReport(
            action="configure",
            extra={"registry": {"credential": "skipped", "reason": f"could not resolve the credential: {exc}"}},
        )

    detail: dict[str, object] = {}

    if result.ok:
        detail["credential"] = "posed" if result.changed else "already posed"
        if result.locations:
            detail["locations"] = list(result.locations)
        if cred is not None and cred.rotated:
            detail["rotated"] = True
            detail["reposed"] = list(cred.reposed)
    else:
        detail["credential"] = "skipped"
        detail["reason"] = result.error

    if cred is not None and cred.info is not None and cred.info.missing_scopes:
        detail["missing_scopes"] = list(cred.info.missing_scopes)

    return InstallReport(action="configure", extra={"registry": detail})


def augment_state(name: str, state: ToolState) -> ToolState:
    """Add the ``name`` ecosystem's credential state to a tool's ``get_state``.

    Sets ``needs_reconfigure`` only when a *usable* credential exists that is
    not posed here — that is the case ``tools install --configure-only``
    repairs. With no credential at all the tool stays clean, so a developer who
    never uses the private registries is not nagged forever.

    Never raises, for the same reason as :func:`configure_report`: the
    credential is an add-on to the tool's state, never a reason to lose it.
    """
    try:
        payload = state_of(name)
    except Exception as exc:  # noqa: BLE001
        state.extra["registry"] = {"configured": False, "credential": "unknown", "error": str(exc)}
        return state

    state.extra["registry"] = payload
    if payload.get("credential") == "usable" and not payload.get("configured"):
        state.needs_reconfigure = True
    return state


def uninstall_report(name: str, *, dry_run: bool = False) -> InstallReport:
    """``do_uninstall`` body: drop the credential this ecosystem holds.

    Never raises — an uninstall must not stall on a machine whose ``git`` or
    ``glab`` has already been removed.
    """
    try:
        if dry_run:
            current = CONSUMERS_BY_NAME[name].state(targets())
            return InstallReport(action="uninstall", extra={"removed": list(current.locations)})
        return InstallReport(action="uninstall", extra={"removed": list(remove_from(name))})
    except Exception as exc:  # noqa: BLE001
        return InstallReport(action="uninstall", extra={"removed": [], "error": str(exc)})


def identity_lines(state: dict[str, object]) -> list[tuple[str, str | None]]:
    """Status-display lines for a tool's registry credential."""
    payload = state.get("registry")
    if not isinstance(payload, dict):
        return []

    credential_state = payload.get("credential")
    if payload.get("configured"):
        label, color = "registry: configured", typer.colors.GREEN
    elif credential_state == "usable":
        label, color = "registry: credential available, not posed", typer.colors.YELLOW
    elif credential_state == "unusable":
        label, color = "registry: credential revoked or expired", typer.colors.RED
    else:
        label, color = f"registry: no {TOKEN_VAR}", typer.colors.BRIGHT_BLACK

    lines: list[tuple[str, str | None]] = [(label, color)]
    days = payload.get("expires_in_days")
    if isinstance(days, int):
        lines.append((f"credential expires in {days}d", typer.colors.BRIGHT_BLACK))
    missing = payload.get("missing_scopes")
    if isinstance(missing, list) and missing:
        lines.append((f"credential lacks {', '.join(str(s) for s in missing)}", typer.colors.YELLOW))
    # Only when a credential is actually in play. A developer who never uses the
    # private registries has nothing to date, and `augment_state` already keeps
    # them out of the reconfigure nag for the same reason.
    if credential_state in ("usable", "unusable"):
        lines.append((_lifecycle_line(payload), typer.colors.BRIGHT_BLACK))
    return lines


def render_sweep(result: Sweep) -> None:
    """Human output for ``tools rotate-tokens``: what was verified, what changed."""
    typer.echo("")
    if result.blocked is not None:
        typer.secho(f"  ⊘ rotation skipped — {result.blocked}", fg=typer.colors.BRIGHT_BLACK)
        return
    if not result.token_found:
        typer.secho(
            f"  ✗ no ${TOKEN_VAR} to check — create one at {pat.creation_url(result.host)}", fg=typer.colors.RED
        )
        return
    if not result.checked:
        typer.secho(f"  ⚠ {result.host} did not answer — validity could not be verified", fg=typer.colors.YELLOW)
        return
    if not result.usable:
        typer.secho(
            f"  ✗ ${TOKEN_VAR} is revoked or expired on {result.host} — "
            f"create a new one at {pat.creation_url(result.host)}",
            fg=typer.colors.RED,
        )
        return

    remaining = f"expires in {result.expires_in_days}d" if result.expires_in_days is not None else "never expires"
    typer.secho(f"  ✓ ${TOKEN_VAR} checked on {result.host} — valid, {remaining}", fg=typer.colors.GREEN)
    if result.rotated:
        where = f" — re-posed in {', '.join(result.reposed)}" if result.reposed else ""
        typer.secho(f"  ↻ rotated{where}", fg=typer.colors.CYAN)
    elif not result.can_renew:
        typer.secho("  ⚠ cannot renew itself — the token lacks self_rotate", fg=typer.colors.YELLOW)
    else:
        typer.secho(
            f"  ⊙ no rotation needed — renews within {pat.ROTATION_THRESHOLD_DAYS}d of expiry",
            fg=typer.colors.BRIGHT_BLACK,
        )


def _lifecycle_line(payload: dict[str, object]) -> str:
    """One line dating the last validity check and the last rotation.

    Rotation runs unattended, so this is the only place it becomes visible after
    the fact. A credential never checked yet says so rather than staying silent —
    "no news" and "never verified" are not the same thing.
    """
    checked = _relative(payload.get("checked_at"))
    parts = [f"validity checked {checked}" if checked else "validity never checked"]
    rotated = _relative(payload.get("rotated_at"))
    parts.append(f"last rotated {rotated}" if rotated else "never rotated")
    return " · ".join(parts)


def _relative(raw: object) -> str:
    """Humanise a recorded instant as an age, or "" when it never happened."""
    if not isinstance(raw, str):
        return ""
    try:
        instant = datetime.fromisoformat(raw)
    except ValueError:
        return ""
    seconds = journal.age_seconds(instant if instant.tzinfo is not None else instant.replace(tzinfo=UTC))
    if seconds is None:
        return ""
    if seconds < 90:
        return "just now"
    if seconds < 5400:
        return f"{round(seconds / 60)} min ago"
    if seconds < 172800:
        return f"{round(seconds / 3600)} h ago"
    return f"{round(seconds / 86400)} d ago"
