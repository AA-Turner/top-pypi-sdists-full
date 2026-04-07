from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ScalingGroupResourceRequest:
    """Resource requests for a scaling group container.

    Parameters
    ----------
    cpu
        CPU limit (e.g. "2", "500m").
    memory
        Memory limit (e.g. "4Gi", "512Mi").
    gpu
        GPU spec as "type:count" (e.g. "nvidia-tesla-t4:1").
    """

    cpu: Optional[str] = None
    memory: Optional[str] = None
    gpu: Optional[str] = None


@dataclass
class AutoScalingSpec:
    """Autoscaling configuration for a scaling group.

    Parameters
    ----------
    min_replicas
        Minimum number of replicas for autoscaling.
    max_replicas
        Maximum number of replicas for autoscaling.
    target_cpu_utilization_percentage
        Target CPU utilization for autoscaling.
    """

    min_replicas: int = 1
    max_replicas: int = 1
    target_cpu_utilization_percentage: Optional[int] = None
