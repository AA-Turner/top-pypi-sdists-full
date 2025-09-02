from .action import NHCAction
from .const import PRESET_MODES, MODES

class NHCFan(NHCAction):

  @property
  def modes(self) -> list:
    return MODES

  @property
  def mode(self) -> str:
    for mode, value in PRESET_MODES.items():
        if value == self._state:
            return mode

    return PRESET_MODES['low']

  async def set_mode(self, preset_mode: str) -> None:
      await self._controller.execute(self.id, PRESET_MODES[preset_mode])
