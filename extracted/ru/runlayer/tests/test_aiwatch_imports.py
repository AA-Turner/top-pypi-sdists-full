"""Regression: ``aiwatch`` + ``aiwatch-hook`` closures must not import bundle-excluded modules.

Spawns a subprocess with each excluded module blocked at import and asserts
``runlayer_cli.aiwatch`` + the hook closure still load. ``_BLOCKED_TOPLEVEL``
must stay in sync with ``excludes=`` in ``cli/packaging/aiwatch.spec``;
``test_blocked_list_matches_spec_excludes`` enforces this.
"""

from __future__ import annotations

import re
import subprocess
import sys
import textwrap
from pathlib import Path

CLI_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = CLI_ROOT / "packaging" / "aiwatch.spec"

# Modules PyInstaller excludes from the aiwatch bundle. Must match the
# `excludes=` list in `cli/packaging/aiwatch.spec` exactly.
#
# `python-dotenv` is the distribution name (not importable); the importable
# module is `dotenv`. Both appear in the spec for clarity, both stay here so
# the in-sync check is a literal equality.
_BLOCKED_TOPLEVEL = (
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
)


def _run_import_probe(import_stmt: str) -> subprocess.CompletedProcess[str]:
    """Spawn a fresh interpreter with blocked modules and run `import_stmt`.

    Blocker matches a name as blocked if `fullname == entry` or
    `fullname.startswith(entry + ".")`. This handles both top-level entries
    (`mcp` blocks `mcp.types`) and dotted entries that block only a subtree.
    """
    blocked = repr(_BLOCKED_TOPLEVEL)
    probe = textwrap.dedent(
        f"""
        import sys

        _BLOCKED = {blocked}

        def _is_blocked(fullname):
            for entry in _BLOCKED:
                if fullname == entry or fullname.startswith(entry + "."):
                    return True
            return False

        class _Blocker:
            def find_module(self, fullname, path=None):
                return self.find_spec(fullname, path)

            def find_spec(self, fullname, path=None, target=None):
                if _is_blocked(fullname):
                    raise ModuleNotFoundError(
                        f"blocked by aiwatch import probe: {{fullname}}"
                    )
                return None

        sys.meta_path.insert(0, _Blocker())

        {import_stmt}

        leaked = sorted(m for m in sys.modules if _is_blocked(m))
        if leaked:
            raise SystemExit("leaked: " + ",".join(leaked))
        """
    )
    return subprocess.run(
        [sys.executable, "-c", probe],
        cwd=CLI_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_blocked_list_matches_spec_excludes():
    """`_BLOCKED_TOPLEVEL` must equal `excludes=` in `packaging/aiwatch.spec`.

    Drift here means either the bundle ships modules we don't test for, or
    the test blocks modules that aren't actually excluded — both hide bugs.
    """
    spec_text = SPEC_PATH.read_text()
    match = re.search(r"excludes=\[(.*?)\]", spec_text, re.DOTALL)
    assert match, f"could not find `excludes=[...]` in {SPEC_PATH}"
    spec_excludes = tuple(re.findall(r'"([^"]+)"', match.group(1)))
    assert set(spec_excludes) == set(_BLOCKED_TOPLEVEL), (
        f"spec excludes vs test blocklist drift:\n"
        f"  only in spec: {sorted(set(spec_excludes) - set(_BLOCKED_TOPLEVEL))}\n"
        f"  only in test: {sorted(set(_BLOCKED_TOPLEVEL) - set(spec_excludes))}"
    )


def test_aiwatch_imports_without_mcp():
    result = _run_import_probe("import runlayer_cli.aiwatch")
    assert result.returncode == 0, (
        f"aiwatch import pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_scan_command_imports_without_mcp():
    result = _run_import_probe("import runlayer_cli.commands.scan")
    assert result.returncode == 0, (
        f"scan command import pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_api_module_imports_without_mcp():
    result = _run_import_probe("import runlayer_cli.api")
    assert result.returncode == 0, (
        f"api module import pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_hook_closure_imports_under_blocklist():
    """The merged ``aiwatch-hook`` closure must also import cleanly.

    Both ``aiwatch[.exe]`` and ``aiwatch-hook[.exe]`` share one
    PyInstaller Analysis; an import-time pull of a blocked module from any
    hook module would crash the hook exe at startup just like it would
    crash scan.
    """
    probe = "\n        ".join(
        [
            "import runlayer_cli.aiwatch",
            "import runlayer_cli.hook.dispatch",
            "import runlayer_cli.hook.relay",
            "import runlayer_cli.enrollment",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"hook closure pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_bootstrap_closure_imports_under_blocklist():
    """The ``aiwatch bootstrap`` closure must import cleanly under bundle excludes.

    ``aiwatch setup hooks install`` / ``aiwatch bootstrap`` is invoked by the
    macOS enroll LaunchAgent + bootstrap LaunchDaemon pair (user + root) and
    the Windows Intune Remediations pair (SYSTEM). An import-time
    pull of a blocked module (``questionary`` / ``json5`` / etc.) would crash
    the bundled exe at startup. ``hook_install`` is the slim re-implementation
    of the per-client write logic precisely so these paths stay clean.
    """
    probe = "\n        ".join(
        [
            "import runlayer_cli.commands.enroll",
            "import runlayer_cli.commands.aiwatch_setup",
            "import runlayer_cli.commands.bootstrap",
            "import runlayer_cli.hook_install",
            "import runlayer_cli.hook_install.clients",
            "import runlayer_cli.hook_install.check",
            "import runlayer_cli.hook_install.console_user",
            "import runlayer_cli.hook_install.paths",
            "import runlayer_cli.hook_install.tolerant_json",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"bootstrap closure pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_mdm_config_parses_plist_under_blocklist():
    """`mdm_config._read_macos` must parse a real plist under bundle exclusions.

    `mdm_config` calls `plistlib.load` at scan time on macOS to read the MDM
    Configuration Profile. `plistlib` uses `xml.parsers.expat` (not
    `xml.etree.ElementTree`), but the XML stdlib is fragile under aggressive
    PyInstaller `excludes=`. This probe exercises the real parse path with the
    same blocklist the bundle ships, so any future exclude that breaks the XML
    subsystem fails here instead of in production on a customer Mac.
    """
    # Indented to 8 spaces to match the surrounding block in
    # `_run_import_probe`'s textwrap.dedent template — newlines inside the
    # interpolated string would otherwise break dedent's common-prefix detection.
    probe = "\n        ".join(
        [
            "import tempfile, pathlib",
            "from runlayer_cli.mdm_config import _read_macos",
            (
                'plist = b\'<?xml version="1.0" encoding="UTF-8"?>'
                '<plist version="1.0"><dict>'
                "<key>Host</key><string>https://t.example.com</string>"
                "<key>OrgApiKey</key><string>rl_org_k</string>"
                "</dict></plist>'"
            ),
            "with tempfile.NamedTemporaryFile(suffix='.plist', delete=False) as f:",
            "    f.write(plist)",
            "    path = pathlib.Path(f.name)",
            "got = _read_macos((path,))",
            "assert got == {'host': 'https://t.example.com', 'org_api_key': 'rl_org_k'}, got",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"mdm_config plist parse failed under bundle blocklist:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
