# ======================================== IMPORTS ========================================
from typing import Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from ._time import TimeManager
    from ._coordinates import CoordinatesManager
    from ._event import EventManager
    from ._key import KeyManager
    from ._mouse import MouseManager
    from ._inputs import InputsManager
    from ._ui import UIManager
    from ._audio import AudioManager

# ======================================== CONTEXT ========================================
class ContextManager:
    """Contexte des managers"""
    __slots__ = (
        "time",
        "coordinates",
        "event",
        "key",
        "mouse",
        "inputs",
        "ui",
        "audio",
    )

    def __init__(self):
        self.time: TimeManager = None
        self.coordinates: CoordinatesManager = None
        self.event: EventManager = None
        self.key: KeyManager = None
        self.mouse: MouseManager = None
        self.inputs: InputsManager = None
        self.ui: UIManager = None
        self.audio: AudioManager = None

    def __iter__(self) -> Iterator:
        """Itère sur les itérateurs"""
        for manager in self.__slots__:
            yield getattr(self, manager, None)

# ======================================== EXPORTS ========================================
__all__ = [
    "ContextManager",
]