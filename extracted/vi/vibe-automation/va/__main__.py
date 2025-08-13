import typer
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

from va.constants import VA_ENABLE_RECOVERY
from .cli import auth
import asyncio
from .skeleton import create_workflow_skeleton
from .mcp_server.main import main as mcp_main
from .code.loader import load_instrumented_module

load_dotenv()

app = typer.Typer(help="Vibe automation CLI")
app.add_typer(auth.app, name="auth", help="Authentication commands")


@app.command()
def run(
    file: Path = typer.Argument(
        ..., file_okay=True, dir_okay=False, help="Python file to execute"
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

    # Create the workflow file if not exist, which would ask users regarding the goal
    if not file.exists():
        create_workflow_skeleton(file)

    workflow_code = file.read_text()

    # Store the workflow code globally for recovery access
    os.environ["VA_WORKFLOW_CODE"] = workflow_code
    os.environ["VA_WORKFLOW_FILE"] = str(file)

    # Add the file's directory to sys.path so relative imports work
    file_dir = str(file.parent.absolute())
    if file_dir not in sys.path:
        sys.path.insert(0, file_dir)

    try:
        # load with instrumentation for exception trapping unless disabled
        if VA_ENABLE_RECOVERY:
            module = load_instrumented_module(file)
        else:
            # Load module normally without instrumentation
            import importlib.util

            spec = importlib.util.spec_from_file_location("__main__", file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        # Check if module has a main function
        if hasattr(module, "main") and callable(module.main):
            if asyncio.iscoroutinefunction(module.main):
                asyncio.run(module.main())
            else:
                module.main()

            # Print final workflow code (may include recovery modifications)
            typer.echo("\n✅ Workflow completed successfully!")
            final_code = os.environ.get("VA_FINAL_WORKFLOW_CODE", workflow_code)
            typer.echo(f"\n📄 Final workflow code:\n{final_code}")
        else:
            typer.echo(
                f"Error: No callable 'main' function found in '{file}'", err=True
            )
            raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error executing '{file}': {e}", err=True)
        raise typer.Exit(1)
    finally:
        # Clean up sys.path
        if file_dir in sys.path:
            sys.path.remove(file_dir)


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
