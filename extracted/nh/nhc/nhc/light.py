from .action import NHCAction

class NHCLight(NHCAction):

    @property
    def is_on(self) -> bool:
        """Is on."""
        return self._state > 0

    async def turn_on(self, brightness=255) -> None:
        """Turn On."""
        if (self.is_dimmable):
            await self._controller.execute(self.id, round(brightness / 2.55))
        else:
            await self._controller.execute(self.id, brightness)

    async def turn_off(self) -> None:
        """Turn off."""
        await self._controller.execute(self.id, 0)

    async def toggle(self) -> None:
        """Toggle on/off."""
        if self.is_on:
            await self.turn_off()
        else:
            await self.turn_on()
