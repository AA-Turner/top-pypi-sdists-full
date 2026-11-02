from __future__ import annotations


def main() -> None:
    try:
        from mistralai.agents._cli_app import app  # noqa: PLC0415
    except ModuleNotFoundError as exc:
        if exc.name != "typer":
            raise
        raise SystemExit("The `agents` CLI requires the `cli` extra: install mistralai-agents[cli].") from exc

    try:
        app()
    except ValueError as exc:
        from mistralai.vibe_agents.sdk.app._unused_env import UnusedEnvironmentError  # noqa: PLC0415

        if not isinstance(exc, UnusedEnvironmentError):
            raise
        # Strict settings refuse on the first settings read, wherever a command does it.
        raise SystemExit(str(exc)) from exc
