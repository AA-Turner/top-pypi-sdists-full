# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, Literal, Required, TypedDict

from trajectory._types import SequenceNotStr
from trajectory.types._internal_params import BenchmarkMessageParam
from trajectory.types.env_resources_param import EnvResourcesParam
from trajectory.types.runtime_spec_param import RuntimeSpecParam
from trajectory.types.secret_ref_param import SecretRefParam


class TaskSpecParam(TypedDict, total=False):
  name: Required[str]
  id: str | None
  split: Literal["train", "test"] | None
  input_messages: Iterable[BenchmarkMessageParam]
  """
  Messages stored on the task. For SDK evaluation and training, your agent script must pass
  messages to the model; this field does not do that automatically.
  """
  reference_trajectory_id: str | None
  image: None
  runtime: RuntimeSpecParam | None
  run_command: Required[str]
  """
  For SDK evaluation and training, the command to run your agent in the sandbox, e.g. `python
  /app/agent.py`. Your script must call the model, run any tools, log a reward, and finalize the
  trajectory before exiting.
  """
  env_vars: Mapping[str, str | SecretRefParam]
  env_resources: EnvResourcesParam
  spec: Mapping[str, Any]
  task_spec_uri: str | None
  tags: SequenceNotStr[str]
