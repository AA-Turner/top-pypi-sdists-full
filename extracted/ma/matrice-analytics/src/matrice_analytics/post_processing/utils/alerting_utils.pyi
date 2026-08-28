"""Auto-generated stub for module: alerting_utils."""
from typing import Any, Dict, List

from .filter_utils import filter_by_confidence

# Functions
def check_dwell_time_alert(track_dwell_times: Dict[int, float], max_dwell_time: float) -> Dict:
    """
    Check dwell time alerts.
    """
    ...
def check_threshold_alert(results: Any, threshold: int, category: str = 'all') -> Dict:
    """
    Check if count exceeds threshold.
    """
    ...
def check_zone_occupancy_alert(zone_counts: Dict[str, int], zone_thresholds: Dict[str, int]) -> Dict:
    """
    Check zone occupancy alerts.
    """
    ...
def trigger_alerts(results: Any, category_count_threshold: Dict[str, int] = None, category_triggers: List[str] = None) -> List[Dict]:
    """
    Convenience function to trigger alerts.
    
    Args:
        results: Detection/tracking results
        category_count_threshold: Count thresholds by category
        category_triggers: Categories that should trigger alerts
    
    Returns:
        List of triggered alert events
    """
    ...

# Classes
class AlertingLibrary:
    # Library class for handling alerting and event triggering.

    def __init__(self: Any) -> None: ...

    def clear_alert_history(self: Any) -> Any:
        """
        Clear alert history.
        """
        ...

    def filter_by_confidence(self: Any, results: Any, threshold: float) -> Any:
        """
        Filter results by confidence threshold.
        """
        ...

    def get_alert_history(self: Any) -> List[Dict]:
        """
        Get history of triggered alerts.
        """
        ...

    def trigger_events(self: Any, results: Any, category_count_threshold: Dict[str, int] = None, category_triggers: List[str] = None) -> List[Dict]:
        """
        Trigger events based on detection conditions.
        """
        ...

class SimpleAlerter:
    # Simple alerter for common use cases.

    def __init__(self: Any) -> None: ...

    def check_dwell_time_alert(self: Any, track_dwell_times: Dict[int, float], max_dwell_time: float) -> Dict:
        """
        Check dwell time alerts.
        """
        ...

    def check_threshold_alert(self: Any, results: Any, threshold: int, category: str = 'all') -> Dict:
        """
        Check if count exceeds threshold.
        """
        ...

    def check_zone_occupancy_alert(self: Any, zone_counts: Dict[str, int], zone_thresholds: Dict[str, int]) -> Dict:
        """
        Check zone occupancy alerts.
        """
        ...

