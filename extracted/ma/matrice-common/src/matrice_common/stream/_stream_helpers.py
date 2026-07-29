"""Shared helper utilities for Redis and Kafka stream classes.

This module extracts common code patterns that were duplicated between sync and
async variants of RedisUtils and KafkaUtils, reducing code duplication while
keeping all public API signatures unchanged.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from collections import deque
from datetime import datetime, timezone
from typing import Any, Deque, Dict, List, Optional, Tuple, Union

# ---------------------------------------------------------------------------
# Standalone helper functions (no class dependency)
# ---------------------------------------------------------------------------


def safe_decode(value: Union[str, bytes], keep_binary: bool = True) -> Any:
    """Safely decode bytes to string, handling both str and bytes input.

    Args:
        value: Value to decode (str or bytes)
        keep_binary: If True, return bytes as-is if UTF-8 decoding fails

    Returns:
        Decoded string or original bytes if decoding fails and keep_binary=True
    """
    if isinstance(value, bytes):
        if keep_binary:
            try:
                return value.decode("utf-8")
            except UnicodeDecodeError:
                return value
        else:
            return value.decode("utf-8")
    elif isinstance(value, str):
        return value
    else:
        return str(value)


def serialize_value(value: Any) -> bytes:
    """Serialize message value to bytes.

    Args:
        value: Message value to serialize

    Returns:
        Serialized value as bytes
    """
    if isinstance(value, dict):
        return json.dumps(value).encode("utf-8")
    elif isinstance(value, str):
        return value.encode("utf-8")
    elif isinstance(value, bytes):
        return value
    else:
        return str(value).encode("utf-8")


def serialize_key(key: Any) -> Optional[bytes]:
    """Serialize message key to bytes.

    Args:
        key: Message key to serialize

    Returns:
        Serialized key as bytes or None
    """
    if key is None:
        return None
    elif isinstance(key, str):
        return key.encode("utf-8")
    elif isinstance(key, bytes):
        return key
    else:
        return str(key).encode("utf-8")


def parse_message_value(value: bytes) -> Any:
    """Parse message value from bytes.

    Args:
        value: Message value in bytes

    Returns:
        Parsed value or original bytes if parsing fails
    """
    if not value:
        return None

    try:
        return json.loads(value.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return value


def parse_stream_fields(fields: Dict) -> Tuple[Dict, Optional[str], int]:
    """Parse raw Redis stream fields into structured data.

    Returns:
        Tuple of (parsed_data, message_key, total_size)
    """
    parsed_data: Dict[str, Any] = {}
    message_key = None
    total_size = 0

    for field_name, field_value in fields.items():
        field_name = safe_decode(field_name)

        # Skip UTF-8 decode for binary content fields to preserve raw bytes
        if isinstance(field_value, bytes) and ("__content" in field_name or field_name == "content"):
            total_size += len(field_name) + len(field_value)
            parsed_data[field_name] = field_value
            continue

        field_value = safe_decode(field_value)
        total_size += len(field_name) + len(field_value)

        if field_name == "_message_key":
            message_key = field_value
            continue

        try:
            parsed_data[field_name] = json.loads(field_value)
        except ValueError:
            parsed_data[field_name] = field_value

    return parsed_data, message_key, total_size


def compute_dynamic_batch_size(avg_throughput: float) -> int:
    """Return the optimal batch size for the given throughput level.

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
    if avg_throughput < 1000:
        return 50
    elif avg_throughput < 10000:
        return 200
    elif avg_throughput < 50000:
        return 500
    else:
        return 1000


# ---------------------------------------------------------------------------
# Latency statistics helpers (shared by Redis and Kafka aggregation)
# ---------------------------------------------------------------------------

_SKIP_NAMES = {"(timeout)", "(error)", "unknown"}


def new_stream_stats(name: str, name_key: str, add_op: str, read_op: Union[str, tuple]) -> Dict:
    """Create a fresh statistics dict for a stream/topic.

    Args:
        name: Stream or topic name
        name_key: Key to store the name under ("stream" or "topic")
        add_op: Operation name for add/publish counting
        read_op: Operation name (or tuple of names) for read/consume counting

    Returns:
        Dict with initial zero counters
    """
    return {
        name_key: name,
        "_add_op": add_op,
        "_read_op": read_op,
        "addCount": 0,
        "readCount": 0,
        "totalLatency": 0,
        "latencies": [],
        "avgLatency": 0,
        "minlatency": float("inf"),
        "maxlatency": 0,
    }


def accumulate_metric(stats: Dict, metric: Dict) -> None:
    """Accumulate a single metric into stream/topic stats.

    Args:
        stats: The running statistics dict (modified in place)
        metric: A single metric entry
    """
    operation = metric.get("operation", "unknown")
    success = metric.get("success", False)
    duration_ms = metric.get("duration_ms", 0)

    add_op = stats.get("_add_op", "add")
    read_op = stats.get("_read_op", "read")

    if operation == add_op and success:
        stats["addCount"] += 1
    elif (isinstance(read_op, tuple) and operation in read_op) or operation == read_op:
        if success:
            stats["readCount"] += 1

    if success and duration_ms > 0:
        latency_ns = int(duration_ms * 1_000_000)
        stats["latencies"].append(latency_ns)
        stats["totalLatency"] += latency_ns
        stats["minlatency"] = min(stats["minlatency"], latency_ns)
        stats["maxlatency"] = max(stats["maxlatency"], latency_ns)


def finalize_stats(all_stats: Dict[str, Dict]) -> None:
    """Compute averages and remove temporary fields from all stats dicts.

    Args:
        all_stats: Mapping of name -> stats dict (modified in place)
    """
    for stats in all_stats.values():
        if stats["latencies"]:
            stats["avgLatency"] = stats["totalLatency"] // len(stats["latencies"])
        else:
            stats["avgLatency"] = 0
            stats["minlatency"] = 0
        del stats["latencies"]
        # Remove internal helper keys
        stats.pop("_add_op", None)
        stats.pop("_read_op", None)


def aggregate_redis_metrics(raw_metrics: List[Dict], host: str, port: int) -> Dict:
    """Aggregate raw Redis metrics into the API format expected by backend.

    Works for both sync and async Redis classes.

    Args:
        raw_metrics: List of raw metric dictionaries
        host: Redis host
        port: Redis port

    Returns:
        Aggregated metrics payload dict
    """
    stream_stats: Dict[str, Dict] = {}
    current_time = datetime.now(timezone.utc).isoformat()

    for metric in raw_metrics:
        stream = metric.get("stream", "unknown")
        if stream in _SKIP_NAMES:
            continue

        if stream not in stream_stats:
            stream_stats[stream] = new_stream_stats(stream, "stream", "add", ("read", "get_message"))
        accumulate_metric(stream_stats[stream], metric)

    finalize_stats(stream_stats)

    return {
        "stream": list(stream_stats.values()),
        "status": "success",
        "host": host,
        "port": str(port),
        "createdAt": current_time,
        "updatedAt": current_time,
    }


def aggregate_kafka_metrics(raw_metrics: List[Dict], ip: str, port: str) -> Dict:
    """Aggregate raw Kafka metrics into the API format expected by backend.

    Works for both sync and async Kafka classes.

    Args:
        raw_metrics: List of raw metric dictionaries
        ip: Kafka broker IP
        port: Kafka broker port

    Returns:
        Aggregated metrics payload dict
    """
    topic_stats: Dict[str, Dict] = {}
    current_time = datetime.now(timezone.utc).isoformat()

    for metric in raw_metrics:
        topic = metric.get("topic", "unknown")
        if topic in _SKIP_NAMES:
            continue

        if topic not in topic_stats:
            topic_stats[topic] = new_stream_stats(topic, "topic", "produce", "consume")
            # Kafka uses different counter names
            topic_stats[topic]["publishCount"] = 0
            topic_stats[topic]["consumeCount"] = 0
        stats = topic_stats[topic]

        operation = metric.get("operation", "unknown")
        success = metric.get("success", False)
        duration_ms = metric.get("duration_ms", 0)

        if operation == "produce" and success:
            stats["publishCount"] += 1
        elif operation == "consume" and success:
            stats["consumeCount"] += 1

        if success and duration_ms > 0:
            latency_ns = int(duration_ms * 1_000_000)
            stats["latencies"].append(latency_ns)
            stats["totalLatency"] += latency_ns
            stats["minlatency"] = min(stats["minlatency"], latency_ns)
            stats["maxlatency"] = max(stats["maxlatency"], latency_ns)

    finalize_stats(topic_stats)

    # Remove internal keys that Kafka API doesn't need
    for stats in topic_stats.values():
        stats.pop("addCount", None)
        stats.pop("readCount", None)

    return {
        "topic": list(topic_stats.values()),
        "status": "success",
        "ip": ip,
        "port": port,
        "granularity": "minute",
        "createdAt": current_time,
        "updatedAt": current_time,
    }


# ---------------------------------------------------------------------------
# MetricsReporterMixin — shared metrics infrastructure
# ---------------------------------------------------------------------------


class MetricsReporterMixin:
    """Mixin providing common metrics infrastructure for stream classes.

    Subclasses must define:
        _metrics_lock: threading.Lock
        _metrics_log: Deque[Dict[str, Any]]
        _metrics_reporting_config: Optional[Dict[str, Any]]
        _metrics_thread: Optional[threading.Thread]
        _metrics_stop_event: threading.Event

    And must implement:
        _build_metric_entry(...) -> Dict  — build the metric dict with class-specific fields
        _aggregate_metrics_for_api(raw_metrics) -> Dict
        _get_api_path() -> str  — the POST endpoint for metrics
        _get_reporter_label() -> str  — label for log messages (e.g. "Redis" or "Kafka")
    """

    # -- Attributes provided by subclasses -----------------------------------

    _metrics_lock: threading.Lock
    _metrics_log: Deque[Dict[str, Any]]
    _metrics_reporting_config: Optional[Dict[str, Any]]
    _metrics_thread: Optional[threading.Thread]
    _metrics_stop_event: threading.Event

    # -- Provided by the mixin -----------------------------------------------

    def get_metrics(self, clear_after_read: bool = False) -> List[Dict]:
        """Get collected metrics for aggregation and reporting.

        Args:
            clear_after_read: Whether to clear metrics after reading

        Returns:
            List of metric dictionaries
        """
        with self._metrics_lock:
            metrics = list(self._metrics_log)
            if clear_after_read:
                self._metrics_log.clear()
        return metrics

    def _start_metrics_reporter(self, thread_name: str) -> None:
        """Start the background metrics reporter thread if not already running.

        Args:
            thread_name: Name for the background thread
        """
        if not self._metrics_thread or not self._metrics_thread.is_alive():
            self._metrics_stop_event.clear()
            t = threading.Thread(target=self._metrics_reporter_worker, daemon=True, name=thread_name)
            self._metrics_thread = t
            t.start()

    def _metrics_reporter_worker(self) -> None:
        """Background thread worker for sending metrics to backend API."""
        label = self._get_reporter_label()
        logging.info("%s metrics reporter thread started", label)

        while not self._metrics_stop_event.is_set():
            try:
                cfg = self._metrics_reporting_config
                if not cfg or not cfg.get("enabled"):
                    self._metrics_stop_event.wait(10)
                    continue

                interval = cfg.get("interval", 60)

                if self._metrics_stop_event.wait(interval):
                    break

                self._collect_and_send_metrics()

            except Exception as exc:
                logging.exception("Error in %s metrics reporter thread: %s", label, exc)
                self._metrics_stop_event.wait(30)

        logging.info("%s metrics reporter thread stopped", label)

    def _collect_and_send_metrics(self) -> None:
        """Collect metrics and send them to the backend API."""
        label = self._get_reporter_label()
        collection_key = self._get_metrics_collection_key()
        try:
            raw_metrics = self.get_metrics(clear_after_read=True)

            if not raw_metrics:
                logging.debug("No new %s metrics to report", label)
                return

            aggregated_data = self._aggregate_metrics_for_api(raw_metrics)

            if aggregated_data.get(collection_key):
                success = self._send_metrics_to_api(aggregated_data)
                if success:
                    logging.info("Successfully sent %d %s metrics to backend API", len(raw_metrics), label)
                    if "Redis" in label:
                        # Demoted from INFO: dumping the full raw_metrics deque
                        # (up to 10k dicts) on every report was megabytes/interval
                        # on busy nodes. Count is already logged above.
                        logging.debug("%s Metrics: %s", label, raw_metrics)
                else:
                    logging.warning("Failed to send %s metrics to backend API", label)
            else:
                logging.debug("No %s-level metrics to report", collection_key)

        except Exception as exc:
            logging.exception("Error collecting and sending %s metrics: %s", label, exc)

    def _send_metrics_to_api(self, aggregated_metrics: Dict) -> bool:
        """Send aggregated metrics to backend API using RPC client.

        Args:
            aggregated_metrics: Metrics data in API format

        Returns:
            bool: True if successful, False otherwise
        """
        label = self._get_reporter_label()
        try:
            cfg: Dict[str, Any] = self._metrics_reporting_config or {}
            rpc_client = cfg.get("rpc_client")
            if not rpc_client:
                logging.error("No RPC client configured for %s metrics reporting", label)
                return False

            response = rpc_client.post(path=self._get_api_path(), payload=aggregated_metrics, timeout=30)

            if response and response.get("success"):
                logging.debug("Successfully sent %s metrics to backend API", label)
                return True
            else:
                error_msg = response.get("message", "Unknown error") if response else "No response"
                logging.error("Backend API rejected %s metrics: %s", label, error_msg)
                return False

        except Exception as exc:
            logging.exception("Error sending %s metrics to API: %s", label, exc)
            return False

    def stop_metrics_reporting(self) -> None:
        """Stop the background metrics reporting thread."""
        label = self._get_reporter_label()
        if self._metrics_reporting_config:
            self._metrics_reporting_config["enabled"] = False

        if self._metrics_thread and self._metrics_thread.is_alive():
            logging.info("Stopping %s metrics reporting thread...", label)
            self._metrics_stop_event.set()
            self._metrics_thread.join(timeout=5)
            if self._metrics_thread.is_alive():
                logging.warning("%s metrics reporting thread did not stop gracefully", label)
            else:
                logging.info("%s metrics reporting thread stopped", label)

    # -- Abstract methods subclasses must implement --------------------------

    def _get_reporter_label(self) -> str:
        raise NotImplementedError

    def _get_metrics_collection_key(self) -> str:
        """Return the key used to check if aggregated data has entries (e.g. 'stream' or 'topic')."""
        raise NotImplementedError

    def _get_api_path(self) -> str:
        raise NotImplementedError

    def _aggregate_metrics_for_api(self, raw_metrics: List[Dict]) -> Dict:
        raise NotImplementedError
