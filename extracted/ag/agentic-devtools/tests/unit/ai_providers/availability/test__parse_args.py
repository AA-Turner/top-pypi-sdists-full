import sys

import pytest

from agentic_devtools.ai_providers.availability import _parse_args


def test__parse_args_accepts_dry_run_and_publish_flags(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "availability.py",
            "--dry-run",
            "--publish",
            "--evidence-path",
            "tmp/evidence.json",
            "--doc-path",
            "tmp/adr.md",
        ],
    )

    args = _parse_args()

    assert args.dry_run is True
    assert args.publish is True
    assert args.evidence_path == "tmp/evidence.json"
    assert args.doc_path == "tmp/adr.md"


def test__parse_args_defaults_optional_paths_to_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["availability.py"])

    args = _parse_args()

    assert args.evidence_path is None
    assert args.doc_path is None
