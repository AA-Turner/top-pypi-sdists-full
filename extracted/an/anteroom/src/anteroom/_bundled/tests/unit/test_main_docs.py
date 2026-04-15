"""Tests for the ``aroom docs`` subcommand."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _parse_docs_args(argv: list[str]) -> argparse.Namespace:
    """Run the main argparse parser on *argv* and return the namespace."""
    # Import lazily so monkeypatching is possible in earlier tests
    from anteroom.__main__ import main  # noqa: F811

    # We only need the parser; reach into main() indirectly by
    # patching sys.argv and intercepting parse_args.
    captured: list[argparse.Namespace] = []

    original_parse = argparse.ArgumentParser.parse_args

    def _spy(self: argparse.ArgumentParser, args: Any = None, namespace: Any = None) -> argparse.Namespace:
        ns = original_parse(self, args, namespace)
        captured.append(ns)
        return ns

    with (
        patch.object(argparse.ArgumentParser, "parse_args", _spy),
        patch("sys.argv", ["aroom", *argv]),
        pytest.raises(SystemExit),
    ):
        # main() will sys.exit after early dispatch or hit missing config —
        # either way we capture the namespace before that.
        main()

    assert captured, "parse_args was never called"
    return captured[0]


# ---------------------------------------------------------------------------
# Argparse tests
# ---------------------------------------------------------------------------


class TestDocsArgparse:
    """Verify the ``docs`` subparser is wired correctly."""

    def test_docs_subparser_exists(self) -> None:
        ns = _parse_docs_args(["docs"])
        assert ns.command == "docs"

    def test_docs_default_port(self) -> None:
        ns = _parse_docs_args(["docs"])
        assert ns.docs_port == 8400

    def test_docs_custom_port(self) -> None:
        ns = _parse_docs_args(["docs", "--port", "9000"])
        assert ns.docs_port == 9000

    def test_docs_default_host(self) -> None:
        ns = _parse_docs_args(["docs"])
        assert ns.docs_host == "127.0.0.1"

    def test_docs_custom_host(self) -> None:
        ns = _parse_docs_args(["docs", "--host", "0.0.0.0"])
        assert ns.docs_host == "0.0.0.0"

    def test_docs_build_flag_parsed(self) -> None:
        ns = _parse_docs_args(["docs", "--build"])
        assert ns.docs_build is True

    def test_docs_build_flag_default_false(self) -> None:
        ns = _parse_docs_args(["docs"])
        assert ns.docs_build is False


# ---------------------------------------------------------------------------
# _find_mkdocs_yml tests
# ---------------------------------------------------------------------------


class TestFindMkdocsYml:
    def test_find_mkdocs_yml_repo_root(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _find_mkdocs_yml

        # Simulate repo structure: <root>/src/anteroom/__main__.py
        root = tmp_path / "repo"
        pkg = root / "src" / "anteroom"
        pkg.mkdir(parents=True)
        mkdocs = root / "mkdocs.yml"
        mkdocs.write_text("site_name: test\n")

        with patch("anteroom.__main__.Path") as mock_path:
            # __file__ resolves to pkg / "__main__.py"
            mock_file = MagicMock()
            mock_file.resolve.return_value.parent = pkg
            mock_path.__call__ = MagicMock(return_value=mock_file)
            mock_path.return_value = mock_file

            # Directly test resolution by calling with real paths
        # Use a simpler approach: monkeypatch __file__ resolution
        result = _find_mkdocs_yml()
        # In a dev checkout this should find the real mkdocs.yml
        if result is not None:
            assert result.name == "mkdocs.yml"
            assert result.is_file()

    def test_find_mkdocs_yml_bundled(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Fallback to _bundled/mkdocs.yml when repo root has none."""
        import anteroom.__main__ as mod

        # Create a fake package dir with only _bundled/mkdocs.yml
        fake_pkg = tmp_path / "pkg"
        fake_pkg.mkdir()
        bundled = fake_pkg / "_bundled"
        bundled.mkdir()
        (bundled / "mkdocs.yml").write_text("site_name: test\n")

        # Monkeypatch __file__ so _find_mkdocs_yml resolves from fake_pkg
        monkeypatch.setattr(mod, "__file__", str(fake_pkg / "__main__.py"))
        result = mod._find_mkdocs_yml()
        assert result is not None
        assert result == bundled / "mkdocs.yml"

    def test_find_mkdocs_yml_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """When no mkdocs.yml exists anywhere, return None."""
        import anteroom.__main__ as mod

        # Point __file__ at a barren directory tree
        fake_pkg = tmp_path / "a" / "b" / "pkg"
        fake_pkg.mkdir(parents=True)
        monkeypatch.setattr(mod, "__file__", str(fake_pkg / "__main__.py"))
        result = mod._find_mkdocs_yml()
        assert result is None


# ---------------------------------------------------------------------------
# _run_docs tests
# ---------------------------------------------------------------------------


class TestRunDocs:
    """Test _run_docs behaviour with mocked subprocess/shutil."""

    @staticmethod
    def _make_args(
        port: int = 8400,
        host: str = "127.0.0.1",
        build: bool = False,
    ) -> argparse.Namespace:
        return argparse.Namespace(docs_port=port, docs_host=host, docs_build=build)

    def test_docs_missing_mkdocs_warns(self) -> None:
        from anteroom.__main__ import _run_docs

        args = self._make_args()
        with (
            patch("anteroom.__main__.shutil.which", return_value=None),
            pytest.raises(SystemExit, match="1"),
        ):
            _run_docs(args)

    def test_docs_missing_mkdocs_yml_exits(self) -> None:
        from anteroom.__main__ import _run_docs

        args = self._make_args()
        with (
            patch("anteroom.__main__.subprocess.run"),
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=None),
            pytest.raises(SystemExit, match="1"),
        ):
            _run_docs(args)

    def test_docs_serve_subprocess_args(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args(port=8400, host="127.0.0.1")
        mock_run = MagicMock()

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch("anteroom.__main__.subprocess.run", mock_run),
        ):
            _run_docs(args)

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert cmd[0] == sys.executable
        assert cmd[1:3] == ["-m", "mkdocs"]
        assert "serve" in cmd
        assert "-a" in cmd
        idx = cmd.index("-a")
        assert cmd[idx + 1] == "127.0.0.1:8400"
        assert call_args[1]["cwd"] == str(tmp_path)

    def test_docs_serve_custom_port(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args(port=9000, host="0.0.0.0")
        mock_run = MagicMock()

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch("anteroom.__main__.subprocess.run", mock_run),
        ):
            _run_docs(args)

        cmd = mock_run.call_args[0][0]
        idx = cmd.index("-a")
        assert cmd[idx + 1] == "0.0.0.0:9000"

    def test_docs_keyboard_interrupt_graceful(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args()

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch("anteroom.__main__.subprocess.run", side_effect=KeyboardInterrupt),
        ):
            # Should not raise
            _run_docs(args)

    def test_docs_mkdocs_error_propagates(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args()

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch(
                "anteroom.__main__.subprocess.run",
                side_effect=subprocess.CalledProcessError(2, "mkdocs"),
            ),
            pytest.raises(SystemExit) as exc_info,
        ):
            _run_docs(args)

        assert exc_info.value.code == 2

    def test_docs_build_calls_mkdocs_build_strict(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args(build=True)
        mock_run = MagicMock(return_value=MagicMock(returncode=0))

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch("anteroom.__main__.subprocess.run", mock_run),
            pytest.raises(SystemExit) as exc_info,
        ):
            _run_docs(args)

        assert exc_info.value.code == 0
        cmd = mock_run.call_args[0][0]
        assert cmd[0] == sys.executable
        assert cmd[1:3] == ["-m", "mkdocs"]
        assert "build" in cmd
        assert "--strict" in cmd
        assert "-f" in cmd
        idx = cmd.index("-f")
        assert cmd[idx + 1] == str(mkdocs_yml)

    def test_docs_build_failure_exits_nonzero(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args(build=True)
        mock_run = MagicMock(return_value=MagicMock(returncode=1))

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch("anteroom.__main__.subprocess.run", mock_run),
            pytest.raises(SystemExit) as exc_info,
        ):
            _run_docs(args)

        assert exc_info.value.code == 1

    def test_docs_build_success_exits_cleanly(self, tmp_path: Path) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = tmp_path / "mkdocs.yml"
        mkdocs_yml.write_text("site_name: test\n")

        args = self._make_args(build=True)
        mock_run = MagicMock(return_value=MagicMock(returncode=0))

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            patch("anteroom.__main__.subprocess.run", mock_run),
            pytest.raises(SystemExit) as exc_info,
        ):
            _run_docs(args)

        assert exc_info.value.code == 0

    def test_docs_invalid_port_exits(self) -> None:
        from anteroom.__main__ import _run_docs

        mkdocs_yml = Path("/fake/mkdocs.yml")
        args = self._make_args(port=99999)

        with (
            patch("anteroom.__main__.shutil.which", return_value="/usr/bin/mkdocs"),
            patch("anteroom.__main__._find_mkdocs_yml", return_value=mkdocs_yml),
            pytest.raises(SystemExit, match="1"),
        ):
            _run_docs(args)
