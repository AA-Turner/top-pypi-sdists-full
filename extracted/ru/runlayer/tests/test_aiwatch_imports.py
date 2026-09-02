"""Regression: AI Watch closures respect bundle and hot-path import boundaries.

Spawns a subprocess with each excluded module blocked at import and asserts
``runlayer_cli.aiwatch`` + the hook closure still load. ``_BLOCKED_TOPLEVEL``
must stay in sync with ``excludes=`` in ``cli/packaging/aiwatch.spec``;
``test_blocked_list_matches_spec_excludes`` enforces this.
"""

from __future__ import annotations

import ast

from runlayer_cli import regex_safe
import subprocess
import sys
import textwrap
from pathlib import Path

from runlayer_cli import regex_safe

CLI_ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = CLI_ROOT / "packaging" / "aiwatch.spec"
PY2EXE_SETUP_PATH = CLI_ROOT / "packaging" / "py2exe" / "setup_py2exe.py"

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
    "tkinter",
    "unittest",
    "PIL",
    "numpy",
    "pandas",
)

_LAZY_DAEMON_IMPORTS = frozenset(
    {
        "anyio",
        "anyio._backends._asyncio",
        "typer",
        "runlayer_cli.daemon",
        "runlayer_cli.daemon.runtime",
        "runlayer_cli.daemon.server",
        "runlayer_cli.daemon.status",
        "runlayer_cli.daemon.windows_scm",
        "runlayer_cli.daemon.windows_service",
        "runlayer_cli.daemon.windows_pipe",
        "runlayer_cli.hook.daemon_client",
        "runlayer_cli.hook.daemon_protocol",
        "runlayer_cli.hook_install.daemon_lifecycle",
        "runlayer_cli.commands.aiwatch_update",
        "runlayer_cli.commands.auth",
        "runlayer_cli.commands.logs",
        "runlayer_cli.commands.org_api_key",
        "runlayer_cli.commands.scan",
        "runlayer_cli.tls",
    }
)


def _run_import_probe(
    import_stmt: str,
    blocked_modules: tuple[str, ...] = _BLOCKED_TOPLEVEL,
) -> subprocess.CompletedProcess[str]:
    """Spawn a fresh interpreter with blocked modules and run `import_stmt`.

    Blocker matches a name as blocked if `fullname == entry` or
    `fullname.startswith(entry + ".")`. This handles both top-level entries
    (`mcp` blocks `mcp.types`) and dotted entries that block only a subtree.
    """
    blocked = repr(blocked_modules)
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
    match = regex_safe.search(r"excludes=\[(.*?)\]", spec_text, regex_safe.DOTALL)
    assert match, f"could not find `excludes=[...]` in {SPEC_PATH}"
    spec_excludes = tuple(regex_safe.findall(r'"([^"]+)"', match.group(1)))
    assert set(spec_excludes) == set(_BLOCKED_TOPLEVEL), (
        f"spec excludes vs test blocklist drift:\n"
        f"  only in spec: {sorted(set(spec_excludes) - set(_BLOCKED_TOPLEVEL))}\n"
        f"  only in test: {sorted(set(_BLOCKED_TOPLEVEL) - set(spec_excludes))}"
    )


def _scan_module_imports(text: str) -> set[str]:
    """Every quoted ``runlayer_cli.scan...`` *module* path in a packaging file.

    Dotted only, so the ``runlayer_cli/scan/agents`` data-file destinations
    (slash-separated) never match — those are data, not importable modules.
    """
    return set(regex_safe.findall(r'"(runlayer_cli\.scan(?:\.[^"]+)?)"', text))


def test_py2exe_includes_cover_spec_scan_modules():
    """py2exe ``includes`` must list every ``runlayer_cli.scan.*`` module the
    PyInstaller spec ships as a hidden import.

    Both freezers enumerate the scan submodules explicitly (belt-and-suspenders;
    most are also transitively reachable). py2exe's modulefinder usually traces
    static imports, but drift here — spec gains ``scan.agent_scan`` /
    ``scan.skip_dirs`` but the py2exe setup doesn't — risks a frozen Windows
    py2exe bundle that can't find them at runtime.
    """
    spec_scan = _scan_module_imports(SPEC_PATH.read_text())
    py2exe_scan = _scan_module_imports(PY2EXE_SETUP_PATH.read_text())
    missing = spec_scan - py2exe_scan
    assert not missing, (
        f"py2exe setup ({PY2EXE_SETUP_PATH.name}) is missing scan modules the "
        f"PyInstaller spec ships:\n  {sorted(missing)}"
    )


def test_freezers_include_lazy_daemon_closure():
    for packaging_file in (SPEC_PATH, PY2EXE_SETUP_PATH):
        tree = ast.parse(packaging_file.read_text())
        configured = {
            node.value
            for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        }
        missing = _LAZY_DAEMON_IMPORTS - configured
        assert not missing, (
            f"{packaging_file.name} is missing lazy daemon imports: {sorted(missing)}"
        )


def test_aiwatch_imports_without_mcp():
    result = _run_import_probe("import runlayer_cli.aiwatch")
    assert result.returncode == 0, (
        f"aiwatch import pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_aiwatch_module_top_is_stdlib_only():
    result = _run_import_probe(
        "import runlayer_cli.aiwatch",
        ("typer", "httpx", "truststore", "anyio"),
    )
    assert result.returncode == 0, (
        f"aiwatch module top pulled in a hot-path dependency:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_daemon_served_hook_path_never_imports_typer_httpx_or_anyio():
    probe = "\n        ".join(
        [
            "import io, sys",
            "import runlayer_cli.aiwatch as aiwatch",
            "from runlayer_cli.hook import daemon_client",
            "daemon_client.daemon_is_enabled = lambda: True",
            (
                "daemon_client.try_daemon_hook = lambda _stdin, **_kwargs: "
                "{'stdout': '', 'stderr': '', 'exit_code': 0}"
            ),
            "sys.stdin = io.StringIO('{}')",
            "try:",
            "    aiwatch._run_hook_daemon_first()",
            "except SystemExit as exc:",
            "    assert exc.code == 0",
        ]
    )
    result = _run_import_probe(
        probe,
        ("typer", "httpx", "truststore", "anyio"),
    )
    assert result.returncode == 0, (
        f"daemon-served hook path pulled in a hot-path dependency:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_daemon_server_module_defers_anyio_import():
    result = _run_import_probe(
        "import runlayer_cli.daemon.server",
        ("anyio",),
    )
    assert result.returncode == 0, (
        f"daemon server imported anyio before run_daemon:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_windows_service_module_is_cross_platform_stdlib_only():
    result = _run_import_probe(
        "import runlayer_cli.daemon.windows_service",
        (
            "typer",
            "anyio",
            "win32api",
            "win32service",
            "win32serviceutil",
            "pywintypes",
        ),
    )
    assert result.returncode == 0, (
        f"Windows service module imported a forbidden dependency:\n"
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


def test_client_presence_imports_under_blocklist():
    result = _run_import_probe("import runlayer_cli.scan.client_presence")
    assert result.returncode == 0, (
        f"client presence probes pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_aiwatch_checkin_imports_under_blocklist():
    """``runlayer_cli.aiwatch_checkin`` is only lazily imported by scan/enroll.

    It is declared in ``hiddenimports`` so the onedir bundle ships it; this
    probe guards that its import closure (api / hook_install / mdm_config /
    scan.*) stays free of bundle-excluded modules.
    """
    result = _run_import_probe("import runlayer_cli.aiwatch_checkin")
    assert result.returncode == 0, (
        f"aiwatch_checkin import pulled in a blocked module:\n"
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


def test_container_command_imports_under_blocklist():
    """The Mode A container classifier must stay stdlib-only.

    ``config_parser`` imports it on every scan, so an import-time pull of the
    excluded ``docker`` SDK (or any other blocked module) here would crash the
    frozen aiwatch bundle. The classifier is deliberately subprocess-free and
    stdlib-only; this probe locks that in.
    """
    result = _run_import_probe("import runlayer_cli.scan.container_command")
    assert result.returncode == 0, (
        f"container_command import pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_container_scanner_imports_under_blocklist():
    """Mode B uses the CLI or stdlib socket client, never the excluded SDK."""
    result = _run_import_probe("import runlayer_cli.scan.containers")
    assert result.returncode == 0, (
        f"container scanner pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_command_metrics_closure_imports_under_blocklist():
    """Per-command perf telemetry must stay import-safe in the aiwatch bundle.

    ``aiwatch.py:main`` imports ``command_metrics`` on every non-hook
    invocation, and ``flow_contract`` (hook closure) imports
    ``command_contract`` for its envelope os/source detection. Both must load
    with only stdlib + httpx + structlog — httpx/config/api are deferred inside
    functions, so the top-level import closure stays clean under bundle
    excludes. ``command_metrics`` top-level imports ``logging`` (for
    ``ensure_base_logging_configured``), so its closure is guarded here too.
    """
    probe = "\n        ".join(
        [
            "import runlayer_cli.command_contract",
            "import runlayer_cli.command_metrics",
            "import runlayer_cli.logging",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"command-metrics closure pulled in a blocked module:\n"
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
            # Flow tracing modules are stdlib-only by contract (cli/AGENTS.md):
            # the hook closure loads them on every fire. `flow_contract` is
            # imported explicitly (not just transitively via flow_delivery /
            # flow_spool) so its `command_contract` dependency — the one
            # sanctioned non-flow sibling import — stays directly pinned.
            "import runlayer_cli.flow_trace",
            "import runlayer_cli.flow_contract",
            "import runlayer_cli.flow_delivery",
            "import runlayer_cli.flow_spool",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"hook closure pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_native_messaging_closure_imports_under_blocklist():
    """The Chrome native messaging host closure must import cleanly.

    Chrome launches the frozen aiwatch bundle through the
    ``aiwatch-native-messaging-host`` symlink, which conditionally imports
    ``runlayer_cli.native_messaging`` from ``aiwatch.py``. Keep that module in
    the PyInstaller hidden imports and free of excluded dependencies.
    """
    result = _run_import_probe("import runlayer_cli.native_messaging")
    assert result.returncode == 0, (
        f"native messaging closure pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_hook_dispatch_does_not_import_hook_install():
    """The blocking hook path must not pull in the MDM install stack.

    ``hook_install/__init__.py`` eagerly re-exports ``check`` / ``clients`` /
    ``paths`` / ``console_user`` / ``presence``, so importing *any* submodule --
    even a leaf like ``tolerant_json`` -- drags all of it into every ``aiwatch
    hook`` process. The blocklist probes above cannot catch that, because none of
    those modules is itself a blocked third-party dep. Asserted positively so a
    convenience import can't silently reintroduce the cost.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            textwrap.dedent(
                """
                import sys
                import runlayer_cli.hook.dispatch  # noqa: F401

                leaked = sorted(
                    name
                    for name in sys.modules
                    if name == "runlayer_cli.hook_install"
                    or name.startswith("runlayer_cli.hook_install.")
                )
                if leaked:
                    print("LEAKED:" + ",".join(leaked))
                    raise SystemExit(1)
                """
            ),
        ],
        capture_output=True,
        text=True,
        cwd=CLI_ROOT,
    )
    assert result.returncode == 0, (
        f"hook dispatch imported hook_install:\n{result.stdout}\n{result.stderr}"
    )


def test_bootstrap_closure_imports_under_blocklist():
    """The ``aiwatch bootstrap`` closure must import cleanly under bundle excludes.

    ``aiwatch setup hooks install`` / ``aiwatch bootstrap`` is invoked by the
    macOS enroll LaunchAgent + bootstrap LaunchDaemon pair (user + root) and
    the Windows AIWatchHooks scheduled task (SYSTEM). An import-time
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
            "import runlayer_cli.hook_install.presence",
            "import runlayer_cli.tolerant_json",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"bootstrap closure pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_agent_detection_closure_imports_under_blocklist():
    """The ``scan.agents`` engine must stay standard-library only.

    The static agent detector *and* the agent-report submission builder run on
    the scan path inside the frozen bundle. An import-time pull of a blocked
    module (``mcp`` / ``anyio`` / etc.) from any agents module would crash scan.
    The engine is intentionally stdlib-only (``json`` / ``re`` / ``ast`` /
    ``configparser`` / ``xml.etree`` / ``tomllib`` with a ``tomli`` fallback) and
    ``redact`` (the submission scrubber) adds only ``re`` + stdlib
    ``pathlib``/``runlayer_cli.paths``, so this probe locks that in.
    """
    probe = "\n        ".join(
        [
            "import runlayer_cli.scan.agents.languages",
            "import runlayer_cli.scan.agents.discover",
            # Package import pulls every per-ecosystem manifest parser submodule.
            "import runlayer_cli.scan.agents.manifests",
            "import runlayer_cli.scan.agents.registry",
            "import runlayer_cli.scan.agents.detect",
            "import runlayer_cli.scan.agents.report",
            "import runlayer_cli.scan.agents.openclaw_detector",
            "import runlayer_cli.scan.agents.install",
            # The redacted per-agent submission builder (ai-watch/agents) must
            # stay stdlib-only too -- it is on the scan/submit path in the bundle.
            "import runlayer_cli.scan.agents.redact",
            # Exercise the real registry load + a detection so the data-file
            # resolution and JSON parse run under the bundle blocklist too.
            "from runlayer_cli.scan.agents.detect import load_detector",
            "det = load_detector()",
            "assert det.frameworks, 'registry loaded no frameworks'",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"agent-detection closure pulled in a blocked module:\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


def test_process_discovery_closure_imports_under_blocklist():
    """The ``scan.processes`` runtime channel must stay standard-library only.

    PHASE 12 (``scan --detect-processes``) runs inside the frozen bundle: it
    enumerates the process table + listening sockets via ``subprocess``/``/proc``
    and scores/redacts the results. An import-time pull of a blocked module
    (``psutil`` is not even a dependency; ``mcp`` / ``anyio`` etc. must not leak
    in transitively) would crash scan. The channel is intentionally stdlib-only
    (``subprocess`` / ``os`` / ``pathlib`` / ``hashlib`` / ``urllib``) plus the
    stdlib-only ``scan.agents.redact`` + ``scan.agents.registry`` siblings, so
    this probe locks that in and exercises a real classify pass.
    """
    probe = "\n        ".join(
        [
            "import runlayer_cli.scan.processes",
            "import runlayer_cli.scan.processes.models",
            "import runlayer_cli.scan.processes.enumerate",
            "import runlayer_cli.scan.processes.redact",
            "import runlayer_cli.scan.processes.classify",
            # Exercise the scoring/redaction path (which lazily loads the agent
            # signature registry) so its data-file resolution + JSON parse run
            # under the bundle blocklist too.
            "from runlayer_cli.scan.processes.classify import (",
            "    ClassifierContext, classify_processes,",
            ")",
            "from runlayer_cli.scan.processes.models import ProcessCandidate",
            "ctx = ClassifierContext()",
            "cand = ProcessCandidate(",
            "    pid=1, argv=['npx', '-y', '@modelcontextprotocol/server-x'],",
            "    exe='npx',",
            ")",
            "out = classify_processes([cand], ctx)",
            "assert out and out[0].kind == 'mcp_server', out",
        ]
    )
    result = _run_import_probe(probe)
    assert result.returncode == 0, (
        f"process-discovery closure pulled in a blocked module:\n"
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
