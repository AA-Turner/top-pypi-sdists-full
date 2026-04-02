import os
from datetime import datetime
from typing import Any

import requests

from seshat.general.exceptions import InvalidArgumentsError
from seshat.transformer import Transformer


class ActionGate(Transformer):
    """
    ActionGate runs an action on the input SFrame if a condition is met.

    Parameters
    ----------
    condition : Callable[[SFrame], bool]
        Function that accepts an SFrame and returns a boolean indicating whether to run on_success.
    on_success : Callable[[SFrame], SFrame] or Transformer, optional
        Action to run if condition returns True. If a Transformer,
        its run on data and it's result return. If a function,
        it is called with the SFrame and the input is returned unchanged.
    webhook_url : str, optional
        URL to call when condition is met. Sends a POST request with SFrame metadata.
    trigger_run_number : int, optional
        Specific run number to trigger the action on.
    """

    from typing import Callable

    from seshat.data_class import SFrame

    def __init__(
        self,
        webhook_url: str = None,
        on_success: Callable[[SFrame], Any] | Transformer = None,
        trigger_run_number: int = None,
        condition: Callable[[SFrame], bool] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if not webhook_url and not on_success:
            raise InvalidArgumentsError(
                "Either webhook_url or on_success must be provided."
            )
        self.condition = condition
        self.trigger_run_number = trigger_run_number
        self.webhook_url = webhook_url
        self.on_success = on_success

    def __call_webhook(self, sf_input):
        """Call the configured webhook with SFrame metadata."""
        if not self.webhook_url:
            return

        try:
            # Prepare webhook payload
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "run_number": os.getenv("HEISENBERG_RUN_NUMBER", "1"),
                "job_id": os.getenv("HEISENBERG_JOB_ID", "unknown"),
                "agent_id": os.getenv("DATA_AGENT_ID", "unknown"),
                "pipeline_name": os.getenv("HEISENBERG_PIPELINE_NAME", "unknown"),
                "status": "ok",
            }

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            response.raise_for_status()

            if hasattr(self, "logger") and self.logger:
                self.logger.info(f"Webhook called successfully: {self.webhook_url}")

        except requests.exceptions.Timeout:
            error_msg = f"Webhook timeout: {self.webhook_url}"
            if hasattr(self, "logger") and self.logger:
                self.logger.error(error_msg)
            else:
                print(f"ERROR: {error_msg}")

        except requests.exceptions.RequestException as e:
            error_msg = f"Webhook request failed: {self.webhook_url} - {str(e)}"
            if hasattr(self, "logger") and self.logger:
                self.logger.error(error_msg)
            else:
                print(f"ERROR: {error_msg}")

        except Exception as e:
            error_msg = f"Unexpected error calling webhook: {str(e)}"
            if hasattr(self, "logger") and self.logger:
                self.logger.error(error_msg)
            else:
                print(f"ERROR: {error_msg}")

    def __should_run(self, sf_input):
        if self.condition:
            return self.condition(sf_input)
        if self.trigger_run_number:
            return str(self.trigger_run_number) == os.getenv(
                "HEISENBERG_RUN_NUMBER", "1"
            )
        return True

    def __call__(self, sf_input: "SFrame", *args, **kwargs):
        on_success = self.__call_webhook
        if self.on_success:
            on_success = self.on_success

        if not self.__should_run(sf_input):
            return sf_input
        if isinstance(self.on_success, Transformer):
            return on_success(sf_input)
        on_success(sf_input)
        return sf_input
