"""The wizard menu's "am I current?" rows.

WHY THE MENU NEEDS ITS OWN. The comparison already existed and `probe doctor`
already printed it -- but doctor is a command you have to already suspect
something to run, and the one screen every user does see said what was switched
ON and nothing about whether the thing switched on was the version we publish. A
machine three releases behind looked identical to a current one.

These rows are a SECOND RENDERING of `probe.cli.versions`, never a second
grading, so the two surfaces can differ in wording and never in verdict.

THE PROPERTIES THAT MATTER, and that this file pins:

  * an unreadable or absent manifest never renders as good news -- the invariant
    versions.py exists around, and the one a compact summary is most tempted to
    drop, because "no problems found" and "nothing was checked" both want the
    same short line;
  * one unreadable component does NOT outrank three graded ones (a Codex-only box
    has no Claude plugin ledger, and would otherwise read as unchecked forever);
  * a verdict graded against a stale manifest says so, and stops being green;
  * every row fits the frame. The block is aligned on a 28-column label, and a
    value that wraps renders as a phantom row with a blank label;
  * a Claude Code tap is graded by the ledger entry `probe update` reads once
    that is ahead of the stamp, so the menu never says "Update needed" under
    Update's "already at the latest". Another agent's tap keeps its own stamp.
"""

from __future__ import annotations

import json

import pytest

from probe.cli import capabilities, setup, updater
from probe.cli.capabilities import Capabilities
from probe.cli.versions import Comparison, VersionStatus, compare, overall

MANIFEST = {
    "cli": {"latest": "0.162.0", "min": "0.127.0"},
    "plugin": {"latest": "0.81.0", "min": "0.63.0"},
    "tap": {"latest": "0.6.1", "min": "0.6.0"},
}


def _local(cli="0.162.0", plugin="0.81.0", tap="0.6.1"):
    return {"cli": cli, "sdk": cli, "plugin": plugin, "tap": tap}


def _caps(local=None, *, manifest=MANIFEST, age=60.0) -> Capabilities:
    rows = tuple(compare(manifest, local or _local())) if manifest else ()
    return Capabilities(version_rows=rows, version_manifest_age_s=age)


def _rendered(caps: Capabilities) -> str:
    return "\n".join(setup.describe_versions(caps))


# -- the verdict --------------------------------------------------------------


def test_a_current_machine_is_told_so_with_the_numbers() -> None:
    """Good news is stated, not implied by silence. Printing only problems is
    what made a clean machine and an unchecked one look the same."""
    rendered = _rendered(_caps())
    assert "Up to date" in rendered
    assert "CLI 0.162.0" in rendered
    assert "plugin 0.81.0" in rendered


def test_a_current_machine_reads_green() -> None:
    line = setup.describe_versions(_caps())[0]
    assert getattr(line, "style", "") == "class:selected"


def test_a_behind_component_names_the_move() -> None:
    rendered = _rendered(_caps(_local(plugin="0.80.0")))
    assert "Update available" in rendered
    assert "plugin 0.80.0 → 0.81.0" in rendered


def test_two_behind_keep_both_sets_of_numbers() -> None:
    """The pair that fits exactly. It did not, while the row charged for an
    ellipsis it was not using, and the second component vanished."""
    rendered = _rendered(_caps(_local(cli="0.161.0", plugin="0.80.0")))
    assert "CLI 0.161.0 → 0.162.0" in rendered
    assert "plugin 0.80.0 → 0.81.0" in rendered


def test_more_moves_than_fit_name_every_component_rather_than_some_numbers() -> None:
    """Degrading to names keeps the answer COMPLETE. A truncated list of moves
    reads as "the CLI is behind" while silently dropping the two that also are."""
    rendered = _rendered(_caps(_local(cli="0.161.0", plugin="0.80.0", tap="0.6.0")))
    assert "CLI, plugin and tap behind" in rendered
    assert "…" not in rendered


def test_below_the_minimum_outranks_a_routine_update() -> None:
    rendered = _rendered(_caps(_local(cli="0.120.0", plugin="0.80.0")))
    assert "Update required" in rendered
    assert "Update available" not in rendered


def test_below_recommended_speaks_in_the_middle_voice() -> None:
    manifest = {**MANIFEST, "tap": {"latest": "0.6.1", "min": "0.6.0", "recommended": "0.6.1"}}
    rendered = _rendered(_caps(_local(tap="0.6.0"), manifest=manifest))
    assert "Update needed" in rendered
    assert "misbehave" in rendered


def test_the_wizard_verdict_matches_the_doctor_grading() -> None:
    """One comparison, two renderings. A menu saying "up to date" over a doctor
    saying "update required" reads as the warning being wrong."""
    caps = _caps(_local(cli="0.120.0"))
    assert overall(caps.version_rows) is VersionStatus.REQUIRED
    assert "Update required" in _rendered(caps)


# -- what it must never claim -------------------------------------------------


def test_no_cached_manifest_is_not_up_to_date() -> None:
    rendered = _rendered(_caps(manifest=None, age=None))
    assert "Up to date" not in rendered
    assert "Not checked" in rendered
    assert "cached" in rendered


def test_unreadable_local_versions_are_not_up_to_date() -> None:
    rendered = _rendered(_caps(_local(cli=None, plugin=None, tap=None)))
    assert "Up to date" not in rendered
    assert "could not be read" in rendered


def test_one_unreadable_component_does_not_outrank_the_graded_ones() -> None:
    """A Codex-only box has no Claude plugin ledger and no tap state file. It is
    not an unchecked machine; it is a machine with a checked CLI."""
    rendered = _rendered(_caps(_local(plugin=None, tap=None)))
    assert "Up to date" in rendered
    assert "CLI 0.162.0" in rendered


def test_a_stale_manifest_qualifies_the_good_news_and_drops_the_green() -> None:
    """Three days is well past both the 15m refresh and the 1h failure backoff,
    so "up to date" is a claim about a list that may predate several releases."""
    line = setup.describe_versions(_caps(age=3 * 86400))[0]
    assert "checked 3d ago" in line
    assert getattr(line, "style", "") != "class:selected"


def test_a_fresh_manifest_does_not_carry_the_qualifier() -> None:
    assert "checked" not in setup.describe_versions(_caps(age=300))[0]


# -- which tap number it grades ----------------------------------------------

TAP_MANIFEST = {"tap": {"latest": "0.8.3", "min": "0.6.0", "recommended": "0.8.0"}}


@pytest.fixture
def tap_disk(tmp_path, monkeypatch):
    """A fake HOME: each agent's tap state dir, and Claude Code's install ledger.

    The real default paths, not the env overrides, so `probe update`'s own
    ledger reader (which only knows `~/.claude`) reads the same file the menu does.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    for name in (
        "PROBE_AGENT",
        "PROBE_INSTALLED_PLUGINS_JSON",
        "PROBE_RESEARCH_TAP_PLUGIN_DIR",
        "PRBE_CODEX_TAP_PLUGIN_DIR",
        "PROBE_PI_TAP_PLUGIN_DIR",
    ):
        monkeypatch.delenv(name, raising=False)
    ledger = tmp_path / ".claude" / "plugins" / "installed_plugins.json"

    def write(*, ran: str | None = None, installed, agent: str = "claude_code") -> None:
        """`installed` is a user-scope version, or `[(scope, version), ...]`."""
        if ran is not None:
            state = capabilities.tap_plugin_dir(agent)
            state.mkdir(parents=True, exist_ok=True)
            (state / ".installed_version").write_text(ran)
        pairs = [("user", installed)] if isinstance(installed, str) else installed
        entries = [{"scope": scope, "version": version} for scope, version in pairs]
        ledger.parent.mkdir(parents=True, exist_ok=True)
        ledger.write_text(json.dumps({"plugins": {updater.TAP_PLUGIN_ID: entries}}))

    return write


def _tap_row():
    (row,) = [row for row in compare(TAP_MANIFEST) if row.kind == "tap"]
    return row


def test_an_installed_update_is_not_graded_as_still_needed(tap_disk) -> None:
    """The menu said "Update needed — tap 0.6.1 → 0.8.3" directly after
    `probe update` said "transcript tap already at the latest (0.8.3)". The stamp
    it graded is only rewritten when a session next starts, so pressing Update
    again could never clear it."""
    tap_disk(ran="0.6.1", installed="0.8.3")

    row = _tap_row()
    assert row.installed == updater.installed_tap_version() == "0.8.3"
    assert row.status is VersionStatus.CURRENT
    rendered = _rendered(Capabilities(version_rows=(row,), version_manifest_age_s=60.0))
    assert "Update needed" not in rendered
    assert "0.6.1" not in rendered


@pytest.mark.parametrize(
    "entries",
    [
        [("user", "0.8.3"), ("project", "0.6.1")],
        [("project", "0.6.1"), ("user", "0.8.3")],
        [("project", "0.8.3"), ("user", "0.6.1")],
    ],
)
def test_the_menu_grades_the_ledger_entry_probe_update_reports(tap_disk, entries) -> None:
    """One plugin, several install scopes. A second parse of the ledger kept the
    LAST entry while `probe update` kept the highest, so a user install listed
    ahead of a project copy brought the same contradiction straight back. The
    menu now asks `probe update`'s own reader, so the two cannot disagree."""
    tap_disk(ran="0.6.1", installed=entries)
    assert _tap_row().installed == updater.installed_tap_version() == "0.8.3"


def test_a_stamp_ahead_of_the_ledger_is_kept(tap_disk) -> None:
    """The ledger only ever raises the number, never lowers it."""
    tap_disk(ran="0.9.0", installed="0.8.3")
    assert _tap_row().installed == "0.9.0"


def test_an_unparseable_stamp_is_not_lowered_by_the_ledger(tap_disk) -> None:
    tap_disk(ran="0.9.0.dev1", installed="0.8.3")
    assert _tap_row().installed == "0.9.0.dev1"


def test_a_blank_ledger_version_leaves_the_stamp_graded(tap_disk) -> None:
    """A blank string used to reach `split()[-1]` and raise, which doctor
    swallows by dropping EVERY version row."""
    tap_disk(ran="0.8.3", installed="   ")
    assert _tap_row().status is VersionStatus.CURRENT


@pytest.mark.parametrize("agent", ["codex", "pi"])
def test_the_claude_ledger_never_overrides_another_agents_stamp(
    tap_disk, monkeypatch, agent
) -> None:
    """The ledger is Claude Code's. It says nothing about a Codex or pi tap, so
    one that is really behind stays behind."""
    monkeypatch.setenv("PROBE_AGENT", agent)
    tap_disk(ran="0.6.1", installed="0.8.3", agent=agent)

    row = _tap_row()
    assert row.installed == "0.6.1"
    assert row.status is VersionStatus.NEEDED


@pytest.mark.parametrize("agent", ["codex", "pi"])
def test_another_agents_tap_without_a_stamp_reads_unknown(tap_disk, monkeypatch, agent) -> None:
    """Not Claude Code's number: a tap that has never run under this agent is
    unreadable, never current."""
    monkeypatch.setenv("PROBE_AGENT", agent)
    tap_disk(installed="0.8.3")

    row = _tap_row()
    assert row.installed is None
    assert row.status is VersionStatus.UNKNOWN


# -- the frame ----------------------------------------------------------------


# -- overall() ----------------------------------------------------------------


def _row(kind: str, status: VersionStatus) -> Comparison:
    return Comparison(kind=kind, installed="1.0.0", latest="1.0.0", minimum=None, status=status)


def test_overall_returns_the_worst_tier() -> None:
    rows = [
        _row("cli", VersionStatus.CURRENT),
        _row("plugin", VersionStatus.UPDATE),
        _row("tap", VersionStatus.REQUIRED),
    ]
    assert overall(rows) is VersionStatus.REQUIRED


def test_overall_ignores_unknown_when_anything_was_gradeable() -> None:
    rows = [_row("cli", VersionStatus.CURRENT), _row("plugin", VersionStatus.UNKNOWN)]
    assert overall(rows) is VersionStatus.CURRENT


def test_overall_is_unknown_when_nothing_was_gradeable() -> None:
    rows = [_row("cli", VersionStatus.UNKNOWN), _row("plugin", VersionStatus.UNKNOWN)]
    assert overall(rows) is VersionStatus.UNKNOWN


def test_overall_of_nothing_is_unknown() -> None:
    assert overall([]) is VersionStatus.UNKNOWN


# -- the manifest warm-up ------------------------------------------------------
#
# `probe doctor` deliberately never fetches: it is the command people run when
# things are already broken, and it has to work offline. The wizard is the
# opposite case, and without a fetch the row above could not exist on the
# machines that need it -- the only other refresher is gated on auto-update being
# ON, so a box with it off would never hold a manifest to be graded against.


class _Policy:
    """A stand-in for `probe.version_policy` that records what was asked of it."""

    TTL = 900

    def __init__(self, *, manifest=None, fresh=False, claim=True):
        self._manifest = manifest
        self._fresh = fresh
        self._claim = claim
        self.fetched = 0
        self.claimed = 0
        self.released = 0
        self.reads = 0

    def read_cache(self):
        self.reads += 1
        return (self._manifest, 1.0, True)

    def cache_is_fresh(self, _fetched_at, _ok):
        return self._fresh

    def claim_refresh(self):
        self.claimed += 1
        return self._claim

    def release_refresh(self, owner=None):
        self.released += 1

    def refresh(self, base=None, *, context=None):
        self.fetched += 1
        self._manifest = {"cli": {"latest": "9.9.9"}}
        return self._manifest


@pytest.fixture
def policy(monkeypatch):
    import probe

    def install(stub):
        monkeypatch.setattr(probe, "version_policy", stub, raising=False)
        return stub

    return install


def test_a_fresh_cache_is_not_refetched(policy) -> None:
    """The row is rendered on every pass through the menu. A fetch per pass would
    put a network round trip behind a keystroke."""
    from probe.cli import versions

    stub = policy(_Policy(manifest={"cli": {}}, fresh=True))
    versions.warm_manifest()
    assert (stub.fetched, stub.claimed) == (0, 0)


def test_a_stale_cache_is_refetched_and_the_claim_released(policy) -> None:
    from probe.cli import versions

    stub = policy(_Policy(manifest={"cli": {}}, fresh=False))
    versions.warm_manifest()
    assert (stub.fetched, stub.released) == (1, 1)


def test_a_claim_held_elsewhere_is_never_raced(policy) -> None:
    """The detached refresher this same CLI spawns at startup usually holds it.
    A stale manifest is a fine thing to render while a fresh one lands."""
    from probe.cli import versions

    stub = policy(_Policy(manifest={"cli": {}}, fresh=False, claim=False))
    versions.warm_manifest()
    assert (stub.fetched, stub.released) == (0, 0)


def test_with_nothing_cached_it_waits_for_the_other_fetch(policy) -> None:
    """The one case worth waiting for: a first run on a fresh machine, where
    returning now means the row can only say "not checked"."""
    from probe.cli import versions

    stub = policy(_Policy(manifest=None, fresh=False, claim=False))

    reads = {"n": 0}
    original = stub.read_cache

    def landing_read():
        reads["n"] += 1
        if reads["n"] > 2:
            stub._manifest = {"cli": {"latest": "9.9.9"}}
        return original()

    stub.read_cache = landing_read
    versions.warm_manifest(wait_s=2.0)
    assert reads["n"] > 2


def test_the_wait_is_bounded(policy) -> None:
    import time

    from probe.cli import versions

    policy(_Policy(manifest=None, fresh=False, claim=False))
    started = time.monotonic()
    versions.warm_manifest(wait_s=0.4)
    assert time.monotonic() - started < 3.0


def test_a_failing_fetch_never_reaches_the_caller(policy) -> None:
    """An offline machine still gets its menu. The row says "not checked", which
    is the true answer, and nothing above it breaks."""
    from probe.cli import versions

    stub = _Policy(manifest=None, fresh=False)

    def boom(base=None):
        raise OSError("no network")

    stub.refresh = boom
    policy(stub)
    versions.warm_manifest()
    assert stub.released == 1
