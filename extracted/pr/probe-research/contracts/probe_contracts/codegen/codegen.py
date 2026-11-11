"""Codegen: render every client view of the records, the event and surface catalogs, the client-message,
transcript-switch, settings, pane API and pin vocabularies, the sample and live-event contracts, then write it or check
it is current.

    python -m probe_contracts.codegen           # write every target
    python -m probe_contracts.codegen --check   # exit 1 naming each stale target
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from ..probe_contracts import CONTRACTS, Contracts
from .client_messages import render_client_messages_stdlib, render_client_messages_typescript
from .events import (
    render_agent_events,
    render_agent_surfaces,
    render_dashboard_events,
    render_dashboard_surfaces,
    render_server_events,
    render_server_surfaces,
)
from .live import DESTINATION as LIVE_DESTINATION
from .live import list_live_files, make_live_copy_render
from .pane_api import render_pane_api_python, render_pane_api_typescript
from .pins import render_pins_agent, render_pins_server, render_pins_typescript
from .python import render_python
from .samples import DESTINATION as SAMPLES_DESTINATION
from .samples import list_sample_files, make_sample_copy_render, render_record_copy
from .settings import (
    GOLDEN_NAMES,
    make_copy_render,
    render_settings_stdlib,
    render_settings_typescript,
)
from .transcript_switch import render_transcript_switch_stdlib
from .typescript import render_typescript

#: The research-os checkout this file sits in (contracts/probe_contracts/codegen/).
REPO_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Target:
    """One generated file: where it lives (repo-relative) and how it is drawn."""

    path: str
    render: Callable[[Contracts], str]


TARGETS = (
    Target("agent/src/probe/generated/records.py", render_python),
    Target("packages/core/src/generated/records.ts", render_typescript),
    Target("app/external/analytics/generated/events.py", render_server_events),
    Target("agent/src/probe/analytics/generated/events.py", render_agent_events),
    Target("packages/analytics/src/generated/events.ts", render_dashboard_events),
    Target("app/external/analytics/generated/surfaces.py", render_server_surfaces),
    Target("agent/src/probe/analytics/generated/surfaces.py", render_agent_surfaces),
    Target("packages/analytics/src/generated/surfaces.ts", render_dashboard_surfaces),
    Target("agent/src/probe/generated/client_messages.py", render_client_messages_stdlib),
    # The tap's own copy, beside its copy of `probe.foundation.server_messages` (it cannot import
    # probe). The hooks (Python 3.9) cannot load it: they mirror the two words they need.
    Target("agent/plugins/probe-tap/tap/server_messages/client_messages.py",
           render_client_messages_stdlib),
    Target("packages/core/src/generated/client-messages.ts", render_client_messages_typescript),
    Target("agent/src/probe/generated/transcript_switch.py", render_transcript_switch_stdlib),
    Target("agent/src/probe/generated/settings_vocabulary.py", render_settings_stdlib),
    Target("packages/core/src/generated/settings.ts", render_settings_typescript),
    # The Mac app's Rust writer reads these through the vendored @probe/core (plan app-never-waits S11).
    Target("packages/core/src/settings/settings.schema.json", make_copy_render("settings.schema.json")),
    *(Target(f"packages/core/src/settings/golden/{name}", make_copy_render(f"golden/{name}")) for name in GOLDEN_NAMES),
    # What a pane's code may call (pane_api/): the server's lint and data caps, the dashboard's frame.
    Target("app/projects/panes/generated/pane_api.py", render_pane_api_python),
    Target("dashboard/src/shared/generated/pane-api.generated.ts", render_pane_api_typescript),
    # What a project's Pinned area can hold (pins/): the server's routes, the CLI's and the dashboard's views.
    Target("app/projects/pins/generated/pins.py", render_pins_server),
    Target("agent/src/probe/generated/pins.py", render_pins_agent),
    Target("dashboard/src/shared/generated/pins.generated.ts", render_pins_typescript),
    # The sample store's contract for the SDK (rl-data PR5): the same files, no TypeScript until the dashboard PR.
    *(Target(f"{SAMPLES_DESTINATION}/{name}", make_sample_copy_render(name)) for name in list_sample_files()),
    Target(f"{SAMPLES_DESTINATION}/record.py", render_record_copy),
    # The live events contract for the SDK and CLI (rl-next W52): the same files, no TypeScript until the dashboard.
    *(Target(f"{LIVE_DESTINATION}/{name}", make_live_copy_render(name)) for name in list_live_files()),
)


class Codegen:
    """Draws every target from one Contracts registry into one checkout."""

    def __init__(self, root: Path = REPO_ROOT, contracts: Contracts = CONTRACTS,
                 targets: tuple[Target, ...] = TARGETS) -> None:
        if not (root / "contracts" / "probe_contracts").is_dir():
            raise SystemExit(f"codegen: {root} is not a research-os checkout (pass --root)")
        self.root = root
        self.contracts = contracts
        self.targets = targets

    def find_stale(self) -> list[str]:
        """Targets whose file is missing or differs from a fresh render."""
        stale = []
        for target in self.targets:
            path = self.root / target.path
            if not path.is_file() or path.read_text(encoding="utf-8") != target.render(self.contracts):
                stale.append(target.path)
        return stale

    def write(self) -> list[str]:
        """Write every stale target; returns the paths written."""
        written = self.find_stale()
        for target in self.targets:
            if target.path in written:
                path = self.root / target.path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(target.render(self.contracts), encoding="utf-8")
        return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m probe_contracts.codegen", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="fail when a generated file is stale")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="the research-os checkout")
    args = parser.parse_args(argv)
    codegen = Codegen(args.root.resolve())
    if args.check:
        stale = codegen.find_stale()
        for path in stale:
            print(f"stale: {path} (run `python -m probe_contracts.codegen`)")
        return 1 if stale else 0
    for path in codegen.write():
        print(f"wrote {path}")
    return 0
