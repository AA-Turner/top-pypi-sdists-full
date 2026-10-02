"""Modules both the SDK and the CLI need (plan 2.11, D29).

`probe.cli`'s package initializer imports the whole CLI (typer, questionary and
every command), so an SDK module that reached into `probe.cli` for one helper
paid for all of it at `import probe` time -- and, on an install without the CLI's
dependencies, would lose that helper silently behind the `except Exception`
every such call site wraps it in: no run lock (auto-update could land mid-run)
and no worker telemetry. What lives here imports nothing from `probe.cli`.

`probe.cli.run_lock` and `probe.cli.telemetry` remain importable: each is the
SAME module object as its counterpart here (not a copy), so a monkeypatch
through either name is seen by both.
"""
