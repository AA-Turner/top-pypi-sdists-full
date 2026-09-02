"""Every plugin skill and agent loads with real metadata (PF-398).

Two failure modes here are silent, which is the only reason this file exists.

**An unquoted `": "` in a plain YAML scalar does not error** -- the frontmatter
fails to parse and the component loads with *empty metadata* instead. It is
still "installed"; it simply describes itself as nothing, so the model never
picks it. `claude plugin validate` does not catch it: run against either the
marketplace manifest or the plugin root, it validates the *manifest* and does
not descend into `skills/` or `agents/` at all. CI runs both paths and both
pass with a broken skill sitting right there.

**A component outside `plugins/innoday/` is never loaded.** The plugin root is
declared by `source` in `.claude-plugin/marketplace.json`; a skill dropped in a
top-level `skills/` directory is simply outside the plugin, with no error
anywhere. See CLAUDE.md, "The Claude Code plugin lives in `plugins/innoday/`".
"""

from pathlib import Path

import pytest
import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[1] / "plugins" / "innoday"
COMPONENTS = sorted(
    list(PLUGIN_ROOT.glob("skills/*/SKILL.md")) + list(PLUGIN_ROOT.glob("agents/*.md"))
)


def frontmatter(path: Path) -> dict:
    text = path.read_text()
    assert text.startswith("---"), f"{path} has no frontmatter block"
    _, block, _ = text.split("---", 2)
    return yaml.safe_load(block) or {}


def test_there_are_components_to_check():
    """A glob that silently matches nothing would make every test below vacuous."""
    assert COMPONENTS


@pytest.mark.parametrize("path", COMPONENTS, ids=lambda p: p.stem)
def test_frontmatter_parses_to_real_metadata(path):
    meta = frontmatter(path)
    assert meta, f"{path} parsed to empty metadata — check for an unquoted ': '"
    assert meta.get("name"), f"{path} has no name"
    assert meta.get("description"), f"{path} has no description"


@pytest.mark.parametrize("path", COMPONENTS, ids=lambda p: p.stem)
def test_a_skill_directory_matches_its_declared_name(path):
    if path.name != "SKILL.md":
        return
    assert frontmatter(path)["name"] == path.parent.name


def test_no_components_live_outside_the_plugin_root():
    """Outside `plugins/innoday/` they are silently never loaded."""
    repo = PLUGIN_ROOT.parents[1]
    for stray in ("skills", "agents"):
        assert not (repo / stray).exists(), (
            f"{stray}/ at the repo root is outside the plugin and will never "
            "load — move it under plugins/innoday/"
        )
