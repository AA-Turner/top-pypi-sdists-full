"""integrations: kill switches in every tap state folder, then each agent's integration removed."""

from __future__ import annotations

import contextlib


def _set_killswitches(lines: list[str]) -> None:
    """`.disabled` in every tap state folder that EXISTS (never made here): a
    session starting meanwhile does not start an uploader of its own."""
    from probe.cli.install.uninstall import agent_traces as uninstall_agents

    for folder in uninstall_agents.tap_dirs():
        if folder.is_dir() and not folder.is_symlink():
            with contextlib.suppress(OSError):
                (folder / ".disabled").write_text("disabled by probe uninstall\n", encoding="utf-8")


# -- integrations (U-T7) -----------------------------------------------------------------------


def _phase_integrations(run: Run) -> list[str]:
    from probe.cli.install.uninstall import agent_traces as uninstall_agents
    from probe.core import events
    from probe.foundation.harness_registry import get_registry

    lines = run.out
    _set_killswitches(lines)  # past the point of no return: no session starts an uploader of its own
    registry = get_registry()
    agents = [edit.get("agent") for edit in run.plan.get("agent_edits", [])]
    agents += [a for a in uninstall_agents.all_traces() if a not in agents]
    failed = 0
    for agent in agents:
        harness = registry.find(agent)
        if harness is None:
            continue
        removed = uninstall_agents.remove(harness)
        left = {k: v for k, v in uninstall_agents.traces(harness).items() if k != "capture"}
        failed += bool(left)
        lines.append(f"{harness.label}:")
        lines.extend(f"  {line}" for line in removed)
        plugins = set(left.get("plugins", []))
        from probe.cli.wizard.state.state import TAP_PLUGIN_NAME

        if run.options.embedded:
            continue
        events.agent_result(
            agent,
            requested={"tracking": False, "capture": False, "agent_rules": False},
            actual={
                "tracking": any(TAP_PLUGIN_NAME not in p for p in plugins) or bool(left.get("skills")),
                "capture": any(TAP_PLUGIN_NAME in p for p in plugins),
                "agent_rules": bool(left.get("rules")),
            },
            ok=not left,
            message="\n".join(line for line in removed if line.startswith("!")),
        )
    lines.extend(uninstall_agents.remove_hollow())  # what Probe's install left that now holds nothing
    _step(events.Step.UNINSTALL_INTEGRATIONS, events.Status.FAILED if failed else events.Status.DONE,
          f"{len(agents)} coding agent(s)" + (f", {failed} with something left" if failed else ""))
    if failed:
        raise Stop(EXIT_PARTIAL, (
            f"probe uninstall: Probe is still in {failed} coding agent(s) (the lines above say what and where). "
            "Fix that, then run `probe uninstall` again to finish."))
    return lines
from probe.cli.install.uninstall.state import Run, Stop, _step  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.install.uninstall.uninstall import EXIT_PARTIAL, run  # noqa: E402 -- pieces need each other; the front door loads this one first
