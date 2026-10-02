"""The plugin's skill copies must match the canonical `skills/`.

`plugins/probe-research/skills/` is a COPY of `skills/`, not a symlink — the plugin
ships self-contained, so the duplication is deliberate. `make sync-plugin-skills`
reconciles them and nothing enforced it, which meant an edit to `skills/` shipped a
plugin still teaching the old thing, silently and indefinitely.

That failure is invisible in the worst way: the tests pass, the MCP is correct, and
only the AGENT is wrong — it drives a capable tool with stale instructions. Since
"thin harness, fat skills" puts the knowledge of which view to ask for INTO these
files, a drifted copy is not a docs nit; it is half the product being wrong.

Same contract as tests/test_parity.py and tests/test_deploy_scope.py: guard it,
never rely on someone remembering. CI (`ci.yml`, `release.yml`) and the MCP deploy
(`deploy-mcp.yml`) all run `pytest -q`, so this blocks the rollout too.
"""

from __future__ import annotations

import filecmp
import re
from pathlib import Path

import pytest

from probe import skill_versions

_ROOT = Path(__file__).resolve().parent.parent

_CANONICAL = _ROOT / "skills"
_PLUGIN = _ROOT / "plugins" / "probe-research" / "skills"

# Mirrors the Makefile's sync-plugin-skills list.
_SYNCED = (
    "probe",
    "track-work",
    "visualize-progress",
    "instrument-code",
    "audit-team-note",
    "edit-notes",
    # one-release stub (renamed to audit-team-note 2026-09-17); drop with 0.91
    "notes-audit",
)

#: A fenced block, lazily matched so adjacent fences do not merge into one.
_FENCED_BLOCK = re.compile(r"```.*?```", re.DOTALL)


def _files(root: Path) -> dict[str, Path]:
    """Every file under `root`, keyed by its path relative to root."""
    return {
        str(path.relative_to(root)): path
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


@pytest.mark.parametrize("skill", _SYNCED)
def test_plugin_skill_copy_matches_canonical(skill: str) -> None:
    canonical, plugin = _CANONICAL / skill, _PLUGIN / skill
    assert canonical.is_dir(), f"canonical skill {skill} is missing"
    assert plugin.is_dir(), f"plugin copy of {skill} is missing; run `make sync-plugin-skills`"

    left, right = _files(canonical), _files(plugin)
    if (canonical / skill_versions.VERSIONS).is_dir():
        # One base, one version per reader: the copy is the MAIN AGENT's version
        # and carries no `versions/` (the writer's header never reaches it).
        left = {k: v for k, v in left.items() if not k.startswith(skill_versions.VERSIONS + "/")}
        assert (plugin / "SKILL.md").read_text(encoding="utf-8") == skill_versions.render(
            canonical, skill_versions.MAIN_AGENT), f"{skill}: not the main agent's version -- run `make sync-plugin`"
        left.pop("SKILL.md")
        right = {k: v for k, v in right.items() if k != "SKILL.md"}
    assert sorted(left) == sorted(right), (
        f"{skill}: plugin copy has a different file list than skills/{skill} "
        f"— run `make sync-plugin-skills`"
    )
    drifted = [name for name in left if not filecmp.cmp(left[name], right[name], shallow=False)]
    assert not drifted, (
        f"{skill}: {drifted} differ from the canonical skills/{skill} "
        f"— run `make sync-plugin-skills` (edit skills/, never the plugin copy)"
    )


def test_every_canonical_skill_is_covered_by_this_guard() -> None:
    """A new skill must be added to the Makefile's sync list AND to `_SYNCED`.

    Without this, adding skills/foo/ without wiring the sync would leave the plugin
    silently missing it while every parametrized case above still passed."""
    on_disk = {path.name for path in _CANONICAL.iterdir() if path.is_dir()}
    covered = set(_SYNCED)
    assert on_disk == covered, (
        f"skills/ holds {sorted(on_disk)} but this guard covers {sorted(covered)}; "
        "add it to _SYNCED + the Makefile"
    )


def test_the_wheel_ships_the_canonical_skills_not_a_third_copy() -> None:
    """The THIRD copy path nothing guarded.

    `pyproject.toml` ships `skills` as shared-data
    (`share/probe-research/skills`). That is a third distribution of the same
    files, and unlike the plugin copy it had no guard at all — a wheel built
    from a tree with drifted skills would install them and nothing would fail.

    Point it at the canonical directory, and assert it stays pointed there: the
    moment it names a copy instead, the copy can drift the way the plugin's did.
    """
    from probe._compat import tomllib

    with (_ROOT / "pyproject.toml").open("rb") as fh:
        config = tomllib.load(fh)
    shared = config["tool"]["hatch"]["build"]["targets"]["wheel"]["shared-data"]
    assert "skills" in shared, (
        "the wheel no longer ships skills/ — if that is deliberate, delete this "
        "guard; if it now ships a COPY, point it back at skills/"
    )


def test_no_skill_names_a_tool_that_does_not_exist() -> None:
    """A skill naming a retired tool teaches an agent to call nothing.

    This is the failure that actually shipped: the installed copy of
    track-experiment was measured 30 lines behind the repo, still teaching a
    surface that had moved. No test can reach a user's installed cache, but this
    at least stops the SOURCE from naming tools that are gone.
    """
    import re

    # Read the declared tool names from the server source rather than standing a
    # server up: this guard is about the SKILLS being consistent with the code,
    # and it should not need a client, a fake backend, or an event loop to say so.
    server_src = (_ROOT / "src" / "probe" / "mcp" / "server.py").read_text()
    declared = set(re.findall(r"^    def ([a-z_]+)\(", server_src, re.M))

    referenced: dict[str, set[str]] = {}
    for skill_dir in _CANONICAL.iterdir():
        if not skill_dir.is_dir():
            continue
        text = (skill_dir / "SKILL.md").read_text()
        # Tool-shaped mentions: `name(` or `name` in backticks.
        found = set(
            re.findall(
                r"`(browse_research|search_knowledge|get_entity|probe_procedures|research_\w+)",
                text,
            )
        )
        referenced[skill_dir.name] = found

    for skill, names in referenced.items():
        unknown = sorted(n for n in names if n not in declared)
        assert not unknown, f"{skill} names tools that do not exist: {unknown}"


def test_user_facing_docs_do_not_advertise_the_retired_surface() -> None:
    """The README and the setup command are what a NEW user reads first.

    The skills guard above covers `skills/`, which is why this slipped: the
    README and `plugins/*/commands/` were pointing new users at the five names
    that disappear next release. Deprecated names may be MENTIONED (they still
    answer), but not presented as the surface.
    """
    for rel in ("README.md", "plugins/probe-research/commands/probe-research-setup.md"):
        text = (_ROOT / rel).read_text()
        assert "browse" in text, f"{rel} does not mention the current surface"
        assert "search_knowledge" in text, f"{rel} does not mention the current surface"
        assert "entity" in text, f"{rel} does not mention the current surface"
        # If it names a deprecated tool it must say so within a few lines.
        if "research_resolve" in text:
            assert "deprecat" in text.lower(), (
                f"{rel} names retired tools without marking them deprecated"
            )


def test_the_setup_command_mints_the_token_before_installing_the_plugin() -> None:
    """The plugin must not land before there is a credential for it to serve.

    `tests/test_setup_wizard.py` already guards this ordering for `probe wizard`,
    on the observable call order. That test cannot see this file. So #165 moved
    the approval first in the CLI and left the slash command installing the plugin
    two steps BEFORE `probe mcp token set` — the same bug, still shipping, on the
    path a Claude Code user actually takes.

    The window is the whole defect. The plugin ships an `.mcp.json` for the hosted
    MCP; installed with no `mcp_token` stored, it connects with no `Authorization`
    header, the edge answers 401 with a `WWW-Authenticate` challenge, and Claude
    Code discovers an authorization server from it and PINS the connection to
    OAuth. Minting the token afterwards does not undo the pin — the install
    finishes, says "done", and sends the user to `/mcp` to authenticate a device
    the wizard already authorized.

    Asserted on the order of the two COMMANDS, not on step numbers, so renumbering
    the document cannot silently satisfy it. The mint is the wizard's sign-in
    now: every device setup goes through the wizard (2026-09-29), and its
    sign-in grants `mcp` alongside `api` (`setup.sign_in`).

    Scoped to FENCED BLOCKS, which is where a command someone runs actually lives.
    Matching raw text would make the prose unable to name the command it is warning
    about -- a warning against installing early, placed early, would read as the
    install itself and fail a correct document.
    """
    rel = "plugins/probe-research/commands/probe-research-setup.md"
    text = (_ROOT / rel).read_text()
    # Concatenated in document order, so relative position is preserved.
    runnable = "\n".join(m.group(0) for m in _FENCED_BLOCK.finditer(text))

    mint = runnable.find("probe wizard --action login")
    install = runnable.find("/plugin install probe-research")

    assert mint != -1, f"{rel} no longer mints an MCP read token"
    assert install != -1, f"{rel} no longer installs the plugin"
    assert mint < install, (
        f"{rel} installs the plugin before minting the MCP token; a fresh install "
        "will pin itself to OAuth and send the user to /mcp to re-authenticate"
    )


def test_workflow_skill_teaches_the_entity_prose_contract() -> None:
    """Creation-only guidance is missed once a project already exists.

    The tracking entry point must teach storage choice and ownership: the
    authored Markdown below AI Summary is the researcher's by policy (the
    `--summary` flag still exists), and agent prose goes to the hidden notes,
    whose method is the `edit-notes` skill.
    """
    for skill in ("track-work",):
        text = (_CANONICAL / skill / "SKILL.md").read_text() + (
            _CANONICAL / skill / "reference.md"
        ).read_text()
        assert "description" in text
        assert "authored Markdown" in text
        assert "summary_markdown" in text
        assert "the RESEARCHER's - never write it" in text
        assert "hidden" in text and "notes" in text
        assert "AI Summary" in text
        assert "`edit-notes`" in text


def test_openai_skill_manifests_surface_dashboard_context() -> None:
    """The selection prompt is read before the skill body, so it must make the
    trigger discoverable: what to record, and that it fires unprompted."""
    for skill in ("track-work",):
        text = (_CANONICAL / skill / "agents" / "openai.yaml").read_text()
        assert "ALL related work" in text
        assert "unprompted" in text


def test_every_skill_description_parses_as_yaml() -> None:
    """A description that does not parse takes the whole skill down, silently.

    The guards above compare the three copies to each other and check that the
    tool names are real. Neither reads the frontmatter as YAML, so a `: ` inside
    a plain scalar -- `reproduce: training, evaluation` -- terminates the scalar,
    breaks the document, and the skill stops loading. Every test still passes,
    the copies are still byte-identical, and the only casualty is the agent,
    which now has no instructions at all.

    Caught by writing exactly that bug into a description and watching this
    file's other tests go green on it. `: ` is the whole trap: it is the one
    two-character sequence that ends a plain scalar, and skill descriptions are
    prose full of colons.
    """
    yaml = pytest.importorskip("yaml")

    for skill in _SYNCED:
        text = (_CANONICAL / skill / "SKILL.md").read_text()
        assert text.startswith("---\n"), f"{skill}: SKILL.md has no frontmatter block"
        _, frontmatter, _ = text.split("---", 2)

        try:
            parsed = yaml.safe_load(frontmatter)
        except yaml.YAMLError as exc:  # pragma: no cover - the failure message is the point
            pytest.fail(f"{skill}: frontmatter is not valid YAML -- {exc}")

        assert isinstance(parsed, dict), f"{skill}: frontmatter did not parse to a mapping"
        assert parsed.get("name") == skill, f"{skill}: name field does not match its directory"

        description = parsed.get("description")
        assert isinstance(description, str) and description.strip(), (
            f"{skill}: description is missing or empty after parsing"
        )
        assert ": " not in description, (
            f"{skill}: description contains a ': ' sequence, which terminates the plain "
            f"scalar and breaks the frontmatter. Use an em-dash."
        )


def test_the_makefile_sync_list_matches_synced() -> None:
    """The two lists were tied only by comments; a hand-copied plugin dir plus
    an updated _SYNCED leaves the Makefile stale while every test passes, and
    the copy-drift failure message then recommends a command that no longer
    fixes the drift it detects. Parse the for-loop and make the mirror
    mechanical."""
    import re

    makefile = (_ROOT / "Makefile").read_text(encoding="utf-8")
    m = re.search(r"sync-plugin-skills:\n\t@for s in ([^;]+); do", makefile)
    assert m, "could not parse the sync-plugin-skills loop"
    assert set(m.group(1).split()) == set(_SYNCED)


#: The removed team-rules ("workflow memory") surface: its MCP tool, its skills
#: and its CLI group. None of them exists any more, so shipped text that names
#: one sends an agent after nothing.
_REMOVED_RULES_SURFACE = ("probe_procedures", "read-rules", "set-rule", "probe rule ")


def test_no_shipped_text_names_the_removed_team_rules_surface() -> None:
    """Every text an agent loads from us, scanned for the removed feature.

    `test_no_skill_names_a_tool_that_does_not_exist` only sees the tool names in
    its own pattern, and the always-loaded block's allow-list only sees
    hyphenated backticked names -- so `probe_procedures` or `probe rule list`
    coming back through a restored paragraph would pass both.
    """
    from probe.cli import agent_rules
    from probe.mcp.server import MCP_INSTRUCTIONS

    surfaces = {
        "agent_rules.POINTER_BODY": agent_rules.POINTER_BODY,
        "mcp.server.MCP_INSTRUCTIONS": MCP_INSTRUCTIONS,
    }
    for root in (
        _CANONICAL,
        _PLUGIN,
        _ROOT / "plugins" / "probe-research-pi" / "skills",
        _ROOT / "plugins" / "probe-research" / "commands",
    ):
        for path in root.rglob("*.md"):
            surfaces[str(path.relative_to(_ROOT))] = path.read_text(encoding="utf-8")
    assert len(surfaces) > 10, "the scan found almost nothing to read; a root moved"
    leaks = [
        (where, name)
        for where, text in surfaces.items()
        for name in _REMOVED_RULES_SURFACE
        if name in text
    ]
    assert not leaks, f"shipped text still names the removed team-rules surface: {leaks}"
