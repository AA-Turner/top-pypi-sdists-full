from typing import Any
import asyncio
from asyncdb import AsyncDB
from .abstract import AbstractTaskStorage


class DatabaseTaskStorage(AbstractTaskStorage):
    """Saving Tasks on an postgreSQL Database."""
    _name_: str = "Database"

    def __init__(
        self,
        driver: str = "pg",
        dsn: str = None,
        credentials: dict = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)
        self._connection = AsyncDB(
            driver, dsn=dsn, params=credentials, loop=self.loop, **kwargs
        )

    async def open_task(
        self,
        task: str = None,
        program: str = None,
        **kwargs,
    ) -> Any:
        ## TODO: getting tasks from a external Task Storage (like a database).
        return self._task
