# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect, positive
from ...abc import Space
from ...math import Point, Vector

from pyglet.math import Mat4

from numbers import Real

# ======================================== VIEWPORT ========================================
class Viewport(Space):
    """Zone de l'espace logique

    Args:
        position: position du coin bas gauche du viewport
        width: largeur en pixels logiques (None = tout)
        height: hauteur en pixels logiques (None = tout)
        origin: origine locale relative du viewport *((0.5, 0.5) = centre)*
        x_direction: direction locale des coordonnées horizontales
        y_direction: direction locale des coordonnées verticales
    """
    __slots__ = (
        "_position",
        "_width", "_height",
        "_origin", "_x_direction", "_y_direction",
    )

    _VIEWPORT_CACHE: dict[tuple, Mat4] = {}

    def __init__(
        self,
        position: Point = (0.0, 0.0),
        width: Real = 0.0,
        height: Real = 0.0,
        origin: Point = (0.0, 0.0),
        x_direction: Vector = (1.0, 0.0),
        y_direction: Vector = (0.0, 1.0),
    ):
        # Transtypage
        position = Point(position)
        width = float(width)
        height = float(height)
        origin = Point(origin)
        x_direction = Vector(x_direction)
        y_direction = Vector(y_direction)

        # Debugging
        if __debug__:
            positive(width, arg="width")
            positive(height, arg="height")
            if x_direction.is_collinear(y_direction): raise ValueError("A basis cannot have collinear direction vectors")

        # Attributs publiques
        self._position: Point = position
        self._width: float = width
        self._height: float = height
        self._origin: Point = origin
        self._x_direction: Vector = x_direction
        self._y_direction: Vector = y_direction

    # ======================================== PROPERTIES ========================================
    @property
    def position(self) -> Point:
        """Position du coin bas gauche

        La position peut-être un objet mathématique ``Point`` ou un tuple ``(x, y)``
        """
        return self._position
    
    @position.setter
    def position(self, value: Point):
        self._position.x, self._position.y = value

    @property
    def x(self) -> float:
        """Cordonnée horizontale du coin bas gauche
        
        La valeur doit être un ``Réel``.
        """
        return self._position.x
    
    @x.setter
    def x(self, value: Real):
        self._position.x = value

    @property
    def y(self) -> float:
        """Coordonnée verticale du coin bas gauche

        La valeur doit être un ``Réel``.
        """
        return self._position.y
    
    @y.setter
    def y(self, value: Real):
        self._position.y = value

    @property
    def width(self) -> float:
        """Largeur du viewport
        
        La largeur doit être un ``Réel`` positif non nul.
        """
        return self._width
    
    @width.setter
    def width(self, value: Real):
        value = float(value)
        if __debug__:
            positive(value)
        self._width = value

    @property
    def height(self) -> float:
        """Hauteur du viewport
        
        La hauteur doit être un ``Réel`` positif non nul.
        """
        return self._height
    
    @height.setter
    def height(self, value: Real):
        value = float(value)
        if __debug__:
            positive(value)
        self._height = value

    @property
    def origin(self) -> Point:
        """Origine relative du viewport

        L'origine peut être un objet ``Point`` ou un tuple ``(ox, oy)``.
        Les coordonnées de l'origine doivent être dans l'intervalle [0, 1].
        """
        return self._origin
    
    @origin.setter
    def origin(self, value: Point) -> None:
        self._origin.x, self._origin.y = value

    @property
    def x_direction(self) -> Vector:
        """Vecteur directionnel x

        Le vecteur peut être un objet ``Vector`` ou un tuple ``(dx, dy)``.
        Cette propriété permet de transformer la direction horiontale dans le viewport.
        """
        return self._x_direction

    @x_direction.setter
    def x_direction(self, value: Vector) -> None:
        self._x_direction.x, self._x_direction.y = value

    @property
    def y_direction(self) -> Vector:
        """Vecteur directionnel y

        Le vecteur peut être un objet ``Vector`` ou un tuple ``(dx, dy)``.
        Cette propriété permet de transformer la direction verticale dans le viewport.
        """
        return self._y_direction

    @y_direction.setter
    def y_direction(self, value: Vector) -> None:
        self._y_direction.x, self._y_direction.y = value

    # ======================================== COLLECTIONS ========================================
    def copy(self) -> Viewport:
        """Crée une copie du viewport"""
        return Viewport(
            position = self._position,
            width = self._width,
            height = self._height,
            origin = self._origin,
            x_direction = self._x_direction,
            y_direction = self._y_direction,
        )
    
    # ======================================== RESOLVE ========================================
    def resolve(self, fb_width: int, fb_height: int) -> tuple[int, int, int, int]:
        """Renvoie le viewport résolu ``(x, y, width, height)`` dans le Framebuffer
        
        Args:
            fb_width: largeur du framebuffer
            fb_height: hauteur du framebuffer
        """
        x = int(self._position.x)
        y = int(self._position.y)
        width = int(self._width) if self._width != 0.0 else fb_width
        height = int(self._height) if self._height != 0.0 else fb_height
        return (x, y, width, height)
    
    def basis_resolve(self) -> tuple[float, float, float, float, float, float]:
        """Renvoie la résolution locale ``(ox, oy, ix, iy, jx, jy)`` dans le viewport"""
        ox, oy = self._origin
        ix, iy = self._x_direction
        jx, jy = self._y_direction
        return (ox, oy, ix, iy, jx, jy)

    # ======================================== COMPUTE ========================================
    def viewport_matrix(self) -> Mat4:
        """Renvoie la matrice du viewport"""
        # Renommage
        ox, oy = self._origin
        ix, iy = self._x_direction
        jx, jy = self._y_direction

        # Cache
        viewport_key: tuple = (ox, oy, ix, iy, jx, jy)
        if viewport_key in self._VIEWPORT_CACHE:
            return self._VIEWPORT_CACHE[viewport_key]
        
        # Construction
        matrix = self._compute_viewport(ox, oy, ix, iy, jx, jy)
        self._VIEWPORT_CACHE[viewport_key] = matrix
        return matrix
    
    # ======================================== INTERNALS ========================================
    def _compute_viewport(self, ox: float, oy: float, ix: float, iy: float, jx: float, jy: float) -> Mat4:
        """Compute la matrice du viewport *(TS)^(-1)*

        Espace: *NDC* to *NDC*

        Args:
            ox: origine horizontale relative locale du viewport
            oy: origine verticale relative locale du viewport
            ix: composante x du vecteur directionnel i
            iy: composante y du vecteur directionnel i
            jx: composante x du vecteur directionnel j
            jy: composante y du vecteur directionnel j
        """
        # Calcul des paramètres
        ox_ndc = 2 * ox - 1
        oy_ndc = 2 * oy - 1

        det = ix * jy - iy * jx
        inv_det = 1.0 / det

        m00 =  jy * inv_det
        m01 = -jx * inv_det
        m10 = -iy * inv_det
        m11 =  ix * inv_det

        # Translation inverse
        tu = -(m00 * ox_ndc + m01 * oy_ndc)
        tv = -(m10 * ox_ndc + m11 * oy_ndc)

        # Construction de la matrice
        return Mat4(
            m00,   m10,   0,     0,
            m01,   m11,   0,     0,
            0,     0,     1,     0,
            tu,    tv,    0,     1,
        )