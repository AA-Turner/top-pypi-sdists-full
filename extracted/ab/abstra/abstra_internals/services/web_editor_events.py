"""Fire-and-forget reporting of web-editor backend events to cloud-api.

The stall watchdog reports each finished stall episode here so it becomes a
Prometheus metric on cloud-api (POST /cli/web-editor/events, the same
endpoint the frontend beacons hit). Best-effort: runs on its own thread and
swallows every error, so a telemetry failure never reaches the watchdog or
the editor. The endpoint is unauthenticated (it validates the projectId
against the database), so no credentials are sent. Severity classification
(the 24s/60s thresholds) lives on cloud-api, not here, so it can change
without a lib release; this only ships the raw numbers.
"""

from typing import Any, Dict

import requests

from abstra_internals.environment import (
    CLOUD_API_CLI_URL,
    PROJECT_ID,
    REQUEST_TIMEOUT,
)
from abstra_internals.threaded import threaded
from abstra_internals.utils.env import is_dev_env, is_test_env


@threaded
def report_stall_episode(episode: Dict[str, Any]) -> None:
    try:
        if is_test_env() or is_dev_env():
            return
        payload = {
            "type": "stall",
            "source": "backend",
            "projectId": PROJECT_ID,
            "stallCount": episode["stallCount"],
            "stallTotalSeconds": episode["stallTotalSeconds"],
            "stallMaxSeconds": episode["stallMaxSeconds"],
            "episodeSeconds": episode["episodeSeconds"],
            "thresholdSeconds": episode["thresholdSeconds"],
        }
        requests.post(
            f"{CLOUD_API_CLI_URL}/web-editor/events",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except Exception:
        # Telemetry only — never let a reporting failure surface.
        pass
