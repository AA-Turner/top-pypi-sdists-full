"""Workflow management endpoints."""

import asyncio
import json
import re
import subprocess
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import get_config
from ..agent.providers import get_provider
from ..agent.providers.factory import DEFAULT_MODEL

router = APIRouter(prefix="/workflows", tags=["workflows"])


# ───────────────── Models ─────────────────


class WorkflowStepConfig(BaseModel):
    """Configuration for a workflow step."""
    type: str = Field(..., description="Step type: agent, script, or decision")
    # Agent fields
    agentName: str = Field(default="default", description="Agent name: 'default' or custom agent name")
    agentMode: Optional[str] = None
    prompt: Optional[str] = None
    # Script fields
    command: Optional[str] = None
    description: Optional[str] = None
    # Decision fields
    condition: Optional[str] = None
    trueBranch: Optional[str] = None
    falseBranch: Optional[str] = None


class WorkflowStepModel(BaseModel):
    """A single step in a workflow."""
    id: str
    name: str
    config: WorkflowStepConfig
    status: Optional[str] = None


class WorkflowModel(BaseModel):
    """Full workflow model."""
    id: str
    name: str
    description: str = ""
    steps: list[WorkflowStepModel] = []
    status: str = "draft"
    tags: list[str] = []
    createdAt: int
    updatedAt: int
    lastRunAt: Optional[int] = None
    chatHistory: list[dict] = []


class CreateWorkflowRequest(BaseModel):
    """Request to create a workflow."""
    name: str = Field(..., description="Workflow name")
    description: str = Field(default="", description="Workflow description")
    steps: list[WorkflowStepModel] = Field(default=[], description="Workflow steps")
    tags: list[str] = Field(default=[], description="Tags")


class UpdateWorkflowRequest(BaseModel):
    """Request to update a workflow."""
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[list[WorkflowStepModel]] = None
    status: Optional[str] = None
    tags: Optional[list[str]] = None
    chatHistory: Optional[list[dict]] = None


class GenerateWorkflowRequest(BaseModel):
    """Request to generate a workflow from natural language."""
    prompt: str = Field(..., description="Natural language description of the desired workflow")
    model: Optional[str] = Field(default=None, description="LLM model to use")


class GenerateWorkflowResponse(BaseModel):
    """Response from AI workflow generation."""
    name: str
    description: str
    steps: list[WorkflowStepModel]
    tags: list[str] = []


class ExecScriptRequest(BaseModel):
    """Request to execute a shell command."""
    command: str = Field(..., description="Shell command to execute")
    timeout: int = Field(default=30, description="Timeout in seconds")


class ExecScriptResponse(BaseModel):
    """Response from script execution."""
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool


GENERATE_SYSTEM_PROMPT = """\
You are a workflow generator. Given a natural language description, produce a JSON workflow definition.

Return ONLY valid JSON with this exact structure (no extra text, no markdown fences):

{
  "name": "Short Workflow Name",
  "description": "One-sentence description of what this workflow does.",
  "steps": [
    {
      "id": "step-1",
      "name": "Human-readable step name",
      "config": { ... }
    }
  ],
  "tags": ["tag1", "tag2"]
}

Each step config must be one of these types:

1. Agent step — runs an AI agent:
   {"type": "agent", "agentName": "default", "prompt": "What the agent should do"}
   agentName is always "default" (the built-in EmDash agent).

2. Script step — runs a shell command:
   {"type": "script", "command": "shell command here", "description": "What this does"}

3. Decision step — conditional branch:
   {"type": "decision", "condition": "condition to evaluate", "trueBranch": "action if true", "falseBranch": "action if false"}

Rules:
- Each step must have a unique id like "step-1", "step-2", etc.
- Generate between 2 and 8 steps.
- Choose the most appropriate step types for the described workflow.
- Use descriptive step names.
- Return ONLY the JSON object, nothing else.
"""


# ───────────────── Helpers ─────────────────


def _get_workflows_dir() -> Path:
    """Get the workflows directory for the current repo."""
    config = get_config()
    if config.repo_root:
        return Path(config.repo_root) / ".emdash" / "workflows"
    return Path.cwd() / ".emdash" / "workflows"


def _read_workflow(path: Path) -> dict:
    """Read a workflow JSON file."""
    return json.loads(path.read_text())


def _write_workflow(path: Path, data: dict) -> None:
    """Write a workflow JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


# ───────────────── Endpoints ─────────────────


@router.get("")
async def list_workflows():
    """List all workflows."""
    workflows_dir = _get_workflows_dir()
    workflows = []

    if workflows_dir.exists():
        for wf_file in sorted(workflows_dir.glob("*.json")):
            try:
                data = _read_workflow(wf_file)
                workflows.append(data)
            except (json.JSONDecodeError, OSError):
                continue

    return {"workflows": workflows}


@router.post("", response_model=WorkflowModel)
async def create_workflow(request: CreateWorkflowRequest):
    """Create a new workflow."""
    workflows_dir = _get_workflows_dir()
    workflows_dir.mkdir(parents=True, exist_ok=True)

    wf_id = str(uuid.uuid4())[:8]
    now = int(__import__("time").time() * 1000)

    workflow = WorkflowModel(
        id=wf_id,
        name=request.name,
        description=request.description,
        steps=request.steps,
        status="draft",
        tags=request.tags,
        createdAt=now,
        updatedAt=now,
    )

    wf_path = workflows_dir / f"{wf_id}.json"
    _write_workflow(wf_path, workflow.model_dump())

    return workflow


@router.post("/exec_script", response_model=ExecScriptResponse)
async def exec_script(request: ExecScriptRequest):
    """Execute a shell command and return the result."""
    config = get_config()
    cwd = config.repo_root or str(Path.cwd())

    loop = asyncio.get_event_loop()
    timed_out = False

    def _run():
        nonlocal timed_out
        try:
            result = subprocess.run(
                request.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=request.timeout,
                cwd=cwd,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            return "", f"Command timed out after {request.timeout}s", 124

    try:
        stdout, stderr, exit_code = await loop.run_in_executor(None, _run)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Script execution failed: {exc}")

    return ExecScriptResponse(
        stdout=stdout,
        stderr=stderr,
        exit_code=exit_code,
        timed_out=timed_out,
    )


@router.post("/generate", response_model=GenerateWorkflowResponse)
async def generate_workflow(request: GenerateWorkflowRequest):
    """Generate a workflow from a natural language description using AI."""
    try:
        provider = get_provider(request.model or DEFAULT_MODEL)
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="AI provider not available. Check that your API key is configured.",
        )

    try:
        response = provider.chat(
            messages=[{"role": "user", "content": request.prompt}],
            system=GENERATE_SYSTEM_PROMPT,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI model call failed: {exc}",
        )

    raw = response.content or ""

    # Strip markdown fences if the LLM wrapped its response
    raw = re.sub(r"^```(?:json)?\s*\n?", "", raw.strip())
    raw = re.sub(r"\n?```\s*$", "", raw.strip())

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="The AI returned an invalid response. Please try rephrasing your request.",
        )

    try:
        result = GenerateWorkflowResponse(**data)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail="The AI response did not match the expected workflow format. Please try again.",
        )

    return result


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get a single workflow."""
    wf_path = _get_workflows_dir() / f"{workflow_id}.json"

    if not wf_path.exists():
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")

    return _read_workflow(wf_path)


@router.put("/{workflow_id}", response_model=WorkflowModel)
async def update_workflow(workflow_id: str, request: UpdateWorkflowRequest):
    """Update a workflow."""
    wf_path = _get_workflows_dir() / f"{workflow_id}.json"

    if not wf_path.exists():
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")

    data = _read_workflow(wf_path)

    # Merge updates
    updates = request.model_dump(exclude_none=True)
    if "steps" in updates:
        updates["steps"] = [s.model_dump() for s in request.steps]  # type: ignore
    data.update(updates)
    data["updatedAt"] = int(__import__("time").time() * 1000)

    _write_workflow(wf_path, data)

    return WorkflowModel(**data)


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow."""
    wf_path = _get_workflows_dir() / f"{workflow_id}.json"

    if not wf_path.exists():
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_id}' not found")

    wf_path.unlink()
    return {"deleted": True, "id": workflow_id}
