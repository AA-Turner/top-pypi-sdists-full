"""Guards the astral-sh/setup-uv `version:` input across all workflows.

Scope is .github/workflows/** only. specs/** and .devcontainer/** carry the
same-looking string as valid PEP 440 — a different grammar — and must not be
touched. Selection is structural (uses:/with:), so prose can never match.
"""

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOW_DIR = REPO_ROOT / ".github" / "workflows"
_SETUP_UV = re.compile(r"^astral-sh/setup-uv@")


def _setup_uv_sites() -> list[tuple[str, str, str, str]]:
    """Return (file, job, step_label, version) for every setup-uv step."""
    found: list[tuple[str, str, str, str]] = []
    for path in sorted([*WORKFLOW_DIR.glob("*.yml"), *WORKFLOW_DIR.glob("*.yaml")]):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict):
            continue
        for job_id, job in (doc.get("jobs") or {}).items():
            if not isinstance(job, dict):
                continue
            for index, step in enumerate(job.get("steps") or []):
                if not isinstance(step, dict):
                    continue
                uses = step.get("uses")
                if not isinstance(uses, str) or not _SETUP_UV.match(uses.strip()):
                    continue
                with_block = step.get("with")
                version = with_block.get("version", "") if isinstance(with_block, dict) else ""
                label = f"step={index} {step.get('name') or '<unnamed>'!r}"
                found.append((path.name, str(job_id), label, str(version) if version is not None else ""))
    return found


class TestSetupUvVersionGrammar:
    def test_guard_is_wired_to_at_least_one_site(self) -> None:
        assert _setup_uv_sites(), "No astral-sh/setup-uv step found; guard is dead code."

    def test_every_site_is_pinned(self) -> None:
        """An unpinned site would otherwise surface as spurious divergence."""
        unpinned = [s for s in _setup_uv_sites() if not s[3].strip()]
        assert not unpinned, f"setup-uv step(s) with no `version:` input: {unpinned}"

    def test_version_is_valid_node_semver(self) -> None:
        """The `version:` input is node-semver, which rejects comma-separated ranges."""
        offenders = [s for s in _setup_uv_sites() if "," in s[3]]
        assert not offenders, (
            f"Comma-separated range(s) found: {offenders}. The setup-uv `version:` input is "
            "node-semver, not PEP 440; a comma matches no release. Use a hyphen range, "
            'e.g. "0.7 - 0.11".'
        )

    def test_all_sites_agree(self) -> None:
        """Catches partial updates: five sites bumped, one missed."""
        sites = [s for s in _setup_uv_sites() if s[3].strip()]
        assert len({s[3] for s in sites}) <= 1, f"Divergent setup-uv versions across sites: {sites}"
