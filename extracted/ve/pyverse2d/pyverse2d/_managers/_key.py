# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..abc import Manager

from ._context import ContextManager

import pyglet.window.key as _key
from typing import TypeAlias

# ======================================== STR ========================================
_NAMES: dict[KeyManager.Key, str] = {
    # Lettres
    _key.A: "A", _key.B: "B", _key.C: "C", _key.D: "D", _key.E: "E",
    _key.F: "F", _key.G: "G", _key.H: "H", _key.I: "I", _key.J: "J",
    _key.K: "K", _key.L: "L", _key.M: "M", _key.N: "N", _key.O: "O",
    _key.P: "P", _key.Q: "Q", _key.R: "R", _key.S: "S", _key.T: "T",
    _key.U: "U", _key.V: "V", _key.W: "W", _key.X: "X", _key.Y: "Y",
    _key.Z: "Z",

    # Rangée de chiffres
    _key._0: "0", _key._1: "1", _key._2: "2", _key._3: "3", _key._4: "4",
    _key._5: "5", _key._6: "6", _key._7: "7", _key._8: "8", _key._9: "9",

    # Numpad
    _key.NUM_0: "Numpad 0", _key.NUM_1: "Numpad 1", _key.NUM_2: "Numpad 2",
    _key.NUM_3: "Numpad 3", _key.NUM_4: "Numpad 4", _key.NUM_5: "Numpad 5",
    _key.NUM_6: "Numpad 6", _key.NUM_7: "Numpad 7", _key.NUM_8: "Numpad 8",
    _key.NUM_9: "Numpad 9",

    # Navigation
    _key.UP: "Up", _key.DOWN: "Down", _key.LEFT: "Left", _key.RIGHT: "Right",

    # Modificateurs
    _key.LSHIFT: "Left Shift", _key.RSHIFT: "Right Shift",
    _key.LCTRL: "Left Ctrl",  _key.RCTRL: "Right Ctrl",
    _key.LALT: "Left Alt",    _key.RALT: "Right Alt",

    # Actions
    _key.SPACE:     "Space",
    _key.RETURN:    "Enter",
    _key.BACKSPACE: "Backspace",
    _key.TAB:       "Tab",
    _key.ESCAPE:    "Escape",
    _key.DELETE:    "Delete",

    # Fonctions
    _key.F1:  "F1",  _key.F2:  "F2",  _key.F3:  "F3",  _key.F4:  "F4",
    _key.F5:  "F5",  _key.F6:  "F6",  _key.F7:  "F7",  _key.F8:  "F8",
    _key.F9:  "F9",  _key.F10: "F10", _key.F11: "F11", _key.F12: "F12",
}

# ======================================== MANAGER ========================================
class KeyManager(Manager):
    """Gestionnaire de la souris"""
    __slots__ = ("_step", "_pressed", "_released_this_frame")

    _ID: str = "key"

    # Alias
    Key: TypeAlias = int

    # Lettres
    K_A = _key.A
    K_B = _key.B
    K_C = _key.C
    K_D = _key.D
    K_E = _key.E
    K_F = _key.F
    K_G = _key.G
    K_H = _key.H
    K_I = _key.I
    K_J = _key.J
    K_K = _key.K
    K_L = _key.L
    K_M = _key.M
    K_N = _key.N
    K_O = _key.O
    K_P = _key.P
    K_Q = _key.Q
    K_R = _key.R
    K_S = _key.S
    K_T = _key.T
    K_U = _key.U
    K_V = _key.V
    K_W = _key.W
    K_X = _key.X
    K_Y = _key.Y
    K_Z = _key.Z

    # Rangée de chiffres
    K_0 = _key._0
    K_1 = _key._1
    K_2 = _key._2
    K_3 = _key._3
    K_4 = _key._4
    K_5 = _key._5
    K_6 = _key._6
    K_7 = _key._7
    K_8 = _key._8
    K_9 = _key._9

    # Numpad
    K_NUM_0 = _key.NUM_0
    K_NUM_1 = _key.NUM_1
    K_NUM_2 = _key.NUM_2
    K_NUM_3 = _key.NUM_3
    K_NUM_4 = _key.NUM_4
    K_NUM_5 = _key.NUM_5
    K_NUM_6 = _key.NUM_6
    K_NUM_7 = _key.NUM_7
    K_NUM_8 = _key.NUM_8
    K_NUM_9 = _key.NUM_9

    # Navigation
    K_UP = _key.UP
    K_DOWN = _key.DOWN
    K_LEFT = _key.LEFT
    K_RIGHT = _key.RIGHT

    # Modificateurs
    K_LSHIFT = _key.LSHIFT
    K_RSHIFT = _key.RSHIFT
    K_LCTRL = _key.LCTRL
    K_RCTRL = _key.RCTRL
    K_LALT = _key.LALT
    K_RALT = _key.RALT

    # Actions
    K_SPACE = _key.SPACE
    K_ENTER = _key.RETURN
    K_BACKSPACE = _key.BACKSPACE
    K_TAB = _key.TAB
    K_ESCAPE = _key.ESCAPE
    K_DELETE = _key.DELETE

    # Fonctions
    K_F1 = _key.F1
    K_F2 = _key.F2
    K_F3 = _key.F3
    K_F4 = _key.F4
    K_F5 = _key.F5
    K_F6 = _key.F6
    K_F7 = _key.F7
    K_F8 = _key.F8
    K_F9 = _key.F9
    K_F10 = _key.F10
    K_F11 = _key.F11
    K_F12 = _key.F12

    def __init__(self, context_manager: ContextManager):
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Etat
        self._step: list[KeyManager.Key] = []
        self._pressed: dict[KeyManager.Key, bool] = {}
        self._released_this_frame: list[KeyManager.Key] = []

        # Abonnements
        self._ctx.event.on_key_press.subscribe(self._on_press)
        self._ctx.event.on_key_release.subscribe(self._on_release)

    # ======================================== KEYS ========================================
    @staticmethod
    def name(key: Key) -> str:
        """Renvoie le ``str`` d'une clé par son identifiant
        
        Args:
            key: identifiant de la clé
        """
        return _NAMES.get(key, "Unknown")

    # ======================================== STATE ========================================
    def is_pressed(self, key: Key) -> bool:
        """Vérifie si une touche est maintenue enfoncée
        
        Args:
            key: identifiant de la clé
        """
        return self._pressed.get(key, False)

    def just_pressed(self, key: Key) -> bool:
        """Vérifie si une touche vient d'être pressée cette frame
        
        Args:
            key: identifiant de la clé
        """
        return key in self._step

    def just_released(self, key: Key) -> bool:
        """Vérifie si une touche vient d'être relâchée cette frame
        
        Args:
            key: identifiant de la clé
        """
        return key in self._released_this_frame

    def _is_currently_pressed(self, key: Key) -> bool:
        """Vérifie si une touche est pressée cette frame ou maintenue
        
        Args:
            key: identifiant de la clé
        """
        return self._pressed.get(key, False) or key in self._step

    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        pass

    def flush(self) -> None:
        """Nettoyage"""
        for key in self._step:
            if key not in self._released_this_frame:
                self._pressed[key] = True
        self._step.clear()
        self._released_this_frame.clear()

    # ======================================== HOOKS ========================================
    def _on_press(self, key: int) -> None:
        """Pression d'une touche
        
        Args:
            key: identifiant de la clé
        """
        self._step.append(key)

    def _on_release(self, key: int) -> None:
        """Relachement d'une touche
        
        Args
            key: identifiant de la clé
        """
        self._pressed[key] = False
        self._released_this_frame.append(key)

# ======================================== EXPORTS ========================================
__all__ = [
    "KeyManager",
]