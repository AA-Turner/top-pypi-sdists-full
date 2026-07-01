"""Headless execution mode for ``dn --print``."""

import os
import sys
import typing as t

from loguru import logger

from dreadnode.app.client.managed_client import ManagedRuntimeClient
from dreadnode.app.client.runtime_client import DEFAULT_MODEL
from dreadnode.app.tui import wire_events as we
from dreadnode.app.tui.wire_events import parse_wire_event


async def run_print_mode(
    prompt: str,
    *,
    model: str | None = None,
    agent: str | None = None,
    capabilities_dirs: list[str] | None = None,
    capabilities: list[str] | None = None,
    capability_flags: list[str] | None = None,
    system_prompt: str | None = None,
    server_url: str | None = None,
    platform_url: str | None = None,
) -> None:
    """Run a single prompt headlessly: stream response text to stdout, progress to stderr."""

    # Resolve model: explicit flag > profile default > hardcoded default
    if model is None:
        model = _resolve_default_model(platform_url)

    client = ManagedRuntimeClient(
        server_url=server_url,
        auto_start=server_url is None,
        capability_dirs=capabilities_dirs,
        enabled_capabilities=capabilities,
        capability_flag_overrides=capability_flags,
        system_prompt_append=system_prompt,
    )

    # Load platform profile if available
    _apply_platform_profile(client, platform_url)

    # Suppress noisy library output (litellm ANSI errors, etc.) from stdout/stderr
    # by redirecting litellm's output during the run.
    _suppress_library_noise()

    # Print mode is a single-shot, non-interactive run: there's no UI to surface
    # a still-connecting MCP server and no later turn where late-arriving tools
    # would appear. Default to synchronous startup so the one agent turn sees the
    # full toolset rather than racing background MCP connects (CAP-MCP-009). An
    # explicit DREADNODE_SYNCHRONOUS_STARTUP in the environment still wins.
    os.environ.setdefault("DREADNODE_SYNCHRONOUS_STARTUP", "1")

    await client.start()

    # Validate --agent and --capability against loaded runtime
    runtime = await client.fetch_runtime_info()
    _validate_runtime_args(runtime, agent=agent, capabilities=capabilities)

    session = await client.create_session(agent=agent, model=model, policy="headless")
    session_id = session.session_id

    try:
        async for raw_event in client.stream_chat(
            session_id=session_id,
            message=prompt,
            model=model,
            agent=agent,
        ):
            event = parse_wire_event(raw_event)
            if event is None:
                continue
            done = await _handle_event(event, client, session_id)
            if done:
                break
    except KeyboardInterrupt:
        raise SystemExit(130) from None
    finally:
        # Final newline to ensure clean stdout
        sys.stdout.write("\n")
        sys.stdout.flush()
        await client.close()


async def _handle_event(
    event: we.WireEvent,
    client: ManagedRuntimeClient,  # noqa: ARG001 — kept for symmetry with future event handlers
    session_id: str,  # noqa: ARG001
) -> bool:
    """Process a single typed wire event. Returns True when the turn is done."""
    if isinstance(event, we.GenerationStep):
        if event.data.content:
            sys.stdout.write(event.data.content)
            sys.stdout.flush()
        return False

    if isinstance(event, we.GenerationError):
        # Domain error surfaced from the event stream — not a type mismatch.
        raise RuntimeError(event.data.error or "Generation error")  # noqa: TRY004

    if isinstance(event, we.UserInputRequired):
        prompt = event.data
        first_question = prompt.questions[0].prompt if prompt.questions else ""
        raise RuntimeError(  # noqa: TRY004 — interactive input is a control-flow signal, not a type error
            f"Interactive input required in headless mode: {first_question}"
        )

    if isinstance(event, we.AgentEnd):
        return True

    if isinstance(event, we.RuntimeErrorEvent):
        _error(event.error or "unknown error")
        return True

    return False


def _error(message: str) -> None:
    """Write an error message to stderr."""
    sys.stderr.write(f"error: {message}\n")
    sys.stderr.flush()


def _suppress_library_noise() -> None:
    """Suppress noisy library output that leaks to stdout/stderr.

    litellm in particular prints ANSI-colored error messages directly
    to stdout, which corrupts piped output.
    """
    os.environ.setdefault("LITELLM_LOG", "ERROR")
    os.environ.setdefault("LITELLM_SUPPRESS_DEBUG_INFO", "1")


def _apply_platform_profile(
    client: ManagedRuntimeClient,
    platform_url: str | None,
) -> None:
    """Load and apply the platform profile to the client."""
    try:
        from dreadnode.app.config import Profile, UserConfig, urls_match

        config = UserConfig.read()

        if platform_url:
            # Find profile matching the override URL
            for profile in config.servers.values():
                if urls_match(profile.url, platform_url):
                    client.set_platform_profile(profile)
                    return
            # No matching profile — create a minimal one
            client.set_platform_profile(
                Profile(url=platform_url, api_key=None, default_organization=None)
            )
        elif config.active and config.active in config.servers:
            client.set_platform_profile(config.servers[config.active])
    except Exception:
        logger.debug("Could not load platform profile", exc_info=True)


def _validate_runtime_args(
    runtime: t.Any,
    *,
    agent: str | None,
    capabilities: list[str] | None,
) -> None:
    """Validate CLI args against loaded runtime state. Exits on mismatch."""
    enabled = [c for c in runtime.capabilities if getattr(c, "enabled", True)]
    loaded_capabilities = {c.name for c in enabled}
    available_agents = {"default"} | {a.name for c in enabled for a in c.agents}

    # Check --capability values matched something that loaded
    if capabilities:
        missing = [c for c in capabilities if c not in loaded_capabilities]
        if missing:
            _error(f"unknown capability(ies): {', '.join(missing)}")
            if loaded_capabilities:
                _error(f"available: {', '.join(sorted(loaded_capabilities))}")
            else:
                _error("no capabilities are loaded")
            sys.exit(1)

    # Check --agent exists
    if agent and agent not in available_agents:
        _error(f"unknown agent: {agent}")
        _error(f"available: {', '.join(sorted(available_agents))}")
        sys.exit(1)


def _resolve_default_model(platform_url: str | None) -> str:
    """Resolve default model from profile, falling back to DEFAULT_MODEL."""
    if platform_url:
        return DEFAULT_MODEL
    try:
        from dreadnode.app.config import UserConfig

        config = UserConfig.read()
        if config.active and config.active in config.servers:
            profile = config.servers[config.active]
            if profile.default_model:
                return profile.default_model
    except Exception:
        logger.debug("Could not load profile for default model", exc_info=True)
    return DEFAULT_MODEL
