"""Codegen: render every client view of the records, the event catalog, the client-message and
transcript-switch and settings vocabularies, then write it or check it is current.

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
from .events import render_agent_events, render_dashboard_events, render_server_events
from .python import render_python
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
    Target("agent/src/probe/generated/client_messages.py", render_client_messages_stdlib),
    # The tap's own copy, beside its copy of `probe.foundation.server_messages` (it cannot import
    # probe). The hooks (Python 3.9) cannot load it: they mirror the two words they need.
    Target("agent/plugins/probe-research-tap/tap/server_messages/client_messages.py",
           render_client_messages_stdlib),
    Target("packages/core/src/generated/client-messages.ts", render_client_messages_typescript),
    Target("agent/src/probe/generated/transcript_switch.py", render_transcript_switch_stdlib),
    Target("agent/src/probe/generated/settings_vocabulary.py", render_settings_stdlib),
    Target("packages/core/src/generated/settings.ts", render_settings_typescript),
    # The Mac app's Rust writer reads these through the vendored @probe/core (plan app-never-waits S11).
    Target("packages/core/src/settings/settings.schema.json", make_copy_render("settings.schema.json")),
    *(Target(f"packages/core/src/settings/golden/{name}", make_copy_render(f"golden/{name}")) for name in GOLDEN_NAMES),
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
