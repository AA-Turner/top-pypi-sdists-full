# ======================================== IMPORTS ========================================
from __future__ import annotations
from ..abc import Asset
from typing import Union, Tuple


class Color(tuple, Asset):
    """
    Descripteur de couleur immuable.
    Stockée en float [0.0; 1.0] en interne.
    Accepte les composantes soit en float [0.0; 1.0], soit en int [0; 255].

    Supports:
        Color(Color)
        Color(r, g, b)
        Color(r, g, b, a)
        Color((r, g, b))
        Color((r, g, b, a))
    """

    def __new__(cls, *args, argument: str = "Argument"):
        # Color(Color) — retour direct, pas de recopie inutile
        if len(args) == 1 and isinstance(args[0], cls):
            return args[0]

        # Dépaquetage tuple/séquence ou args directs
        if len(args) == 1 and isinstance(args[0], (tuple, list)):
            value = args[0]
            if len(value) < 3:
                raise ValueError(f"{argument} must have at least 3 elements")
            r, g, b = value[:3]
            a = value[3] if len(value) >= 4 else 1.0
        elif 3 <= len(args) <= 4:
            r, g, b = args[:3]
            a = args[3] if len(args) == 4 else 1.0
        else:
            raise TypeError(f"{argument}: invalid arguments {args}")

        r = cls._to_float(r, "red",   argument)
        g = cls._to_float(g, "green", argument)
        b = cls._to_float(b, "blue",  argument)
        a = cls._to_float(a, "alpha", argument)

        return tuple.__new__(cls, (r, g, b, a))

    def __init__(self, *args, **kwargs):
        ...

    # ======================================== CONVERSIONS ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de la couleur"""
        r, g, b, a = self
        return f"Color(r={r:.3f}, g={g:.3f}, b={b:.3f}, a={a:.3f})"

    def __copy__(self) -> Color:
        """Renvoie une copie de la couleur"""
        return self  # immuable, inutile de copier

    def copy(self) -> Color:
        """Renvoie une copie de la couleur"""
        return self

    # ======================================== GETTERS ========================================
    @property
    def r(self) -> float:
        """Renvoie la composante rouge [0.0; 1.0]"""
        return self[0]

    @property
    def g(self) -> float:
        """Renvoie la composante verte [0.0; 1.0]"""
        return self[1]

    @property
    def b(self) -> float:
        """Renvoie la composante bleue [0.0; 1.0]"""
        return self[2]

    @property
    def a(self) -> float:
        """Renvoie la composante alpha [0.0; 1.0]"""
        return self[3]

    @property
    def rgb(self) -> Tuple[float, float, float]:
        """Renvoie les composantes RGB en float [0.0; 1.0]"""
        return self[0], self[1], self[2]

    @property
    def rgba(self) -> Tuple[float, float, float, float]:
        """Renvoie les composantes RGBA en float [0.0; 1.0]"""
        return self[0], self[1], self[2], self[3]

    @property
    def rgb8(self) -> Tuple[int, int, int]:
        """Renvoie les composantes RGB en int [0; 255]"""
        return (
            int(round(self[0] * 255)),
            int(round(self[1] * 255)),
            int(round(self[2] * 255)),
        )

    @property
    def rgba8(self) -> Tuple[int, int, int, int]:
        """Renvoie les composantes RGBA en int [0; 255]"""
        return (
            int(round(self[0] * 255)),
            int(round(self[1] * 255)),
            int(round(self[2] * 255)),
            int(round(self[3] * 255)),
        )

    # ======================================== PUBLIC METHODS ========================================
    def with_alpha(self, a: Union[int, float]) -> Color:
        """
        Renvoie une nouvelle Color avec un alpha différent

        Args:
            a(int | float): nouvelle valeur alpha
        """
        return Color(self[0], self[1], self[2], self._to_float(a, "alpha", "with_alpha"))

    # ======================================== INTERNALS ========================================
    @staticmethod
    def _to_float(v: Union[int, float], name: str, argument: str) -> float:
        if isinstance(v, int):
            if not (0 <= v <= 255):
                raise ValueError(f"{argument}: {name} out of range ({v})")
            return v / 255.0
        elif isinstance(v, float):
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"{argument}: {name} out of range ({v})")
            return v
        else:
            raise TypeError(f"{argument}: invalid {name} type {type(v).__name__}")