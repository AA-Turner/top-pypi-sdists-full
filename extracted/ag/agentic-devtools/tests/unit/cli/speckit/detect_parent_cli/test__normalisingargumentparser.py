"""Tests for detect_parent_cli._NormalisingArgumentParser."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.speckit.detect_parent_cli import _NormalisingArgumentParser


class TestNormalisingArgumentParser:
    """Tests for the argparse error normalisation subclass."""

    def test_error_exits_1_not_2(self, capsys):
        """error() exits with code 1, not argparse's default 2, and writes to stderr."""
        parser = _NormalisingArgumentParser()
        with pytest.raises(SystemExit) as exc_info:
            parser.error("something went wrong")
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "something went wrong" in captured.err

    def test_error_emits_status_error_line(self, capsys):
        """error() emits 'status=error' on stdout."""
        parser = _NormalisingArgumentParser()
        with pytest.raises(SystemExit):
            parser.error("something went wrong")
        captured = capsys.readouterr()
        assert "status=error" in captured.out
        assert "parent=null" in captured.out
        assert "level=null" in captured.out
        assert "title=null" in captured.out

    def test_error_emits_detail_on_stderr(self, capsys):
        """error() writes the error detail to stderr."""
        parser = _NormalisingArgumentParser()
        with pytest.raises(SystemExit):
            parser.error("missing required argument")
        captured = capsys.readouterr()
        assert "missing required argument" in captured.err
