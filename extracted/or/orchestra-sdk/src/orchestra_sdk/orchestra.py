import logging
import os
import random
import uuid
from functools import wraps
from typing import Any

from orchestra_sdk.check_environment import validate_environment
from orchestra_sdk.enum import TaskRunStatus, WebhookEventType
from orchestra_sdk.http import HTTPClient

logger = logging.getLogger(__name__)


class OrchestraSDK:
    _http_client = None

    @property
    def http_client(self) -> HTTPClient | None:
        if not self._http_client and self.api_key and self.task_run_id and self.webhook_url:
            self._http_client = HTTPClient(
                api_key=self.api_key, task_run_id=self.task_run_id, webhook_url=self.webhook_url
            )
        if not self._http_client:
            logger.warning("Environment not configured correctly to send update for Task.")
        return self._http_client

    def __init__(self, api_key: str, log_file: str = "orchestra.log", send_logs: bool = False):
        self.api_key = api_key
        self.log_file = log_file
        self.send_logs = send_logs
        self.task_run_id = None
        self.webhook_url = None

        self._http_client = None

        self.task_run_id = validate_environment()
        self.webhook_url = os.getenv("ORCHESTRA_WEBHOOK_URL") or "https://webhook.getorchestra.io"

    def _update_task(self, status: TaskRunStatus, message: str) -> None:
        if self.http_client:
            logger.debug(f"Updating '{self.task_run_id}' to {status.value.lower()}.")
            self.http_client.request(
                event_type=WebhookEventType.UPDATE_STATUS,
                json={"status": status.value, "message": message},
                method="POST",
            )

    def send_running_status(self, function_name: str) -> None:
        self._update_task(status=TaskRunStatus.RUNNING, message=f"{function_name} started.")

    def send_failed_status(self, function_name: str, func_error: Exception) -> None:
        self._update_task(
            status=TaskRunStatus.FAILED,
            message=f"{function_name} failed. Error: {str(func_error)[:250]}",
        )

    def send_success_status(self, function_name: str) -> None:
        self._update_task(status=TaskRunStatus.SUCCEEDED, message=f"{function_name} succeeded.")

    def _send_log_file(self) -> None:
        try:
            if not self.http_client:
                return

            if not os.path.exists(self.log_file):
                logger.warning(f"Log file '{self.log_file}' not found.")
                return

            with open(self.log_file, "r") as lf:
                self.http_client.request(
                    event_type=WebhookEventType.LOG,
                    json={"log_name": self.log_file, "data": lf.read()},
                    method="POST",
                )
        except Exception as e:
            logger.error(f"Failed to send log file orchestra_output.log to Orchestra: {e}")

    def run(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self._http_client = None
                self.send_running_status(func.__name__)
                try:
                    fn_result = func(*args, **kwargs)
                    self.send_success_status(func.__name__)
                    return fn_result
                except Exception as failed_func_err:
                    self.send_failed_status(func.__name__, failed_func_err)
                finally:
                    if self.send_logs:
                        self._send_log_file()

            return wrapper

        return decorator

    def update_task(self, status: TaskRunStatus, message: str | None = None) -> bool:
        """
        Update the Task with the provided status and message.

        Args:
            status (TaskRunStatus): The status to update the Task with.
            message (str | None): The message to update the Task with.

        Returns:
            bool: True if the Task updated request was sent successfully, False otherwise.
        """
        if not self.http_client:
            return False

        logger.debug(
            f"Updating '{self.task_run_id}'. Status: {status.value.lower() if status else 'None'}. Message: {str(message)}."
        )

        payload = {"status": status.value}
        if message:
            payload["message"] = message

        return self.http_client.request(
            event_type=WebhookEventType.UPDATE_STATUS,
            json=payload,
            method="POST",
        )

    def set_output(self, name: str, value: Any) -> bool:
        """
        Set the output for the Task.

        Args:
            name (str): Case insensitive name of the output. Must be a valid key containing only letters, and underscores.
            value: The value of the output.

        Returns:
            bool: True if the output was set successfully, False otherwise.
        """
        if not self.http_client:
            return False

        logger.debug(
            f"Setting output for task run '{self.task_run_id}'. Name: '{name}'. Value: '{value}'."
        )

        return self.http_client.request(
            event_type=WebhookEventType.SET_OUTPUT,
            json={"output_name": name, "output_value": value},
            method="POST",
        )

    def configure_aws_lambda_event(self, event: dict[str, Any]) -> None:
        """
        Configures the object instance with the values from the incoming JSON payload in AWS Lambda.
        Log file also prepended with `/tmp/` to ensure it is writable, and with a random number to avoid conflicts
        when lambda functions retry.

        Args:
            event (dict[str, Any]): The JSON payload from the AWS Lambda event.
        """
        self.task_run_id = uuid.UUID(event.get("orchestra_task_run_id"))
        self.log_file = f"/tmp/{self.task_run_id}_{random.randint(0,10000)}.log"
        self.webhook_url = event.get("orchestra_webhook_url")
        self._http_client = None
