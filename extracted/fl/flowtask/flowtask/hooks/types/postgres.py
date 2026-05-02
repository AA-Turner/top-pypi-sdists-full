from typing import Optional
from dataclasses import dataclass
import asyncio
import asyncpg
import backoff  # For exponential backoff
from navconfig.logging import logging
from navigator.conf import default_dsn  # Your default DSN configuration
from .base import BaseTrigger  # Base class for triggers


@dataclass
class Notification:
    channel: str
    payload: str
    pid: str


class PostgresTrigger(BaseTrigger):
    """PostgresTrigger.

    Trigger that listens for PostgreSQL events and sends notifications.
    Using LISTEN/NOTIFY Infraestructure.
    """
    def __init__(
        self,
        *args,
        dsn: Optional[str] = None,
        channel: str = 'notifications',
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.dsn = dsn or default_dsn
        self.channel = channel
        self.connection: Optional[asyncpg.Connection] = None
        self._listening_task: Optional[asyncio.Task] = None
        self._reconnecting = False

    async def on_startup(self, app):
        self._logger.info(
            f"Starting PostgresTrigger listening on channel '{self.channel}'"
        )
        await self.connect()

    async def on_shutdown(self, app):
        self._logger.info("Shutting down PostgresTrigger")
        if self._listening_task:
            self._listening_task.cancel()
        if self.connection:
            await self.connection.close()

    @backoff.on_exception(
        backoff.expo,
        (asyncpg.exceptions.PostgresError, ConnectionError),
        max_tries=5,
        on_backoff=lambda details: logging.warning(f"Retrying connection in {details['wait']} seconds...")
    )
    async def connect(self):
        self.connection = await asyncpg.connect(dsn=self.dsn)
        await self.connection.add_listener(
            self.channel,
            self.notification_handler
        )
        self._logger.info(
            f"Connected to PostgreSQL and listening on channel '{self.channel}'"
        )
        self._listening_task = asyncio.create_task(self.keep_listening())

    async def keep_listening(self):
        try:
            while True:
                await asyncio.sleep(3600)  # Keep the coroutine alive
        except asyncio.CancelledError:
            self._logger.info(
                "Listening task cancelled"
            )
        except Exception as e:
            self._logger.error(
                f"Error in keep_listening: {e}"
            )
            await self.reconnect()

    async def reconnect(self):
        if not self._reconnecting:
            self._reconnecting = True
            if self.connection:
                await self.connection.close()
            self._logger.info(
                "Attempting to reconnect to PostgreSQL..."
            )
            await self.connect()
            self._reconnecting = False

    async def notification_handler(self, connection, pid, channel, payload):
        self._logger.info(
            f"Received notification on channel '{channel}': {payload}"
        )
        notification = Notification(channel=channel, payload=payload, pid=pid)
        await self.run_actions(notification=notification)
