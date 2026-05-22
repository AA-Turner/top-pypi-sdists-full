# ======================================== IMPORTS ========================================
class FrameContext:
    """Contexte partagé entre tous les systèmes pour une frame donnée
    
    Réinitialisé par la scène en début de frame via ``reset()``.
    """
    __slots__ = ("_data",)

    def __init__(self) -> None:
        self._data: dict = {}

    # ======================================== INTERFACE ========================================
    def reset(self) -> None:
        """Vide le contexte — à appeler en début de frame"""
        self._data.clear()

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def set(self, key: str, value) -> None:
        self._data[key] = value

    # ======================================== PREDICATES ========================================
    def __contains__(self, key: str) -> bool:
        return key in self._data
    
# ======================================== EXPORTS ========================================
__all__ = [
    "FrameContext",
]