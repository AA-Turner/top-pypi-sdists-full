import json
import uuid

import responses

from orchestra_sdk.enum import WebhookEventType
from orchestra_sdk.http import HTTPClient


class TestHTTP:
    @responses.activate
    def test_retry_mechanism_works(self):
        mock_api_key = "mock_api_key"
        mock_url = "http://mock.url"
        mock_task_run_id = uuid.uuid4()

        responses.post(mock_url, status=503)
        responses.post(mock_url, status=500)
        r3 = responses.post(mock_url, status=200, json={"result": "all good"})

        assert HTTPClient(
            api_key=mock_api_key, task_run_id=mock_task_run_id, webhook_url=mock_url
        ).request(event_type=WebhookEventType.UPDATE_STATUS)

        assert len(responses.calls) == 3
        assert json.loads(r3.calls[0].request.body or "{}") == {
            "event_type": "UPDATE_STATUS",
            "metadata": {},
            "task_run_id": str(mock_task_run_id),
        }
        assert r3.calls[0].request.headers["Authorization"] == f"Bearer {mock_api_key}"
