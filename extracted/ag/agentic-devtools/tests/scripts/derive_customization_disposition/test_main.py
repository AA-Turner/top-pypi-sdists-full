"""Tests for main in derive_customization_disposition."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.scripts.derive_customization_disposition import REPO_ROOT, derive, row


def test_published_table_is_up_to_date() -> None:
    """The published table is generated; a stale one is a silent lie."""
    assert derive.main(["--check"]) == 0


def test_verify_partition_passes_against_the_published_table() -> None:
    """A later issue re-runs this instead of re-deriving the predicate."""
    assert derive.main(["--verify-partition"]) == 0


def test_verify_authored_passes_before_anything_is_authored() -> None:
    """Nothing authored yet means nothing unexpected, so the mode succeeds."""
    assert derive.main(["--verify-authored"]) == 0


def test_derive_writes_the_document(tmp_path: Path) -> None:
    """Regenerating to a fresh path reproduces the published document."""
    out = tmp_path / "map.md"
    assert derive.main(["--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == (REPO_ROOT / derive.PUBLISHED_PATH).read_text(encoding="utf-8")


def test_check_fails_when_the_table_is_stale(tmp_path: Path) -> None:
    """`--check` is what keeps the table and the corpus from drifting apart."""
    out = tmp_path / "map.md"
    out.write_text("# Stale\n", encoding="utf-8")
    assert derive.main(["--check", "--out", str(out)]) == 1


def test_check_fails_when_the_table_is_missing(tmp_path: Path) -> None:
    """A missing table cannot be up to date."""
    assert derive.main(["--check", "--out", str(tmp_path / "absent.md")]) == 1


def test_verify_partition_fails_when_the_table_is_missing(tmp_path: Path) -> None:
    """Verification never silently passes on an absent file."""
    assert derive.main(["--verify-partition", "--out", str(tmp_path / "absent.md")]) == 1


def test_verify_partition_fails_on_a_broken_table(tmp_path: Path) -> None:
    """A row carrying no batch is exactly the gap the partition rule forbids."""
    out = tmp_path / "map.md"
    out.write_text(
        f"{derive.ROWS_HEADING}\n| `.github/agents/agdt.a.agent.md` | `agdt.a` | delete | - | - | none |\n",
        encoding="utf-8",
    )
    assert derive.main(["--verify-partition", "--out", str(out)]) == 1


def test_verify_authored_fails_on_an_unexpected_unit(tmp_path: Path) -> None:
    """An authored skill the map does not expect fails the comparison."""
    skill = tmp_path / ".agents" / "skills" / "agdt-surprise"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# Surprise\n", encoding="utf-8")
    assert (
        derive.main(
            [
                "--verify-authored",
                "--repo-root",
                str(tmp_path),
                "--out",
                str(REPO_ROOT / derive.PUBLISHED_PATH),
            ]
        )
        == 1
    )


def test_verify_authored_fails_when_the_table_is_missing(tmp_path: Path) -> None:
    """Without the published table there is nothing to compare against."""
    assert derive.main(["--verify-authored", "--out", str(tmp_path / "absent.md")]) == 1


def test_verify_authored_kind_mismatch_is_reported_not_raised(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A kind mismatch returns exit code 1 instead of surfacing a traceback."""
    published = tmp_path / "map.md"
    table = derive.render_table([row(path=".github/prompts/agdt.example.prompt.md")])
    published.write_text(
        f"# Map\n\n{derive.ROWS_HEADING}\n{table}\n",
        encoding="utf-8",
    )
    agents = tmp_path / ".github" / "agents"
    agents.mkdir(parents=True)
    (agents / "agdt-example.agent.md").write_text("# Example\n", encoding="utf-8")
    assert derive.main(["--verify-authored", "--repo-root", str(tmp_path), "--out", str(published)]) == 1
    captured = capsys.readouterr()
    assert "expects a skill artifact" in captured.err


def test_verify_partition_passes_with_matching_expected_total() -> None:
    """--expected-total accepts a count matching the published table."""
    rows = derive.parse_table((REPO_ROOT / derive.PUBLISHED_PATH).read_text(encoding="utf-8"))
    assert derive.main(["--verify-partition", "--expected-total", str(len(rows))]) == 0


def test_verify_partition_fails_with_wrong_expected_total(tmp_path: Path) -> None:
    """--expected-total fails when the published table has a different row count."""
    # Write a minimal valid single-row table.
    out = tmp_path / "map.md"
    out.write_text(
        f"{derive.ROWS_HEADING}\n"
        "| `.github/agents/agdt.a.agent.md` | `agdt.a` | skill | singleton-a | `agdt-a` | residue |\n",
        encoding="utf-8",
    )
    # The table has 1 row but we claim 2.
    assert derive.main(["--verify-partition", "--out", str(out), "--expected-total", "2"]) == 1


def test_verify_partition_enforces_fixture_total_by_default(tmp_path: Path) -> None:
    """Bare --verify-partition without --expected-total uses the fixture-derived corpus count."""
    out = tmp_path / "map.md"
    out.write_text(
        f"{derive.ROWS_HEADING}\n"
        "| `.github/agents/agdt.a.agent.md` | `agdt.a` | skill | singleton-a | `agdt-a` | residue |\n",
        encoding="utf-8",
    )
    # The table has 1 valid row; without --expected-total the fixture count (266) is
    # used and the mismatch causes verification to fail.
    assert derive.main(["--verify-partition", "--out", str(out)]) == 1


def test_verify_partition_fails_when_fixture_is_missing_and_no_expected_total(tmp_path: Path) -> None:
    """When the fixture is absent and --expected-total is omitted, verification fails.

    This prevents the count check from being silently skipped.
    """
    assert (
        derive.main(
            [
                "--verify-partition",
                "--repo-root",
                str(tmp_path),
                "--out",
                str(REPO_ROOT / derive.PUBLISHED_PATH),
            ]
        )
        == 1
    )


def test_derivation_failure_is_reported_not_raised(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A broken derivation exits 1 with a message rather than a traceback."""
    monkeypatch.setattr(derive, "derive_rows", lambda _root: (_ for _ in ()).throw(ValueError("boom")))
    assert derive.main(["--out", str(tmp_path / "map.md")]) == 1


def test_runtime_derivation_failure_is_reported_not_raised(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A runtime derivation error exits 1 with a message rather than a traceback."""
    monkeypatch.setattr(derive, "derive_rows", lambda _root: (_ for _ in ()).throw(RuntimeError("boom")))
    assert derive.main(["--out", str(tmp_path / "map.md")]) == 1


def test_derive_fails_when_fixture_is_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Derivation fails when the expected fixture is absent from the repo root."""
    monkeypatch.setattr(
        derive,
        "derive_rows",
        lambda _root: [row(path=".github/agents/agdt.a.agent.md", slug="agdt.a", target="agdt-a", batch="residue")],
    )
    monkeypatch.setattr(derive, "count_files", lambda _root: (1, 0))
    monkeypatch.setattr(derive, "collisions", lambda _rows: {})
    monkeypatch.setattr(derive, "render_document", lambda _rows, _root: "# map\n")
    assert derive.main(["--repo-root", str(tmp_path), "--out", str(tmp_path / "map.md")]) == 1
