import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from connector.config import config
from connector.httpx_rewrite import AsyncClient


@dataclass
class LogInput:
    agent_identifier: str
    log: str

    def model_dump(self) -> dict[str, Any]:
        return {
            "agent_identifier": self.agent_identifier,
            "log": self.log,
        }


# Create a separate logger for this module that only uses stdout
# This is to avoid recursive calls to the logger
http_logger = logging.getLogger("lumos_log_handler")
# Prevent this logger from inheriting the custom https handler which would call itself
http_logger.propagate = False
# Add a basic stdout handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"))
http_logger.addHandler(handler)


class LumosLogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        if not config.agent_identifier:
            http_logger.error("agent_identifier must be set in config")
            raise ValueError("agent_identifier must be set in config")
        self.agent_identifier = config.agent_identifier

    def emit(self, record: logging.LogRecord) -> None:
        # Only process ERROR level logs for now
        if record.levelno < logging.ERROR:
            return

        try:
            log_data = LogInput(
                agent_identifier=self.agent_identifier,
                log=self.format(record),
            )

            # Create event loop if one doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Run the async send operation
            loop.run_until_complete(self._send_log(log_data))
        except Exception:
            http_logger.error("Failed to emit log record", exc_info=True)
            self.handleError(record)

    async def _send_log(self, log_data: LogInput) -> None:
        if not config.base_url:
            http_logger.error("base_url must be set in config")
            return
        if not config.on_prem_agent_api_key:
            http_logger.error("on_prem_agent_api_key must be set in config")
            return

        try:
            headers = {
                "Authorization": f"Bearer {config.on_prem_agent_api_key}",
                "X-Agent-Identifier": self.agent_identifier,
                "Content-Type": "application/json",
            }

            async with AsyncClient(
                base_url=config.base_url,
                headers=headers,
            ) as client:
                try:
                    response = await client.post(
                        "/logs",
                        json=log_data.model_dump(),
                    )
                    response.raise_for_status()
                except Exception as e:
                    http_logger.error(f"Failed to send log to Lumos: {e}", exc_info=True)
        except Exception as e:
            http_logger.error(f"Failed to send log to Lumos: {e}", exc_info=True)
