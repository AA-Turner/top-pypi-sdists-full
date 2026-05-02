"""CLI entry point — Click command group."""

from __future__ import annotations

import click

from ghost_pc import __version__


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name="GhostPC")
@click.pass_context
def main(ctx: click.Context) -> None:
    """GhostPC — Control your Windows PC from WhatsApp with AI vision."""
    if ctx.invoked_subcommand is None:
        # Double-click behavior: setup if first run, start if configured
        from ghost_pc.config.schema import GhostConfig

        cfg = GhostConfig.load()
        if cfg.setup_completed:
            ctx.invoke(start)
        else:
            ctx.invoke(setup)


@main.command()
@click.option("--port", type=int, default=None, help="Stream port override.")
@click.option("--fps", type=int, default=None, help="Screen capture FPS override.")
@click.option("--log-level", type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]), default=None)
def start(port: int | None, fps: int | None, log_level: str | None) -> None:
    """Start the GhostPC agent."""
    from ghost_pc.cli.runner import run_agent

    run_agent(port=port, fps=fps, log_level=log_level)


@main.command()
@click.option("--no-gui", is_flag=True, default=False, help="Use terminal wizard instead of GUI.")
def setup(no_gui: bool) -> None:
    """Interactive setup wizard — configure API keys, WhatsApp, and more."""
    auto_start = False

    if no_gui:
        from ghost_pc.cli.wizard import run_wizard

        run_wizard()
    else:
        from ghost_pc.web.setup_server import run_setup_gui

        auto_start = run_setup_gui()

    if auto_start:
        from ghost_pc.cli.runner import run_agent

        run_agent()


@main.command()
def doctor() -> None:
    """Run health checks on your GhostPC installation."""
    from ghost_pc.cli.doctor import run_doctor

    run_doctor()


@main.command()
def status() -> None:
    """Show current configuration and connection state."""
    from ghost_pc.cli.status import show_status

    show_status()


@main.group()
def config() -> None:
    """Read and write config values."""


@config.command("get")
@click.argument("key")
def config_get(key: str) -> None:
    """Read a config value."""
    from ghost_pc.cli.config_cmd import get_config_value

    get_config_value(key)


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Write a config value."""
    from ghost_pc.cli.config_cmd import set_config_value

    set_config_value(key, value)


@config.command("path")
def config_path() -> None:
    """Print the config file path."""
    from ghost_pc.config.schema import CONFIG_PATH

    click.echo(CONFIG_PATH)


if __name__ == "__main__":
    main()
