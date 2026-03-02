"""Agent chat endpoint with SSE streaming."""

import asyncio
import json
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..config import get_config
from ..models.agent import AgentChatRequest, AgentMode, AgentType
from ..sse.stream import SSEHandler, EventType
from ..utils.logger import log
from ..checkpoint import CheckpointManager

router = APIRouter(prefix="/agent", tags=["agent"])

# Thread pool for running blocking agent code
_executor = ThreadPoolExecutor(max_workers=4)

# Active sessions (in-memory for now)
_sessions: dict[str, dict] = {}


def _read_checkpoints_enabled(repo_root: Path) -> bool:
    """Read checkpoint flag from project config.json.

    Source of truth: {repo_root}/.emdash/config.json -> settings.checkpoints_enabled.
    Defaults to True if unset or unreadable.
    """
    config_path = repo_root / ".emdash" / "config.json"
    if not config_path.exists():
        return True

    try:
        data = json.loads(config_path.read_text())
        value = data.get("settings", {}).get("checkpoints_enabled", True)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "on")
        return bool(value)
    except Exception as e:
        log.warning(f"Failed reading checkpoint setting from {config_path}: {e}; defaulting enabled")
        return True


def _get_github_token_from_request(request: Request) -> str | None:
    """Extract GitHub token from the user's auth session.

    Args:
        request: FastAPI request object

    Returns:
        GitHub access token or None if not authenticated
    """
    try:
        # Import the auth sessions from the GitHub auth module
        from .auth_github import _sessions as auth_sessions

        session_id = request.cookies.get("session_id")
        if session_id and session_id in auth_sessions:
            return auth_sessions[session_id].get("access_token")
    except Exception as e:
        log.debug(f"Could not get GitHub token from session: {e}")

    return None


def _configure_git_for_session(github_token: str) -> None:
    """Configure git credentials for the current session.

    This sets up git to use the GitHub token for authentication.
    Works by writing to ~/.netrc which git reads automatically.

    Args:
        github_token: GitHub access token
    """
    from pathlib import Path

    try:
        # Write credentials to ~/.netrc - git reads this automatically
        # This is more reliable than git credential approve in containers
        netrc_path = Path.home() / ".netrc"

        # Build the new netrc content
        # If file exists, remove any existing github.com entry
        existing_content = ""
        if netrc_path.exists():
            existing_content = netrc_path.read_text()

        # Filter out existing github.com entry
        lines = existing_content.split("\n")
        new_lines = []
        skip_until_machine = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("machine github.com"):
                skip_until_machine = True
                continue
            if skip_until_machine and stripped.startswith("machine "):
                skip_until_machine = False
            if not skip_until_machine:
                new_lines.append(line)

        # Add new GitHub entry with token
        github_entry = f"""
machine github.com
  login x-access-token
  password {github_token}
"""
        new_content = "\n".join(new_lines).strip() + github_entry

        # Write .netrc with restrictive permissions
        netrc_path.write_text(new_content)
        netrc_path.chmod(0o600)  # Required for .netrc security

        log.info("Git credentials written to ~/.netrc")

    except Exception as e:
        log.warning(f"Failed to write ~/.netrc: {e}")

    # Also set environment variables
    os.environ["GITHUB_TOKEN"] = github_token
    os.environ["GIT_TERMINAL_PROMPT"] = "0"

    # Create a GIT_ASKPASS script that returns the token
    # This is the most reliable method for containers
    try:
        askpass_script = Path.home() / ".git-askpass.sh"
        askpass_content = f'''#!/bin/sh
echo "{github_token}"
'''
        askpass_script.write_text(askpass_content)
        askpass_script.chmod(0o700)  # Make executable
        os.environ["GIT_ASKPASS"] = str(askpass_script)
        log.info(f"GIT_ASKPASS script created at {askpass_script}")
    except Exception as e:
        log.warning(f"Failed to create GIT_ASKPASS script: {e}")


def _get_agent_name(agent_type: str) -> str:
    """Get display name for agent type."""
    if agent_type == "coworker":
        return "Emdash Coworker"
    elif agent_type == "open":
        return "Emdash Open"
    else:
        return "Emdash Code"


def _save_conversation(agent, conv_path: Path):
    """Persist agent messages to disk.

    Saves the last 50 non-system messages to avoid unbounded growth.
    """
    try:
        conv_path.parent.mkdir(parents=True, exist_ok=True)
        messages = [m for m in agent._messages if m.get("role") != "system"]
        # Keep last 50 messages to avoid unbounded growth
        if len(messages) > 50:
            messages = messages[-50:]
        data = {
            "messages": messages,
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "message_count": len(messages),
        }
        conv_path.write_text(json.dumps(data, indent=2, default=str))
        log.info(f"Saved {len(messages)} messages to {conv_path}")
    except Exception as e:
        log.warning(f"Failed to save conversation: {e}")


def _ensure_emdash_importable():
    """Ensure the emdash_core package is importable.

    This is now a no-op since we use emdash_core directly.
    """
    pass  # emdash_core is already in the package


def _resolve_requested_model(request_model: str | None, sse_handler: SSEHandler | None = None) -> str:
    """Resolve the chat model from registry config, ignoring server env overrides.

    Resolution rules:
    - Use request model if it's configured in ModelRegistry.
    - Otherwise fall back to registry default_model.
    - Return canonical ``provider:model_name`` form.
    """
    from ..agent.providers.models import ModelRegistry

    registry = ModelRegistry.get()
    default_name = registry.default_model
    default_entry = registry.get_model(default_name) if default_name else None
    if not default_entry:
        raise ValueError(
            "No valid default_model configured in .emdash/config.json. "
            f"default_model={default_name!r} config_path={registry.config_path}"
        )

    requested = (request_model or "").strip()
    if requested:
        resolved = registry.get_model(requested)
        if resolved:
            return f"{resolved.provider}:{resolved.name}"
        if sse_handler:
            sse_handler.emit(EventType.WARNING, {
                "message": (
                    f"Model '{requested}' is not configured in {registry.config_path}. "
                    f"Falling back to '{default_name}'."
                ),
            })

    return f"{default_entry.provider}:{default_entry.name}"


def _run_agent_sync(
    message: str,
    model: str,
    max_iterations: int,
    sse_handler: SSEHandler,
    session_id: str,
    images: list = None,
    plan_mode: bool = False,
    history: list = None,
    use_worktree: bool = False,
    agent_type: str = "coding",
    personality: str = None,
    domain_context: str = None,
    github_token: str = None,
    cwd: str = None,
):
    """Run the agent synchronously (in thread pool).

    This function runs in a background thread and emits events
    to the SSE handler for streaming to the client.

    Args:
        message: User message/task
        model: LLM model to use
        max_iterations: Maximum agent iterations
        sse_handler: SSE handler for streaming events
        session_id: Session ID for conversation continuity
        images: Optional list of images for vision-capable models
        history: Optional list of previous messages to pre-populate conversation
        use_worktree: If True, creates a git worktree for isolated changes
        agent_type: Type of agent ('coding' or 'coworker')
        personality: Coworker personality style
        domain_context: Coworker domain context
        github_token: GitHub access token for git operations
    """
    # Set up GitHub credentials if token is available
    if github_token:
        _configure_git_for_session(github_token)
    # Set session context for ModeState isolation between concurrent sessions
    from ..agent.tools.modes import ModeState
    token = ModeState.set_session_context(session_id)

    try:
        _ensure_emdash_importable()

        # Import agent components from emdash_core
        from ..agent.events import AgentEventEmitter

        # Determine agent name based on type
        if agent_type == "coworker":
            agent_name = "Emdash Coworker"
        elif agent_type == "open":
            agent_name = "Emdash Open"
        else:
            agent_name = "Emdash Code"

        # Create an emitter that forwards to SSE handler
        class SSEBridgeHandler:
            """Bridges AgentEventEmitter to SSEHandler."""

            def __init__(self, sse_handler: SSEHandler):
                self._sse = sse_handler

            def handle(self, event):
                """Forward event to SSE handler."""
                self._sse.handle(event)

        # Create agent with event emitter
        emitter = AgentEventEmitter(agent_name=agent_name)
        emitter.add_handler(SSEBridgeHandler(sse_handler))

        # Add hook handler for user-defined hooks
        from ..agent.hooks import HookHandler, get_hook_manager
        hook_manager = get_hook_manager()
        hook_manager.set_session_id(session_id)
        emitter.add_handler(HookHandler(hook_manager))

        # Get repo_root: prefer client cwd, then server config, then process cwd
        from pathlib import Path
        from ..config import get_config
        from ..utils.logger import log
        config = get_config()
        if cwd:
            repo_root = Path(cwd)
        elif config.repo_root:
            repo_root = Path(config.repo_root)
        else:
            repo_root = Path.cwd()
        log.info(f"Agent API: cwd={cwd}, config.repo_root={config.repo_root}, resolved repo_root={repo_root}, agent_type={agent_type}")

        # Create worktree for isolated changes if requested (coding agent only)
        worktree_info = None
        if use_worktree and not plan_mode and agent_type == "coding":
            from ..agent.worktree import WorktreeManager
            try:
                worktree_manager = WorktreeManager(repo_root)
                # Use session_id as task slug (truncated for safety)
                task_slug = session_id[:20] if len(session_id) > 20 else session_id
                worktree_info = worktree_manager.create_worktree(task_slug, force=True)
                repo_root = worktree_info.path
                log.info(f"Created worktree at {repo_root} on branch {worktree_info.branch}")
            except Exception as e:
                log.warning(f"Failed to create worktree: {e}. Running in main repo.")
                worktree_info = None

        # Create agent based on type
        if agent_type == "coworker":
            # CoworkerAgent - general-purpose assistant without coding capabilities
            from ..agent.factory import create_coworker_agent

            agent = create_coworker_agent(
                model=model,
                emitter=emitter,
                max_iterations=max_iterations,
                session_id=session_id,
                personality=personality or "helpful_professional",
                domain_context=domain_context,
            )

            # Inject pre-loaded conversation history if provided
            if history:
                agent._messages = list(history)
                log.info(f"Injected {len(history)} messages from saved session")

            # Store session state BEFORE running
            # Agent has .name and .agent_type properties
            _sessions[session_id] = {
                "agent": agent,  # CoworkerAgent has .name and .agent_type properties
                "message_count": 1,
                "model": model,
                "personality": personality,
                "domain_context": domain_context,
            }

            # Convert image data if provided
            agent_images = None
            if images:
                import base64
                from ..agent.providers.base import ImageContent
                agent_images = [
                    ImageContent(
                        image_data=base64.b64decode(img.data),
                        format=img.format
                    )
                    for img in images
                ]

            # Run the agent
            response = agent.run(message, images=agent_images)
            return response

        elif agent_type == "open":
            # OpenAgent - self-evolving personal assistant with learning capabilities
            from ..agent.factory import create_open_agent

            agent = create_open_agent(
                model=model,
                repo_root=repo_root,
                emitter=emitter,
                max_iterations=max_iterations,
                session_id=session_id,
            )

            # Persistent conversation file (configurable via EMDASH_CONVERSATION_FILE_PATH)
            conv_path = Path(os.environ.get("EMDASH_CONVERSATION_FILE_PATH", ".emdash/memory/conversation.json"))
            if not conv_path.is_absolute():
                conv_path = repo_root / conv_path
            log.info(f"OpenAgent conversation path: {conv_path} (exists={conv_path.exists()})")

            # Auto-load previous conversation if no explicit history provided
            if history:
                agent._messages = list(history)
                log.info(f"Injected {len(history)} messages from request history")
            elif conv_path.exists():
                try:
                    saved = json.loads(conv_path.read_text())
                    saved_messages = saved.get("messages", [])
                    if saved_messages:
                        agent._messages = saved_messages
                        log.info(f"Loaded {len(saved_messages)} messages from {conv_path}")
                    else:
                        log.info(f"Conversation file exists but has no messages: {conv_path}")
                except Exception as e:
                    log.warning(f"Failed to load conversation from {conv_path}: {e}")
            else:
                log.info(f"No previous conversation found at {conv_path}, starting fresh")

            # Emit SESSION_START for OpenAgent
            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": model,
                "session_id": session_id,
                "query": message,
                "mode": "open",
                "agent_type": agent_type,
                "system_prompt": agent.system_prompt,
                "conv_path": str(conv_path),
                "loaded_messages": len(agent._messages),
            })

            # Store session state BEFORE running (include conv_path for continue handler)
            _sessions[session_id] = {
                "agent": agent,
                "message_count": 1,
                "model": model,
                "conv_path": conv_path,
            }

            # Convert image data if provided
            agent_images = None
            if images:
                import base64
                from ..agent.providers.base import ImageContent
                agent_images = [
                    ImageContent(
                        image_data=base64.b64decode(img.data),
                        format=img.format
                    )
                    for img in images
                ]

            # Use chat() when we have loaded history so we append to existing messages;
            # use run() for a fresh conversation
            try:
                if agent._messages:
                    response = agent.chat(message, images=agent_images)
                else:
                    response = agent.run(message, images=agent_images)
                return response
            finally:
                # Always save conversation, even if agent errors mid-run
                log.info(f"OpenAgent run complete, saving {len(agent._messages)} messages to {conv_path}")
                _save_conversation(agent, conv_path)

        else:
            # CodingAgent - full-featured coding assistant
            from ..agent.runner import AgentRunner
            from ..agent.toolkit import AgentToolkit

            t0 = time.monotonic()

            # Create toolkit - plan_mode is now config-driven and doesn't restrict tools
            toolkit = AgentToolkit(repo_root=repo_root, plan_mode=plan_mode)
            t1 = time.monotonic()

            # Create checkpoint manager for persisting session state
            checkpoint_manager = None
            checkpoints_enabled = _read_checkpoints_enabled(repo_root)
            if checkpoints_enabled:
                try:
                    checkpoint_manager = CheckpointManager(
                        repo_root=repo_root,
                        session_id=session_id,
                    )
                except Exception as e:
                    log.warning(f"Could not initialize checkpoint manager: {e}. Checkpoints disabled.")
            t2 = time.monotonic()

            runner = AgentRunner(
                toolkit=toolkit,
                model=model,
                verbose=True,
                max_iterations=max_iterations,
                emitter=emitter,
                session_id=session_id,
                checkpoint_manager=checkpoint_manager,
            )
            t3 = time.monotonic()

            log.info(
                f"[PERF] Agent init: toolkit={t1-t0:.2f}s checkpoint={t2-t1:.2f}s "
                f"runner={t3-t2:.2f}s total={t3-t0:.2f}s"
            )

            # Emit SESSION_START now that we have the runner with system_prompt
            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": model,
                "session_id": session_id,
                "query": message,
                "mode": "plan" if plan_mode else "code",
                "use_worktree": use_worktree,
                "agent_type": agent_type,
                "system_prompt": runner.system_prompt,
            })

            # Persistent conversation file (configurable via EMDASH_CONVERSATION_FILE_PATH)
            conv_path = Path(os.environ.get("EMDASH_CONVERSATION_FILE_PATH", ".emdash/memory/conversation.json"))
            if not conv_path.is_absolute():
                conv_path = repo_root / conv_path
            log.info(f"CodingAgent conversation path: {conv_path} (exists={conv_path.exists()})")

            # Inject pre-loaded conversation history if provided
            if history:
                runner._messages = list(history)
                log.info(f"Injected {len(history)} messages from saved session")
            elif conv_path.exists():
                try:
                    saved = json.loads(conv_path.read_text())
                    saved_messages = saved.get("messages", [])
                    if saved_messages:
                        runner._messages = saved_messages
                        log.info(f"Loaded {len(saved_messages)} messages from {conv_path}")
                    else:
                        log.info(f"Conversation file exists but has no messages: {conv_path}")
                except Exception as e:
                    log.warning(f"Failed to load conversation from {conv_path}: {e}")
            else:
                log.info(f"No previous conversation found at {conv_path}, starting fresh")

            # Store session state BEFORE running (so it exists even if interrupted)
            # Use unified "agent" key - both AgentRunner and CoworkerAgent have .name and .agent_type properties
            _sessions[session_id] = {
                "agent": runner,  # AgentRunner has .name and .agent_type properties
                "message_count": 1,
                "model": model,
                "plan_mode": plan_mode,
                "worktree_info": worktree_info,
                "conv_path": conv_path,
            }

            # Convert image data if provided
            agent_images = None
            if images:
                import base64
                from ..agent.providers.base import ImageContent
                agent_images = [
                    ImageContent(
                        image_data=base64.b64decode(img.data),
                        format=img.format
                    )
                    for img in images
                ]

            # Run the agent
            try:
                response = runner.run(message, images=agent_images)
                return response
            finally:
                # Always save conversation, even if agent errors mid-run
                log.info(f"CodingAgent run complete, saving {len(runner._messages)} messages to {conv_path}")
                _save_conversation(runner, conv_path)

    except Exception as e:
        # Emit error event
        sse_handler.emit(EventType.ERROR, {
            "message": str(e),
            "details": None,
        })
        raise

    finally:
        # Reset session context for ModeState
        ModeState.reset_session_context(token)


async def _run_agent_async(
    request: AgentChatRequest,
    sse_handler: SSEHandler,
    session_id: str,
    github_token: str = None,
):
    """Run agent in thread pool and stream events."""
    # Resolve strictly from ModelRegistry (.emdash/config.json), not env defaults.
    model = _resolve_requested_model(request.model, sse_handler)

    max_iterations = request.options.max_iterations
    plan_mode = request.options.mode == AgentMode.PLAN
    use_worktree = request.options.use_worktree
    agent_type = request.options.agent_type.value if request.options.agent_type else "coding"
    personality = request.options.personality
    domain_context = request.options.domain_context

    # Determine agent name based on type
    if agent_type == "coworker":
        agent_name = "Emdash Coworker"
    elif agent_type == "open":
        agent_name = "Emdash Open"
    else:
        agent_name = "Emdash Code"

    # Note: SESSION_START is now emitted from _run_agent_sync after runner is created
    # so we have access to the system_prompt

    loop = asyncio.get_event_loop()

    try:
        # Run agent in thread pool using lambda to pass all args
        await loop.run_in_executor(
            _executor,
            lambda: _run_agent_sync(
                message=request.message,
                model=model,
                max_iterations=max_iterations,
                sse_handler=sse_handler,
                session_id=session_id,
                images=request.images,
                plan_mode=plan_mode,
                history=request.history,
                use_worktree=use_worktree,
                agent_type=agent_type,
                personality=personality,
                domain_context=domain_context,
                github_token=github_token,
                cwd=request.cwd,
            ),
        )

        # Emit session end
        sse_handler.emit(EventType.SESSION_END, {
            "success": True,
            "session_id": session_id,
        })

    except Exception as e:
        sse_handler.emit(EventType.SESSION_END, {
            "success": False,
            "error": str(e),
            "session_id": session_id,
        })

    finally:
        sse_handler.close()


@router.post("/chat")
async def agent_chat(request: AgentChatRequest, http_request: Request):
    """Start an agent chat session with SSE streaming.

    The response is a Server-Sent Events stream containing:
    - session_start: Initial session info
    - tool_start: When a tool begins execution
    - tool_result: When a tool completes
    - thinking: Agent reasoning messages
    - response/partial_response: Agent text output
    - clarification: When agent needs user input
    - error/warning: Error messages
    - session_end: Session completion

    Example:
        curl -N -X POST http://localhost:8765/api/agent/chat \\
            -H "Content-Type: application/json" \\
            -d '{"message": "Find authentication code"}'
    """
    # Generate or use provided session ID
    session_id = request.session_id or str(uuid.uuid4())

    # Get agent name from request options
    agent_type = request.options.agent_type.value if request.options.agent_type else "coding"
    agent_name = _get_agent_name(agent_type)

    # Get GitHub token from user's auth session for git operations
    github_token = _get_github_token_from_request(http_request)

    # Create SSE handler
    sse_handler = SSEHandler(agent_name=agent_name)

    # Store SSE handler reference for abort support
    if session_id not in _sessions:
        _sessions[session_id] = {}
    _sessions[session_id]["sse_handler"] = sse_handler
    _sessions[session_id]["github_token"] = github_token  # Store for continue endpoint

    # Start agent in background
    asyncio.create_task(_run_agent_async(request, sse_handler, session_id, github_token))

    # Return SSE stream
    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.post("/chat/{session_id}/continue")
async def continue_chat(session_id: str, request: AgentChatRequest, http_request: Request):
    """Continue an existing chat session.

    This allows multi-turn conversations by reusing the session state.
    """
    if session_id not in _sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )

    session = _sessions[session_id]

    # Get agent (unified key - both AgentRunner and CoworkerAgent have .name and .chat())
    agent = session.get("agent")
    if not agent:
        raise HTTPException(
            status_code=400,
            detail="Session has no active agent"
        )

    # Get GitHub token - from session or from current request
    github_token = session.get("github_token") or _get_github_token_from_request(http_request)

    # Configure git credentials if available
    if github_token:
        _configure_git_for_session(github_token)

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    # Create SSE handler
    sse_handler = SSEHandler(agent_name=agent_name)

    # Store SSE handler reference for abort support
    session["sse_handler"] = sse_handler

    async def _continue_session():
        sse_handler.emit(EventType.SESSION_START, {
            "agent_name": agent_name,
            "model": session["model"],
            "session_id": session_id,
            "query": request.message,
            "continued": True,
        })

        loop = asyncio.get_event_loop()

        # Set session context so tools can access correct ModeState
        from ..agent.tools.modes import ModeState
        token = ModeState.set_session_context(session_id)

        try:
            # Wire up SSE handler to emitter
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            # Create fresh emitter with new SSE handler
            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            # Convert image data if provided
            agent_images = None
            if request.images:
                import base64
                from ..agent.providers.base import ImageContent
                agent_images = [
                    ImageContent(
                        image_data=base64.b64decode(img.data),
                        format=img.format
                    )
                    for img in request.images
                ]

            # Continue conversation - both types have chat() method
            await loop.run_in_executor(
                _executor,
                lambda: agent.chat(request.message, images=agent_images),
            )

            session["message_count"] += 1

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {
                "message": str(e),
            })
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            # Auto-save conversation on continue (in finally so it always runs)
            conv_path = session.get("conv_path")
            if conv_path:
                _save_conversation(agent, conv_path)
            ModeState.reset_session_context(token)
            sse_handler.close()

    asyncio.create_task(_continue_session())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.get("/sessions")
async def list_sessions():
    """List active chat sessions."""
    return {
        "sessions": [
            {
                "session_id": sid,
                "model": data.get("model"),
                "message_count": data.get("message_count", 0),
            }
            for sid, data in _sessions.items()
        ]
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session and cleanup associated files."""
    if session_id in _sessions:
        session = _sessions[session_id]

        # Cleanup persisted conversation file for this session if tracked.
        conv_path = session.get("conv_path")
        if conv_path:
            try:
                path = Path(conv_path)
                if path.exists():
                    path.unlink()
            except OSError:
                pass  # Ignore cleanup errors

        del _sessions[session_id]

        # Cleanup session-specific plan directory
        import shutil
        session_plan_dir = Path.home() / ".emdash" / "sessions" / session_id
        if session_plan_dir.exists():
            try:
                shutil.rmtree(session_plan_dir)
            except OSError:
                pass  # Ignore cleanup errors

        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Session not found")


@router.post("/chat/{session_id}/abort")
async def abort_chat(session_id: str):
    """Abort a running chat session.

    This signals the agent to stop by marking the SSE handler as cancelled.
    The agent checks this flag at regular intervals and will stop execution.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    sse_handler = session.get("sse_handler")

    if not sse_handler:
        return {
            "session_id": session_id,
            "aborted": False,
            "reason": "No active SSE handler for this session",
        }

    # Mark the handler as cancelled - agent will check this flag
    sse_handler._cancelled = True

    # Also close the handler to terminate the SSE stream
    sse_handler.close()

    log.info(f"Aborted session {session_id}")

    return {
        "session_id": session_id,
        "aborted": True,
    }


@router.get("/chat/{session_id}/export")
async def export_session(session_id: str, limit: int = 10):
    """Export session messages for persistence.

    Args:
        session_id: The session ID
        limit: Maximum number of messages to return (default 10)

    Returns:
        JSON with messages array and metadata
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        return {
            "session_id": session_id,
            "messages": [],
            "message_count": 0,
            "model": session.get("model"),
            "mode": "plan" if session.get("plan_mode") else "code",
        }

    # Get messages from agent
    messages = getattr(agent, "_messages", [])

    # Debug: check if compacted summary content is intact
    if len(messages) > 1 and messages[1].get("role") == "assistant":
        content = messages[1].get("content", "")
        print(f"[DEBUG EXPORT] msg[1] content length: {len(content)}")
        print(f"[DEBUG EXPORT] Contains 'Analysis:': {'Analysis:' in content}")
        print(f"[DEBUG EXPORT] First 200 chars: {content[:200]}")

    # Trim to limit (most recent)
    if len(messages) > limit:
        messages = messages[-limit:]

    return {
        "session_id": session_id,
        "messages": messages,
        "message_count": len(messages),
        "model": session.get("model"),
        "mode": "plan" if session.get("plan_mode") else "code",
    }


@router.post("/chat/{session_id}/compact")
async def compact_session(session_id: str):
    """Compact the session's message history using LLM summarization.

    This manually triggers the same compaction that happens automatically
    when context reaches 80% capacity.

    Returns:
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    # Get current messages
    messages = getattr(agent, "_messages", [])
    # Need more than KEEP_RECENT + 2 = 8 messages to have anything to compact
    if len(messages) <= 8:
        return {
            "compacted": False,
            "reason": f"Not enough messages to compact (have {len(messages)}, need more than 8)",
            "message_count": len(messages),
        }

    # Import compaction utilities
    from ..agent.runner.context import compact_messages_with_llm, estimate_context_tokens

    # Create a simple emitter that captures compaction status
    class CompactionCapture:
        def __init__(self):
            self.compaction_failed = False
            self.error_message = None

        def emit_thinking(self, text):
            # Detect compaction failure from the thinking message
            if "Compaction failed" in text or "using simple truncation" in text:
                self.compaction_failed = True
                self.error_message = text

    emitter = CompactionCapture()

    # Estimate current tokens
    original_tokens = estimate_context_tokens(messages)

    # Get toolkit from agent for file tracking reset
    toolkit = getattr(agent, "toolkit", None)

    # Compact messages
    compacted_messages = compact_messages_with_llm(
        messages,
        emitter,
        target_tokens=int(original_tokens * 0.5),
        toolkit=toolkit,
    )

    # Check if compaction failed (fell back to truncation)
    if emitter.compaction_failed:
        # Still update messages (truncated) but report the failure
        agent._messages = compacted_messages
        new_tokens = estimate_context_tokens(compacted_messages)
        return {
            "compacted": True,
            "llm_summary": False,
            "summary": None,
            "error": emitter.error_message or "LLM compaction failed, used simple truncation",
            "original_message_count": len(messages),
            "new_message_count": len(compacted_messages),
            "original_tokens": original_tokens,
            "new_tokens": new_tokens,
            "reduction_percent": round((1 - new_tokens / original_tokens) * 100, 1) if original_tokens > 0 else 0,
        }

    # Extract the summary from the compacted messages
    # The LLM-generated summary starts with "This session is being continued..."
    summary_text = None
    for msg in compacted_messages:
        content = str(msg.get("content", ""))
        if msg.get("role") == "assistant":
            # Check for the new format (starts with continuation note)
            if "This session is being continued" in content:
                # Extract everything before the final note
                end_marker = "---\nNote: Context was compacted"
                end_idx = content.find(end_marker)
                if end_idx > 0:
                    summary_text = content[:end_idx].strip()
                else:
                    summary_text = content.strip()
                break
            # Legacy format check
            elif "[CONTEXT COMPACTION" in content:
                start_marker = "[CONTEXT COMPACTION - Working State Summary]"
                end_marker = "[END SUMMARY]"
                start = content.find(start_marker)
                if start >= 0:
                    start += len(start_marker)
                end = content.find(end_marker)
                if start >= 0 and end > start:
                    summary_text = content[start:end].strip()
                break

    # Update agent's messages
    agent._messages = compacted_messages
    # Set flag to prevent agent loop from overwriting compacted messages
    agent._messages_compacted_externally = True

    # Estimate new tokens
    new_tokens = estimate_context_tokens(compacted_messages)

    return {
        "compacted": True,
        "llm_summary": summary_text is not None,
        "summary": summary_text,
        "original_message_count": len(messages),
        "new_message_count": len(compacted_messages),
        "original_tokens": original_tokens,
        "new_tokens": new_tokens,
        "reduction_percent": round((1 - new_tokens / original_tokens) * 100, 1) if original_tokens > 0 else 0,
    }


@router.get("/chat/{session_id}/stats")
async def get_session_stats(session_id: str):
    """Get real-time token usage and cost for a session.

    Returns current token counts and estimated cost based on model pricing.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    # Import pricing utilities
    from ..agent.providers.models import calculate_cost

    # Get token counts from agent
    input_tokens = getattr(agent, "_total_input_tokens", 0)
    output_tokens = getattr(agent, "_total_output_tokens", 0)
    thinking_tokens = getattr(agent, "_total_thinking_tokens", 0)
    total_tokens = input_tokens + output_tokens + thinking_tokens

    # Get model from agent
    model = getattr(agent, "model", None)
    if model is None:
        # Try to get from provider
        provider = getattr(agent, "provider", None)
        if provider:
            model = getattr(provider, "model", "unknown")
        else:
            model = "unknown"

    # Calculate cost
    cost = calculate_cost(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        model=str(model),
        thinking_tokens=thinking_tokens,
    )

    return {
        "session_id": session_id,
        "model": str(model),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "thinking_tokens": thinking_tokens,
        "total_tokens": total_tokens,
        "estimated_cost": round(cost, 6),
        "cost_formatted": f"${cost:.4f}",
    }


@router.get("/chat/{session_id}/plan")
async def get_pending_plan(session_id: str):
    """Get the pending plan for a session, if any.

    Returns 404 if session not found, 204 if no pending plan.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    pending_plan = agent.get_pending_plan() if hasattr(agent, 'get_pending_plan') else None
    if not pending_plan:
        return {"has_plan": False, "plan": None}

    return {
        "has_plan": True,
        "session_id": session_id,
        "plan": pending_plan,
    }


@router.post("/chat/{session_id}/plan/approve")
async def approve_plan(session_id: str):
    """Approve the pending plan and transition to code mode.

    Returns SSE stream for the implementation phase.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    if not hasattr(agent, 'has_pending_plan') or not agent.has_pending_plan():
        raise HTTPException(status_code=400, detail="No pending plan to approve")

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    # Create SSE handler for streaming the implementation
    sse_handler = SSEHandler(agent_name=agent_name)

    async def _run_approval():
        loop = asyncio.get_event_loop()

        # Set session context for this coroutine so tools can access correct ModeState
        from ..agent.tools.modes import ModeState
        token = ModeState.set_session_context(session_id)

        try:
            # Wire up SSE handler
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": session.get("model", "unknown"),
                "session_id": session_id,
                "query": "Plan approved - implementing...",
                "plan_approved": True,
            })

            # Reset cycle state for new mode (use session-specific state)
            ModeState.get_instance(session_id).reset_cycle()

            # Approve and run implementation
            await loop.run_in_executor(
                _executor,
                agent.approve_plan,
            )

            session["plan_mode"] = False  # Now in code mode

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            ModeState.reset_session_context(token)
            sse_handler.close()

    asyncio.create_task(_run_approval())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.post("/chat/{session_id}/plan/reject")
async def reject_plan(session_id: str, feedback: str = ""):
    """Reject the pending plan with feedback.

    Returns SSE stream for the revised planning phase.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    if not hasattr(agent, 'has_pending_plan') or not agent.has_pending_plan():
        raise HTTPException(status_code=400, detail="No pending plan to reject")

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    sse_handler = SSEHandler(agent_name=agent_name)

    async def _run_rejection():
        loop = asyncio.get_event_loop()

        # Set session context for this coroutine so tools can access correct ModeState
        from ..agent.tools.modes import ModeState
        token = ModeState.set_session_context(session_id)

        try:
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": session.get("model", "unknown"),
                "session_id": session_id,
                "query": f"Plan rejected - revising... {feedback}",
                "plan_rejected": True,
            })

            # Reset cycle state for revision (use session-specific state)
            ModeState.get_instance(session_id).reset_cycle()

            # Reject and continue planning
            await loop.run_in_executor(
                _executor,
                lambda: agent.reject_plan(feedback),
            )

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            ModeState.reset_session_context(token)
            sse_handler.close()

    asyncio.create_task(_run_rejection())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.post("/chat/{session_id}/planmode/approve")
async def approve_plan_mode(session_id: str):
    """Approve entering plan mode.

    Called when user approves the agent's request to enter plan mode.
    Returns SSE stream for the planning phase.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    # Check if plan mode was actually requested (use session-specific state)
    from ..agent.tools.modes import ModeState
    state = ModeState.get_instance(session_id)
    if not state.plan_mode_requested:
        raise HTTPException(status_code=400, detail="No pending plan mode request")

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    sse_handler = SSEHandler(agent_name=agent_name)

    async def _run_approval():
        loop = asyncio.get_event_loop()

        # Set session context for this coroutine so tools can access correct ModeState
        token = ModeState.set_session_context(session_id)

        try:
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": session.get("model", "unknown"),
                "session_id": session_id,
                "query": "Plan mode approved - entering plan mode...",
                "plan_mode_approved": True,
            })

            # Approve and enter plan mode
            await loop.run_in_executor(
                _executor,
                agent.approve_plan_mode,
            )

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            ModeState.reset_session_context(token)
            sse_handler.close()

    asyncio.create_task(_run_approval())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.post("/chat/{session_id}/clarification/answer")
async def answer_clarification(session_id: str, answer: str):
    """Answer a pending clarification question.

    Called when the user responds to a clarification question asked by the agent
    via ask_choice_questions tool. This resumes the agent with the user's answer.

    Args:
        session_id: The session ID
        answer: The user's answer to the clarification question

    Returns:
        SSE stream for the agent's continued execution
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    sse_handler = SSEHandler(agent_name=agent_name)

    async def _run_answer():
        loop = asyncio.get_event_loop()

        try:
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": session.get("model", "unknown"),
                "session_id": session_id,
                "query": f"Clarification answered: {answer[:100]}...",
                "clarification_answered": True,
            })

            # Answer the clarification and resume the agent
            await loop.run_in_executor(
                _executor,
                lambda: agent.answer_clarification(answer),
            )

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            sse_handler.close()

    asyncio.create_task(_run_answer())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


class ChoiceAnswersRequest(BaseModel):
    """Request body for choice answers."""
    responses: list[dict]


@router.post("/chat/{session_id}/choices/answer")
async def answer_choice_questions(session_id: str, request: ChoiceAnswersRequest):
    """Answer pending choice questions.

    Called when the user responds to choice questions asked by the agent
    via ask_choice_questions tool. This resumes the agent with the user's selections.

    Args:
        session_id: The session ID
        request: Request body with list of responses (question + answer)

    Returns:
        SSE stream for the agent's continued execution
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    sse_handler = SSEHandler(agent_name=agent_name)
    responses = request.responses

    async def _run_answer():
        loop = asyncio.get_event_loop()

        # Set session context so tools (e.g. enter_plan_mode) can access
        # the correct per-session ModeState via ModeState.get_instance()
        from ..agent.tools.modes import ModeState
        token = ModeState.set_session_context(session_id)

        try:
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": session.get("model", "unknown"),
                "session_id": session_id,
                "query": f"Choice questions answered: {len(responses)} selections",
                "choices_answered": True,
            })

            # Answer the choice questions and resume the agent
            await loop.run_in_executor(
                _executor,
                lambda: agent.answer_choice_questions(responses),
            )

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            ModeState.reset_session_context(token)
            sse_handler.close()

    asyncio.create_task(_run_answer())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.post("/chat/{session_id}/planmode/reject")
async def reject_plan_mode(session_id: str, feedback: str = ""):
    """Reject entering plan mode.

    Called when user rejects the agent's request to enter plan mode.
    Returns SSE stream for continued code mode execution.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    agent = session.get("agent")

    if not agent:
        raise HTTPException(status_code=400, detail="Session has no active agent")

    # Check if plan mode was actually requested (use session-specific state)
    from ..agent.tools.modes import ModeState
    state = ModeState.get_instance(session_id)
    if not state.plan_mode_requested:
        raise HTTPException(status_code=400, detail="No pending plan mode request")

    # Use agent's name property (polymorphism)
    agent_name = agent.name

    sse_handler = SSEHandler(agent_name=agent_name)

    async def _run_rejection():
        loop = asyncio.get_event_loop()

        # Set session context for this coroutine so tools can access correct ModeState
        token = ModeState.set_session_context(session_id)

        try:
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            emitter = AgentEventEmitter(agent_name=agent_name)
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            agent.emitter = emitter

            sse_handler.emit(EventType.SESSION_START, {
                "agent_name": agent_name,
                "model": session.get("model", "unknown"),
                "session_id": session_id,
                "query": f"Plan mode rejected - continuing in code mode... {feedback}",
                "plan_mode_rejected": True,
            })

            # Reject and stay in code mode
            await loop.run_in_executor(
                _executor,
                lambda: agent.reject_plan_mode(feedback),
            )

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {"message": str(e)})
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            ModeState.reset_session_context(token)
            sse_handler.close()

    asyncio.create_task(_run_rejection())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.get("/chat/{session_id}/todos")
async def get_todos(session_id: str):
    """Get the current todo list for a session.

    Returns the agent's task list including status of each item.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get todos from TaskState singleton
    from ..agent.tools.tasks import TaskState
    state = TaskState.get_instance()

    todos = state.get_all_tasks()

    # Count by status
    pending = sum(1 for t in todos if t["status"] == "pending")
    in_progress = sum(1 for t in todos if t["status"] == "in_progress")
    completed = sum(1 for t in todos if t["status"] == "completed")

    return {
        "session_id": session_id,
        "todos": todos,
        "summary": {
            "total": len(todos),
            "pending": pending,
            "in_progress": in_progress,
            "completed": completed,
        },
    }


@router.post("/chat/{session_id}/todos")
async def add_todo(session_id: str, title: str, description: str = ""):
    """Add a new todo item to the agent's task list.

    This allows users to inject tasks for the agent to work on.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    # Add todo via TaskState singleton
    from ..agent.tools.tasks import TaskState
    state = TaskState.get_instance()

    task = state.add_task(title=title.strip(), description=description.strip())

    return {
        "session_id": session_id,
        "task": task.to_dict(),
        "total_tasks": len(state.tasks),
    }


# ==================== Worktree Management ====================


@router.get("/chat/{session_id}/worktree")
async def get_worktree_status(session_id: str):
    """Get the worktree status for a session.

    Returns information about whether the session is using a worktree,
    the branch name, and any uncommitted changes.
    """
    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    worktree_info = session.get("worktree_info")

    if not worktree_info:
        return {
            "session_id": session_id,
            "has_worktree": False,
        }

    # Check for uncommitted changes in the worktree
    import subprocess
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_info.path),
            capture_output=True,
            text=True,
        )
        has_changes = bool(result.stdout.strip())
        changes = result.stdout.strip().split("\n") if has_changes else []
    except Exception:
        has_changes = False
        changes = []

    return {
        "session_id": session_id,
        "has_worktree": True,
        "worktree_path": str(worktree_info.path),
        "branch": worktree_info.branch,
        "base_branch": worktree_info.base_branch,
        "has_changes": has_changes,
        "changes": changes,
    }


@router.post("/chat/{session_id}/worktree/apply")
async def apply_worktree_changes(session_id: str, commit_message: str = None):
    """Apply worktree changes to the main branch.

    This merges the worktree branch into the base branch and cleans up.
    """
    from ..utils.logger import log

    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    worktree_info = session.get("worktree_info")

    if not worktree_info:
        raise HTTPException(status_code=400, detail="Session is not using a worktree")

    import subprocess
    from pathlib import Path

    try:
        worktree_path = worktree_info.path
        branch = worktree_info.branch
        base_branch = worktree_info.base_branch

        # First, commit any uncommitted changes in the worktree
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(worktree_path),
            capture_output=True,
            text=True,
        )
        if result.stdout.strip():
            # Stage all changes
            subprocess.run(["git", "add", "-A"], cwd=str(worktree_path), check=True)
            # Commit
            msg = commit_message or f"Agent session {session_id[:8]} changes"
            subprocess.run(
                ["git", "commit", "-m", msg],
                cwd=str(worktree_path),
                check=True,
            )
            log.info(f"Committed changes in worktree: {msg}")

        # Get the main repo root (parent of .emdash-worktrees)
        from ..config import get_config
        config = get_config()
        main_repo = Path(config.repo_root) if config.repo_root else Path.cwd()

        # Merge the worktree branch into base branch
        subprocess.run(
            ["git", "checkout", base_branch],
            cwd=str(main_repo),
            check=True,
        )
        subprocess.run(
            ["git", "merge", branch, "--no-ff", "-m", f"Merge {branch}"],
            cwd=str(main_repo),
            check=True,
        )
        log.info(f"Merged {branch} into {base_branch}")

        # Clean up the worktree
        from ..agent.worktree import WorktreeManager
        worktree_manager = WorktreeManager(main_repo)
        worktree_manager.remove_worktree(worktree_info.task_slug)
        log.info(f"Removed worktree {worktree_info.task_slug}")

        # Clear worktree info from session
        session["worktree_info"] = None

        return {
            "session_id": session_id,
            "success": True,
            "message": f"Changes from {branch} merged into {base_branch}",
        }

    except subprocess.CalledProcessError as e:
        log.error(f"Failed to apply worktree changes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to apply changes: {e.stderr if hasattr(e, 'stderr') else str(e)}"
        )
    except Exception as e:
        log.error(f"Error applying worktree changes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/chat/{session_id}/worktree")
async def discard_worktree(session_id: str):
    """Discard worktree changes and clean up.

    This removes the worktree and branch without merging.
    """
    from ..utils.logger import log

    if session_id not in _sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = _sessions[session_id]
    worktree_info = session.get("worktree_info")

    if not worktree_info:
        raise HTTPException(status_code=400, detail="Session is not using a worktree")

    try:
        from pathlib import Path
        from ..config import get_config
        from ..agent.worktree import WorktreeManager

        config = get_config()
        main_repo = Path(config.repo_root) if config.repo_root else Path.cwd()

        worktree_manager = WorktreeManager(main_repo)
        worktree_manager.remove_worktree(worktree_info.task_slug)
        log.info(f"Discarded worktree {worktree_info.task_slug}")

        # Clear worktree info from session
        session["worktree_info"] = None

        return {
            "session_id": session_id,
            "success": True,
            "message": f"Worktree {worktree_info.task_slug} discarded",
        }

    except Exception as e:
        log.error(f"Error discarding worktree: {e}")
        raise HTTPException(status_code=500, detail=str(e))
