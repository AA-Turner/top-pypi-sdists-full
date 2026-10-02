# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Literal, TypedDict

from trajectory._types import SequenceNotStr
from trajectory.types.benchmarks.mcp_server_spec_param import McpServerSpecParam


class EnvResourcesParam(TypedDict, total=False):
  docker_engine: bool
  """
  Require a Docker-capable sandbox. The user image must provide Docker and the harness; the
  harness owns nested containers and grading.
  """
  cpus: float | None
  memory_mb: int | None
  gpus: int
  network_mode: Literal["no-network", "public", "allowlist"]
  allowed_hosts: SequenceNotStr[str]
  agent_user: str | None
  env: Mapping[str, str]
  setup_commands: Iterable[SequenceNotStr[str]]
  mcp_servers: Iterable[McpServerSpecParam]
  allow_internet: bool | None
