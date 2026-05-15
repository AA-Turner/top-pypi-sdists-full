"""Auto-generated stub for module: _stream_helpers."""
from typing import Any, Dict, List, Optional, Tuple, Union

# Functions
def accumulate_metric(stats: Dict, metric: Dict) -> None:
    """
    Accumulate a single metric into stream/topic stats.
    
        Args:
            stats: The running statistics dict (modified in place)
            metric: A single metric entry
    """
    ...
def aggregate_kafka_metrics(raw_metrics: List[Dict], ip: str, port: str) -> Dict:
    """
    Aggregate raw Kafka metrics into the API format expected by backend.
    
        Works for both sync and async Kafka classes.
    
        Args:
            raw_metrics: List of raw metric dictionaries
            ip: Kafka broker IP
            port: Kafka broker port
    
        Returns:
            Aggregated metrics payload dict
    """
    ...
def aggregate_redis_metrics(raw_metrics: List[Dict], host: str, port: int) -> Dict:
    """
    Aggregate raw Redis metrics into the API format expected by backend.
    
        Works for both sync and async Redis classes.
    
        Args:
            raw_metrics: List of raw metric dictionaries
            host: Redis host
            port: Redis port
    
        Returns:
            Aggregated metrics payload dict
    """
    ...
def compute_dynamic_batch_size(avg_throughput: float) -> int:
    """
    Return the optimal batch size for the given throughput level.
    
        Adaptive batching strategy:
        - Low throughput (< 1K msg/sec): batch_size = 50 (responsive, low latency)
        - Medium throughput (1K-10K msg/sec): batch_size = 200 (balanced)
        - High throughput (10K-50K msg/sec): batch_size = 500 (efficient batching)
        - Very high throughput (> 50K msg/sec): batch_size = 1000 (maximum efficiency)
    
        Args:
            avg_throughput: Average messages per second
    
        Returns:
            Optimal batch size integer
    """
    ...
def finalize_stats(all_stats: Dict[str, Dict]) -> None:
    """
    Compute averages and remove temporary fields from all stats dicts.
    
        Args:
            all_stats: Mapping of name -> stats dict (modified in place)
    """
    ...
def new_stream_stats(name: str, name_key: str, add_op: str, read_op: Union[str, tuple]) -> Dict:
    """
    Create a fresh statistics dict for a stream/topic.
    
        Args:
            name: Stream or topic name
            name_key: Key to store the name under ("stream" or "topic")
            add_op: Operation name for add/publish counting
            read_op: Operation name (or tuple of names) for read/consume counting
    
        Returns:
            Dict with initial zero counters
    """
    ...
def parse_message_value(value: Any) -> Any:
    """
    Parse message value from bytes.
    
        Args:
            value: Message value in bytes
    
        Returns:
            Parsed value or original bytes if parsing fails
    """
    ...
def parse_stream_fields(fields: Dict) -> Tuple[Dict, Optional[str], int]:
    """
    Parse raw Redis stream fields into structured data.
    
        Returns:
            Tuple of (parsed_data, message_key, total_size)
    """
    ...
def safe_decode(value: Union[str, Any], keep_binary: bool = True) -> Any:
    """
    Safely decode bytes to string, handling both str and bytes input.
    
        Args:
            value: Value to decode (str or bytes)
            keep_binary: If True, return bytes as-is if UTF-8 decoding fails
    
        Returns:
            Decoded string or original bytes if decoding fails and keep_binary=True
    """
    ...
def serialize_key(key: Any) -> Optional[Any]:
    """
    Serialize message key to bytes.
    
        Args:
            key: Message key to serialize
    
        Returns:
            Serialized key as bytes or None
    """
    ...
def serialize_value(value: Any) -> Any:
    """
    Serialize message value to bytes.
    
        Args:
            value: Message value to serialize
    
        Returns:
            Serialized value as bytes
    """
    ...

# Classes
class MetricsReporterMixin:
    # Mixin providing common metrics infrastructure for stream classes.
    #
    #     Subclasses must define:
    #         _metrics_lock: threading.Lock
    #         _metrics_log: Deque[Dict[str, Any]]
    #         _metrics_reporting_config: Optional[Dict[str, Any]]
    #         _metrics_thread: Optional[threading.Thread]
    #         _metrics_stop_event: threading.Event
    #
    #     And must implement:
    #         _build_metric_entry(...) -> Dict  — build the metric dict with class-specific fields
    #         _aggregate_metrics_for_api(raw_metrics) -> Dict
    #         _get_api_path() -> str  — the POST endpoint for metrics
    #         _get_reporter_label() -> str  — label for log messages (e.g. "Redis" or "Kafka")

    def get_metrics(self: Any, clear_after_read: bool = False) -> List[Dict]:
        """
        Get collected metrics for aggregation and reporting.
        
                Args:
                    clear_after_read: Whether to clear metrics after reading
        
                Returns:
                    List of metric dictionaries
        """
        ...

    def stop_metrics_reporting(self: Any) -> None:
        """
        Stop the background metrics reporting thread.
        """
        ...

