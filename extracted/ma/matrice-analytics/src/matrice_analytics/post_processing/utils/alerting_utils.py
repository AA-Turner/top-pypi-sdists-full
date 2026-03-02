"""
Alerting utilities for post-processing operations.
"""

import time
from typing import List, Dict, Any
from .filter_utils import filter_by_confidence


class AlertingLibrary:
    """Library class for handling alerting and event triggering."""
    
    def __init__(self):
        self.alert_history = []
    
    def filter_by_confidence(self, results: Any, threshold: float) -> Any:
        """Filter results by confidence threshold."""
        return filter_by_confidence(results, threshold)
    
    def trigger_events(self, results: Any, category_count_threshold: Dict[str, int] = None,
                      category_triggers: List[str] = None) -> List[Dict]:
        """Trigger events based on detection conditions."""
        triggered_events = []
        
        # Count-based triggers
        if category_count_threshold:
            category_counts = self._count_by_category(results)
            
            # Handle "all" threshold
            if "all" in category_count_threshold:
                total_detections = sum(category_counts.values())
                if total_detections >= category_count_threshold["all"]:
                    event = {
                        "event_type": "count_threshold_exceeded",
                        "threshold": category_count_threshold["all"],
                        "actual_count": total_detections,
                        "timestamp": time.time()
                    }
                    triggered_events.append(event)
                    self.alert_history.append(event)
            
            # Category-specific count thresholds
            for category, threshold in category_count_threshold.items():
                if category != "all" and category_counts.get(category, 0) >= threshold:
                    event = {
                        "event_type": "category_count_threshold_exceeded",
                        "category": category,
                        "threshold": threshold,
                        "actual_count": category_counts[category],
                        "timestamp": time.time()
                    }
                    triggered_events.append(event)
                    self.alert_history.append(event)
        
        # Category-based triggers
        if category_triggers:
            detected_categories = self._get_detected_categories(results)
            for trigger_category in category_triggers:
                if trigger_category in detected_categories:
                    event = {
                        "event_type": "category_detected",
                        "category": trigger_category,
                        "timestamp": time.time()
                    }
                    triggered_events.append(event)
                    self.alert_history.append(event)
        
        return triggered_events
    
    def _count_total_detections(self, results: Any) -> int:
        """Count total detections in results."""
        total_detections = 0
        if isinstance(results, list):
            total_detections = len(results)
        elif isinstance(results, dict):
            for detections in results.values():
                if isinstance(detections, list):
                    total_detections += len(detections)
        return total_detections
    
    def _get_detected_categories(self, results: Any) -> set:
        """Get set of detected categories from results."""
        detected_categories = set()
        if isinstance(results, list):
            detected_categories.update(r.get("category", "") for r in results)
        elif isinstance(results, dict):
            for detections in results.values():
                if isinstance(detections, list):
                    detected_categories.update(d.get("category", "") for d in detections)
        return detected_categories
    
    def _count_by_category(self, results: Any) -> Dict[str, int]:
        """Count detections by category."""
        category_counts = {}
        if isinstance(results, list):
            for result in results:
                category = result.get("category", "unknown")
                category_counts[category] = category_counts.get(category, 0) + 1
        elif isinstance(results, dict):
            for detections in results.values():
                if isinstance(detections, list):
                    for detection in detections:
                        category = detection.get("category", "unknown")
                        category_counts[category] = category_counts.get(category, 0) + 1
        return category_counts
    
    def get_alert_history(self) -> List[Dict]:
        """Get history of triggered alerts."""
        return self.alert_history.copy()
    
    def clear_alert_history(self):
        """Clear alert history."""
        self.alert_history.clear()


# Convenience alerting functions
class SimpleAlerter:
    """Simple alerter for common use cases."""
    
    def __init__(self):
        self.alerting_lib = AlertingLibrary()
    
    def check_threshold_alert(self, results: Any, threshold: int, category: str = "all") -> Dict:
        """Check if count exceeds threshold."""
        alerts = self.alerting_lib.trigger_events(
            results, 
            category_count_threshold={category: threshold}
        )
        return {
            "alert_triggered": len(alerts) > 0,
            "alerts": alerts,
            "threshold": threshold,
            "category": category
        }
    
    def check_zone_occupancy_alert(self, zone_counts: Dict[str, int], 
                                  zone_thresholds: Dict[str, int]) -> Dict:
        """Check zone occupancy alerts."""
        alerts = []
        for zone_name, count in zone_counts.items():
            if zone_name in zone_thresholds and count >= zone_thresholds[zone_name]:
                alert = {
                    "event_type": "zone_occupancy_exceeded",
                    "zone": zone_name,
                    "count": count,
                    "threshold": zone_thresholds[zone_name],
                    "timestamp": time.time()
                }
                alerts.append(alert)
        
        return {
            "alert_triggered": len(alerts) > 0,
            "alerts": alerts,
            "zone_thresholds": zone_thresholds
        }
    
    def check_dwell_time_alert(self, track_dwell_times: Dict[int, float], 
                              max_dwell_time: float) -> Dict:
        """Check dwell time alerts."""
        alerts = []
        for track_id, dwell_time in track_dwell_times.items():
            if dwell_time >= max_dwell_time:
                alert = {
                    "event_type": "dwell_time_exceeded",
                    "track_id": track_id,
                    "dwell_time": dwell_time,
                    "threshold": max_dwell_time,
                    "timestamp": time.time()
                }
                alerts.append(alert)
        
        return {
            "alert_triggered": len(alerts) > 0,
            "alerts": alerts,
            "max_dwell_time": max_dwell_time
        }


def trigger_alerts(results: Any, category_count_threshold: Dict[str, int] = None,
                  category_triggers: List[str] = None) -> List[Dict]:
    """
    Convenience function to trigger alerts.
    
    Args:
        results: Detection/tracking results
        category_count_threshold: Count thresholds by category
        category_triggers: Categories that should trigger alerts
        
    Returns:
        List of triggered alert events
    """
    alerter = AlertingLibrary()
    return alerter.trigger_events(results, category_count_threshold, category_triggers)


def check_threshold_alert(results: Any, threshold: int, category: str = "all") -> Dict:
    """Check if count exceeds threshold."""
    alerter = SimpleAlerter()
    return alerter.check_threshold_alert(results, threshold, category)


def check_zone_occupancy_alert(zone_counts: Dict[str, int], 
                              zone_thresholds: Dict[str, int]) -> Dict:
    """Check zone occupancy alerts."""
    alerter = SimpleAlerter()
    return alerter.check_zone_occupancy_alert(zone_counts, zone_thresholds)


def check_dwell_time_alert(track_dwell_times: Dict[int, float], 
                          max_dwell_time: float) -> Dict:
    """Check dwell time alerts."""
    alerter = SimpleAlerter()
    return alerter.check_dwell_time_alert(track_dwell_times, max_dwell_time) 