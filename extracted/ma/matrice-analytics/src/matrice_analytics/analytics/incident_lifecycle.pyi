"""Auto-generated stub for module: incident_lifecycle."""
from typing import Any, List

from .schemas import SEVERITY_ORDER, IncidentEvent, IncidentLifecycleState, LifecycleConfig, SeverityLevel

# Constants
logger: Any

# Classes
class IncidentLifecycle:
    # Per-camera incident lifecycle state machine.
    #
    #     Pure computation: no I/O.  Given a severity level for each frame it
    #     maintains per-camera state and emits :class:`IncidentEvent` instances
    #     when the confirmed severity level changes or an incident ends.
    #
    #     Args:
    #         config: Tunable consecutive-frame thresholds.

    def __init__(self: Any, config: Any | None = None) -> None:
        """
        Initialize with optional lifecycle configuration (defaults applied).
        """
        ...

    def get_all_states(self: Any) -> dict[str, Any]:
        """
        Return copies of all per-camera lifecycle states.
        """
        ...

    def get_state(self: Any, camera_id: str) -> Any | None:
        """
        Return a copy of the lifecycle state for a camera, or ``None``.
        """
        ...

    def process_frame(self: Any, camera_id: str, severity_level: Any, incident_quant: float, event_confidence: float, frame_ts: float, frame_id: str, incident_type: str) -> list[Any]:
        """
        Run one frame through the lifecycle for *camera_id*.
        
                Args:
                    camera_id: Unique camera identifier.
                    severity_level: Computed severity for this frame.
                    incident_quant: Quantitative incident measurement (0-100).
                    event_confidence: Maximum detection confidence (0-1).
                    frame_ts: Frame timestamp in seconds.
                    frame_id: Frame identifier string.
                    incident_type: Incident type key from the manifest.
        
                Returns:
                    List of ``IncidentEvent`` models emitted this frame (usually 0 or 1).
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear all per-camera state.
        """
        ...

    def reset_camera(self: Any, camera_id: str) -> None:
        """
        Clear state for a single camera.
        """
        ...

