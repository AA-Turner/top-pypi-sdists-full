# Plato SDK v2
#
# Usage:
#   from plato.v2 import Plato, Session, Environment  # Sync
#   from plato.v2 import AsyncPlato, AsyncSession, AsyncEnvironment  # Async
#   from plato.v2 import DatagenSession, AsyncDatagenSession, DatagenResponse  # Agent runtime
#   from plato.v2 import Env, SimConfigCompute, Flow  # Helpers
#
# For Chronos, use `from plato.chronos.sdk import Chronos, AsyncChronos`.

# Models
# Sync exports (default)
from plato._generated.models import ArtifactInfoResponse, Flow
from plato.v2 import async_, sync
from plato.v2._wait_for_ready import JobTerminalStatusError

# Async exports (prefixed with Async)
from plato.v2.async_.cdp_bridge import shared_cdp_chromium
from plato.v2.async_.client import AsyncPlato
from plato.v2.async_.datagen_session import DatagenSession as AsyncDatagenSession
from plato.v2.async_.environment import Environment as AsyncEnvironment
from plato.v2.async_.flow_backends import FlowBackend as AsyncFlowBackend
from plato.v2.async_.flow_backends import PlaywrightBackend as AsyncPlaywrightBackend
from plato.v2.async_.flow_backends import make_ssh_run_cmd
from plato.v2.async_.flow_executor import FlowExecutionError as AsyncFlowExecutionError
from plato.v2.async_.flow_executor import FlowExecutor as AsyncFlowExecutor
from plato.v2.async_.session import SerializedSession
from plato.v2.async_.session import Session as AsyncSession
from plato.v2.async_.simulators import AsyncSimulatorsManager
from plato.v2.async_.testcase import AsyncTestcaseManager
from plato.v2.sync.client import Plato
from plato.v2.sync.datagen_session import (
    DATA_LOAD_INSTRUCTION,
    DatagenResponse,
    DatagenSession,
)
from plato.v2.sync.environment import Environment
from plato.v2.sync.flow_backends import (
    FlowBackend,
    PlaywrightBackend,
)
from plato.v2.sync.flow_executor import FlowExecutionError, FlowExecutor
from plato.v2.sync.sandbox import SandboxClient
from plato.v2.sync.session import LoginResult, Session
from plato.v2.sync.simulators import SimulatorArtifact, SimulatorsManager
from plato.v2.sync.testcase import TestcaseManager

# DatagenResponse lives in both sync and async datagen_session modules
# (structurally identical pydantic models) — the sync export is the
# canonical public one.
# Helper types
from plato.v2.types import (
    Env,
    EnvFromArtifact,
    EnvFromResource,
    EnvFromSimulator,
    SimConfigCompute,
)

__all__ = [
    # Sync
    "Plato",
    "Session",
    "DatagenSession",
    "DatagenResponse",
    "DATA_LOAD_INSTRUCTION",
    "Environment",
    "LoginResult",
    "FlowExecutor",
    "FlowExecutionError",
    "FlowBackend",
    "PlaywrightBackend",
    "ArtifactInfoResponse",
    "SandboxClient",
    "SimulatorArtifact",
    "SimulatorsManager",
    "TestcaseManager",
    "JobTerminalStatusError",
    # Async
    "AsyncPlato",
    "AsyncSession",
    "AsyncDatagenSession",
    "AsyncEnvironment",
    "AsyncFlowExecutor",
    "AsyncFlowExecutionError",
    "AsyncFlowBackend",
    "AsyncPlaywrightBackend",
    "make_ssh_run_cmd",
    "shared_cdp_chromium",
    "SerializedSession",
    "AsyncSimulatorsManager",
    "AsyncTestcaseManager",
    # Models
    "Flow",
    # Helpers
    "Env",
    "EnvFromSimulator",
    "EnvFromArtifact",
    "EnvFromResource",
    "SimConfigCompute",
    # Submodules
    "sync",
    "async_",
]
