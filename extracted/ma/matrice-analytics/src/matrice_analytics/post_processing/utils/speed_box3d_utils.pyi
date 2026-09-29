"""Auto-generated stub for module: speed_box3d_utils."""
from typing import Any, Dict, List, Optional, Tuple

# Constants
logger: Any

# Functions
def footprint(det: Dict[str, Any], ground_indices: Any[int], width: int, height: int, min_corner_conf: float = 0.5, min_size_px: float = 12.0, margin_px: float = 2.0) -> Optional[Any.Any]:
    """
    The 4 ground-contact corners of a detection, ``(4, 2)`` pixels, or ``None``.
    
        ``None`` for anything that is not a trustworthy footprint: no keypoints, a corner
        below ``min_corner_conf``, a corner outside the frame (a vehicle cut off at the edge
        has corners the detector guessed), or a footprint too small to measure. Keypoints
        that arrive normalised (every coordinate within the unit square) are scaled up.
    """
    ...
def solve_camera(footprints: Any.Any, width: int, height: int, car_length_m: float = 4.5, car_width_m: float = 1.8, init_height_m: float = 8.0, max_dim_error: float = 0.15) -> Any:
    """
    Fit ``(f, tilt, roll, h)`` to ``footprints`` -- ``(N, 4, 2)`` pixels, cyclic order.
    """
    ...

# Classes
class Box3DFallback:
    # Collects car footprints from the first frame; solves the camera once triggered.
    #
    #     Triggered when the paint calibration has not produced a camera within
    #     ``after_seconds`` of frame time, or has declared the camera uncalibratable. Collection
    #     starts at once, so a camera that needs the fallback has its evidence ready by then.

    def __init__(self: Any, enabled: bool = True, after_seconds: float = 60.0, ground_indices: Any[int] = (0, 1, 2, 3), categories: Any[str] = ('car',), car_length_m: float = 4.5, car_width_m: float = 1.8, init_height_m: float = 8.0, min_footprints: int = 300, min_tracks: int = 20, retry_footprints: int = 300, max_footprints: int = 3000, min_corner_conf: float = 0.5, min_size_px: float = 12.0, max_dim_error: float = 0.15) -> None: ...

    def corners(self: Any, det: Dict[str, Any], width: int, height: int) -> Optional[Any.Any]:
        """
        This detection's footprint under this fallback's settings.
        """
        ...

    def footprints_seen(self: Any) -> int:
        """
        Usable footprints received so far. 0 means the detector sends no 3D corners.
        """
        ...

    def locate(self: Any, det: Dict[str, Any], width: int, height: int) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        ``(pixel, (along, across))`` of this vehicle's footprint centre, or ``None``.
        
                The centre of the four ground corners, each mapped onto the road first: on the
                road, so free of the height bias a box edge carries, and not tied to whichever
                corner happens to be lowest in the image.
        """
        ...

    def observe(self: Any, detections: List[Dict[str, Any]], frame_ts: float, width: int, height: int, paint_failed: bool) -> bool:
        """
        Collect this frame's footprints; solve when due. True the frame it succeeds.
        """
        ...

class Box3DPlane:
    # Maps a pixel to ``(along, across)`` metres on the road, like ``RoadPlane``.
    #
    #     Same interface as :class:`speed_geometry_utils.RoadPlane` -- ``project`` and
    #     ``metres_per_pixel`` -- so the fitting and uncertainty code runs on either unchanged.

    def __init__(self: Any, pp: Tuple[float, float], focal: float, tilt: float, roll: float, height_m: float, road_angle: float = 0.0) -> None: ...

    def ground(self: Any, x: float, y: float) -> Optional[Tuple[float, float]]:
        """
        Pixel -> world ``(X, Y)`` metres on the road, or ``None`` above the horizon.
        """
        ...

    def metres_per_pixel(self: Any, x: float, y: float, pixels: float) -> float:
        """
        Ground metres spanned by ``pixels`` of vertical wobble at this image point.
        """
        ...

    def pixel(self: Any, world_x: float, world_y: float) -> Tuple[float, float]:
        """
        World ``(X, Y)`` on the road -> pixel. The inverse of :meth:`ground`.
        """
        ...

    def project(self: Any, x: float, y: float) -> Optional[Tuple[float, float]]:
        """
        Pixel -> ``(along, across)`` in METRES, along being the road direction.
        """
        ...

class Box3DResult:
    # One solve: a plane, or the reason there is none.

    def __init__(self: Any, plane: Optional[Any] = None, reason: str = '', diagnostics: Optional[Dict[str, float]] = None) -> None: ...

    def ok(self: Any) -> bool: ...

