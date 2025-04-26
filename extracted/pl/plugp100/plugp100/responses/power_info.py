import dataclasses
from typing import Dict, Any


@dataclasses.dataclass
class PowerInfo:
    current_power: float = property(lambda self: self.info["current_power"])

    def __init__(self, info: Dict[str, Any]):
        self.info = info

    def get_unmapped_state(self):
        return self.info
