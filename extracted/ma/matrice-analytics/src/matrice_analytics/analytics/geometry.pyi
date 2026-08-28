"""Auto-generated stub for module: geometry."""
from typing import Any, Dict, Union

from ..post_processing.utils.counting_utils import ABLineCounter, PolygonCounter, parse_line_config, polygon_offset_inward

# Constants
logger: Any

# Functions
def assign_detections_to_zones(detections: list[dict[str, Any]], zones_px: dict[str, Any.Any], use_foot_center: bool = False) -> dict[str, list[dict[str, Any]]]:
    """
    Partition detections into named zones by point-in-polygon containment.
    
        Each detection is assigned to the **first** zone whose polygon contains
        the detection's reference point.  Detections that fall in no zone are
        discarded.
    
        Args:
            detections: Raw detection dicts (with ``bounding_box`` / ``bbox``).
            zones_px: Mapping of zone name to polygon vertices as a numpy array
                of shape ``(N, 2)`` in **pixel** coordinates (``int32``).
            use_foot_center: Use bottom-center of bbox instead of center.
    
        Returns:
            Dict mapping ``zone_name`` to the list of detections whose reference
            point falls inside that zone.
    """
    ...
def build_zone_polygons_px(zones_normalized: dict[str, list[list[float]]], width: int, height: int) -> dict[str, Any.Any]:
    """
    Denormalize zone polygons and convert to numpy arrays for OpenCV.
    
        Args:
            zones_normalized: Zone name to list of ``[x_norm, y_norm]`` vertices.
            width: Frame width in pixels.
            height: Frame height in pixels.
    
        Returns:
            Dict mapping zone name to ``np.ndarray`` of shape ``(N, 1, 2)``
            with ``int32`` dtype (format expected by ``cv2.pointPolygonTest``).
    """
    ...
def create_counter_from_zone_config(zone_config_px: dict[str, Any], method: str = 'abline', in_direction: str = 'A_to_B', use_foot_center: bool = False, inner_polygon_offset: int = _DEFAULT_INNER_POLYGON_OFFSET) -> Union[Any, Any]:
    """
    Create a counting counter from a pixel-space zone_config.
    
        The ``method`` parameter selects which counter to build:
    
        * ``"abline"``: requires >= 2 lines in ``zone_config_px["lines"]``.
          The first two lines become ``line_a`` and ``line_b`` for ``ABLineCounter``.
        * ``"polygon"``: requires >= 1 zone in ``zone_config_px["zones"]``.
          First zone is ``outer_polygon``; second (if present) is ``inner_polygon``.
          When only one zone is provided, ``inner_polygon`` is auto-computed via
          ``polygon_offset_inward``.
    
        Args:
            zone_config_px: Dict with ``"lines"`` and/or ``"zones"`` in pixel coords.
            method: ``"abline"`` or ``"polygon"``.
            in_direction: For abline -- ``"A_to_B"`` or ``"B_to_A"``.
            use_foot_center: Use bottom-center of bbox instead of center.
            inner_polygon_offset: Pixel inset for auto-computed inner polygon.
    
        Returns:
            An ``ABLineCounter`` or ``PolygonCounter`` instance.
    
        Raises:
            ValueError: If required geometry is missing for the chosen method.
    """
    ...
def denormalize_zone_config(zone_config: dict[str, Any], width: int, height: int) -> dict[str, Any]:
    """
    Convert a zone_config from normalized (0-1) coords to integer pixel coords.
    
        Args:
            zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized coords.
            width: Frame width in pixels.
            height: Frame height in pixels.
    
        Returns:
            Deep copy of zone_config with all coordinates converted to pixels.
    """
    ...
def get_detection_reference_point(detection: dict[str, Any], use_foot_center: bool = False) -> tuple[float, float] | None:
    """
    Extract the reference point (center or foot-center) from a detection.
    
        Args:
            detection: Dict with ``bounding_box`` or ``bbox`` key.
            use_foot_center: If ``True``, return the bottom-center of the bbox
                instead of the geometric center.
    
        Returns:
            ``(x, y)`` in the same coordinate space as the bounding box, or
            ``None`` if the bbox is missing / invalid.
    """
    ...
def point_in_polygon(point: tuple[float, float], polygon: Any.Any) -> bool:
    """
    Test whether *point* lies inside *polygon* using OpenCV.
    
        Args:
            point: ``(x, y)`` in pixel coordinates.
            polygon: Numpy array of shape ``(N, 2)`` with integer pixel vertices.
    
        Returns:
            ``True`` if the point is inside or on the edge of the polygon.
    """
    ...
