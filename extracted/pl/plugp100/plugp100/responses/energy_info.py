import dataclasses
from typing import Dict, Any


@dataclasses.dataclass
class EnergyInfo:
    today_runtime: float = property(lambda self: self.info["today_runtime"])
    month_runtime: float = property(lambda self: self.info["month_runtime"])
    today_energy: float = property(lambda self: self.info["today_energy"])
    month_energy: float = property(lambda self: self.info["month_energy"])
    current_power: float = property(lambda self: self.info["current_power"])

    def __init__(self, info: Dict[str, Any]):
        self.info = info

    def get_unmapped_state(self):
        return self.info
