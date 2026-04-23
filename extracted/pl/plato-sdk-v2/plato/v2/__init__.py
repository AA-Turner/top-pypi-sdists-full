# Plato SDK v2
#
# Usage:
#   from plato.v2 import Plato, Session, Environment  # Sync
#   from plato.v2 import AsyncPlato, AsyncSession, AsyncEnvironment  # Async
#   from plato.v2 import Env, SimConfigCompute, Flow  # Helpers
#
# For Chronos, use `from plato.chronos.sdk import Chronos, AsyncChronos`.

# Models
# Sync exports (default)
from plato._generated.models import ArtifactInfoResponse, Flow
from plato.v2 import async_, sync

# Async exports (prefixed with Async)
from plato.v2.async_.cdp_bridge import shared_cdp_chromium
from plato.v2.async_.client import AsyncPlato
from plato.v2.async_.environment import Environment as AsyncEnvironment
from plato.v2.async_.flow_backends import FlowBackend as AsyncFlowBackend
from plato.v2.async_.flow_backends import PlaywrightBackend as AsyncPlaywrightBackend
from plato.v2.async_.flow_backends import make_ssh_run_cmd
from plato.v2.async_.flow_executor import FlowExecutionError as AsyncFlowExecutionError
from plato.v2.async_.flow_executor import FlowExecutor as AsyncFlowExecutor
from plato.v2.async_.session import SerializedSession
from plato.v2.async_.session import Session as AsyncSession
from plato.v2.async_.testcase import AsyncTestcaseManager
from plato.v2.sync.client import Plato
from plato.v2.sync.environment import Environment
from plato.v2.sync.flow_backends import (
    FlowBackend,
    PlaywrightBackend,
)
from plato.v2.sync.flow_executor import FlowExecutionError, FlowExecutor
from plato.v2.sync.sandbox import SandboxClient
from plato.v2.sync.session import LoginResult, Session
from plato.v2.sync.testcase import TestcaseManager

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
    "Environment",
    "LoginResult",
    "FlowExecutor",
    "FlowExecutionError",
    "FlowBackend",
    "PlaywrightBackend",
    "ArtifactInfoResponse",
    "SandboxClient",
    "TestcaseManager",
    # Async
    "AsyncPlato",
    "AsyncSession",
    "AsyncEnvironment",
    "AsyncFlowExecutor",
    "AsyncFlowExecutionError",
    "AsyncFlowBackend",
    "AsyncPlaywrightBackend",
    "make_ssh_run_cmd",
    "shared_cdp_chromium",
    "SerializedSession",
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
