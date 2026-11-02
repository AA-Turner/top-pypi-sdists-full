"""parse `--agent` into installable harness ids (repeatable, `both`/`all` aliases, registry cli flags) for the wizard and the install commands."""

from __future__ import annotations

import typer


def _installable_agent(name: str):
    """The installable registry row `--agent NAME` names: its cli_flag, id or alias."""
    from probe.foundation.harness_registry import get_registry

    wanted = name.strip().lower()
    return next(
        (h for h in get_registry().installable() if wanted == h.cli_flag or wanted in h.names), None
    )


def _agent_flags() -> str:
    from probe.foundation.harness_registry import get_registry

    return ", ".join(h.cli_flag for h in get_registry().installable() if h.cli_flag)


#: The single-agent `--agent` values, from the registry ("claude, codex, ...").
_AGENT_FLAGS = _agent_flags()

#: `--agent`'s help, on `install` and `wizard` alike.
_AGENT_HELP = (
    f"configure {_AGENT_FLAGS}, or both (both = claude+codex); repeat for several "
    "(--agent claude --agent pi), all in one browser approval (default: choose interactively)"
)

#: The `--agent` values that name Claude Code AND Codex. pi and every other agent
#: are reachable only by name (see `_explicit_agent_sources`).
_BOTH_AGENTS = frozenset({"both", "all", "claude,codex", "codex,claude"})


def _agent_values(agent) -> list[str]:
    """`--agent` as the list of values given: repeatable now, a single string
    from a direct Python caller, nothing at all when it was not passed."""
    if isinstance(agent, str):
        return [agent]
    if isinstance(agent, (list, tuple)):
        return [value for value in agent if isinstance(value, str)]
    return []


def _explicit_agent_sources(agent) -> tuple[str, ...] | None:
    """The agents `--agent` names, in order and once each; None when it names none.

    "both"/"all" keep their EXISTING meaning -- claude_code + codex, the two
    coding agents this wizard can install a marketplace plugin for (see
    setup.INSTALLABLE_AGENT_SOURCES). pi is deliberately NOT swept into either
    alias: it has no plugin for this run to install, only a capture credential
    to pair (see the pi-only selection scoping in `_wizard_session`), so
    silently including it in "both" would promise install work for a run that
    does something categorically different. pi is reachable only by naming it.

    Every other value names ONE agent: its registry `cli_flag`, id or alias
    (`claude`, `kimi`, ...), so a new installable row is reachable here
    the moment it lands -- and, like pi, only by name. Repeating the flag adds
    agents (`--agent claude --agent pi`): one run, one browser approval.
    """
    sources: list[str] = []
    for value in _agent_values(agent):
        normalized = value.strip().lower()
        if normalized in _BOTH_AGENTS:
            sources.extend(("claude_code", "codex"))
            continue
        named = _installable_agent(normalized)
        if named is None:
            raise typer.BadParameter(f"--agent must be {_AGENT_FLAGS}, or both")
        sources.append(named.id)
    return tuple(dict.fromkeys(sources)) or None
