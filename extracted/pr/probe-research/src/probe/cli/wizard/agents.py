"""the coding agents a wizard run can act on: installable and detected harnesses, their labels, logos and instruction files."""

from __future__ import annotations
from collections.abc import Sequence
from pathlib import Path
from probe.shared.harness.harnesses import pi as pi_config
from probe.shared.harness import plugins as plugin_cli

#: Display name per capture source. The COMPLETE set this wizard knows about
#: for naming purposes (messages, confirmations, per-source copy) -- NOT the
#: set step 1 offers to auto-detect, which is `detectable_sources()` below
#: (a live PATH/marketplace check, not a fixed tuple), and NOT the set
#: `install_plugin`/`uninstall_plugin` know how to install something for,
#: which is `INSTALLABLE_AGENT_SOURCES`. Conflating
#: the display-name set with either is exactly how the confirm-screen label
#: at the bottom of `authorize()` used to name every non-codex capture source
#: "Claude Code": a two-way ternary is silently correct only while there are
#: exactly two sources, and pi's addition is what made that stop being true.
#: Look a source up here (via `agent_label`) instead of adding another branch.
def _installable_rows():
    from probe.foundation.harness_registry import get_registry

    return get_registry().installable()


AGENT_LABELS = {h.id: h.label for h in _installable_rows()}


def agent_logo(source: str) -> bytes | None:
    """The agent's logo as the PNG a terminal draws in the device summary
    (Richard 2026-10-06: "actually get the correct icons", in "this circular
    colored background style"): its brand mark in white on a circle of its
    brand colour, rendered by `agent/tools/render_harness_icons.py` into
    `probe/cli/icons/<registry icon stem>.png`."""
    from probe.foundation.harness_registry import get_registry

    harness = get_registry().find(source)
    if harness is None or not harness.icon:
        return None
    path = Path(__file__).parents[1] / "icons" / f"{Path(harness.icon).stem}.png"
    return path.read_bytes() if path.is_file() else None

#: The sources that install through a plugin MARKETPLACE (`plugin_cli.py`'s
#: `install`/`marketplace update`/`marketplace add`) rather than pi's
#: settings.json `packages` entry. NOT "the sources step 1 offers" any more --
#: that used to be true, on the theory that "pi has no CLI for it to find". It
#: was never actually true: pi IS a binary on PATH (`shutil.which("pi")`
#: resolves it exactly like `claude`/`codex`) -- what pi lacks is a
#: *marketplace*, and that is what this constant actually gates now: the
#: refresh step (`refresh_marketplace`) and the degraded-screen filter
#: (`main.py`'s `plugin_promising_sources`), both of which only mean something
#: for a source with a marketplace behind it. The step-1 picker's row set
#: comes from `detectable_sources()` below, which DOES include pi when its
#: binary is found -- see that function's docstring for the history this one
#: used to carry.
MARKETPLACE_AGENT_SOURCES: tuple[str, ...] = tuple(h.id for h in _installable_rows() if h.family == "hook-plugin")

#: Every source `install_plugin`/`uninstall_plugin`/`apply_capture` know how
#: to install or remove something for -- but not through one shared
#: mechanism. claude_code and codex go through their own marketplace
#: commands (`plugin_cli.py`, `claude_cli.py`, `codex_config.py`); pi has no
#: marketplace at all, so it goes through `pi_config`'s settings.json
#: `packages` array entry instead -- ONE entry that installs pi's extension,
#: skills, and MCP manifest together (see
#: `agent/plugins/probe-research-pi/README.md`, "Route A"). This replaces
#: the old manual `~/.pi/agent/extensions/` symlink install (now retired via
#: `migrate_legacy_symlink` on the packages-entry install). The entry is a
#: local checkout path for a plugin developer and the PUBLIC MIRROR git source
#: (`git:github.com/prbe-ai/research-os-agent`) for everyone else -- see
#: `pi_config.resolve_install_source`. Not npm: the mirror repo is the channel
#: Claude and Codex already install from, and its root `package.json` carries
#: a `pi` manifest, so one mirror push releases all three clients.
#: Because pi's install is one package covering every capability, not one
#: plugin per capability, `install_plugin`'s `name` argument is ignored on
#: pi's branch: `apply_tracking`'s and `apply_capture`'s calls both land on
#: the same idempotent write. Pairing a pi device's capture credential (see
#: `authorize`) does not depend on this tuple; it is keyed off
#: `capture_sources`/`captures`, not this list. NOT the set step 1's picker
#: offers -- see `MARKETPLACE_AGENT_SOURCES` above for that narrower one.
INSTALLABLE_AGENT_SOURCES: tuple[str, ...] = tuple(h.id for h in _installable_rows())


#: The pi `--help` "coding" sniff, MOVED to `pi_config` and re-exported here
#: under its original name so every caller and test that says
#: `setup.pi_binary_available` -- including the autouse fixture that pins pi
#: detection off for the whole suite -- keeps working. It moved because
#: `backfill.which_agent` needs the same sniff to tell a real pi from a
#: two-letter impostor, and backfill cannot import this module (this one
#: reaches into backfill). `pi_config` imports neither, so it is where a
#: function both need can live. Read that docstring for the impostor-guard
#: rationale.
pi_binary_available = pi_config.pi_binary_available


def detectable_sources(*, sniff: bool = True) -> tuple[str, ...]:
    """Every `INSTALLABLE_AGENT_SOURCES` member actually found on this
    machine, right now -- claude_code/codex via `plugin_cli.available`
    (their marketplace CLI), pi via `pi_binary_available` (its own binary,
    never through `plugin_cli`, which raises for it).

    This is the corrected version of the claim `MARKETPLACE_AGENT_SOURCES`
    used to encode: "pi has no CLI for a picker to find". It does -- pi ships
    a real binary, `shutil.which("pi")` resolves it exactly the way it
    resolves `claude`/`codex` -- what pi lacks is a *marketplace*, which is
    a different question with a different answer, and conflating the two is
    the bug this function exists to not repeat. `run_agent_menu` (step 1) and
    `main.py`'s `available_sources` both call this, so a pi binary shows up
    in exactly one place instead of two independently-maintained checks
    drifting apart.

    `sniff=False` (`probe status` without --refresh, which runs no
    subprocess) takes a pi binary on PATH at its word instead of asking its
    `--help`: the one difference, and the impostor guard it gives up.
    """
    detected = [source for source in MARKETPLACE_AGENT_SOURCES if plugin_cli.available(source)]
    if pi_binary_available() if sniff else pi_config.pi_on_path():
        detected.append("pi")
    return tuple(detected)


def short_path(path: Path) -> str:
    """`~/.codex/AGENTS.md`, not the full home-prefixed path.

    A summary bullet is read at a glance, and `/Users/<name>/` at the front of
    every path is the part with no information in it."""
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)


def agent_label(sources: tuple[str, ...] | list[str] | str) -> str:
    """User-facing name for the exact agents selected in this wizard run."""
    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    labels = [AGENT_LABELS[source] for source in AGENT_LABELS if source in normalized]
    if not labels:
        return "coding agent"
    if len(labels) == 1:
        return labels[0]
    return f"{', '.join(labels[:-1])} and {labels[-1]}"


def instruction_files(sources: tuple[str, ...] | list[str] | str) -> str:
    """Name the real global instruction files for the selected agents."""
    from probe.foundation.harness_registry import get_registry

    normalized = (sources,) if isinstance(sources, str) else tuple(sources)
    names: list[str] = []
    for source in normalized:
        harness = get_registry().find(source)
        name = (harness.instructions or {}).get("global") if harness else None
        if name and name not in names:
            names.append(name)
    return " + ".join(names) or "agent instructions"


def spoken_list(items: Sequence[str]) -> str:
    """`a`, `a and b`, `a, b and c`."""
    items = list(items)
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} and {items[-1]}"


def agents_counted(sources: Sequence[str], done: Sequence[str]) -> str:
    """"Claude Code", "all 4 coding agents", "3 of 4 coding agents"."""
    if len(sources) == 1:
        return agent_label(sources[0])
    if len(done) == len(sources):
        return "both coding agents" if len(sources) == 2 else f"all {len(sources)} coding agents"
    return f"{len(done)} of {len(sources)} coding agents"
