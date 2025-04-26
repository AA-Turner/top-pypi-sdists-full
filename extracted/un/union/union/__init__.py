import os

from flytekit import (
    ContainerTask,
    Deck,
    ImageSpec,
    LaunchPlan,
    PodTemplate,
    Resources,
    Secret,
    StructuredDataset,
    current_context,
    dynamic,
    map_task,
    task,
    workflow,
)
from flytekit.core.cache import Cache, CachePolicy, VersionParameters
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile

from union._logging import _init_global_loggers
from union.actor import ActorEnvironment, actor_cache
from union.artifacts import Artifact
from union.map import map
from union.remote import UnionRemote

# Set GRPC_VERBOSITY to NONE if not already set to silence unwanted output
# This addresses the issue with grpcio >=1.68.0 causing unwanted output
if "GRPC_VERBOSITY" not in os.environ:
    os.environ["GRPC_VERBOSITY"] = "NONE"

_init_global_loggers()


__all__ = [
    "ActorEnvironment",
    "Artifact",
    "Cache",
    "CachePolicy",
    "ContainerTask",
    "Deck",
    "FlyteDirectory",
    "FlyteFile",
    "ImageSpec",
    "LaunchPlan",
    "PodTemplate",
    "Resources",
    "Secret",
    "StructuredDataset",
    "UnionRemote",
    "VersionParameters",
    "actor_cache",
    "current_context",
    "dynamic",
    "map",
    "map_task",
    "task",
    "workflow",
]
