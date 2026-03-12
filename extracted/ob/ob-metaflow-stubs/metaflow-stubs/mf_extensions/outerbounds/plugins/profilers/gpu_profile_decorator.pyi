######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.21.1+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-03-12T00:19:49.760870                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.user_decorators.user_step_decorator

from .....user_decorators.user_step_decorator import StepMutator as StepMutator
from .....user_decorators.user_step_decorator import user_step_decorator as user_step_decorator
from ...profilers.gpu import GPUProfiler as GPUProfiler
from ...profilers.gpu_card_utils import build_subprocess_config as build_subprocess_config

class gpu_profile(metaflow.user_decorators.user_step_decorator.StepMutator, metaclass=metaflow.user_decorators.user_step_decorator.UserStepDecoratorMeta):
    """
    Monitors GPU utilization and memory usage during a step.
    
    Produces a live-updating Metaflow card with:
    
    - Driver and CUDA version info
    - Device summary (ID, type, memory)
    - Multi-GPU interconnect topology (when multiple GPUs are present)
    - Peak utilization table
    - Per-device time-series charts for GPU utilization and memory
    
    Profiling runs with negligible overhead on your training loop.
    
    Readings are stored up to the ``max_memory_mb`` limit. When full,
    the oldest readings are dropped automatically. At the defaults
    (100 MB, 1-second interval), coverage is approximately:
    
    - **1 GPU:** ~4.5 days
    - **4 GPUs:** ~1.1 days
    - **8 GPUs:** ~13.5 hours
    
    Increase ``max_memory_mb`` for longer runs; decrease it on large
    multi-GPU nodes to save memory.
    
    The full set of retained readings is saved as an artifact at step
    end, so the artifact size is proportional to ``max_memory_mb``.
    
    Artifacts (when ``include_artifacts=True``):
    
    - ``{artifact_prefix}num_gpus``: number of GPUs detected.
    - ``{artifact_prefix}data``: dict with per-GPU time series,
      driver/CUDA versions, device metadata, and interconnect topology.
    
    Parameters
    ----------
    interval : int, default 1
        How often to sample GPU metrics, in seconds.
    max_memory_mb : int, default 100
        Memory budget in MB for storing GPU readings. Controls how
        far back readings extend before the oldest are dropped.
    include_artifacts : bool, default True
        Whether to save profiling data as Metaflow artifacts.
    artifact_prefix : str, default ``"gpu_profile_"``
        Prefix for artifact names.
    """
    def init(self, **kwargs):
        ...
    def mutate(self, mutable_step):
        ...
    @classmethod
    def __init_subclass__(cls_, **_kwargs):
        ...
    ...

