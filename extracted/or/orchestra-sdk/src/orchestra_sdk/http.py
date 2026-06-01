import logging
import uuid
from typing import Any, Literal

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from orchestra_sdk.enum import WebhookEventType

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, api_key: str, task_run_id: uuid.UUID, webhook_url: str):
        self.api_key = api_key
        self.task_run_id = task_run_id
        self.webhook_url = webhook_url

    def _get_response_json(self, r: requests.Response) -> dict | None:
        try:
            return r.json()
        except Exception:
            return None

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=3, min=2, max=15),
    )
    def _make_request(
        self, json: dict[str, Any], headers: dict[str, str], method: Literal["POST"], url: str
    ) -> None:
        logger.debug(f"Sending request to {url}...")
        r = requests.request(json=json, method=method, url=url, headers=headers)
        logger.debug(f"Status: {r.status_code}. Response: {self._get_response_json(r)}")
        r.raise_for_status()

    def request(
        self,
        event_type: WebhookEventType,
        metadata: dict[str, Any] = {},
        json: dict[str, Any] = {},
        method: Literal["POST"] = "POST",
    ) -> bool:
        try:
            self._make_request(
                json={
                    "event_type": event_type.value,
                    "metadata": metadata,
                    "task_run_id": str(self.task_run_id),
                    **json,
                },
                headers={"Authorization": f"Bearer {self.api_key}"},
                method=method,
                url=self.webhook_url,
            )
            return True
        except requests.exceptions.HTTPError as e:
            logger.error(
                f"Failed request ({e.response.status_code}): {self._get_response_json(e.response)}"
            )
        except Exception as e:
            logger.error(f"Could not send {method} request to {self.webhook_url} - {e}")
        return False
