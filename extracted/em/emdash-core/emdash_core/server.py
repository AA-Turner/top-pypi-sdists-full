"""FastAPI server entry point for emdash-core."""

import argparse
import os
import signal
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from .api import api_router
from .config import get_config, set_config


def _load_env_files(repo_root: Optional[str] = None):
    """Load .env files.

    Load order (later files override earlier):
    1. ~/.emdash/.env (user-level defaults)
    2. .emdash/.env in repo root (project-level)
    3. .env in repo root (project-level, legacy)
    """
    # Load user-level ~/.emdash/.env first (lower priority)
    user_env = Path.home() / ".emdash" / ".env"
    if user_env.exists():
        load_dotenv(user_env, override=True)

    # Load from repo root if provided (highest priority)
    if repo_root:
        root = Path(repo_root)
        # Project-level .emdash/.env
        project_env = root / ".emdash" / ".env"
        if project_env.exists():
            load_dotenv(project_env, override=True)
        # Legacy .env in repo root
        env_path = root / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=True)


def _shutdown_executors():
    """Shutdown all module-level thread pool executors and database connections."""
    from concurrent.futures import ThreadPoolExecutor

    # Import all modules with executors and shut them down
    executor_modules = [
        "emdash_core.api.index",
        "emdash_core.api.auth",
        "emdash_core.api.swarm",
        "emdash_core.api.tasks",
        "emdash_core.api.research",
        "emdash_core.api.spec",
        "emdash_core.api.team",
        "emdash_core.api.review",
        "emdash_core.api.agent",
        "emdash_core.api.projectmd",
        "emdash_core.agent.inprocess_subagent",
    ]

    for module_name in executor_modules:
        try:
            module = sys.modules.get(module_name)
            if module and hasattr(module, "_executor"):
                executor = getattr(module, "_executor")
                if executor and isinstance(executor, ThreadPoolExecutor):
                    executor.shutdown(wait=False)
        except Exception:
            pass  # Ignore errors during shutdown

    # Close database connections
    try:
        from .graph.connection import get_connection, _read_connection
        conn = get_connection()
        if conn:
            conn.close()
        if _read_connection:
            _read_connection.close()
    except Exception:
        pass  # Ignore errors during shutdown


def _prewarm_agent(config):
    """Pre-warm agent initialization during server startup.

    Runs the heavy parts of agent setup (module imports, provider creation,
    MCP tool discovery) so the first user message doesn't pay the cold-start cost.
    """
    import time

    start = time.monotonic()

    try:
        from .agent.providers.models import ModelRegistry

        registry = ModelRegistry.get()

        # Pre-warm: create default provider and warm up the HTTP connection pool.
        # The provider is cached in factory._provider_cache so the first message
        # reuses both the client object AND the established TCP/TLS connection.
        default_model = registry.default_model
        if default_model:
            try:
                from .agent.providers.factory import get_provider

                provider = get_provider(default_model)
                # Warm the httpx connection pool with a raw HEAD request to the
                # base URL. This establishes TCP + TLS without requiring a valid
                # API endpoint (works with custom proxies like Wix).
                try:
                    base_url = str(provider.client.base_url).rstrip("/")
                    provider.client._client.head(base_url, timeout=5)
                except Exception:
                    pass  # TCP+TLS may still have been established
                print(f"  Pre-warmed provider + connection: {default_model}")
            except Exception as e:
                print(f"  Pre-warm provider skipped: {e}")

        # Pre-warm: populate MCP tool cache so first message loads from disk
        try:
            from .agent.mcp.manager import MCPServerManager
            from .agent.mcp.config import get_default_mcp_config_path

            repo_root = Path(config.repo_root) if config.repo_root else Path.cwd()
            mcp_config_path = get_default_mcp_config_path(repo_root)
            manager = MCPServerManager(config_path=mcp_config_path)
            manager.discover_tools()
            tool_count = len(manager._tool_registry)
            # Shut down servers if they were started for first-time discovery;
            # they'll restart lazily when MCP tools are actually called
            if manager._started:
                manager.shutdown_all()
            print(f"  Pre-warmed MCP tools: {tool_count} tools cached")
        except Exception as e:
            print(f"  Pre-warm MCP skipped: {e}")

        elapsed = time.monotonic() - start
        print(f"  Pre-warm completed in {elapsed:.2f}s")

    except Exception as e:
        elapsed = time.monotonic() - start
        print(f"  Pre-warm failed after {elapsed:.2f}s: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    config = get_config()

    # Startup
    print(f"EmDash Core starting on http://{config.host}:{config.port}")
    if config.repo_root:
        print(f"Repository root: {config.repo_root}")

    # Print model config path and contents
    try:
        from .agent.providers.models import ModelRegistry
        registry = ModelRegistry.get()
        print(f"Model config: {registry.config_path}")
        model_names = list(registry.models.keys())
        print(f"  Models ({len(model_names)}): {', '.join(model_names)}")
        if registry.default_model:
            print(f"  Default: {registry.default_model}")
    except Exception as e:
        print(f"Model config: failed to load ({e})")

    # Print loaded rules
    try:
        from .agent.rules import _get_global_rules_dir
        repo_root_path = Path(config.repo_root) if config.repo_root else Path.cwd()
        local_rules_dir = repo_root_path / ".emdash" / "rules"
        global_rules_dir = _get_global_rules_dir()
        global_rule_files = sorted(f.name for f in global_rules_dir.glob("*.md")) if global_rules_dir.exists() else []
        local_rule_files = sorted(f.name for f in local_rules_dir.glob("*.md")) if local_rules_dir.exists() else []
        all_rule_files = global_rule_files + local_rule_files
        if all_rule_files:
            print(f"Rules ({len(all_rule_files)}): {', '.join(all_rule_files)}")
        else:
            print("Rules: none")
    except Exception as e:
        print(f"Rules: failed to load ({e})")

    # Print loaded skills
    try:
        from .agent.skills import SkillRegistry
        skill_registry = SkillRegistry.get_instance()
        repo_root_path = Path(config.repo_root) if config.repo_root else Path.cwd()
        skills = skill_registry.load_skills(repo_root_path / ".emdash" / "skills")
        if skills:
            skill_names = sorted(skills.keys())
            print(f"Skills ({len(skill_names)}): {', '.join(skill_names)}")
        else:
            print("Skills: none")
    except Exception as e:
        print(f"Skills: failed to load ({e})")

    # Multiuser is lazily initialized on first /share or /join
    # Just check config to inform the user
    try:
        from .multiuser.config import is_multiuser_enabled, get_multiuser_config
        if is_multiuser_enabled():
            cfg = get_multiuser_config()
            print(f"Multiuser available (provider: {cfg.provider.value})")
        else:
            print("Multiuser disabled")
    except Exception as e:
        print(f"Multiuser config check: {e}")

    # Note: Port file management is handled by ServerManager (per-repo files)

    # Initialize channel router
    from .channels.router import ChannelRouter, set_channel_router
    emdash_dir = Path(config.repo_root) / ".emdash" if config.repo_root else Path.cwd() / ".emdash"
    router = ChannelRouter(emdash_dir)
    app.state.channel_router = router
    set_channel_router(router)

    # Auto-connect Telegram if configured (so automation can deliver)
    try:
        from .channels.telegram.config import get_config as get_tg_config
        tg_config = get_tg_config()
        if tg_config.is_configured():
            from .agent.tools.channel import start_telegram_channel
            result = await start_telegram_channel(
                server_url=f"http://{config.host}:{config.port}",
                agent_options={"agent_type": "open"},
            )
            if result.get("error"):
                print(f"Telegram auto-connect failed: {result['error']}")
            else:
                print(f"Telegram auto-connected (@{result.get('bot_username', '?')})")
    except Exception as e:
        print(f"Telegram auto-connect skipped: {e}")

    # Initialize automation manager (cron, heartbeat, webhooks)
    from .automation.manager import AutomationManager, set_automation_manager, get_automation_manager
    automation_mgr = AutomationManager(emdash_dir)
    set_automation_manager(automation_mgr)
    await automation_mgr.start(f"http://{config.host}:{config.port}")

    # Pre-warm agent components in background so health endpoint responds immediately
    import threading
    threading.Thread(target=_prewarm_agent, args=(config,), daemon=True).start()

    yield

    # Shutdown
    automation_mgr = get_automation_manager()
    if automation_mgr:
        await automation_mgr.stop()

    print("EmDash Core shutting down...")
    _shutdown_executors()


def create_app(
    repo_root: Optional[str] = None,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    # Load environment variables from .env files
    _load_env_files(repo_root)

    # Export repo_root so ModelRegistry can find project-level config.json
    # (without importing config module, which would cause circular imports)
    if repo_root:
        resolved_repo_root = str(Path(repo_root).resolve())
        os.environ["EMDASH_REPO_ROOT"] = resolved_repo_root
        # Align process cwd with the target repo so all cwd-based lookups
        # (model config, rules, skills, local .emdash assets) resolve correctly.
        try:
            os.chdir(resolved_repo_root)
        except OSError as e:
            print(f"Warning: could not set working directory to {resolved_repo_root}: {e}")

    # Reset ModelRegistry — top-level imports (api → workflows → factory) may have
    # already initialized the singleton before EMDASH_REPO_ROOT was set, loading
    # the built-in fallback instead of the project's config.json.
    from .agent.providers.models import ModelRegistry
    ModelRegistry.reset()

    # Set configuration
    set_config(
        host=host,
        port=port,
        repo_root=repo_root,
    )

    app = FastAPI(
        title="EmDash Core",
        description="FastAPI server for code intelligence",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS middleware for Electron app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for local development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(api_router)

    # Serve install script at /install.sh for: curl -fsSL https://emdash.dev/install.sh | bash
    @app.get("/install.sh")
    async def serve_install_script():
        """Serve the bash installer script."""
        install_path = Path("/app/install.sh")
        if not install_path.exists():
            # Local dev fallback
            install_path = Path(__file__).parent.parent.parent.parent / "scripts" / "install.sh"
        if install_path.exists():
            return PlainTextResponse(
                install_path.read_text(),
                media_type="text/plain",
            )
        return PlainTextResponse("#!/bin/bash\necho 'Install script not found'; exit 1", status_code=404)

    # Serve static files (React build or fallback)
    # Check Docker build location first, then local dev location
    static_dir = Path("/app/static")
    if not static_dir.exists():
        static_dir = Path(__file__).parent / "static"

    if static_dir.exists():
        # Serve static assets (js, css, images, etc.)
        app.mount("/assets", StaticFiles(directory=static_dir / "assets" if (static_dir / "assets").exists() else static_dir), name="assets")

        @app.get("/")
        async def serve_index():
            """Serve the React app."""
            return FileResponse(static_dir / "index.html")

        # Catch-all for client-side routing (must be after API routes)
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            """Serve React app for client-side routing."""
            # Check if it's a static file
            file_path = static_dir / full_path
            if file_path.exists() and file_path.is_file():
                return FileResponse(file_path)
            # Otherwise serve index.html for client-side routing
            return FileResponse(static_dir / "index.html")

    return app


def main():
    """Main entry point for the server."""
    parser = argparse.ArgumentParser(description="EmDash Core Server")
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port to bind to (default: 8765)"
    )
    parser.add_argument(
        "--repo-root",
        help="Repository root path"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )

    args = parser.parse_args()

    # Handle graceful shutdown
    def signal_handler(signum, frame):
        print("\nReceived shutdown signal...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create app
    app = create_app(
        repo_root=args.repo_root,
        host=args.host,
        port=args.port,
    )

    # Run server
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
