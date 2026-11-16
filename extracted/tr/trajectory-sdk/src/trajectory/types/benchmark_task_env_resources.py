# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from trajectory._models import BaseModel
from trajectory.types.network_mode import NetworkMode


class BenchmarkTaskEnvResources(BaseModel):
  cpus: float | None
  """CPU cores requested; null uses the provider default."""

  memory_mb: int | None
  """Memory requested in MiB; null uses the default."""

  gpus: int
  """GPUs requested."""

  network_mode: NetworkMode
  """
    `public` allows all outbound traffic, `allowlist` allows only `allowed_hosts` and the
    platform's own endpoints, and `no-network` allows only the platform's own endpoints.
    """

  allowed_hosts: list[str]
  """Domain names the sandbox may reach; only set with `allowlist`."""
