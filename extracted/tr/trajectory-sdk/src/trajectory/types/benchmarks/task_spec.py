# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Literal, TypeAlias

from trajectory._models import BaseModel
from trajectory.types._internal import BenchmarkMessage
from trajectory.types.benchmarks.runtime_spec import RuntimeSpec
from trajectory.types.benchmarks.secret_ref import SecretRef
from trajectory.types.task_split import TaskSplit


class McpServerSpec(BaseModel):
  name: str

  transport: Literal["sse", "streamable-http", "stdio"] = "sse"

  url: str | None = None

  command: str | None = None

  args: list[str] | None = None


NetworkMode: TypeAlias = Literal["no-network", "public", "allowlist"]


class EnvResources(BaseModel):
  docker_engine: bool = False
  """
    Require a Docker-capable sandbox. The user image must provide Docker and the harness;
    the harness owns nested containers and grading.
    """

  cpus: float | None = None

  memory_mb: int | None = None

  gpus: int = 0

  network_mode: NetworkMode = "no-network"

  allowed_hosts: list[str] | None = None

  agent_user: str | None = None

  env: dict[str, str] | None = None

  setup_commands: list[list[str]] | None = None

  mcp_servers: list[McpServerSpec] | None = None

  allow_internet: bool | None = None


class TaskSpec(BaseModel):
  name: str

  id: str | None = None

  split: TaskSplit | None = None

  input_messages: list[BenchmarkMessage] | None = None
  """
    Messages stored on the task. For SDK evaluation and training, your agent script must
    pass messages to the model; this field does not do that automatically.
    """

  reference_trajectory_id: str | None = None

  image: None = None

  runtime: RuntimeSpec | None = None

  run_command: str
  """
    For SDK evaluation and training, the command to run your agent in the sandbox, e.g.
    `python /app/agent.py`. Your script must call the model, run any tools, log a reward,
    and finalize the trajectory before exiting.
    """

  env_vars: dict[str, str | SecretRef] | None = None

  env_resources: EnvResources | None = None

  spec: dict[str, Any] | None = None

  task_spec_uri: str | None = None

  tags: list[str] | None = None
