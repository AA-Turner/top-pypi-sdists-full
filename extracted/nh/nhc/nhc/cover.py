from .action import NHCAction
from .const import COVER_OPEN, COVER_CLOSE, COVER_STOP

class NHCCover(NHCAction):

    @property
    def is_open(self) -> bool:
        return self._state > 0

    async def open(self) -> None:
        await self._controller.execute(self.id, COVER_OPEN)

    async def close(self) -> None:
        await self._controller.execute(self.id, COVER_CLOSE)

    async def stop(self) -> None:
        await self._controller.execute(self.id, COVER_STOP)
