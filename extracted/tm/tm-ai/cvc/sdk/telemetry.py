import asyncio
import json
import logging
import os
from urllib import request, error

logger = logging.getLogger(__name__)

def emit_telemetry_sync(payload: dict):
    port = os.environ.get("CVC_DASHBOARD_PORT", "13421")
    try:
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"http://127.0.0.1:{port}/api/telemetry",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        request.urlopen(req, timeout=0.5)
    except Exception:
        pass

async def emit_telemetry(payload: dict):
    asyncio.create_task(asyncio.to_thread(emit_telemetry_sync, payload))
