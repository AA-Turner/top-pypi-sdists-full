import typer
import sys
import importlib.util
from pathlib import Path
from .cli import auth
import asyncio
from .mcp_server.main import main as mcp_main

app = typer.Typer(help="Vibe automation CLI")

# Add 'auth' group
app.add_typer(auth.app, name="auth", help="Authentication commands")


@app.command()
def run(
    file: Path = typer.Argument(
        ..., exists=True, file_okay=True, dir_okay=False, help="Python file to execute"
    ),
):
    """
    Run the main method from the given Python file.

    This command loads a Python file and executes its main() function.
    The file must contain a callable main() function.

    Examples:
        va run script.py
        va run examples/workflow.py
        va run /path/to/automation.py

    Alternative invocation:
        python -m va run script.py
    """
    # Check if file is a Python file
    if file.suffix != ".py":
        typer.echo(f"Error: File '{file}' is not a Python file", err=True)
        raise typer.Exit(1)

    try:
        # Load the module from the file
        module_name = file.stem  # Use filename without extension as module name
        spec = importlib.util.spec_from_file_location(module_name, file)
        if spec is None or spec.loader is None:
            typer.echo(f"Error: Could not load module from '{file}'", err=True)
            raise typer.Exit(1)

        module = importlib.util.module_from_spec(spec)

        # Add the file's directory to sys.path so relative imports work
        file_dir = str(file.parent.absolute())
        if file_dir not in sys.path:
            sys.path.insert(0, file_dir)

        try:
            # Execute the module
            spec.loader.exec_module(module)

            # Check if module has a main function
            if hasattr(module, "main") and callable(module.main):
                # Support both sync and async main functions

                if asyncio.iscoroutinefunction(module.main):
                    # Run async main using asyncio.run
                    asyncio.run(module.main())
                else:
                    # Call synchronous main directly
                    module.main()

            else:
                typer.echo(
                    f"Error: No callable 'main' function found in '{file}'", err=True
                )
                raise typer.Exit(1)

        finally:
            # Clean up sys.path
            if file_dir in sys.path:
                sys.path.remove(file_dir)

    except Exception as e:
        typer.echo(f"Error executing '{file}': {e}", err=True)
        raise typer.Exit(1)


@app.command()
def mcp(
    mode: str = typer.Option(
        "full",
        "--mode",
        help="Server mode: 'full' (all tools) or 'vision-html' (limited tools for vision-based HTML inspection)",
    ),
):
    """
    Start the MCP (Model Context Protocol) server for web automation.

    This command starts the MCP server which provides web automation tools
    that can be used by MCP clients like Claude Desktop.

    Examples:
        va mcp
        va mcp --mode=vision-html
        uv run va mcp --mode=vision-html
    """
    typer.echo(f"Starting MCP Web Automation Server in {mode} mode...")
    asyncio.run(mcp_main(mode))


def main():
    app()


if __name__ == "__main__":
    main()
