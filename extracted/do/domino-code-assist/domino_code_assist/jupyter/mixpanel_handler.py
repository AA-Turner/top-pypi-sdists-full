import json
import threading
import time
import uuid
from urllib.parse import quote

import requests
from jupyter_server.base.handlers import JupyterHandler

from domino_code_assist import __version__
from domino_code_assist.domino_api import get_domino_api

EVENT_NAME = "LCA show button"


class MixpanelHandler(JupyterHandler):
    async def get(self, path=None):
        unique_id = "na"
        info = get_domino_api().get_user_info()
        if info:
            unique_id = info["id"] if info else None

        self.set_header("Content-Type", "application/json")
        self.write(
            json.dumps(
                {
                    "id": unique_id,
                    "LCA_version": __version__,
                    "Domino_version": get_domino_api().get_domino_version(),
                    "event_name": EVENT_NAME,
                }
            )
        )

    async def post(self, *args):
        data = json.loads(self.request.body)
        self._send_event(EVENT_NAME, data)

    def _send_event(self, event, props):
        unique_id = "na"
        info = get_domino_api().get_user_info()
        if info:
            unique_id = info["id"] if info else None

        event_item = {
            "event": event,
            "properties": {
                **props,
                "time": int(round(time.time() * 1000)),
                "distinct_id": unique_id,
                "$insert_id": str(uuid.uuid4()),
                "LCA_version": __version__,
                "Domino_version": get_domino_api().get_domino_version(),
                "$user_id": unique_id,
            },
        }

        def run():
            try:
                requests.post(
                    "https://api.mixpanel.com/track/",
                    headers={"content-type": "application/x-www-form-urlencoded"},
                    data=f"data={quote(json.dumps([event_item]))}",
                    timeout=3,
                )
            except Exception:
                pass

        threading.Thread(target=run).start()
