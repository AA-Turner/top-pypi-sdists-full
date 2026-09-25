"""Built-in samplers for optimization studies."""

import importlib
import typing as t

from dreadnode.samplers.boundary import BoundarySampler
from dreadnode.samplers.fuzzing import (
    FuzzingSampler,
    SeedEntry,
    fuzzing_sampler,
)
from dreadnode.samplers.graph import (
    GraphSampler,
    beam_search_sampler,
    graph_neighborhood_sampler,
    iterative_sampler,
)
from dreadnode.samplers.grid import GridSampler
from dreadnode.samplers.image import (
    HopSkipJumpSampler,
    ImageSampler,
    NESSampler,
    SimBASampler,
    ZOOSampler,
)
from dreadnode.samplers.mapelites import (
    ArchiveCell,
    MAPElitesSampler,
    MutationTarget,
    mapelites_sampler,
)
from dreadnode.samplers.random import RandomImageSampler, RandomSampler
from dreadnode.samplers.registry import (
    SAMPLER_REGISTRY,
    create_sampler,
    list_samplers,
    register_sampler,
)
from dreadnode.samplers.strategy import (
    Strategy,
    StrategyLibrarySampler,
    StrategyStore,
    strategy_library_sampler,
)

if t.TYPE_CHECKING:
    from dreadnode.samplers.optuna import OptunaSampler

__all__ = [
    "SAMPLER_REGISTRY",
    "ArchiveCell",
    "BoundarySampler",
    "FuzzingSampler",
    "GraphSampler",
    "GridSampler",
    "HopSkipJumpSampler",
    "ImageSampler",
    "MAPElitesSampler",
    "MutationTarget",
    "NESSampler",
    "OptunaSampler",
    "RandomImageSampler",
    "RandomSampler",
    "SeedEntry",
    "SimBASampler",
    "Strategy",
    "StrategyLibrarySampler",
    "StrategyStore",
    "ZOOSampler",
    "beam_search_sampler",
    "create_sampler",
    "fuzzing_sampler",
    "graph_neighborhood_sampler",
    "iterative_sampler",
    "list_samplers",
    "mapelites_sampler",
    "register_sampler",
    "strategy_library_sampler",
]


def __getattr__(name: str) -> t.Any:
    if name == "OptunaSampler":
        component = importlib.import_module("dreadnode.samplers.optuna").OptunaSampler
        globals()[name] = component
        return component
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
