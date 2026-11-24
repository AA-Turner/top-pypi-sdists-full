# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Literal, TypedDict

from trajectory._types import SequenceNotStr


class TasksUpdateEnvResourcesParams(TypedDict, total=False):
  """
  Fields left out keep their stored value.
  """

  cpus: float | None
  """
  CPU cores to request. Set `cpus` and `memory_mb` both to null for the default.
  """
  memory_mb: int | None
  """
  Memory to request in MiB.
  """
  gpus: int
  """
  GPUs to request.
  """
  network_mode: Literal["no-network", "public", "allowlist"]
  """
  `public`, `allowlist` or `no-network`. Leaving `allowlist` clears `allowed_hosts` unless the
  request also sets it.
  """
  allowed_hosts: SequenceNotStr[str]
  """
  Domain names the sandbox may reach, such as `pypi.org` or `*.example.com` for every subdomain;
  no scheme, port, path or IP address. Only valid with `allowlist`.
  """
