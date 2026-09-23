"""Auto-generated stub for module: vehicle_speed_estimation."""
from typing import Any, Dict, Optional

from ..core.base import BaseProcessor, ConfigProtocol, ProcessingContext, ProcessingResult
from ..utils import apply_category_mapping
from ..utils.speed_fit_utils import baseline_slope, over_limit_pct, severity_for, uncertainty_pct
from ..utils.speed_geometry_utils import RoadPlane
from ..utils.speed_paint_calibration_utils import SelfCalibrator
from .vehicle_speed_estimation_config import FACTORS, UNIT_LABELS, VEHICLE_SPEED_ESTIMATION_SCHEMA, VehicleSpeedEstimationConfig

# Classes
class VehicleSpeedEstimationUseCase:
    # Measures vehicle speed using a camera recovered from the road's own markings.

    def __init__(self: Any) -> None: ...

    def get_config_schema(self: Any) -> Dict[str, Any]:
        """
        Get configuration schema for vehicle speed estimation.
        """
        ...

    def process(self: Any, data: Any, config: Any, input_bytes: Optional[Any] = None, context: Optional[Any] = None, stream_info: Optional[Dict[str, Any]] = None) -> Any:
        """
        Measure speed for every tracked vehicle in this frame.
        """
        ...

