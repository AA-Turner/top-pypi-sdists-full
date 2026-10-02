"""The Probe daemon's recording rules ARE `track-work`, byte for byte.

The design's rule: naming and write kinds have one source of truth, the skill
the agent reads. The tap cannot reach the skill at runtime (a separate plugin),
so `make sync-tap-core` vendors it as `tap/companion_rules.md`, and its detailed
`reference.md` as `tap/companion_reference.md`; this fails when a copy drifts.
"""

from pathlib import Path

AGENT = Path(__file__).resolve().parents[1]


def test_the_daemon_reads_the_same_rules_as_the_agent():
    """The same base; a daemon reads the WRITER's version of it (skill_versions)."""
    from probe import skill_versions

    skill = skill_versions.render(AGENT / "skills" / "track-work", skill_versions.WRITER)
    vendored = (AGENT / "plugins" / "probe-research-tap" / "tap" / "companion_rules.md").read_text(encoding="utf-8")
    assert vendored == skill, "run `make -C agent sync-tap-core`"


def test_the_daemon_reads_the_same_reference_as_the_agent():
    reference = (AGENT / "skills" / "track-work" / "reference.md").read_text(encoding="utf-8")
    vendored = (AGENT / "plugins" / "probe-research-tap" / "tap" / "companion_reference.md").read_text(
        encoding="utf-8"
    )
    assert vendored == reference, "run `make -C agent sync-tap-core`"
