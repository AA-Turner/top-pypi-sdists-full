"""Integration guard: the suppressed-comment triage contract stays self-consistent.

This is an integration-style test (not a 1:1:1 unit test): it reads the real agent, prompt
and contract documents under ``.github/`` and ``docs/`` and cross-checks them against each
other. The reaper (``#3686``) is implemented against
``docs/suppressed-comment-triage-contract.md``, so the regular expressions published there
must actually match the sentinel, markers and verdict rows the agent and prompt instruct
the triage agent to emit. A drift between the three files would otherwise only surface as
follow-up PRs that never close.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import pytest

from agentic_devtools.cli.ci import suppressed_reaper
from agentic_devtools.skill_injector import _parse_frontmatter

# Repo root, resolved from this test file's location (tests/workflows/).
_REPO_ROOT = Path(__file__).resolve().parents[2]

_AGENT_PATH = _REPO_ROOT / ".github" / "agents" / "agdt.suppressed-comment-triage.evaluate.agent.md"
_PROMPT_PATH = _REPO_ROOT / ".github" / "prompts" / "agdt.suppressed-comment-triage.evaluate.prompt.md"
_CONTRACT_PATH = _REPO_ROOT / "docs" / "suppressed-comment-triage-contract.md"

_SENTINEL = "SUPPRESSED_COMMENTS_EVALUATION_NO_CHANGES_NEEDED"
_VERDICTS = frozenset({"valid-fix", "valid-no-action", "invalid", "stale", "unparseable"})


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _regex_block_source() -> str:
    """Return the Python source from the contract's ``Regular expressions`` block."""
    match = re.search(r"### Regular expressions\s+```python\r?\n(.*?)\r?\n```", _read(_CONTRACT_PATH), re.DOTALL)
    assert match, "contract document is missing the Regular expressions Python code block"
    return match.group(1)


def _published_patterns() -> dict[str, re.Pattern[str]]:
    """Compile the regular expressions published in the contract document."""
    module = ast.parse(_regex_block_source())
    found: dict[str, re.Pattern[str]] = {}
    for node in module.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or not target.id.endswith("_RE"):
            continue
        value = node.value
        if not (
            isinstance(value, ast.Call)
            and isinstance(value.func, ast.Attribute)
            and isinstance(value.func.value, ast.Name)
            and value.func.value.id == "re"
            and value.func.attr == "compile"
            and value.args
            and isinstance(value.args[0], ast.Constant)
            and isinstance(value.args[0].value, str)
        ):
            continue
        found[target.id] = re.compile(value.args[0].value)
    assert found, "no published regular expressions found in the contract document"
    return found


def _documented_marker_sections(path: Path) -> list[tuple[int, int, int]]:
    """Return ``(section_start, section_end, finding_count)`` for each marker in ``path``."""
    text = _read(path)
    matches = list(_published_patterns()["DEFERRAL_MARKER_RE"].finditer(text))
    assert matches, f"{path.name} shows no parseable deferral marker"
    sections: list[tuple[int, int, int]] = []
    for index, match in enumerate(matches):
        payload = json.loads(match.group(1))
        finding_count = payload.get("finding_count")
        assert isinstance(finding_count, int), f"{path.name} finding_count is not an int"
        section_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.start(), section_end, finding_count))
    return sections


class TestSkillFilesArePlacedAndLoadable:
    """The agent and prompt exist where ``agdt-setup`` mirrors them, and parse."""

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_file_exists_and_is_non_empty(self, path: Path) -> None:
        """Each contract artifact exists and carries content."""
        assert path.is_file(), f"{path} is missing"
        assert _read(path).strip(), f"{path} is empty"

    def test_filenames_follow_the_managed_prefix_convention(self) -> None:
        """Both files use the ``agdt.<name>.<kind>.md`` names the mirror recognises."""
        assert _AGENT_PATH.name == "agdt.suppressed-comment-triage.evaluate.agent.md"
        assert _PROMPT_PATH.name == "agdt.suppressed-comment-triage.evaluate.prompt.md"

    def test_agent_declares_a_description(self) -> None:
        """The agent frontmatter carries the ``description`` used in the managed manifest."""
        frontmatter = _parse_frontmatter(_read(_AGENT_PATH))
        description = frontmatter.get("description")
        assert isinstance(description, str) and description.strip()

    def test_prompt_binds_to_the_agent(self) -> None:
        """The prompt frontmatter names the agent it belongs to."""
        frontmatter = _parse_frontmatter(_read(_PROMPT_PATH))
        assert frontmatter.get("agent") == "agdt.suppressed-comment-triage.evaluate"

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH])
    def test_no_platform_classification_keys(self, path: Path) -> None:
        """Neither file is platform-scoped.

        A classification that does not match the resolved platform makes ``agdt-setup``
        prune the file from the source set, which then **deletes** it from the target
        repository rather than leaving it in place.
        """
        assert "agdt" not in _parse_frontmatter(_read(path))


class TestContractTokensArePresent:
    """The output-contract vocabulary is stated in every artifact that needs it."""

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_sentinel_is_documented(self, path: Path) -> None:
        """The no-change sentinel appears verbatim."""
        assert _SENTINEL in _read(path)

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_markers_are_documented(self, path: Path) -> None:
        """Both the input (issue-side) and output (PR-side) markers appear."""
        text = _read(path)
        assert "ai-pr-loop:suppressed-comment-deferral" in text
        assert "agdt:suppressed-eval:no-changes-needed" in text

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_full_verdict_vocabulary_is_documented(self, path: Path) -> None:
        """Every verdict token is named, so no shape is left to interpretation."""
        text = _read(path)
        missing = sorted(verdict for verdict in _VERDICTS if f"`{verdict}`" not in text)
        assert not missing, f"{path.name} omits verdict(s): {missing}"

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_no_change_requires_per_finding_justification(self, path: Path) -> None:
        """The table header — the per-finding justification — is stated verbatim."""
        assert "| # | Location | Verdict | Justification |" in _read(path)


class TestPublishedRegexesMatchDocumentedExamples:
    """The reaper's published patterns accept the output the agent is told to emit."""

    def test_expected_patterns_are_published(self) -> None:
        """All four reaper patterns are present in the contract."""
        assert set(_published_patterns()) == {
            "SENTINEL_RE",
            "MARKER_RE",
            "DEFERRAL_MARKER_RE",
            "ROW_RE",
        }

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_sentinel_regex_matches_the_documented_sentinel_line(self, path: Path) -> None:
        """``SENTINEL_RE`` matches the sentinel exactly where it is shown on its own line."""
        assert _published_patterns()["SENTINEL_RE"].search(_read(path))

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_marker_regex_captures_the_deferral_issue_number(self, path: Path) -> None:
        """``MARKER_RE`` matches the anchored marker and captures review-id and deferred-issue."""
        match = _published_patterns()["MARKER_RE"].search(_read(path))
        assert match is not None
        assert match.group(1).isdigit()
        assert match.group(2).isdigit()

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_deferral_marker_regex_yields_the_documented_payload(self, path: Path) -> None:
        """``DEFERRAL_MARKER_RE`` matches the issue-side marker and its JSON parses."""
        match = _published_patterns()["DEFERRAL_MARKER_RE"].search(_read(path))
        assert match is not None
        payload = json.loads(match.group(1))
        assert set(payload) == {"pr", "review_id", "base_sha", "finding_count"}
        assert isinstance(payload["finding_count"], int)

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_row_regex_parses_every_example_row(self, path: Path) -> None:
        """``ROW_RE`` reads the example rows and skips header/separator rows."""
        rows = _published_patterns()["ROW_RE"].findall(_read(path))
        assert rows, f"{path.name} shows no parseable verdict rows"
        for index, (number, location, verdict, justification) in enumerate(rows, start=1):
            assert number.isdigit()
            assert verdict in _VERDICTS
            assert justification.strip()
            # A ``stale`` verdict is the only one allowed to omit a resolvable citation.
            # Every other row cites a colon-free repo-relative path plus a ``:line`` anchor.
            if verdict == "stale":
                assert location == "stale", f"row {index} in {path.name}: {location!r}"
            else:
                assert re.fullmatch(r"[^`:]+:\d+", location), f"row {index} in {path.name}: {location!r}"

    @pytest.mark.parametrize("path", [_AGENT_PATH, _PROMPT_PATH, _CONTRACT_PATH])
    def test_example_rows_cover_the_full_documented_finding_range(self, path: Path) -> None:
        """Each documented marker section shows verdict rows for every finding number it declares."""
        text = _read(path)
        row_re = _published_patterns()["ROW_RE"]
        for section_start, section_end, finding_count in _documented_marker_sections(path):
            section = text[section_start:section_end]
            published_numbers = sorted({int(number) for number, _, _, _ in row_re.findall(section)})
            assert published_numbers == list(range(1, finding_count + 1))


class TestReaperImplementsThePublishedContract:
    """The reaper's compiled patterns and vocabulary must equal the published ones.

    The contract document is normative. If an implementation constant drifts from it, the
    reaper silently stops closing valid follow-up PRs, so the drift is asserted here rather
    than discovered as a growing backlog.
    """

    @pytest.mark.parametrize("name", ["SENTINEL_RE", "MARKER_RE", "DEFERRAL_MARKER_RE", "ROW_RE"])
    def test_module_regex_matches_the_contract(self, name: str) -> None:
        assert getattr(suppressed_reaper, name).pattern == _published_patterns()[name].pattern

    def test_verdict_vocabulary_matches_the_contract(self) -> None:
        assert set(suppressed_reaper.VERDICTS) == _VERDICTS

    def test_blocking_verdicts_are_a_subset_of_the_vocabulary(self) -> None:
        assert suppressed_reaper.BLOCKING_VERDICTS <= _VERDICTS

    def test_agent_author_is_documented(self) -> None:
        assert suppressed_reaper.COPILOT_AGENT_AUTHOR in _read(_CONTRACT_PATH)
