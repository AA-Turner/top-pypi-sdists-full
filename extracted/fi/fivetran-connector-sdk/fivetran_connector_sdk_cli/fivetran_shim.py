"""Compatibility entrypoint for the ``fivetran`` console script."""


def main():
    """Run the unified CLI when installed; otherwise run the SDK CLI directly."""
    try:
        from fivetran_cli.cli import main as cli_main
    except ModuleNotFoundError as exc:
        if exc.name != "fivetran_cli":
            raise
        from fivetran_connector_sdk_cli.cli import main as cli_main

    return cli_main()


if __name__ == "__main__":
    # Running this file directly (for example from an IDE) always uses the SDK CLI, never the unified one.
    from fivetran_connector_sdk_cli.cli_commands import main as sdk_main

    sdk_main()
