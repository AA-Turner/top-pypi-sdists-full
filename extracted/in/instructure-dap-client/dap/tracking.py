import json
import time

import aiohttp
import logging
import platform

from . import __version__

logger = logging.getLogger("dap")

is_cli_mode: bool = False

def executing_in_cli_mode() -> None:
    global is_cli_mode
    is_cli_mode = True

class TrackingData:
    exec_mode: str # execution as "cli" or "lib"
    client_id: str
    dap_version: str
    python_version: str
    os_version: str
    db_dialect: str | None = None
    db_version: str | None = None
    command: str | None = None
    namespace: str | None = None
    table: str | None = None

    def __init__(self, client_id: str):
        self.exec_mode = "cli" if is_cli_mode else "lib"
        self.client_id = client_id
        self.dap_version = __version__
        self.python_version = platform.python_version()
        self.os_version = f"{platform.system()} {platform.release()} {platform.machine()}"

    def set_cmd_info(self, command: str | None, namespace: str, table: str | None) -> None:
        self.command = command
        self.namespace = namespace
        self.table = table

    def __str__(self) -> str:
        return (f"exec_mode={self.exec_mode}, client_id={self.client_id}, dap_version={self.dap_version}, "
                f"python_version={self.python_version}, os_version={self.os_version}, "
                f"db_dialect={self.db_dialect}, db_version={self.db_version}, command={self.command}, "
                f"namespace={self.namespace}, table={self.table}")


PENDO_URL = "https://data.pendo.io/data/track"
PENDO_EVENT_TYPE = "track"
PENDO_KEY_NAME = "x-pendo-integration-key"
PENDO_KEY_VALUE = "e1905b3f-afbb-4261-757d-275327fbd11e"
PENDO_MAX_PROPS_JSON_SIZE = 512


def reduce_to_valid_size(properties: dict) -> dict:
    """
    Reduce properties to fit within the Pendo limit described at
    https://support.pendo.io/hc/en-us/articles/360032294291-Configure-Track-Events
    """
    # versions should be short but some DBs/OSs might return a long string
    properties["os_version"] = properties.get("os_version", "")[:32]
    properties["db_version"] = properties.get("db_version", "")[:16]
    # user provided properties can be anything
    properties["namespace"] = properties.get("namespace", "")[:32]
    props_len = len(json.dumps({"properties": properties}))
    if (props_len > PENDO_MAX_PROPS_JSON_SIZE) and ("table" in properties): # all other properties are short
        table_count = len(properties["table"].split(","))
        properties["table"] = f"{table_count} tables"
    return properties


async def send_tracking_data(tracking_data: TrackingData) -> None:
    """
    Send data to pendo.io and also log what was sent. Failure should not disrupt the main functionality.
    """
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=20),
    ) as session:
        try:
            properties = {
                "exec_mode": tracking_data.exec_mode,
                "dap_version": tracking_data.dap_version,
                "python_version": tracking_data.python_version,
                "os_version": tracking_data.os_version,
                "db_dialect": tracking_data.db_dialect,
                "db_version": tracking_data.db_version,
                "command": tracking_data.command,
                "namespace": tracking_data.namespace,
                "table": tracking_data.table,
            }
            async with session.post(
                PENDO_URL,
                headers={ PENDO_KEY_NAME: PENDO_KEY_VALUE },
                json={
                    "type": PENDO_EVENT_TYPE,
                    "event": "execution",
                    "visitorId": tracking_data.client_id,
                    "timestamp": int(time.time() * 1000),
                    "properties": reduce_to_valid_size(properties),
                }) as response:
                if response.status != 200:
                    logger.warning(f"Failed to send usage tracking data, response status: {response.status}, message: {await response.text()}")
                else:
                    logger.debug(f"Usage tracking data sent to pendo.io: {tracking_data}")
        except Exception as e: # tracking failure should not disrupt the main functionality
            logger.warning(f"Error sending usage tracking data: {e}")
