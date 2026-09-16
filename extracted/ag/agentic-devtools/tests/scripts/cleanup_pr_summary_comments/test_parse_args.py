"""Unit tests for parse_args."""

from scripts.cleanup_pr_summary_comments import parse_args


def test_parse_args_defaults() -> None:
    args = parse_args([])
    assert args.prs == []
    assert args.dry_run is False


def test_parse_args_explicit_prs_and_flags() -> None:
    args = parse_args(["4182", "4162", "--repo", "owner/repo", "--dry-run"])
    assert args.prs == [4182, 4162]
    assert args.repo == "owner/repo"
    assert args.dry_run is True
