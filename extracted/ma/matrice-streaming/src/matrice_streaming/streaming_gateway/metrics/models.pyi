"""Auto-generated stub for module: models."""
from typing import Any, Dict

from __future__ import annotations
from dataclasses import dataclass, field

# Classes
class PerCameraStats:
    """
    Statistics snapshot for a single camera, collected each reporting cycle.
    
        ``to_dict()`` produces the nested ``camera_reading`` / ``gateway_sending`` /
        ``frame_size_stats`` shape consumed by ``collector.py`` and sent over Kafka.
    """

    def to_dict(self: Any) -> Dict[str, Any]: ...
        """
        Map to the nested Kafka wire shape used by collector.py.
        
                Output structure:
                    {
                        "camera_id": ...,
                        "camera_reading": {"throughput": fps_stats, "latency": read_stats},
                        "gateway_sending": {"throughput": fps_stats, "latency": write_stats},
                        "frame_size_stats": ...,
                        **self.extra,
                    }
        """

