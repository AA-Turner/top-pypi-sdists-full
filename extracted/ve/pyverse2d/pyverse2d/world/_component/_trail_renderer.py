# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import over, expect_callable
from ...abc import RendererComponent
from ...asset import Image, Color
from ...typing import EasingFunc

from collections import deque
from numbers import Real, Integral
from typing import Callable, ClassVar

# ======================================== COMPONENT ========================================
class TrailRenderer(RendererComponent):
    """Composant gérant le rendu d'un trail continu

    Ce composant est manipulé par le ``RenderSystem``.

    Args:
        width: largeur maximale du ruban en unités monde *(> 0)*
        duration: durée de vie des points en secondes *(> 0)*
        min_distance: distance minimale entre deux points *(> 0)*
        color: couleur RGBA du trail *(mode couleur unie)*
        image: texture du trail *(None = couleur unie, sinon texturé répété)*
        width_easing: courbe de décroissance de la largeur tête→queue *(None = fixe)*
        smooth: active le lissage Catmull-Rom
        opacity: opacité globale *[0, 1]*
        z: ordre de rendu
        visible: visibilité
    """
    __slots__ = (
        "_width", "_duration", "_min_distance",
        "_color", "_image",
        "_width_easing", "_smooth",
        "_points",
    )

    _MAX_POINTS: ClassVar[int] = 64

    def __init__(
        self,
        width: Real = 1.0,
        duration: Real = 0.5,
        min_distance: Real = 0.05,
        color: Color = (255, 255, 255, 1.0),
        image: Image | None = None,
        width_easing: EasingFunc | None = None,
        smooth: bool = False,
        opacity: Real = 1.0,
        z: Integral = 0,
        visible: bool = True,
    ):
        # Initialisation du composant
        super().__init__(opacity, z, visible)

        # Transtypage et vérifications
        width = float(width)
        duration = float(duration)
        min_distance = float(min_distance)
        color = Color(color)
        smooth = bool(smooth)

        if __debug__:
            over(width, 0, include=False)
            over(duration, 0, include=False)
            over(min_distance, 0, include=False)
            expect_callable(width_easing, include_none=True)

        # Attributs publiques
        self._width: float = width
        self._duration: float = duration
        self._min_distance: float = min_distance
        self._color: Color = color
        self._image: Image | None = image
        self._width_easing: Callable[[float], float] | None = width_easing
        self._smooth: bool = smooth

        # Attributs internes
        self._points: deque[tuple[float, float, float]] = deque()

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de la traînée"""
        return f"TrailRenderer(width={self._width}, duration={self._duration}, points={len(self._points)})"

    def get_attributes(self) -> tuple:
        """Renvoie les attributs de la traînée"""
        return (self._width, self._duration, self._min_distance, self._color, self._image, self._smooth, self._opacity, self._z)

    def copy(self) -> TrailRenderer:
        """Renvoie une copie de la traînée"""
        return TrailRenderer(
            self._width, self._duration, self._min_distance,
            self._color, self._image, self._width_easing,
            self._smooth, self._opacity, self._z, self._visible,
        )

    # ======================================== PROPERTIES ========================================
    @property
    def width(self) -> float:
        """Largeur maximale du ruban en unités monde *(> 0)*"""
        return self._width

    @width.setter
    def width(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            over(value, 0, include=False)
        self._width = value

    @property
    def duration(self) -> float:
        """Durée de vie des points en secondes *(> 0)*"""
        return self._duration

    @duration.setter
    def duration(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            over(value, 0, include=False)
        self._duration = value

    @property
    def min_distance(self) -> float:
        """Distance minimale entre deux points *(> 0)*"""
        return self._min_distance

    @min_distance.setter
    def min_distance(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            over(value, 0, include=False)
        self._min_distance = value

    @property
    def color(self) -> Color:
        """Couleur RGBA du trail"""
        return self._color

    @color.setter
    def color(self, value: Color) -> None:
        self._color = Color(value)

    @property
    def image(self) -> Image | None:
        """Texture du trail *(None = couleur unie)*"""
        return self._image

    @image.setter
    def image(self, value: Image | None) -> None:
        self._image = value

    @property
    def width_easing(self) -> Callable[[float], float] | None:
        """Courbe de décroissance de la largeur tête→queue *(None = fixe)*"""
        return self._width_easing

    @width_easing.setter
    def width_easing(self, value: Callable[[float], float] | None) -> None:
        self._width_easing = value

    @property
    def smooth(self) -> bool:
        """Lissage Catmull-Rom activé"""
        return self._smooth

    @smooth.setter
    def smooth(self, value: bool) -> None:
        self._smooth = bool(value)

    @property
    def points(self) -> deque[tuple[float, float, float]]:
        """Buffer interne des points *(lecture seule)*"""
        return self._points

    # ======================================== INTERNALS ========================================
    def _push(self, x: float, y: float) -> None:
        """Ajoute un point si la distance minimale est respectée

        Args:
            x: coordonnée horizontale monde
            y: coordonnée verticale monde
        """
        if self._points:
            lx, ly, _ = self._points[-1]
            dx, dy = x - lx, y - ly
            if dx * dx + dy * dy < self._min_distance * self._min_distance:
                return
        if len(self._points) >= self._MAX_POINTS:
            self._points.popleft()
        self._points.append((x, y, 0.0))

    def _tick(self, dt: float) -> None:
        """Avance les ages et expire les points trop vieux

        Args:
            dt: delta-time
        """
        self._points = deque((x, y, age + dt) for x, y, age in self._points)
        while self._points and self._points[0][2] >= self._duration:
            self._points.popleft()

# ======================================== EXPORTS ========================================
__all__ = [
    "TrailRenderer",
]