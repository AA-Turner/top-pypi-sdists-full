"""``runlayer_cli.main.cli`` pre-typer hook dispatch (mirrors ``aiwatch.main``).

``runlayer setup hooks --install`` now wires ``runlayer hook --client <name>``
into each AI client's hook config, so ``cli()`` must route the ``hook`` token
(and the transcript-stream worker sentinel) straight to the hook runtime before
the typer app loads. A regression here would send every hook fire through typer
and fail open, so assert the routing (not just exit codes).
"""

from __future__ import annotations

import subprocess
import sys

import runlayer_cli.main as main_module
from runlayer_cli.hook.relay import TRANSCRIPT_STREAM_WORKER_SENTINEL


def test_hook_subcommand_routes_to_run_hook(monkeypatch):
    called: dict[str, list[str] | None] = {"argv": None}

    def _fake_run_hook():
        called["argv"] = list(sys.argv)

    monkeypatch.setattr("runlayer_cli.hook.dispatch.run_hook", _fake_run_hook)
    monkeypatch.setattr(
        sys,
        "argv",
        ["runlayer", "hook", "--client", "cursor", "--no-enforcement"],
    )

    main_module.cli()

    # ``hook`` token stripped; the rest of argv is forwarded to run_hook.
    assert called["argv"] == ["runlayer", "--client", "cursor", "--no-enforcement"]


def test_sentinel_routes_to_transcript_stream_worker(monkeypatch):
    called: dict[str, list[str] | None] = {"argv": None}

    def _fake_worker_main():
        called["argv"] = list(sys.argv)

    monkeypatch.setattr(
        "runlayer_cli.hook._transcript_stream_worker.main", _fake_worker_main
    )
    monkeypatch.setattr(
        sys, "argv", ["runlayer", TRANSCRIPT_STREAM_WORKER_SENTINEL, "extra"]
    )

    main_module.cli()

    # Sentinel token stripped; the worker sees the remaining argv.
    assert called["argv"] == ["runlayer", "extra"]


def test_non_hook_argv_routes_to_typer_app(monkeypatch):
    ran = {"run_hook": False, "worker": False, "app": False}

    monkeypatch.setattr(
        "runlayer_cli.hook.dispatch.run_hook",
        lambda: ran.__setitem__("run_hook", True),
    )
    monkeypatch.setattr(
        "runlayer_cli.hook._transcript_stream_worker.main",
        lambda: ran.__setitem__("worker", True),
    )
    # ``app`` is a typer app; stub both it and the backwards-compat shim (which
    # reads ``app.registered_commands``) so the test stays a pure routing check.
    monkeypatch.setattr(main_module, "_ensure_backwards_compatibility", lambda: None)
    monkeypatch.setattr(main_module, "app", lambda: ran.__setitem__("app", True))
    monkeypatch.setattr(sys, "argv", ["runlayer", "scan"])

    main_module.cli()

    assert ran == {"run_hook": False, "worker": False, "app": True}


def test_main_does_not_eager_load_relay():
    """``runlayer run`` / ``runlayer scan`` must not import the hook relay chain.

    ``commands/hooks.py`` (registered on the typer app) used to import
    ``hook.relay`` at module load, so every ``runlayer`` invocation paid for
    ``relay`` + ``runlayer_sdk.hook_transport`` + ``hook.transcript_stream``.
    They are now lazy; run in a fresh interpreter (this pytest process already
    imports ``relay`` via the module-level import above).
    """
    code = (
        "import sys, runlayer_cli.main;"
        "bad=[m for m in ("
        "'runlayer_cli.hook.relay',"
        "'runlayer_sdk.hook_transport',"
        "'runlayer_cli.hook.transcript_stream',"
        ") if m in sys.modules];"
        "assert not bad, bad"
    )
    subprocess.run([sys.executable, "-c", code], check=True)
