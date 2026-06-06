"""py2exe setup for AI Watch (Windows alternative to PyInstaller)."""

import re
from pathlib import Path

from distutils.core import setup

import py2exe  # noqa: F401


def _read_version() -> str:
    # Regex (not tomllib) to avoid a tomli dep on 3.10 and mirror
    # build_pkg.sh / build_msi.ps1's grep / Select-String approach.
    pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    match = re.search(r'^version = "([^"]+)"', pyproject.read_text(), re.MULTILINE)
    if not match:
        raise RuntimeError(f"Failed to read version from {pyproject}")
    return match.group(1)


setup(
    name="aiwatch",
    version=_read_version(),
    description="Runlayer AI Watch — scan-only CLI binary",
    console=[
        {
            "script": "runlayer_cli/aiwatch.py",
            "dest_base": "aiwatch",
        }
    ],
    options={
        "py2exe": {
            "bundle_files": 1,
            "compressed": True,
            "optimize": 2,
            "excludes": [
                "fastmcp",
                "docker",
                "mcp",
                "fakeredis",
                "questionary",
                "dotenv",
                "python-dotenv",
                "anyio",
                "tkinter",
                "unittest",
                "PIL",
                "numpy",
                "pandas",
            ],
            "includes": [
                "runlayer_cli.aiwatch",
                "runlayer_cli.commands.scan",
                "runlayer_cli.commands.auth",
                "runlayer_cli.commands.logs",
                "runlayer_cli.commands.org_api_key",
                "runlayer_cli.scan",
                "runlayer_cli.scan.clients",
                "runlayer_cli.scan.config_parser",
                "runlayer_cli.scan.device",
                "runlayer_cli.scan.service",
                "runlayer_cli.scan.skill_scanner",
                "runlayer_cli.scan.plugin_scanner",
                "runlayer_cli.scan.file_collector",
                "runlayer_cli.scan.project_scanner",
                "runlayer_cli.scan.claude_code_plugins",
                "runlayer_cli.scan.codex_plugins",
                "runlayer_cli.scan.cursor_plugins",
                "runlayer_cli.scan.opencode_plugins",
                "runlayer_cli.scan.openclaw_detector",
                "runlayer_cli.skill_identifier",
                "runlayer_cli.plugins.claude_manifest",
                "runlayer_cli.skills.discovery",
                "keyring.backends.Windows",
            ],
        }
    },
    zipfile=None,
)
