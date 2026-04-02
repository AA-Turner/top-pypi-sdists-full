import os
import threading
import time
from datetime import datetime
from typing import Any, Optional

from seshat.utils.logger.base_logger import BaseLogger, LogLevel, LogConfig
from seshat.utils.rest import RestClient, RestClientException


class LogstashLogger(BaseLogger):
    def __init__(self, config: Optional[LogConfig] = None):
        self.config = config or LogConfig.default_config()
        self.logstash_url = os.getenv(
            "LOGSTASH_URL", "https://logstash.stage.heisenberg.so"
        )
        self.source_key = os.getenv("LOGSTASH_SOURCE", "executor-seshat")
        self.waiting_logs: list[dict[str, Any]] = []
        self.forwarding = False
        self.lock = threading.Lock()

        self.rest_client = RestClient(
            base_url=self.logstash_url,
            timeout=30,
            max_retries=3,
            retry_delay=2,
            headers={"Content-Type": "application/json"},
        )

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
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level.name,
            "message": msg,
            "log_source": self.source_key,
            **fields,
        }

        with self.lock:
            self.waiting_logs.append(log_entry)

        self.sync()

    def sync(self) -> None:
        with self.lock:
            if self.forwarding:
                return
            self.forwarding = True

        def forward_logs():
            try:
                delay = int(os.getenv("LOGSTASH_DEBOUNCE_DELAY", "10"))
                chunk_size = int(os.getenv("LOGSTASH_CHUNK_SIZE", "100"))

                start_time = time.time()
                while (time.time() - start_time) < delay:
                    if len(self.waiting_logs) > chunk_size:
                        break
                    time.sleep(0.5)

                with self.lock:
                    logs_to_send = self.waiting_logs.copy()
                    self._clear_waiting()
                    self.forwarding = False

                self._sync_with_retry(logs_to_send, 2)

            except Exception as e:
                print(f"Error in forward_logs: {e}")
                self.forwarding = False

        threading.Thread(target=forward_logs, daemon=True).start()

    def _sync_with_retry(self, logs: list[dict[str, Any]], retry: int) -> None:
        try:
            self._post_to_logstash(logs)
        except Exception as e:
            retry_delay = retry**2
            print(f"Retry {retry} failed: {e}. Waiting {retry_delay} seconds...")
            time.sleep(retry_delay)
            threading.Thread(
                target=self._sync_with_retry, args=(logs, retry + 1), daemon=True
            ).start()

    def _post_to_logstash(self, logs: list[dict[str, Any]]) -> None:
        if not self.logstash_url:
            raise ValueError("LOGSTASH_URL environment variable not set")

        try:
            self.rest_client.post(endpoint="", json=logs)
        except RestClientException as e:
            raise Exception(f"Failed to post to Logstash: {str(e)}")

    def _clear_waiting(self) -> None:
        self.waiting_logs = []

    def __del__(self):
        if hasattr(self, "rest_client"):
            self.rest_client.session.close()
