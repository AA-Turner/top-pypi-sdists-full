"""Tests for main in rederive_deferral_variants."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from tests.scripts.rederive_deferral_variants import (
    posted_body,
    record,
    rederive,
    round_,
    suppressed_body,
)


def _corpus(tmp_path: Path) -> Path:
    """Write a two-PR corpus: one SP-deferrable, one that must never defer."""
    deferrable = record(
        round_(review_id=1, body=suppressed_body("specs/1/spec.md", "specs/1/plan.md")),
        round_(review_id=2, body=posted_body(1), posted_paths=("specs/1/spec.md",)),
        number=1,
        changed_files=("specs/1/spec.md",),
    )
    executable = record(
        round_(review_id=3, body=suppressed_body("agentic_devtools/state.py")),
        round_(review_id=4, body=posted_body(1), posted_paths=("agentic_devtools/state.py",)),
        number=2,
        changed_files=("agentic_devtools/state.py",),
    )
    path = tmp_path / "corpus.jsonl"
    path.write_text(
        "\n".join(json.dumps(rederive.record_to_json(item)) for item in (deferrable, executable)) + "\n",
        encoding="utf-8",
    )
    return path


def test_analyze_renders_the_variant_table(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """The Markdown report carries a row for every variant."""
    assert rederive.main(["analyze", "--corpus", str(_corpus(tmp_path))]) == 0
    out = capsys.readouterr().out
    for variant in rederive.VARIANTS:
        assert f"| {variant} |" in out


def test_analyze_json_reports_sp_declining_the_executable_pull_request(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A fires on both PRs and loses an executable finding; SP fires on one and loses none."""
    assert rederive.main(["analyze", "--corpus", str(_corpus(tmp_path)), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    by_variant = {entry["variant"]: entry for entry in payload["variants"]}
    assert payload["totalPrs"] == 2
    assert payload["totalRounds"] == 4
    assert by_variant["A"]["prs"] == 2
    assert by_variant["A"]["executablePostedLost"] == 1
    assert by_variant["SP"]["prs"] == 1
    assert by_variant["SP"]["executablePostedLost"] == 0
    assert by_variant["SP"]["roundsSaved"] == 1


def test_analyze_reports_a_missing_corpus(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """A missing corpus is a non-zero exit with a message naming the path."""
    missing = tmp_path / "absent.jsonl"
    assert rederive.main(["analyze", "--corpus", str(missing)]) == 1
    assert str(missing) in capsys.readouterr().err


def test_fetch_writes_the_corpus_and_reports_the_count(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The fetch subcommand delegates to fetch_corpus and prints the record count."""
    out_path = tmp_path / "corpus.jsonl"
    with patch.object(rederive, "fetch_corpus", return_value=399) as fetch:
        exit_code = rederive.main(
            ["fetch", "--first-pr", "2875", "--last-pr", "3612", "--out", str(out_path)],
        )
    assert exit_code == 0
    assert fetch.call_args.args == ("swai-factory", "agentic-devtools", 2875, 3612, out_path)
    assert "Wrote 399 record(s)" in capsys.readouterr().out


def test_fetch_threads_the_merge_cutoff_through(tmp_path: Path) -> None:
    """--merged-before is forwarded to fetch_corpus so the corpus stays frozen."""
    out_path = tmp_path / "corpus.jsonl"
    with patch.object(rederive, "fetch_corpus", return_value=399) as fetch:
        rederive.main(
            [
                "fetch",
                "--first-pr",
                "2875",
                "--last-pr",
                "3612",
                "--out",
                str(out_path),
                "--merged-before",
                "2026-08-11T09:00:00Z",
            ],
        )
    assert fetch.call_args.kwargs == {"merged_before": "2026-08-11T09:00:00Z"}


def test_fetch_corpus_preserves_tmp_suffixed_destination_on_failure(tmp_path: Path) -> None:
    """A failing fetch must not clobber an existing destination that already ends in .tmp."""
    out_path = tmp_path / "corpus.tmp"
    out_path.write_text("existing corpus\n", encoding="utf-8")
    with (
        patch.object(rederive, "merged_numbers_in_range", return_value=[42]),
        patch.object(rederive, "_gh_json", side_effect=RuntimeError("boom")),
    ):
        with pytest.raises(RuntimeError, match="boom"):
            rederive.fetch_corpus("swai-factory", "agentic-devtools", 42, 42, out_path)
    assert out_path.read_text(encoding="utf-8") == "existing corpus\n"
