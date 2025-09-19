from .action import NHCAction

class NHCScene(NHCAction):

    async def activate(self) -> None:
        """Activate the scene."""
        await self._controller.execute(self.id, 255)