"""Regression test: write_file warns when cli.py defines main() but __main__.py is absent.

Common model failure: writes cli.py with def main() + if __name__=="__main__" guard
but never creates __main__.py. Running `python -m pkg` produces no output.

Fix: _check_missing_main_module fires when writing a cli.py-style file into a package
dir that has __init__.py but lacks __main__.py.
"""
from __future__ import annotations

from pathlib import Path
import pytest

from drydock.core.tools.base import BaseToolState
from drydock.core.tools.builtins.write_file import (
    WriteFile,
    WriteFileArgs,
    WriteFileConfig,
    WriteFileResult,
)


def _make_tool(tmp_path: Path) -> WriteFile:
    config = WriteFileConfig(allowed_dirs=[str(tmp_path)])
    state = BaseToolState()
    return WriteFile(config=config, state=state)


async def _invoke(tool: WriteFile, path: str, content: str) -> WriteFileResult:
    args = WriteFileArgs(path=path, content=content, overwrite=True)
    results = []
    async for event in tool.run(args, None):
        if isinstance(event, WriteFileResult):
            results.append(event)
    assert results, "expected a WriteFileResult"
    return results[-1]


CLI_WITH_MAIN = """\
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument("n", type=int)
    args = p.parse_args()
    print(args.n)

if __name__ == "__main__":
    main()
"""


@pytest.mark.asyncio
async def test_warns_when_no_main_module(tmp_path: Path) -> None:
    """Writing cli.py with main() into a package without __main__.py triggers warning."""
    tool = _make_tool(tmp_path)
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")

    r = await _invoke(tool, str(pkg / "cli.py"), CLI_WITH_MAIN)
    msg = r.content or ""
    assert "__main__.py" in msg, (
        f"Expected missing __main__.py warning, got: {msg!r}"
    )
    assert "main()" in msg or "main" in msg, (
        f"Expected main() call suggestion in warning, got: {msg!r}"
    )


@pytest.mark.asyncio
async def test_no_warning_when_main_module_exists(tmp_path: Path) -> None:
    """No warning when __main__.py already exists alongside cli.py."""
    tool = _make_tool(tmp_path)
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    (pkg / "__main__.py").write_text("from mypkg.cli import main\nmain()\n")

    r = await _invoke(tool, str(pkg / "cli.py"), CLI_WITH_MAIN)
    msg = r.content or ""
    assert "MISSING __main__.py" not in msg, (
        f"Should not warn when __main__.py exists, got: {msg!r}"
    )


@pytest.mark.asyncio
async def test_no_warning_outside_package(tmp_path: Path) -> None:
    """No warning for a standalone script (no __init__.py in parent dir)."""
    tool = _make_tool(tmp_path)
    scripts = tmp_path / "scripts"
    scripts.mkdir()

    r = await _invoke(tool, str(scripts / "cli.py"), CLI_WITH_MAIN)
    msg = r.content or ""
    assert "MISSING __main__.py" not in msg, (
        f"Should not warn for standalone scripts, got: {msg!r}"
    )


@pytest.mark.asyncio
async def test_no_warning_for_main_module_itself(tmp_path: Path) -> None:
    """No recursive warning when writing __main__.py itself."""
    tool = _make_tool(tmp_path)
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")

    content = "from mypkg.cli import main\nif __name__ == '__main__':\n    main()\n"
    r = await _invoke(tool, str(pkg / "__main__.py"), content)
    msg = r.content or ""
    assert "MISSING __main__.py" not in msg, (
        f"Should not warn when writing __main__.py itself, got: {msg!r}"
    )
