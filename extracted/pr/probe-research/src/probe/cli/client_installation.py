"""Publish the setup wizard's allowlisted local capability snapshot.

This is an explicit registration after setup changes, not recurring telemetry.
Normal API and MCP requests continue to send only their bearer token; the
backend resolves that credential to the durable installation row.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from contextlib import contextmanager

from probe._compat import StrEnum
from probe.cli.capabilities import Capabilities
from probe.sdk import errors
from probe.sdk.client import Client
from probe.sdk.config import Settings, resolve
from probe.sdk.device import hostname
from probe.sdk.surface import Surface


class Installed(StrEnum):
    """The wire's tri-state for `tracking` and `capture` (the server's
    `InstalledState`)."""

    INSTALLED = "installed"
    ABSENT = "absent"
    UNKNOWN = "unknown"


#: One agent's pass: its state, and whether its run FINISHED (`complete`).
Pass = tuple[Capabilities, bool]


def snapshot(
    caps: Capabilities,
    *,
    complete: bool = True,
    alongside: Sequence[Pass] = (),
) -> dict[str, str]:
    """Return schema v2 using installed state, not runtime health.

    v2 changes two things. `tracking` replaces the v1 `mcp`/`skills` pair, which
    were always one fact: both were set from `caps.tracking_plugin_installed`
    and could never disagree. And `capture` is reported at all for the first
    time -- the wizard's most consent-relevant setting used to be invisible to
    the server, so nobody could tell whether a machine turned session capture on
    at install, off later, or back on.

    `capture` reads `caps.capture_on`, not `capture_plugin_installed`: an
    installed plugin that is killswitched or has no credential ships nothing,
    and reporting that as `installed` would overstate what is running.

    `complete=False` reports the CHOSEN capabilities as `unknown` rather than
    the state the wizard happened to observe. It is the difference between "this
    device ended up without the tracking plugin, on purpose" and "the install
    did not finish, so what is on this device is not a decision anyone made" --
    and the two were previously indistinguishable, because both report
    `absent`. The dashboard waits on this registration to decide an install
    finished, so an unfinished run reporting `absent` told onboarding to move
    on and the approval page to say Installed. The backend now keys its
    install-finished event on the same distinction (control/029).

    Deliberately reuses the EXISTING `unknown` member of the wire enum rather
    than adding an outcome field: `unknown` already round-trips through the
    nullable column (`_installed_db`/`_installed_wire`), so this needs no
    outcome column and no lockstep release. The cost is that an older CLI keeps
    reporting `absent` on a failed install, so the dashboard only stops
    believing it once the CLI updates.

    `alongside` is the rest of the run: the other coding agents' passes,
    oldest first. The server keeps one row per installation -- a machine, not
    an agent -- so `tracking` and `capture` read `installed` when ANY finished
    pass has them, `unknown` when none does and some pass did not finish (an
    unfinished run cannot report a removal), and `absent` only when every pass
    finished without them. Registered agent by agent, a machine with capture in
    one agent and not another reported `absent` then `installed` seconds apart
    on every auto-update, and each `absent` posted a false "Probe removed from
    a machine" (one customer, 2026-10-02 to 10-13: 3 of 3 such pings). Only
    each agent's LATEST pass counts. `auto_update` is a device setting, so it
    is read from `caps`, the newest pass.

    The merge covers the agents IN THIS RUN, not every agent on the machine: a
    run that names one agent still reports that agent alone.
    """
    latest = _latest_per_agent((*alongside, (caps, complete)))
    finished = [state for state, done in latest if done]
    unfinished = any(not done for _state, done in latest)

    def reported(has) -> Installed:
        if any(has(state) for state in finished):
            return Installed.INSTALLED
        return Installed.UNKNOWN if unfinished else Installed.ABSENT

    return {
        "schema_version": 2,
        "auto_update": "on" if caps.auto_update_enabled else "off",
        "tracking": reported(lambda state: state.tracking_plugin_installed),
        "capture": reported(lambda state: state.capture_on),
    }


def _latest_per_agent(passes: Sequence[Pass]) -> list[Pass]:
    """One pass per coding agent, the later winning: an agent whose capture was
    just turned off must not stay `installed` on the strength of its own
    earlier pass."""
    latest: dict[str | None, Pass] = {}
    for state, done in passes:
        latest[state.agent_source] = (state, done)
    return list(latest.values())


#: What `merged_registration` is holding -- (passes, settings) per
#: registration -- or None outside one.
_held: list[tuple[tuple[Pass, ...], Settings | None]] | None = None


@contextmanager
def merged_registration() -> Iterator[list[str]]:
    """Hold every registration made inside, and send ONE for the machine on exit.

    For a wizard action that runs once per coding agent (Update, Settings): each
    pass registered its own agent's state against the machine's one row, so the
    row flipped between agents within seconds (see `snapshot`). Yields the list
    the send's warnings land in, filled when the block exits.

    Sends only on a normal exit: a run that raised leaves the row as it was,
    which can never read as a removal. A pass that was CAUGHT failing (Settings
    contains each agent's) is still held, as unfinished. Nested blocks belong
    to the outermost.
    """
    global _held
    warnings: list[str] = []
    if _held is not None:
        yield warnings
        return
    _held = []
    try:
        yield warnings
    except BaseException:
        _held = None
        raise
    held, _held = _held, None
    if not held:
        return
    *earlier, (latest, done) = [one for passes, _settings in held for one in passes]
    warnings.extend(register(latest, settings=held[-1][1], complete=done, alongside=earlier))


def register(
    caps: Capabilities,
    *,
    settings: Settings | None = None,
    complete: bool = True,
    alongside: Sequence[Pass] = (),
) -> list[str]:
    """Register actual post-action state and adopt a legacy MCP PAT if present.

    Also names the installation after this machine. A legacy installation takes
    its name from whatever PAT it adopted, so a credential minted in the browser
    ends up labelling a laptop -- the CLI is the only party that knows the real
    hostname, and it has always had it without ever sending it.

    `complete=False` marks the run as unfinished (see `snapshot`). The
    registration still HAPPENS on that path -- it is what adopts a legacy MCP
    PAT, and skipping it would strand that credential on a run that got far
    enough to mint one.

    `alongside`: the machine's other agents, merged into the snapshot (see
    `snapshot`). Inside `merged_registration` nothing is sent here; the block
    sends one registration when it ends.

    Returns human-facing warnings. A 404 is ignored throughout so a newly
    released wizard stays compatible with an older or self-hosted backend during
    rollout.
    """
    if _held is not None:
        _held.append(((*alongside, (caps, complete)), settings))
        return []
    settings = settings or resolve()
    if not settings.token:
        return []

    warnings: list[str] = []
    state = snapshot(caps, complete=complete, alongside=alongside)
    try:
        with Client(
            base_url=settings.base_url,
            token=settings.token,
            fail_open=False,
            async_writes=False,
            surface=Surface.CLI.value,
        ) as client:
            registration = client.register_client_capabilities(**state)
            # Naming rides the SAME connection but its own try: it is
            # best-effort, and a machine that cannot be named is still a machine
            # that installed successfully. It is deliberately NOT a field on the
            # capabilities payload -- that model is `extra="forbid"` with a
            # pinned schema_version, so an extra key there would 422 the whole
            # write against an older backend instead of being ignored.
            try:
                client.name_client_installation(hostname=hostname())
            except errors.NotFoundError:
                pass
            except errors.RosError as exc:
                warnings.append(f"! could not record this machine's name: {exc}")
    except errors.NotFoundError:
        return warnings
    except errors.RosError as exc:
        return [f"! could not register this installation with the server: {exc}"]

    installation_id = registration.get("installation_id")
    if not settings.mcp_token or not installation_id:
        return warnings

    try:
        with Client(
            base_url=settings.base_url,
            token=settings.token,
            fail_open=False,
            async_writes=False,
            surface=Surface.CLI.value,
        ) as client:
            attachment = client.create_credential_attachment_grant(
                str(installation_id)
            )
    except errors.NotFoundError:
        return warnings
    except errors.RosError as exc:
        return [*warnings, f"! could not authorize the MCP credential association: {exc}"]
    grant = attachment.get("grant")
    if not isinstance(grant, str) or not grant:
        return [*warnings, "! the server returned an invalid MCP credential attachment grant"]

    try:
        with Client(
            base_url=settings.base_url,
            token=settings.mcp_token,
            fail_open=False,
            async_writes=False,
            surface=Surface.CLI.value,
        ) as client:
            client.attach_current_credential(str(installation_id), grant=grant)
    except errors.NotFoundError:
        return warnings
    except errors.RosError as exc:
        return [
            *warnings,
            f"! could not associate the MCP credential with this installation: {exc}",
        ]
    return warnings
