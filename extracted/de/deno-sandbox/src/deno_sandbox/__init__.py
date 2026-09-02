from typing import Optional

from .apps import (
    Apps,
    AsyncApps,
    App,
    AppListItem,
    Config,
    EnvVar,
    EnvVarInput,
    EnvVarUpdate,
    LayerRef,
    Runtime,
    RuntimeLog,
    RuntimeLogsResponse,
)
from .revisions import (
    Revisions,
    AsyncRevisions,
    Revision,
    RevisionListItem,
    RevisionRetention,
    RevisionProgress,
    ProgressStage,
    ProgressStageStatus,
    FileAsset,
    SymlinkAsset,
    Asset,
    EnvVarInputForDeploy,
    BuildLogEntry,
    BuildStep,
)
from .layers import (
    Layers,
    AsyncLayers,
    Layer,
    LayerAppRef,
)
from .snapshots import Snapshots, AsyncSnapshots
from .timelines import Timelines, AsyncTimelines
from .volumes import Volumes, AsyncVolumes
from .bridge import AsyncBridge
from .sandbox import (
    AsyncSandboxApi,
    SandboxApi,
)
from .console import AsyncConsoleClient
from .errors import HTTPStatusError
from .options import Options, get_internal_options

__all__ = [
    "DenoDeploy",
    "AsyncDenoDeploy",
    "Options",
    "App",
    "AppListItem",
    "Config",
    "EnvVar",
    "EnvVarInput",
    "EnvVarUpdate",
    "LayerRef",
    "Runtime",
    "RuntimeLog",
    "RuntimeLogsResponse",
    "Revision",
    "RevisionListItem",
    "RevisionRetention",
    "RevisionProgress",
    "ProgressStage",
    "ProgressStageStatus",
    "FileAsset",
    "SymlinkAsset",
    "Asset",
    "EnvVarInputForDeploy",
    "BuildLogEntry",
    "BuildStep",
    "Layer",
    "LayerAppRef",
    "HTTPStatusError",
]


class DenoDeploy:
    def __init__(self, options: Optional[Options] = None):
        internal_options = get_internal_options(options)
        bridge = AsyncBridge()

        client = AsyncConsoleClient(internal_options)
        self.apps = Apps(client, bridge)
        self.revisions = Revisions(client, bridge)
        self.layers = Layers(client, bridge)
        self.timelines = Timelines(client, bridge)
        self.sandbox = SandboxApi(client, bridge)
        self.snapshots = Snapshots(client, bridge)
        self.volumes = Volumes(client, bridge)


class AsyncDenoDeploy:
    def __init__(self, options: Optional[Options] = None):
        internal_options = get_internal_options(options)
        client = AsyncConsoleClient(internal_options)

        self.apps = AsyncApps(client)
        self.revisions = AsyncRevisions(client)
        self.layers = AsyncLayers(client)
        self.timelines = AsyncTimelines(client)
        self.sandbox = AsyncSandboxApi(client)
        self.snapshots = AsyncSnapshots(client)
        self.volumes = AsyncVolumes(client)
