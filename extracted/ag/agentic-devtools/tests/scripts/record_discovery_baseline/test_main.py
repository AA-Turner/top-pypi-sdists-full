"""Tests for main in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline, build_repo


def test_writes_the_default_output_path(tmp_path, capsys):
    """Without --output the baseline lands at the documented default path."""
    repo = build_repo(tmp_path, prompts=["agdt.set.prompt.md"])
    assert baseline.main(["--repo-root", str(repo)]) == 0
    written = (repo / baseline.OUTPUT_PATH).read_text(encoding="utf-8")
    assert "| prompt | `/agdt.set` |" in written
    assert "Wrote 1 unit to" in capsys.readouterr().out


def test_writes_an_explicit_output_path(tmp_path):
    """--output redirects the document and creates missing parent directories."""
    repo = build_repo(tmp_path, agents=["agdt.set.agent.md"])
    output = tmp_path / "out" / "baseline.md"
    assert baseline.main(["--repo-root", str(repo), "--output", str(output)]) == 0
    assert "| agent | `agdt.set` |" in output.read_text(encoding="utf-8")


def test_check_mode_returns_zero_when_output_matches(tmp_path, capsys):
    """--check exits zero when the baseline file already matches generated content."""
    repo = build_repo(tmp_path, prompts=["agdt.set.prompt.md"])
    output = tmp_path / "out" / "baseline.md"
    assert baseline.main(["--repo-root", str(repo), "--output", str(output)]) == 0

    assert baseline.main(["--repo-root", str(repo), "--output", str(output), "--check"]) == 0
    assert "Baseline is up to date:" in capsys.readouterr().out


def test_check_mode_returns_nonzero_when_output_is_stale(tmp_path, capsys):
    """--check exits nonzero when units changed after the last write."""
    repo = build_repo(tmp_path, prompts=["agdt.set.prompt.md"])
    output = tmp_path / "out" / "baseline.md"
    assert baseline.main(["--repo-root", str(repo), "--output", str(output)]) == 0
    (repo / ".github/prompts/agdt.get.prompt.md").write_text("prompt", encoding="utf-8")

    assert baseline.main(["--repo-root", str(repo), "--output", str(output), "--check"]) == 1
    assert "Baseline is stale. Regenerate with:" in capsys.readouterr().out


def test_write_preserves_existing_footnotes_on_regeneration(tmp_path):
    """Regenerating an existing baseline retains its manually-added footnote entries."""
    repo = build_repo(tmp_path, prompts=["agdt.set.prompt.md"])
    output = tmp_path / "out" / "baseline.md"
    assert baseline.main(["--repo-root", str(repo), "--output", str(output)]) == 0

    note = "- /agdt.set — not offered by VS Code Copilot Chat."
    content = output.read_text(encoding="utf-8")
    content = content.replace("- None recorded.", note)
    output.write_text(content, encoding="utf-8")

    assert baseline.main(["--repo-root", str(repo), "--output", str(output)]) == 0
    assert note in output.read_text(encoding="utf-8")


def test_check_mode_accepts_baseline_with_custom_footnotes(tmp_path, capsys):
    """--check exits zero when the only difference from default is a custom footnote."""
    repo = build_repo(tmp_path, prompts=["agdt.set.prompt.md"])
    output = tmp_path / "out" / "baseline.md"
    assert baseline.main(["--repo-root", str(repo), "--output", str(output)]) == 0

    note = "- /agdt.set — not offered by VS Code Copilot Chat."
    content = output.read_text(encoding="utf-8")
    content = content.replace("- None recorded.", note)
    output.write_text(content, encoding="utf-8")

    assert baseline.main(["--repo-root", str(repo), "--output", str(output), "--check"]) == 0
    assert "Baseline is up to date:" in capsys.readouterr().out
