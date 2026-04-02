"""Multi-user web server with isolated Docker sandboxes.

This example shows how to build a production web service where each user
gets their own isolated Docker container for code execution.

Requires: pip install pydantic-ai-backend[docker] fastapi uvicorn pydantic-ai jinja2
"""

import asyncio
import contextlib
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic_ai import Agent

from pydantic_ai_backends import (
    DockerSandbox,
    SessionManager,
    create_console_toolset,
    get_console_system_prompt,
)

# ============================================================================
# Session Manager (handles multiple users)
# ============================================================================

session_manager: SessionManager | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and cleanup session manager."""
    global session_manager

    session_manager = SessionManager(
        image="python:3.12-slim",
        workspace_root="/tmp/workspaces",  # Persistent storage
        auto_remove=True,
    )

    yield

    # Cleanup all sessions on shutdown
    if session_manager:
        for session_id in list(session_manager._sandboxes.keys()):
            with contextlib.suppress(Exception):
                await asyncio.to_thread(session_manager.end_session, session_id)


app = FastAPI(
    title="Multi-User Code Sandbox API",
    lifespan=lifespan,
)

# Templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Serve the frontend UI."""
    return templates.TemplateResponse("index.html", {"request": request})


# ============================================================================
# Request/Response Models
# ============================================================================


class CreateSessionResponse(BaseModel):
    session_id: str
    message: str


class WriteFileRequest(BaseModel):
    path: str
    content: str


class ExecuteRequest(BaseModel):
    command: str
    timeout: int = 30


class ExecuteResponse(BaseModel):
    output: str
    exit_code: int | None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# ============================================================================
# Agent Setup
# ============================================================================


@dataclass
class UserDeps:
    """Dependencies for a user's agent session."""

    backend: DockerSandbox
    user_id: str


def create_user_agent() -> Agent[UserDeps, str]:
    """Create an agent for a user session."""
    toolset = create_console_toolset(
        include_execute=True,
        require_write_approval=False,
        require_execute_approval=False,
    )

    agent: Agent[UserDeps, str] = Agent(
        "openai:gpt-4o-mini",
        system_prompt=f"""You are a helpful coding assistant in an isolated sandbox environment.

{get_console_system_prompt()}

The user has their own isolated workspace. You can freely create, read, and execute files.
All changes persist within their session but are isolated from other users.
""",
        deps_type=UserDeps,
    )

    return agent.with_toolset(toolset)


# Shared agent instance
user_agent = create_user_agent()


# ============================================================================
# API Endpoints
# ============================================================================


@app.post("/sessions", response_model=CreateSessionResponse)
async def create_session(user_id: str | None = None) -> CreateSessionResponse:
    """Create a new isolated session for a user."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    session_id = await asyncio.to_thread(
        session_manager.create_session,
        user_id=user_id,
    )

    return CreateSessionResponse(
        session_id=session_id,
        message="Session created. Your workspace is isolated and ready.",
    )


@app.delete("/sessions/{session_id}")
async def end_session(session_id: str) -> dict[str, str]:
    """End a user session and cleanup resources."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    try:
        await asyncio.to_thread(session_manager.end_session, session_id)
        return {"message": "Session ended successfully"}
    except ValueError as e:
        raise HTTPException(404, str(e)) from None


@app.get("/sessions/{session_id}/files")
async def list_files(session_id: str, path: str = ".") -> dict[str, list[dict]]:
    """List files in the user's workspace."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    try:
        sandbox = session_manager.get_session(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from None

    files = sandbox.ls_info(path)
    return {"files": files}


@app.get("/sessions/{session_id}/files/{path:path}")
async def read_file(session_id: str, path: str) -> dict[str, str]:
    """Read a file from the user's workspace."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    try:
        sandbox = session_manager.get_session(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from None

    content = sandbox.read(path)
    return {"content": content}


@app.post("/sessions/{session_id}/files")
async def write_file(session_id: str, request: WriteFileRequest) -> dict[str, str]:
    """Write a file to the user's workspace."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    try:
        sandbox = session_manager.get_session(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from None

    result = sandbox.write(request.path, request.content)
    if result.error:
        raise HTTPException(400, result.error)

    return {"message": f"File written: {result.path}"}


@app.post("/sessions/{session_id}/execute", response_model=ExecuteResponse)
async def execute_command(session_id: str, request: ExecuteRequest) -> ExecuteResponse:
    """Execute a command in the user's sandbox."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    try:
        sandbox = session_manager.get_session(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from None

    result = sandbox.execute(request.command, timeout=request.timeout)
    return ExecuteResponse(
        output=result.output,
        exit_code=result.exit_code,
    )


@app.post("/sessions/{session_id}/chat", response_model=ChatResponse)
async def chat(session_id: str, request: ChatRequest) -> ChatResponse:
    """Chat with an AI agent that has access to the user's sandbox."""
    if not session_manager:
        raise HTTPException(503, "Session manager not initialized")

    try:
        sandbox = session_manager.get_session(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from None

    deps = UserDeps(backend=sandbox, user_id=session_id)
    result = await user_agent.run(request.message, deps=deps)

    return ChatResponse(response=result.output)


# ============================================================================
# Health Check
# ============================================================================


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
