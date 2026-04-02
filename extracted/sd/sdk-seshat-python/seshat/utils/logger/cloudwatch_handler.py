import atexit
import logging
import os
import threading
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class CloudWatchHandler(logging.Handler):
    """
    Python logging handler that sends logs to AWS CloudWatch Logs.

    Implements batching with debounce similar to LogstashLogger pattern,
    respecting CloudWatch API limits.

    Environment Variables:
        AWS_ACCESS_KEY: IAM access key
        AWS_SECRET_ACCESS_KEY: IAM secret key
        AWS_REGION: AWS region (default: us-east-1)
        AWS_LOG_RETENTION_DAYS: Log retention in days (default: 7)
        CLOUDWATCH_DEBOUNCE_DELAY: Batch wait time in seconds (default: 10)
        CLOUDWATCH_CHUNK_SIZE: Batch size threshold (default: 100)
    """

    # CloudWatch API Limits
    MAX_BATCH_SIZE_BYTES = 1_048_576  # 1MB
    MAX_BATCH_COUNT = 10_000
    MAX_EVENT_SIZE_BYTES = 262_144  # 256KB
    EVENT_OVERHEAD_BYTES = 26  # Overhead per log event

    def __init__(
        self,
        log_group: str,
        region: Optional[str] = None,
        retention_days: int = 7,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        """
        Initialize CloudWatch handler.

        Args:
            log_group: CloudWatch log group name (e.g., /heisenberg/pipelines/{pipeline_name})
            region: AWS region (defaults to AWS_REGION env var or us-east-1)
            retention_days: Log retention period in days (default: 7)
            aws_access_key_id: IAM access key (defaults to AWS_ACCESS_KEY env var)
            aws_secret_access_key: IAM secret key (defaults to AWS_SECRET_ACCESS_KEY env var)
        """
        super().__init__()

        self.log_group = log_group
        self.log_stream = self._generate_stream_name()
        self.retention_days = retention_days

        # AWS credentials
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv(
            "AWS_SECRET_ACCESS_KEY"
        )

        # Batching configuration
        self.waiting_logs: List[Dict[str, Any]] = []
        self.forwarding = False
        self._batch_lock = threading.Lock()
        self.debounce_delay = int(os.getenv("CLOUDWATCH_DEBOUNCE_DELAY", "10"))
        self.chunk_size = int(os.getenv("CLOUDWATCH_CHUNK_SIZE", "100"))

        # Initialize CloudWatch client
        self.client = self._create_client()

        # Ensure log group and stream exist
        self._ensure_log_group_exists()
        self._ensure_log_stream_exists()

        # Register flush on program exit
        atexit.register(self.flush)

    def _generate_stream_name(self) -> str:
        """Generate unique log stream name with run number and timestamp."""
        run_number = os.getenv("HEISENBERG_RUN_NUMBER", "0")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{run_number}_{timestamp}"

    def _create_client(self):
        """Create boto3 CloudWatch Logs client with credentials."""
        session_kwargs = {"region_name": self.region}

        if self.aws_access_key_id and self.aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = self.aws_access_key_id
            session_kwargs["aws_secret_access_key"] = self.aws_secret_access_key

        session = boto3.Session(**session_kwargs)
        return session.client("logs")

    def _ensure_log_group_exists(self) -> None:
        """Create log group if it doesn't exist and set retention policy."""
        try:
            self.client.create_log_group(logGroupName=self.log_group)
            print(f"Created CloudWatch log group: {self.log_group}")
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                print(f"Error creating log group: {e}")
                return

        # Set retention policy (always try to set it)
        try:
            self.client.put_retention_policy(
                logGroupName=self.log_group, retentionInDays=self.retention_days
            )
        except ClientError as e:
            print(f"Error setting retention policy: {e}")

    def _ensure_log_stream_exists(self) -> None:
        """Create log stream if it doesn't exist."""
        try:
            self.client.create_log_stream(
                logGroupName=self.log_group, logStreamName=self.log_stream
            )
            print(f"Created CloudWatch log stream: {self.log_stream}")
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                print(f"Error creating log stream: {e}")

    def emit(self, record: logging.LogRecord) -> None:
        """
        Handle a log record from Python's logging system.

        Args:
            record: The log record to process
        """
        try:
            msg = self.format(record)

            # Truncate if message exceeds max size
            msg_bytes = msg.encode("utf-8")
            if len(msg_bytes) > self.MAX_EVENT_SIZE_BYTES - self.EVENT_OVERHEAD_BYTES:
                max_len = self.MAX_EVENT_SIZE_BYTES - self.EVENT_OVERHEAD_BYTES - 50
                msg = msg[:max_len] + "... [TRUNCATED]"

            log_entry = {
                "timestamp": int(record.created * 1000),  # CloudWatch uses milliseconds
                "message": msg,
            }

            with self._batch_lock:
                self.waiting_logs.append(log_entry)

            self._trigger_flush()

        except Exception:
            self.handleError(record)

    def _trigger_flush(self) -> None:
        """Trigger async batch flush with debounce."""
        with self._batch_lock:
            if self.forwarding:
                return
            self.forwarding = True

        def flush_logs():
            try:
                start_time = time.time()

                # Wait for debounce period or until chunk size threshold
                while (time.time() - start_time) < self.debounce_delay:
                    if len(self.waiting_logs) > self.chunk_size:
                        break
                    time.sleep(0.5)

                with self._batch_lock:
                    logs_to_send = self.waiting_logs.copy()
                    self.waiting_logs = []
                    self.forwarding = False

                if logs_to_send:
                    self._send_logs_with_retry(logs_to_send, retry_count=0)

            except Exception as e:
                print(f"Error in CloudWatch flush_logs: {e}")
                with self._batch_lock:
                    self.forwarding = False

        threading.Thread(target=flush_logs, daemon=True).start()

    def _send_logs_with_retry(
        self, logs: List[Dict[str, Any]], retry_count: int
    ) -> None:
        """
        Send logs to CloudWatch with exponential backoff retry.

        Args:
            logs: List of log entries to send
            retry_count: Current retry attempt number
        """
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
                # These errors mean logs were already accepted or we need to retry
                # For newer CloudWatch API, sequence tokens are not required
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
        """
        Send log events to CloudWatch, handling batch size limits.

        Args:
            logs: List of log entries to send
        """
        batches = self._split_into_batches(logs)

        for batch in batches:
            # Sort by timestamp (required by CloudWatch)
            batch.sort(key=lambda x: x["timestamp"])

            self.client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=batch,
            )

    def _split_into_batches(
        self, logs: List[Dict[str, Any]]
    ) -> List[List[Dict[str, Any]]]:
        """
        Split logs into batches respecting CloudWatch limits.

        Args:
            logs: List of log entries to split

        Returns:
            List of batches, each batch is a list of log entries
        """
        batches = []
        current_batch = []
        current_batch_size = 0

        for log in logs:
            message = log["message"]
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

    def flush(self) -> None:
        """Flush any pending logs immediately."""
        with self._batch_lock:
            logs_to_send = self.waiting_logs.copy()
            self.waiting_logs = []

        if logs_to_send:
            try:
                self._put_log_events(logs_to_send)
            except Exception as e:
                print(f"Error flushing CloudWatch logs: {e}")

    def close(self) -> None:
        """Flush remaining logs on shutdown."""
        self.flush()
        super().close()
