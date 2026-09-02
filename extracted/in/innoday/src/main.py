#!/usr/bin/env python3
"""
InnoDay Platform CLI
Main entry point for running the API server.

The browser pages under ``/ui`` are served by that same FastAPI app (see
``src/page_paths.py``) -- there is no separate UI process. A Gradio app used to
live behind a ``ui`` subcommand here; it was removed once the real server-rendered
pages landed, because two things called "the UI" is one too many.
"""

import argparse
import sys

import uvicorn

from src.env_loader import EnvironmentNotSetError, load_env

# Load environment variables (picks .env.local / .env.dev / .env based on ENVIRONMENT)
try:
    _env_file_loaded = load_env()
except EnvironmentNotSetError as e:
    print(f"❌ {e}", file=sys.stderr)
    sys.exit(1)


def run_api(args):
    """Launch the FastAPI server"""
    from src.api.app import app
    from src.banner import print_startup_banner

    app.state.port = args.port
    app.state.env_file = _env_file_loaded

    print_startup_banner("Connector", args.host, args.port)

    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="InnoDay Platform - AI-Powered Team Orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main api              # Run API server (Connector)
  python -m src.main api --reload     # Run with auto-reload
        """,
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Component to run", required=True
    )

    # API subcommand
    api_parser = subparsers.add_parser("api", help="Run the FastAPI server")
    api_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)"
    )
    api_parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind to (default: 8000)"
    )
    api_parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload for development"
    )
    api_parser.set_defaults(func=run_api)

    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
