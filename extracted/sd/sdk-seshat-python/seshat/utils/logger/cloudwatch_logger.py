import atexit
import json
import os
import threading
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from seshat.utils.logger.base_logger import BaseLogger, LogLevel, LogConfig


class CloudWatchLogger(BaseLogger):
    """
    AWS CloudWatch Logs logger implementing BaseLogger interface.

    Sends logs to CloudWatch with batching support, respecting API limits.

    Environment Variables:
        AWS_ACCESS_KEY: IAM access key
        AWS_SECRET_ACCESS_KEY: IAM secret key
        AWS_REGION: AWS region (default: us-east-1)
        AWS_LOG_RETENTION_DAYS: Log retention in days (default: 7)
        CLOUDWATCH_DEBOUNCE_DELAY: Batch wait time in seconds (default: 10)
        CLOUDWATCH_CHUNK_SIZE: Batch size threshold (default: 100)
        HEISENBERG_JOB_NAME: Pipeline name for log group (default: unknown)
    """

    # CloudWatch API Limits
    MAX_BATCH_SIZE_BYTES = 1_048_576  # 1MB
    MAX_BATCH_COUNT = 10_000
    MAX_EVENT_SIZE_BYTES = 262_144  # 256KB
    EVENT_OVERHEAD_BYTES = 26

    def __init__(self, pipeline_name: str, config: Optional[LogConfig] = None):
        """
        Initialize CloudWatch logger.

        Args:
            pipeline_name: Pipeline name for log group naming
            config: Optional LogConfig for level and format settings
        """
        self.config = config or LogConfig.default_config()

        # AWS Configuration
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        # Log group/stream configuration
        self.pipeline_name = pipeline_name
        self.log_group_name = f"/heisenberg/pipelines/{self.pipeline_name}"
        self.log_stream_name = self._generate_stream_name()

        # Retention configuration (in days)
        self.retention_days = int(os.getenv("AWS_LOG_RETENTION_DAYS", "7"))

        # Batching configuration
        self.waiting_logs: List[Dict[str, Any]] = []
        self.forwarding = False
        self.lock = threading.Lock()
        self.debounce_delay = int(os.getenv("CLOUDWATCH_DEBOUNCE_DELAY", "10"))
        self.chunk_size = int(os.getenv("CLOUDWATCH_CHUNK_SIZE", "100"))

        # Initialize CloudWatch client
        self.client = self._create_client()

        # Ensure log group and stream exist
        self._ensure_log_group_exists()
        self._ensure_log_stream_exists()

        # Register flush on program exit
        atexit.register(self._flush_on_exit)

    def _flush_on_exit(self) -> None:
        """Flush remaining logs immediately (called by atexit)."""
        with self.lock:
            logs_to_send = self.waiting_logs.copy()
            self.waiting_logs = []

        if logs_to_send:
            try:
                self._put_log_events(logs_to_send)
            except Exception as e:
                print(f"Error flushing CloudWatch logs on exit: {e}")

    def _generate_stream_name(self) -> str:
        """Generate unique log stream name with run number and timestamp."""
        run_number = os.getenv("HEISENBERG_RUN_NUMBER", "0")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{run_number}_{timestamp}"

    def _create_client(self):
        """Create boto3 CloudWatch Logs client with credentials."""
        session_kwargs = {"region_name": self.aws_region}

        if self.aws_access_key_id and self.aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = self.aws_access_key_id
            session_kwargs["aws_secret_access_key"] = self.aws_secret_access_key

        session = boto3.Session(**session_kwargs)
        return session.client("logs")

    def _ensure_log_group_exists(self) -> None:
        """Create log group if it doesn't exist and set retention policy."""
        try:
            self.client.create_log_group(logGroupName=self.log_group_name)
            print(f"Created CloudWatch log group: {self.log_group_name}")
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                print(f"Error creating log group: {e}")
                return

        # Set retention policy
        try:
            self.client.put_retention_policy(
                logGroupName=self.log_group_name, retentionInDays=self.retention_days
            )
        except ClientError as e:
            print(f"Error setting retention policy: {e}")

    def _ensure_log_stream_exists(self) -> None:
        """Create log stream if it doesn't exist."""
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group_name, logStreamName=self.log_stream_name
            )
            print(f"Created CloudWatch log stream: {self.log_stream_name}")
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                print(f"Error creating log stream: {e}")

    def debug(self, msg: str, **fields: Any) -> None:
        if self._should_log(LogLevel.DEBUG):
            self._add_log(LogLevel.DEBUG, msg, **fields)

    def info(self, msg: str, **fields: Any) -> None:
        if self._should_log(LogLevel.INFO):
            self._add_log(LogLevel.INFO, msg, **fields)

    def warn(self, msg: str, **fields: Any) -> None:
        if self._should_log(LogLevel.WARN):
            self._add_log(LogLevel.WARN, msg, **fields)

    def warning(self, msg: str, **fields: Any) -> None:
        self.warn(msg, **fields)

    def error(self, msg: str, **fields: Any) -> None:
        if self._should_log(LogLevel.ERROR):
            self._add_log(LogLevel.ERROR, msg, **fields)

    def fatal(self, msg: str, **fields: Any) -> None:
        if self._should_log(LogLevel.FATAL):
            self._add_log(LogLevel.FATAL, msg, **fields)

    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on configured level."""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1,
            LogLevel.WARN: 2,
            LogLevel.ERROR: 3,
            LogLevel.FATAL: 4,
        }

        current_level_value = level_order[level]
        config_level_value = level_order[self.config.level]

        return current_level_value >= config_level_value

    def _add_log(self, level: LogLevel, msg: str, **fields: Any) -> None:
        """Add log entry to waiting queue."""
        log_entry = {
            "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
            "level": level.name,
            "message": msg,
            **fields,
        }

        with self.lock:
            self.waiting_logs.append(log_entry)

        self.sync()

    def _format_log_message(self, log_entry: Dict[str, Any]) -> str:
        """Format log entry as JSON string for CloudWatch."""
        message_data = {k: v for k, v in log_entry.items() if k != "timestamp"}
        return json.dumps(message_data, default=str)

    def sync(self) -> None:
        """Trigger async log forwarding with debounce."""
        with self.lock:
            if self.forwarding:
                return
            self.forwarding = True

        def forward_logs():
            try:
                start_time = time.time()

                # Wait for debounce period or until chunk size threshold
                while (time.time() - start_time) < self.debounce_delay:
                    if len(self.waiting_logs) > self.chunk_size:
                        break
                    time.sleep(0.5)

                with self.lock:
                    logs_to_send = self.waiting_logs.copy()
                    self.waiting_logs = []
                    self.forwarding = False

                if logs_to_send:
                    self._send_logs_with_retry(logs_to_send, retry_count=0)

            except Exception as e:
                print(f"Error in CloudWatch forward_logs: {e}")
                with self.lock:
                    self.forwarding = False

        threading.Thread(target=forward_logs, daemon=True).start()

    def _send_logs_with_retry(
        self, logs: List[Dict[str, Any]], retry_count: int
    ) -> None:
        """Send logs to CloudWatch with exponential backoff retry."""
        max_retries = 5

        try:
            self._put_log_events(logs)
        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "ResourceNotFoundException":
                # Log group or stream was deleted, recreate
                self._ensure_log_group_exists()
                self._ensure_log_stream_exists()
                self._send_logs_with_retry(logs, retry_count)

            elif error_code == "ThrottlingException" and retry_count < max_retries:
                # Exponential backoff for throttling
                delay = (2**retry_count) + (retry_count * 0.1)
                print(
                    f"CloudWatch throttled, retrying in {delay}s (attempt {retry_count + 1})"
                )
                time.sleep(delay)
                threading.Thread(
                    target=self._send_logs_with_retry,
                    args=(logs, retry_count + 1),
                    daemon=True,
                ).start()

            elif (
                error_code == "DataAlreadyAcceptedException"
                or error_code == "InvalidSequenceTokenException"
            ):
                if retry_count < max_retries:
                    self._send_logs_with_retry(logs, retry_count + 1)

            elif retry_count < max_retries:
                delay = 2**retry_count
                print(f"CloudWatch error: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                threading.Thread(
                    target=self._send_logs_with_retry,
                    args=(logs, retry_count + 1),
                    daemon=True,
                ).start()
            else:
                print(f"CloudWatch logging failed after {max_retries} retries: {e}")

        except Exception as e:
            if retry_count < max_retries:
                delay = 2**retry_count
                print(f"Unexpected error sending to CloudWatch: {e}. Retrying...")
                time.sleep(delay)
                threading.Thread(
                    target=self._send_logs_with_retry,
                    args=(logs, retry_count + 1),
                    daemon=True,
                ).start()
            else:
                print(f"CloudWatch logging failed after {max_retries} retries: {e}")

    def _put_log_events(self, logs: List[Dict[str, Any]]) -> None:
        """Send log events to CloudWatch, handling batch size limits."""
        batches = self._split_into_batches(logs)

        for batch in batches:
            log_events = [
                {
                    "timestamp": log["timestamp"],
                    "message": self._format_log_message(log),
                }
                for log in batch
            ]

            # Sort by timestamp (required by CloudWatch)
            log_events.sort(key=lambda x: x["timestamp"])

            self.client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=log_events,
            )

    def _split_into_batches(
        self, logs: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """Split logs into batches respecting CloudWatch limits."""
        batches = []
        current_batch = []
        current_batch_size = 0

        for log in logs:
            message = self._format_log_message(log)
            event_size = len(message.encode("utf-8")) + self.EVENT_OVERHEAD_BYTES

            # Truncate if exceeds max size
            if event_size > self.MAX_EVENT_SIZE_BYTES:
                log = self._truncate_log(log)
                message = self._format_log_message(log)
                event_size = len(message.encode("utf-8")) + self.EVENT_OVERHEAD_BYTES

            # Check if adding this event would exceed batch limits
            would_exceed_count = len(current_batch) >= self.MAX_BATCH_COUNT
            would_exceed_size = (
                current_batch_size + event_size
            ) > self.MAX_BATCH_SIZE_BYTES

            if would_exceed_count or would_exceed_size:
                if current_batch:
                    batches.append(current_batch)
                current_batch = []
                current_batch_size = 0

            current_batch.append(log)
            current_batch_size += event_size

        if current_batch:
            batches.append(current_batch)

        return batches

    def _truncate_log(self, log: Dict[str, Any]) -> Dict[str, Any]:
        """Truncate log message to fit within max size."""
        truncated = log.copy()
        original_msg = truncated.get("message", "")

        # Calculate available space
        test_log = {k: v for k, v in truncated.items() if k != "message"}
        test_log["message"] = ""
        overhead = len(json.dumps(test_log, default=str).encode("utf-8"))
        available = (
            self.MAX_EVENT_SIZE_BYTES - self.EVENT_OVERHEAD_BYTES - overhead - 50
        )

        if available > 0:
            truncated["message"] = original_msg[:available] + "... [TRUNCATED]"
        else:
            truncated["message"] = "[TRUNCATED]"

        return truncated

    def __del__(self):
        """Ensure remaining logs are flushed on destruction."""
        if hasattr(self, "waiting_logs") and self.waiting_logs:
            try:
                self._put_log_events(self.waiting_logs)
            except Exception:
                pass
