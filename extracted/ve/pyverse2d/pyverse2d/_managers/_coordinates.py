# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._flag import CoordSpace
from .._rendering import Viewport, Camera
from ..abc import Manager

from pyglet.math import Mat4

from ._context import ContextManager

# ======================================== ERRORS ========================================
class NoContextError(RuntimeError):
    """Aucun contexte appliqué"""
    def __str__(self):
        return "No context applied. Call apply_context() before converting coordinates."

# ======================================== MANAGER ========================================
class CoordinatesManager(Manager):
    """Gestionnaire global des conversions de coordonnées"""
    __slots__ = (
        "_viewport", "_camera", "_temporary_camera",
        "_context_applied",
        "_view_matrix", "_projection_matrix", "_viewport_matrix", "_viewport_resolve",
        "_pipeline", "_inv_pipeline",
    )

    _ID: str = "coordinates"

    def __init__(self, context_manager: ContextManager) -> None:
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Contexte
        self._viewport: Viewport = None
        self._camera: Camera = None
        self._temporary_camera: Camera = None

        # Flag
        self._context_applied: bool = False

        # Cache de contexte
        self._view_matrix: Mat4 = None
        self._projection_matrix: Mat4 = None
        self._viewport_matrix: Mat4 = None
        self._viewport_resolve: tuple[int, int, int, int] = None

        # Cache dynamique
        self._pipeline: Mat4 = None
        self._inv_pipeline: Mat4 = None

    # ======================================== PROPERTIES ========================================
    @property
    def current_viewport(self) -> Viewport | None:
        """Renvoie le viewport courant"""
        return self._viewport
    
    @property
    def current_camera(self) -> Camera | None:
        """Renvoie la caméra courante"""
        return self._temporary_camera or self._camera
    
    @property
    def main_camera(self) -> Camera | None:
        """Renvoie la caméra principale"""
        return self._camera
    
    @property
    def temporary_camera(self) -> Camera | None:
        """Renvoie la caméra temporaire"""
        return self._temporary_camera

    # ======================================== BIND ========================================
    def bind_viewport(self, viewport: Viewport) -> None:
        """Fixe le viewport courant

        Args:
            viewport: viewport courant
            Vp: matrice viewport
        """
        self._viewport = viewport

    def bind_camera(self, camera: Camera) -> None:
        """Fixe la caméra principale courante

        Args:
            camera: caméra principale courante
        """
        self._camera = camera

    def bind_temporary_camera(self, camera: Camera) -> None:
        """Fixe la caméra locale courante

        Args:
            camera: caméra locale courante
        """
        self._temporary_camera = camera

    def unbind_temporary_camera(self) -> None:
        """Restaure la caméra principale"""
        self._temporary_camera = None

    # ======================================== CONTEXT ========================================
    def apply_context(self) -> None:
        """Applique le contexte courant"""
        # Nettoyage des caches
        self.clear_cache()

        # Vérification du viewport
        viewport = self.current_viewport
        if viewport is None:
            raise RuntimeError("Cannot apply context with no viewport set")
        
        # Vérification de la caméra
        camera = self.current_camera
        if camera is None:
            raise RuntimeError("Cannot apply context with no camera set")
        
        # Raccourcis
        fb_width, fb_height = self._window.screen.size
        
        # calcul des matrices et résolutions
        self._view_matrix = camera.view_matrix()
        self._projection_matrix = camera.projection_matrix(fb_width, fb_height)
        self._viewport_matrix = viewport.viewport_matrix()
        self._viewport_resolve = viewport.resolve(fb_width, fb_height)

        # Validation de l'application
        self._context_applied = True

    def clear_context(self) -> None:
        """Nettoie le contexte courant"""
        self._context_applied = False

        self._viewport = None
        self._camera = None
        self._temporary_camera = None

        self.clear_cache()

    def clear_cache(self) -> None:
        """Nettoie le cache courant"""
        self._view_matrix = None
        self._projection_matrix = None
        self._viewport_matrix = None
        self._viewport_resolve = None

        self._pipeline = None
        self._inv_pipeline = None
    
    # ======================================== TRANSFORMATIONS ========================================
    def homogeneous(self, x: float, y: float, vector: bool = False) -> tuple[float, float, float, float]:
        """Rend un objet mathématique homogène en 4D"""
        return (x, y, 0, 0) if vector else (x, y, 0, 1)
    
    # ======================================== INTERFACE ========================================
    def get_frustum_corners(self) -> tuple[tuple[float, float], ...]:
        """Renvoie les coins du frustum visible"""
        # Corners NDC
        corners = (
            (-1, -1, 0, 1),
            ( 1, -1, 0, 1),
            ( 1,  1, 0, 1),
            (-1,  1, 0, 1),
        )

        try:
            # Conversion monde
            inv_Pip = self._get_inv_pipeline()
            return tuple((inv_Pip @ c)[:2] for c in corners)
        except TypeError:
            raise NoContextError() from None
        
    def get_frustum_aabb(self) -> tuple[float, float, float, float]:
        """Renvoie le AABB ``(x_min, y_min, x_max, y_max)`` du frustum visible"""
        corners = self.get_frustum_corners()
        xs, ys = zip(*corners)
        return min(xs), min(ys), max(xs), max(ys)

    # ======================================== FROM WORLD ========================================
    def world_to_framebuffer(self, x: float, y: float, vector: bool = False) -> tuple[float, float]:
        """Conversion ``World`` vers ``Framebuffer``
        
        Args:
            x: coordonnée horizontal *(World)*
            y: coordonnée verticale *(World)*
            vector: ignore la translation
        """
        try:
            return self._world_to_framebuffer(x, y, vector)
        except TypeError:
            raise NoContextError() from None
        
    def _world_to_framebuffer(self, x: float, y: float, vector: bool) -> tuple[float, float]:
        """Logique interne de ``world_to_framebuffer``"""
        M = self.homogeneous(x, y, vector=vector)
        Pip = self._get_pipeline()
        ndc_x, ndc_y, _, _ = Pip @ M
        gx, gy, gw, gh = self._viewport_resolve
        if vector:
            return ndc_x * 0.5 * gw, ndc_y * 0.5 * gh
        else:
            return gx + (ndc_x + 1) * 0.5 * gw, gy + (ndc_y + 1) * 0.5 * gh

    def world_to_window(self, x: float, y: float, vector: bool = False) -> tuple[float, float]:
        """Conversion ``World`` vers ``Window``
        
        Args:
            x: coordonnée horizontal *(World)*
            y: coordonnée verticale *(World)*
            vector: ignore la translation
        """
        try:
            fb_x, fb_y = self._world_to_framebuffer(x, y, vector)
            win_x, win_y = self._framebuffer_to_window(fb_x, fb_y, vector)
            return win_x, win_y
        except TypeError:
            raise NoContextError() from None

    # ======================================== FROM FRAMEBUFFER ========================================
    def framebuffer_to_world(self, x:float, y: float, vector: bool = False) -> tuple[float, float]:
        """Conversion ``Framebuffer`` vers ``World``
        
        Args:
            x: coordonnée horizontal *(Logical)*
            y: coordonnée verticale *(Logical)*
            vector: ignore la translation
        """
        try:
            return self._framebuffer_to_world(x, y, vector)
        except TypeError:
            raise NoContextError() from None
        
    def _framebuffer_to_world(self, x: float, y: float, vector: bool) -> tuple[float, float]:
        """Logique interne de ``framebuffer_to_world``"""
        gx, gy, gw, gh = self._viewport_resolve
        if vector:
            ndc_x = x / gw * 2
            ndc_y = y / gh * 2
        else:
            ndc_x = (x - gx) / gw * 2 - 1
            ndc_y = (y - gy) / gh * 2 - 1
        M = self.homogeneous(ndc_x, ndc_y, vector=vector)
        inv_Pip = self._get_inv_pipeline()
        world_x, world_y, _, _ = inv_Pip @ M
        return world_x, world_y

    def framebuffer_to_window(self, x: float, y: float, vector: bool = False) -> tuple[float, float]:
        """Conversion ``Framebuffer`` vers ``Window``
        
        Args:
            x: coordonnée horizontal *(Logical)*
            y: coordonnée verticale *(Logical)*
            vector: ignore la translation
        """
        try:
            return self._framebuffer_to_window(x, y, vector)
        except TypeError:
            raise NoContextError() from None
        
    def _framebuffer_to_window(self, x: float, y: float, vector: bool) -> tuple[float, float]:
        """Logique interne de ``framebuffer_to_window``"""
        window = self._window
        if vector:
            return x * window.physical_scale, y * window.physical_scale
        canvas = window.canvas
        return canvas.x + x * window.physical_scale, canvas.y + y * window.physical_scale

    # ======================================== FROM WINDOW ========================================
    def window_to_world(self, x: float, y: float, vector: bool = False) -> tuple[float, float]:
        """Conversion ``Window`` vers ``World``
        
        Args:
            x: coordonnée horizontal *(Physical)*
            y: coordonnée verticale *(Physical)*
            vector: ignore la translation
        """
        try:
            fb_x, fb_y = self._window_to_framebuffer(x, y, vector)
            world_x, world_y = self._framebuffer_to_world(fb_x, fb_y, vector)
            return world_x, world_y
        except TypeError:
            raise NoContextError() from None

    def window_to_framebuffer(self, x: float, y: float, vector: bool = False) -> tuple[float, float]:
        """Conversion ``Window``vers ``Framebuffer``
        
        Args:
            x: coordonnée horizontal *(Phyisical)*
            y: coordonnée verticale *(Physical)*
            vector: ignore la translation
        """
        try:
            return self._window_to_framebuffer(x, y, vector)
        except TypeError:
            raise NoContextError() from None
        
    def _window_to_framebuffer(self, x: float, y: float, vector: bool) -> tuple[float, float]:
        """Logique interne de ``window_to_framebuffer``"""
        window = self._window
        if vector:
            return x * window.logical_scale, y * window.logical_scale
        canvas = window.canvas
        return (x - canvas.x) * window.logical_scale, (y - canvas.y) * window.logical_scale

    # ======================================== GLOBAL CONVERSION ========================================
    def convert(
        self,
        x: float,
        y: float,
        from_space: CoordSpace,
        to_space: CoordSpace,
        vector: bool = False,
    ) -> tuple[float, float]:
        """Convertit ``(x, y)`` entre deux espaces quelconques"""
        # Même espace
        if from_space == to_space:
            return (x, y)
        
        # Cas non géré
        handler = getattr(self, f"{from_space}_to_{to_space}", None)
        if handler is None:
            raise RuntimeError(f"No conversion from {from_space} to {to_space} available")
        
        # Conversion
        return handler(x, y, vector=vector)
    
    # ======================================== LIFE CYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        pass

    def flush(self) -> None:
        """Nettoyage"""
        pass

    # ======================================== INTERNALS ========================================
    def _compute_pipeline(self) -> None:
        """Génère la matrice composée"""
        self._pipeline = self._viewport_matrix @ self._projection_matrix @ self._view_matrix

    def _compute_inv_pipeline(self) -> None:
        """Génère la matrice composée inverse"""
        if self._pipeline is None:
            self._compute_pipeline()
        self._inv_pipeline = self._pipeline.__invert__()

    def _get_pipeline(self) -> Mat4:
        """Renvoie la matrice composée ``World`` to ``NDC``"""
        if self._pipeline is None:
            self._compute_pipeline()
        return self._pipeline
    
    def _get_inv_pipeline(self) -> Mat4:
        """Renvoie la matrice composée inverse ``NDC`` to ``World``"""
        if self._inv_pipeline is None:
            self._compute_inv_pipeline()
        return self._inv_pipeline

# ======================================== EXPORTS ========================================
__all__ = [
    "CoordinatesManager",
]