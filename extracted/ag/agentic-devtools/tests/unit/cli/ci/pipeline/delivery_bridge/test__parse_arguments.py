"""Argument validation for the delivery bridge."""

import sys

import pytest

from agentic_devtools.cli.ci.pipeline.delivery_bridge import _parse_arguments

SHA = "aB" * 20
ARGS = ["--repository", "Owner-1/repo.name_2", "--pr-number", "42", "--head-sha", SHA]


def test_valid_arguments() -> None:
    args = _parse_arguments(ARGS)

    assert args.repository == "Owner-1/repo.name_2"
    assert args.pr_number == 42
    assert args.head_sha == SHA


def test_reads_process_arguments(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["delivery-bridge", *ARGS])

    assert _parse_arguments(None).pr_number == 42


@pytest.mark.parametrize(
    ("index", "value"),
    [
        (1, ""),
        (1, "owner"),
        (1, "/repo"),
        (1, "owner/"),
        (1, "owner/repo/extra"),
        (1, "owner/repo\n"),
        (1, "owner/repo name"),
        (1, "owner/répô"),
        (3, "0"),
        (3, "-1"),
        (3, "1.5"),
        (3, "abc"),
        (5, "a" * 39),
        (5, "a" * 41),
        (5, "g" * 40),
        (5, "a" * 40 + "\n"),
    ],
)
def test_rejects_invalid_values(index: int, value: str, capsys: pytest.CaptureFixture[str]) -> None:
    args = ARGS.copy()
    args[index] = value

    with pytest.raises(SystemExit) as exc:
        _parse_arguments(args)

    assert exc.value.code == 2
    assert "error:" in capsys.readouterr().err


@pytest.mark.parametrize("args", [[], ARGS[:2], ARGS[:4], [*ARGS, "--unexpected"]])
def test_requires_all_and_only_known_arguments(args: list[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        _parse_arguments(args)

    assert exc.value.code == 2
