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
                "tkinter",
                "unittest",
                "PIL",
                "numpy",
                "pandas",
            ],
            "includes": [
                "anyio",
                "anyio._backends._asyncio",
                "typer",
                "runlayer_cli.aiwatch",
                "runlayer_cli.daemon",
                "runlayer_cli.daemon.runtime",
                "runlayer_cli.daemon.server",
                "runlayer_cli.daemon.status",
                "runlayer_cli.daemon.windows_scm",
                "runlayer_cli.daemon.windows_service",
                "runlayer_cli.daemon.windows_pipe",
                "runlayer_cli.hook.daemon_client",
                "runlayer_cli.hook.daemon_protocol",
                "runlayer_cli.commands.scan",
                "runlayer_cli.commands.auth",
                "runlayer_cli.commands.aiwatch_update",
                "runlayer_cli.commands.logs",
                "runlayer_cli.commands.org_api_key",
                "runlayer_cli.tls",
                "runlayer_cli.hook_install.daemon_lifecycle",
                "runlayer_cli.hook_install.presence",
                "runlayer_cli.scan",
                "runlayer_cli.scan.client_presence",
                "runlayer_cli.scan.clients",
                "runlayer_cli.scan.config_parser",
                "runlayer_cli.scan.container_command",
                "runlayer_cli.scan.containers",
                "runlayer_cli.scan.containers.collect",
                "runlayer_cli.scan.containers.docker_cli",
                "runlayer_cli.scan.containers.docker_socket",
                "runlayer_cli.scan.containers.inspect_parse",
                "runlayer_cli.scan.containers.k3s_cli",
                "runlayer_cli.scan.containers.proc_walk",
                "runlayer_cli.scan.containers.tar_walk",
                "runlayer_cli.scan.device",
                "runlayer_cli.scan.service",
                "runlayer_cli.scan.skill_scanner",
                "runlayer_cli.scan.windows_users",
                "runlayer_cli.scan.plugin_scanner",
                "runlayer_cli.scan.file_collector",
                "runlayer_cli.scan.project_scanner",
                "runlayer_cli.scan.resource_governor",
                "runlayer_cli.scan.skip_dirs",
                "runlayer_cli.scan.claude_code_plugins",
                "runlayer_cli.scan.codex_plugins",
                "runlayer_cli.scan.cursor_plugins",
                "runlayer_cli.scan.disguised_skills",
                "runlayer_cli.scan.jetbrains_plugins",
                "runlayer_cli.scan.opencode_plugins",
                "runlayer_cli.scan.vscode_extensions",
                "runlayer_cli.scan.agent_scan",
                "runlayer_cli.scan.agents",
                "runlayer_cli.scan.agents.languages",
                "runlayer_cli.scan.agents.discover",
                "runlayer_cli.scan.agents.manifests",
                "runlayer_cli.scan.agents.manifests._common",
                "runlayer_cli.scan.agents.manifests.python",
                "runlayer_cli.scan.agents.manifests.npm",
                "runlayer_cli.scan.agents.manifests.cargo",
                "runlayer_cli.scan.agents.manifests.go",
                "runlayer_cli.scan.agents.manifests.jvm",
                "runlayer_cli.scan.agents.manifests.dotnet",
                "runlayer_cli.scan.agents.registry",
                "runlayer_cli.scan.agents.detect",
                "runlayer_cli.scan.agents.report",
                "runlayer_cli.scan.agents.openclaw_detector",
                "runlayer_cli.scan.agents.install",
                "runlayer_cli.scan.agents.redact",
                "runlayer_cli.scan.processes",
                "runlayer_cli.scan.processes.models",
                "runlayer_cli.scan.processes.enumerate",
                "runlayer_cli.scan.processes.redact",
                "runlayer_cli.scan.processes.classify",
                "runlayer_cli.skill_identifier",
                "runlayer_cli.plugins.claude_manifest",
                "runlayer_cli.skills.discovery",
                "keyring.backends.Windows",
            ],
        }
    },
    # Ship the agent-detection registry next to the exe; scan.agents.registry
    # resolves it via an executable-relative path when frozen.
    data_files=[
        (
            "runlayer_cli/scan/agents",
            ["runlayer_cli/scan/agents/signatures.json"],
        )
    ],
    zipfile=None,
)
