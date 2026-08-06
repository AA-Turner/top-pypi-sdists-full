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

import typer

from ..common.registry_auth import docker as docker_writer
from ..common.registry_auth import npm as npm_writer
from ..common.registry_auth import pat
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
        result = Credential(token=token, targets=resolved_targets, info=pat.token_info(token, resolved_targets.host))
        if result.info is None:
            result = _fall_back_to_cache(result)
        _MEMO[_CREDENTIAL_KEY] = result

    result.rotation_arbitrated = True
    if result.info is not None and result.info.needs_rotation() and result.info.can_rotate:
        _rotate_and_repose(result)

    return result


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

    info = pat.token_info(fallback, rejected.targets.host)
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
    """
    holders = [c for c in CONSUMERS if c.state(current.targets).configured]

    rotated = pat.rotate(current.token, current.targets.host)
    if not rotated:
        return

    current.token = rotated
    current.rotated = True
    current.info = pat.token_info(rotated, current.targets.host)
    _persist(rotated)

    reposed: list[str] = []
    for consumer in holders:
        if consumer.apply(rotated, current.targets).ok:
            reposed.append(consumer.name)
    current.reposed = tuple(reposed)


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

    cached = _MEMO.get(_CREDENTIAL_KEY)
    cred = cached if isinstance(cached, Credential) else None
    if cred is None:
        token = os.environ.get(TOKEN_VAR) or _cached_token()
        if token:
            cred = Credential(token=token, targets=resolved_targets, info=pat.token_info(token, resolved_targets.host))
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
    """Strip the credential from every ecosystem the CLI posed it in."""
    return {consumer.name: consumer.remove(targets()) for consumer in CONSUMERS}


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
    return lines
