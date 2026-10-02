"""The middle tier: "update needed", driven by the manifest's `recommended`.

WHY A THIRD TIER EXISTS. Until this, the hook could say exactly two things about
a stale install: "an update exists" (routine, ignorable, and correctly so) and
"you are below the minimum supported version" (loud, and reserved for installs
the server no longer supports). A breaking change fits neither. Raising `min` to
a release published an hour ago declares the whole fleet unsupported; leaving the
routine nudge to carry it means a user skips it for three weeks while a renamed
field 422s under them.

`recommended` is the version below which we KNOW something is broken and the
install is still supported. It is a VERSION rather than a boolean because a
boolean cannot say who is affected: it shouts at everyone below `latest` until a
human remembers to unset it, and by the second release nobody reads it. The
properties that matter, and that this file asserts:

  * a manifest WITHOUT the field behaves exactly as before -- every manifest
    published to date says nothing about `recommended`, and none of them may
    start warning;
  * below `recommended` speaks in a different voice, and carries the advisory
    and the restart note that the routine nudge deliberately dropped;
  * passing `recommended` returns the install to the routine voice WITH NO
    SECOND PUBLISH -- the property a boolean flag cannot have;
  * `min` still wins over `recommended`, and `recommended` over routine;
  * the grading is PER COMPONENT, because a current CLI beside a plugin that
    predates the change is the ordinary shape of this, not an edge case;
  * the advisory stays out of `additionalContext`. It is fetched over the
    network, and that channel is read by the model as instructions.
"""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path

import pytest

_HOOK = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "probe-research"
    / "hooks"
    / "version_check.py"
)

_ADVISORY = "A CLI below 0.146.0 predates the question rename: amending an experiment returns 422."


def _load_hook():
    """Load the hook the way session-start.sh runs it (its dir on sys.path)."""
    spec = importlib.util.spec_from_file_location("_version_check_tier_test", _HOOK)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    hooks_dir = str(_HOOK.parent)
    added = hooks_dir not in sys.path
    if added:
        sys.path.insert(0, hooks_dir)
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(hooks_dir)
    return module


@pytest.fixture
def hook():
    return _load_hook()


@pytest.fixture(autouse=True)
def _isolate_agent_environment(monkeypatch) -> None:
    monkeypatch.delenv("PROBE_AGENT", raising=False)
    monkeypatch.delenv("PROBE_HOOK_EVENT", raising=False)
    monkeypatch.delenv("PROBE_SESSION_SOURCE", raising=False)


def _manifest(*, cli_recommended=None, plugin_recommended=None, advisory=_ADVISORY):
    manifest = {
        "cli": {"latest": "0.147.0", "min": "0.127.0"},
        "plugin": {"latest": "0.71.0", "min": "0.63.0"},
        "tap": {"latest": "0.4.5", "min": "0.1.0"},
        "advisory": advisory,
    }
    if cli_recommended is not None:
        manifest["cli"]["recommended"] = cli_recommended
    if plugin_recommended is not None:
        manifest["plugin"]["recommended"] = plugin_recommended
    return manifest


def _drive(hook, monkeypatch, *, manifest, cli="0.147.0", plugin="0.71.0", tap="0.4.5"):
    """Run the REAL main() against a stubbed manifest and return its JSON.

    Everything stubbed here is I/O the hook does on the way to the decision --
    the cache, the local version probes, the detached spawns. The comparison and
    the message are the code under test.
    """
    monkeypatch.setattr(
        hook.version_policy, "read_cache", lambda *a, **k: (manifest, 10.0**12, True)
    )
    monkeypatch.setattr(hook.version_policy, "cache_is_fresh", lambda *a, **k: True)
    monkeypatch.setattr(hook, "_local_cli", lambda *_: cli)
    monkeypatch.setattr(hook, "_local_plugin", lambda *_: plugin)
    monkeypatch.setattr(hook, "_local_tap", lambda: tap)
    monkeypatch.setattr(hook, "_spawn_autoupdate", lambda *_: None)
    monkeypatch.setattr(hook, "_spawn_session_maintenance", lambda *a, **k: None)
    monkeypatch.setattr(hook, "_seed_tracking_signal", lambda *a, **k: None)
    monkeypatch.setattr(hook, "_stale_manifest_notice", lambda *a, **k: None)

    buffer = io.StringIO()
    real_stdout = sys.stdout
    sys.stdout = buffer
    try:
        with pytest.raises(SystemExit):
            hook.main()
    finally:
        sys.stdout = real_stdout
    return json.loads(buffer.getvalue())


def _message(out) -> str:
    return out.get("systemMessage", "")


def _context(out) -> str:
    return out.get("hookSpecificOutput", {}).get("additionalContext", "")


# -- the field is absent ------------------------------------------------------


def test_a_manifest_without_the_field_keeps_the_routine_nudge(hook, monkeypatch) -> None:
    """THE COMPATIBILITY GUARD, and the one that matters most on the day this
    ships: every manifest published before this field exists says nothing about
    `recommended`, and not one of them may start shouting because the client
    learned a new word."""
    out = _drive(hook, monkeypatch, manifest=_manifest(), cli="0.144.0")
    assert "update available" in _message(out)
    assert "some features may not work correctly" not in _message(out)


def test_a_routine_nudge_still_omits_the_advisory_and_the_restart_note(hook, monkeypatch) -> None:
    """The trim this tier was built alongside. A routine nudge is what changed
    and what to run; the advisory is one manifest-wide string, so ungated it
    reaches mostly people it does not describe."""
    out = _drive(hook, monkeypatch, manifest=_manifest(), cli="0.144.0")
    assert "Note:" not in _message(out)
    assert "restart Claude Code" not in _message(out)


# -- the field is set ---------------------------------------------------------


def test_below_recommended_speaks_in_the_urgent_voice(hook, monkeypatch) -> None:
    """THE guard for the whole feature: a server flag turns a nudge people
    correctly ignore into one that says what waiting costs them."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.144.0")
    msg = _message(out)
    assert "update needed" in msg, msg
    assert "some features may not work correctly" in msg, msg


def test_below_recommended_carries_the_advisory_and_the_restart_note(hook, monkeypatch) -> None:
    """`recommended` is what makes the advisory addressable. Ungated it went to
    every install; gated on this it reaches the machines it describes, which is
    the only reason it is worth printing at all."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.144.0")
    msg = _message(out)
    assert "422" in msg, f"the advisory did not reach the machine it describes: {msg!r}"
    assert "restart Claude Code" in msg, msg


def test_the_pair_points_at_latest_not_at_recommended(hook, monkeypatch) -> None:
    """`recommended` decides how loudly to speak; it is not the target. Sending
    someone to an intermediate release lands them on a version already behind."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.144.0")
    assert "CLI 0.144.0 → 0.147.0" in _message(out), _message(out)


def test_passing_recommended_returns_to_the_routine_voice(hook, monkeypatch) -> None:
    """THE PROPERTY A BOOLEAN CANNOT HAVE. The flag stays published; the machine
    moved past it, so it stops being warned -- with no second publish and nothing
    for a human to remember to unset."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.146.0")
    msg = _message(out)
    assert "update available" in msg, msg
    assert "some features may not work correctly" not in msg, msg


def test_a_current_install_stays_silent_with_the_flag_published(hook, monkeypatch) -> None:
    """The flag must not wake up a machine that has nothing to update."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"))
    assert out == {"continue": True}, out


# -- precedence and scope -----------------------------------------------------


def test_below_minimum_outranks_below_recommended(hook, monkeypatch) -> None:
    """Worst tier wins. An install past the supported floor is not told the
    softer of the two true things about it."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.100.0")
    msg = _message(out)
    assert "below the minimum supported version" in msg, msg
    assert "update needed" not in msg, msg


def test_the_tier_is_graded_per_component(hook, monkeypatch) -> None:
    """A current CLI beside a plugin that predates the change is the ORDINARY
    shape of a breaking release, because the two ship on independent schedules.
    The message must name the component that is actually behind."""
    out = _drive(
        hook,
        monkeypatch,
        manifest=_manifest(plugin_recommended="0.70.0"),
        cli="0.147.0",
        plugin="0.69.0",
        tap="0.4.5",
    )
    msg = _message(out)
    assert "update needed" in msg, msg
    # The SECOND line is the component list. Asserted on that line alone because
    # the advisory below it is prose and may legitimately mention any component.
    components = msg.splitlines()[1]
    assert components == "plugin 0.69.0 → 0.71.0", (
        f"a current CLI was listed alongside the stale plugin: {components!r}"
    )


def test_the_urgent_summary_lists_only_the_urgent_components(hook, monkeypatch) -> None:
    """A merely-behind tap alongside a CLI below `recommended` must not be listed
    beside it -- flattening the two back together is exactly the distinction the
    tier was added to draw."""
    out = _drive(
        hook,
        monkeypatch,
        manifest=_manifest(cli_recommended="0.146.0"),
        cli="0.144.0",
        tap="0.4.4",
    )
    assert "transcript tap" not in _message(out), _message(out)


# -- the model's channel ------------------------------------------------------


def test_the_agent_is_told_the_tier_is_urgent(hook, monkeypatch) -> None:
    """The model's standing instruction is not to nag, which is right for
    housekeeping and wrong here. Without this it reads every tier as the same
    routine notice and stays quiet through the one that mattered."""
    ctx = _context(
        _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.144.0")
    )
    assert "features may fail" in ctx, ctx
    assert "Do not nag" not in ctx, ctx


def test_the_routine_tier_still_tells_the_agent_not_to_nag(hook, monkeypatch) -> None:
    out = _drive(hook, monkeypatch, manifest=_manifest(), cli="0.144.0")
    assert "Do not nag" in _context(out), _context(out)


def test_the_advisory_never_reaches_the_model_channel(hook, monkeypatch) -> None:
    """The advisory arrives over the network from the version endpoint, and
    additionalContext is read by the model as instructions. It is displayed to a
    person and goes no further -- a compromised or mistyped manifest must not be
    able to hand the agent a directive."""
    out = _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.144.0")
    assert "422" in _message(out), "precondition: the advisory is in the visible line"
    assert "422" not in _context(out), f"advisory leaked into the model channel: {_context(out)!r}"


def test_a_malformed_recommended_does_not_break_the_nudge(hook, monkeypatch) -> None:
    """Unparseable thresholds are ignored rather than fatal -- the hook's whole
    contract is fail-open, and a bad publish must degrade to the routine nudge
    rather than to silence or a crash."""
    manifest = _manifest()
    manifest["cli"]["recommended"] = "not-a-version"
    out = _drive(hook, monkeypatch, manifest=manifest, cli="0.144.0")
    assert "update available" in _message(out), _message(out)


# -- `probe doctor` and `probe update --check` --------------------------------
#
# The hook is not the only surface that grades an install against the manifest.
# `probe doctor` is where a researcher goes to ASK, and its answer has to agree
# with the one the hook volunteered -- a doctor reading "update available" for a
# machine the session start called broken is worse than either message alone,
# because it reads as the warning being wrong.


def _rows(manifest, local):
    from probe.cli import versions

    return {row.kind: row for row in versions.compare(manifest, local)}


def _local(cli="0.147.0", plugin="0.71.0", tap="0.4.5"):
    return {"cli": cli, "sdk": cli, "plugin": plugin, "tap": tap}


def test_doctor_grades_below_recommended_as_needed() -> None:
    from probe.cli.versions import VersionStatus

    rows = _rows(_manifest(cli_recommended="0.146.0"), _local(cli="0.144.0"))
    assert rows["cli"].status is VersionStatus.NEEDED


def test_doctor_grades_at_recommended_as_a_plain_update() -> None:
    from probe.cli.versions import VersionStatus

    rows = _rows(_manifest(cli_recommended="0.146.0"), _local(cli="0.146.0"))
    assert rows["cli"].status is VersionStatus.UPDATE


def test_doctor_without_the_field_is_unchanged() -> None:
    from probe.cli.versions import VersionStatus

    rows = _rows(_manifest(), _local(cli="0.144.0"))
    assert rows["cli"].status is VersionStatus.UPDATE


def test_minimum_still_outranks_recommended_in_doctor() -> None:
    from probe.cli.versions import VersionStatus

    rows = _rows(_manifest(cli_recommended="0.146.0"), _local(cli="0.100.0"))
    assert rows["cli"].status is VersionStatus.REQUIRED


def test_the_sdk_inherits_the_cli_threshold() -> None:
    """The SDK ships inside the same distribution as the CLI and is graded
    against the `cli` pair. A threshold that skipped it would report one number
    as two different verdicts."""
    from probe.cli.versions import VersionStatus

    rows = _rows(_manifest(cli_recommended="0.146.0"), _local(cli="0.144.0"))
    assert rows["sdk"].status is VersionStatus.NEEDED


def test_the_needed_tier_counts_as_behind() -> None:
    """`behind` is what `probe update --check` turns into its exit code. A tier
    that printed a warning and still exited 0 would be invisible to every script
    that reads the code instead of the text."""
    rows = _rows(_manifest(cli_recommended="0.146.0"), _local(cli="0.144.0"))
    assert rows["cli"].behind is True


def test_doctor_names_the_consequence_not_the_severity() -> None:
    """The rendered line has to say what waiting costs, in a list where every
    other line is routine housekeeping."""
    from probe.cli import versions

    rendered = "\n".join(
        versions.render(
            versions.compare(_manifest(cli_recommended="0.146.0"), _local(cli="0.144.0"))
        )
    )
    assert "UPDATE NEEDED" in rendered, rendered
    assert "features may not work correctly" in rendered, rendered


# -- the server writes the sentence -------------------------------------------
#
# The tier is always the same shape: "you are below a threshold we published."
# What it COSTS the reader is different for every breaking change, and only the
# release that introduced it knows. So the sentence is a manifest field, per
# pair, sitting beside the threshold that decides who sees it -- and the client's
# own wording is only the fallback.


def _manifest_with_message(message, *, recommended="0.146.0", key="cli"):
    manifest = _manifest(cli_recommended=recommended if key == "cli" else None)
    if key != "cli":
        manifest[key]["recommended"] = recommended
    manifest[key]["message"] = message
    return manifest


def test_a_published_message_replaces_the_canned_sentence(hook, monkeypatch) -> None:
    """THE guard for the whole field: what the notice says is the publisher's to
    write, not the client's to guess."""
    manifest = _manifest_with_message("experiment writes return 422 on this version")
    msg = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.144.0"))
    assert "experiment writes return 422 on this version" in msg, msg
    assert "some features may not work correctly" not in msg, msg


def test_the_message_rides_the_headline(hook, monkeypatch) -> None:
    """It is the reason the reader is being interrupted, so it belongs on the
    first line -- not below a version list they have to scan past."""
    manifest = _manifest_with_message("run uploads silently drop")
    head = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.144.0")).splitlines()[0]
    assert head == "⚠ Probe Research update needed — run uploads silently drop", head


def test_a_pair_without_a_message_falls_back(hook, monkeypatch) -> None:
    """Every manifest published before the field has none, and the notice still
    has to say something true about why it is speaking."""
    msg = _message(
        _drive(hook, monkeypatch, manifest=_manifest(cli_recommended="0.146.0"), cli="0.144.0")
    )
    assert "some features may not work correctly until you update" in msg, msg


def test_a_message_on_a_current_component_is_not_shown(hook, monkeypatch) -> None:
    """A `message` describes what its component breaks, not a release, so it can
    sit in the manifest permanently. Reading it for a component that is fine
    would put a breakage warning on a machine nothing is wrong with."""
    manifest = _manifest_with_message("experiment writes return 422")
    out = _drive(hook, monkeypatch, manifest=manifest, cli="0.147.0", plugin="0.69.0")
    msg = _message(out)
    assert "update available" in msg, msg
    assert "422" not in msg, f"a current CLI's message leaked into the nudge: {msg!r}"


def test_a_message_on_a_merely_behind_component_is_not_shown(hook, monkeypatch) -> None:
    """Behind `latest` but at or above `recommended` is routine. The routine
    nudge stays one line about what changed -- that is what it is for."""
    manifest = _manifest_with_message("experiment writes return 422")
    msg = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.146.0"))
    assert "422" not in msg, msg
    assert msg.splitlines()[0] == "⚠ Probe Research update available", msg


def test_below_minimum_keeps_its_headline_without_a_message(hook, monkeypatch) -> None:
    """The generic fallback is for `needs_update` only. "Below the minimum
    supported version" already says the worst of it, and appending the softer
    sentence would make the louder tier read as the quieter one."""
    head = _message(_drive(hook, monkeypatch, manifest=_manifest(), cli="0.100.0")).splitlines()[0]
    assert head == "⚠ Probe Research is below the minimum supported version", head


def test_below_minimum_still_carries_a_published_message(hook, monkeypatch) -> None:
    """Not inventing a sentence is different from suppressing one. If the
    publisher wrote something for a component that is past the floor, that is
    exactly when it is worth reading."""
    manifest = _manifest_with_message("tokens minted by this CLI are rejected", recommended=None)
    manifest["cli"].pop("recommended", None)
    head = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.100.0")).splitlines()[0]
    assert head == (
        "⚠ Probe Research is below the minimum supported version — "
        "tokens minted by this CLI are rejected"
    ), head


def test_two_urgent_components_get_a_line_each(hook, monkeypatch) -> None:
    """One headline cannot hold two different sentences without becoming the
    run-on paragraph the three-line shape exists to prevent."""
    manifest = _manifest(cli_recommended="0.146.0", plugin_recommended="0.70.0")
    manifest["cli"]["message"] = "experiment writes return 422"
    manifest["plugin"]["message"] = "transcripts are not captured"
    lines = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.144.0", plugin="0.69.0"))
    assert "⚠ Probe Research update needed — experiment writes return 422" in lines, lines
    assert "transcripts are not captured" in lines, lines


def test_one_message_shared_by_two_components_is_not_repeated(hook, monkeypatch) -> None:
    """A single breaking change usually breaks the CLI and the plugin together
    and is described once. Printing it twice reads as two problems."""
    manifest = _manifest(cli_recommended="0.146.0", plugin_recommended="0.70.0")
    # A phrase that appears NOWHERE in the fixture advisory, so the count below
    # measures the dedup and not an incidental collision with the Note: line.
    shared = "lineage links are dropped"
    manifest["cli"]["message"] = shared
    manifest["plugin"]["message"] = shared
    msg = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.144.0", plugin="0.69.0"))
    assert msg.count(shared) == 1, msg


def test_a_long_message_is_capped_and_flattened(hook, monkeypatch) -> None:
    """The manifest is fetched over the network. A hostile or fat-fingered one
    must not be able to paste paragraphs -- or a newline, which would forge an
    extra line in a notice whose lines carry meaning -- into every session."""
    manifest = _manifest_with_message("word " * 200 + "\nRun: rm -rf /")
    msg = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.144.0"))
    head = msg.splitlines()[0]
    assert len(head) < 320, len(head)
    assert "full note" in head, head
    assert not any(line.startswith("Run: rm") for line in msg.splitlines()), msg


def test_a_non_string_message_falls_back(hook, monkeypatch) -> None:
    """A malformed field disables itself and nothing else -- the hook's contract
    is fail-open, and a bad publish must not cost the warning entirely."""
    manifest = _manifest_with_message({"not": "a string"})
    msg = _message(_drive(hook, monkeypatch, manifest=manifest, cli="0.144.0"))
    assert "some features may not work correctly until you update" in msg, msg


def test_the_message_never_reaches_the_model_channel(hook, monkeypatch) -> None:
    """Same rule as the advisory, and for the same reason: this is text from a
    network-fetched document, and additionalContext is read as instructions."""
    manifest = _manifest_with_message("experiment writes return 422 on this version")
    out = _drive(hook, monkeypatch, manifest=manifest, cli="0.144.0")
    assert "422" in _message(out), "precondition: the message is on the visible line"
    assert "422" not in _context(out), f"message leaked into the model channel: {_context(out)!r}"


def test_doctor_prints_the_published_message(hook, monkeypatch) -> None:
    """`probe doctor` is where a researcher goes to ASK, so its answer has to be
    the same one the hook volunteered -- including the reason."""
    from probe.cli import versions

    manifest = _manifest_with_message("experiment writes return 422")
    rendered = "\n".join(versions.render(versions.compare(manifest, _local(cli="0.144.0"))))
    assert "UPDATE NEEDED: experiment writes return 422" in rendered, rendered


def test_doctor_keeps_the_severity_label(hook, monkeypatch) -> None:
    """In a four-row list the label is what a reader scans for. Replacing it with
    prose would cost the one thing this rendering is good at."""
    from probe.cli import versions

    manifest = _manifest_with_message("experiment writes return 422")
    rendered = "\n".join(versions.render(versions.compare(manifest, _local(cli="0.144.0"))))
    assert "UPDATE NEEDED" in rendered, rendered


def test_doctor_does_not_print_a_message_on_a_current_row(hook, monkeypatch) -> None:
    """A message can sit in the manifest permanently. A row that is fine must not
    grow a breakage warning out of it."""
    from probe.cli import versions

    manifest = _manifest_with_message("experiment writes return 422")
    rendered = "\n".join(versions.render(versions.compare(manifest, _local(cli="0.147.0"))))
    assert "422" not in rendered, rendered


def test_doctor_caps_a_long_message(hook, monkeypatch) -> None:
    """A diagnostic whose rows ARE its output must not let one network-fetched
    row run to a paragraph, or carry a newline that forges another row."""
    from probe.cli import versions

    manifest = _manifest_with_message("word " * 200 + "\nCLI  99.9.9 (ok)")
    rendered = "\n".join(versions.render(versions.compare(manifest, _local(cli="0.144.0"))))
    assert len(max(rendered.splitlines(), key=len)) < 260, rendered
    assert "99.9.9" not in rendered, rendered
