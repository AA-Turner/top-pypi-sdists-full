# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._flag import CoordSpace
from ..abc import Layer

from ._quad import ScreenQuad
from ._fbo import Framebuffer
from ._spaces import Window, LogicalScreen, Viewport, Camera

import pyglet.gl as gl
from pyglet.graphics import Batch, Group
from pyglet.math import Mat4
from pyglet.graphics.shader import ShaderProgram

from typing import TYPE_CHECKING
from dataclasses import dataclass
from contextlib import contextmanager
from ctypes import c_int

if TYPE_CHECKING: 
    from .._managers import CoordinatesManager
    from ..scene import Scene

# ======================================== DATA ========================================
@dataclass(slots=True, frozen=True)
class SceneData:
    fbo: Framebuffer
    layers: dict[Layer, LayerData]

@dataclass(slots=True, frozen=True)
class LayerData:
    batch: Batch
    z_groups: dict[int, Group]

# ======================================== PIPELINE ========================================
class Pipeline:
    """Pipeline de rendu OpenGl

    Args:
        window(Window): fenêtre associée
    """
    __slots__ = (
        "_window", "_quad", "_temp_fbo",
        "_data", "_projection_cache", "_view_cache",
        "_view_buffer", "_default_view",
        "_context",
    )

    _COORD: CoordinatesManager = None

    @classmethod
    def get_coord(cls) -> CoordinatesManager:
        """Renvoie l'instance du gestionnaire de coordonnées"""
        if cls._COORD is None:
            from .._managers import CoordinatesManager
            cls._COORD = CoordinatesManager.get_instance()
        return cls._COORD

    def __init__(self, window: Window):
        # Binding
        self._window: Window = window

        # Objets OpenGl
        self._quad: ScreenQuad = ScreenQuad()
        self._temp_fbo: Framebuffer = None

        # Cache
        self._data: dict[Scene, SceneData] = {}

        # Contexte
        self._context: _PipelineContext = _PipelineContext()

    # ======================================== GETTERS ========================================
    # OpenGl
    @property
    def quad(self) -> ScreenQuad:
        """Rectangle d'écran complet"""
        return self._quad
    
    @property
    def temp_fbo(self) -> Framebuffer:
        """Renvoie le FrameBuffer éphémère"""
        return self._temp_fbo
    
    @property
    def gl_viewport(self) -> tuple[int, int, int, int]:
        """Viewport OpenGl"""
        return self._context.gl_viewport
    
    # Pipeline interne
    @property
    def window(self) -> Window:
        """Fenêtre OS assignée"""
        return self._window
    
    @property
    def screen(self) -> LogicalScreen:
        """Espace logique de référence assigné"""
        return self._window.screen
    
    @property
    def viewport(self) -> Viewport:
        """Viewport de la scène en cours de rendu"""
        return self._context.viewport

    @property
    def camera(self) -> Camera:
        """Caméra du layer en cours de rendu"""
        return self._context.camera
    
    # Assgination courante
    @property
    def scene(self) -> Scene:
        """Scene en cours de rendu"""
        return self._context.scene
    
    @property
    def layer(self) -> Layer:
        """Layer en couche de rendu"""
        return self._context.layer
    
    # Etat courant
    @property
    def batch(self) -> Batch:
        """Batch courant"""
        return self._context.batch
    
    @property
    def fbo(self) -> Framebuffer:
        """Framebuffer courant"""
        return self._context.fbo
    
    @property
    def z_groups(self) -> dict[int, Group]:
        """Groupes du ``Layer`` courant selon leur ``z-order``"""
        return self._context.z_groups
    
    # Résolutions
    @property
    def viewport_resolve(self) -> tuple[float, float, float, float]:
        """Résolution du viewport dans l'espace logique"""
        return self._context.viewport_resolve
    
    @property
    def camera_resolve(self) -> tuple[float, float, float, float, float, float, tuple[float, float]]:
        """Résolution de la caméra"""
        return self._context.camera_resolve
    
    # Matrices
    @property
    def projection_matrix(self) -> Mat4:
        """Matrice de projection"""
        return self._context.projection_matrix
    
    @property
    def view_matrix(self) -> Mat4:
        """Matrice de vue"""
        return self._context.view_matrix
    
    # ======================================== INTERFACE ========================================
    def get_group(self, z: int = 0) -> Group:
        """Renvoie le ``Group`` associé au z-order donné dans le ``Layer``courant

        Args:
            z (int): z-order du groupe
        """
        if z not in self._context.z_groups:
            self._context.z_groups[z] = Group(order=z)
        return self._context.z_groups[z]
    
    def apply_shader(self, program: ShaderProgram, **uniforms) -> None:
        """Applique un shader post-process sur le FBO courant (ping-pong)

        Args:
            program: shader program à appliquer
            **uniforms: uniforms à passer au shader (u_texture réservé)
        """
        scene_fbo = self._context.fbo
        temp_fbo = self._get_temp_fbo(scene_fbo)

        gl.glViewport(0, 0, scene_fbo.width, scene_fbo.height)

        temp_fbo.bind()
        temp_fbo.clear()
        program.use()
        for name, value in uniforms.items():
            program[name] = value
        program['u_texture'] = 0
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, scene_fbo.texture_id)
        self.quad.draw_raw()

        scene_fbo.bind()
        scene_fbo.clear()
        self.quad.blit(temp_fbo.texture_id)
        scene_fbo.bind()

        gl.glViewport(*self._context.gl_viewport)

    # ======================================== PIPELINE ========================================
    def bind_scene(self, scene: Scene) -> None:
        """Configure le contexte de rendu pour une scene

        Args:
            scene: scene courante
        """
        # Raccourcis
        screen = self._window.screen

        # Création du cache si nécessaire
        if scene not in self._data:
            fbo = Framebuffer(screen.width, screen.height)
            self._data[scene] = SceneData(fbo, {})
        else:
            fbo = self._data[scene].fbo

        # Assignation de la scene
        self._context.scene = scene
        self._context.viewport = scene.viewport
        self._context.main_camera = scene.camera
        self._context.fbo = fbo

        # Calcul des matrices de la scene
        Vp: Mat4 = scene.viewport.viewport_matrix()
        P: Mat4 = scene.camera.projection_matrix(screen.width, screen.height)
        V: Mat4 = scene.camera.view_matrix()
        self._context.viewport_matrix = Vp        
        self._context.main_projection = P
        self._context.main_view = V
        self._context.main_static_matrix = Vp @ P

        # Assignation du FrameBuffer
        fbo.bind()

        # Calcul du viewport OpenGl
        gx, gy, gw, gh = self._context.viewport.resolve(screen.width, screen.height)
        gl.glViewport(gx, gy, gw, gh)
        self._context.gl_viewport = (gx, gy, gw, gh)

        # Nettoyage du FrameBuffer
        fbo.clear()

    def bind_layer(self, layer: Layer) -> None:
        """Configure le contexte de rendu pour un layer de la scene courante
        
        Args:
            layer: Layer courant
        """
        # Raccourcis
        screen = self._window.screen

        # Création du cache si nécessaire
        layers_data = self._data[self._context.scene].layers
        if layer not in layers_data:
            layers_data[layer] = LayerData(Batch(), {})

        # Assignation du layer
        self._context.layer = layer
        self._context.camera = layer.camera or self._context.scene.camera
        self._context.batch = layers_data[layer].batch
        self._context.z_groups = layers_data[layer].z_groups

        # Calcul des matrices du layer
        if self._context.camera is self._context.main_camera:
            P: Mat4 = self._context.main_projection
            V: Mat4 = self._context.main_view
            Sc: Mat4 = self._context.main_static_matrix
        else:
            Vp: Mat4 = self._context.viewport_matrix
            P: Mat4 = self._context.camera.projection_matrix(screen.width, screen.height)
            V: Mat4 = self._context.camera.view_matrix()
            Sc: Mat4 = Vp @ P
        self._context.projection_matrix = P
        self._context.view_matrix = V
        self._context.static_matrix = Sc

    def apply(self, projection: Mat4 = None, view: Mat4 = None) -> None:
        """Applique le contexte GPU courant
        
        Args:
            projection: matrice de projection *(par défault la matrice courante)*
            view: matrice de vue *(par défaut la matrice courante)*
        """
        # Application de la matrice de projection
        P = projection or self._context.static_matrix
        if P is not self._window.native.projection:
            self._window.native.projection = P

        # Application de la matrice de vue
        V = view or self._context.view_matrix
        if V is not self._window.native.view:
            self._window.native.view = view or self._context.view_matrix

    def flush(self) -> None:
        """Envoie tout le batch au GPU"""
        self._context.batch.draw()

    def end(self) -> None:
        """Met fin à la connexion avec une scene"""
        canvas = self._window.canvas

        # Blit FBO sur window
        gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
        gl.glViewport(
            canvas.x,
            canvas.y,
            canvas.width,
            canvas.height,
        )
        self._quad.blit(self._context.fbo.texture_id)

        # Nettoyage des caches temporaires
        self._context.camera.flush_view_cache_frame()

        # Nettoyage de l'état courant
        self._context.clear()
        
    # ======================================== SPACE CONVERSIONS ========================================    
    def convert(self, x: float, y: float, from_space: CoordSpace, to_space: CoordSpace, vector: bool = False, viewport: Viewport = None, camera: Camera = None) -> tuple[float, float]:
        """Convertit une position d'un espace à un autre

        x: position horizontale
        y: position verticale
        from_space: espace source
        to_space: espace cible
        viewport: viewport à utiliser (par défaut le viewport courant)
        camera: camera à utiliser (par défaut la camera courante)
        """
        coord = self.get_coord()
        with coord.temporary_context(viewport=viewport, camera=camera):
            return coord.convert(x, y, from_space, to_space, vector=vector)

    def world_to_framebuffer(self, x: float, y: float, vector: bool = False, viewport: Viewport = None, camera: Camera = None) -> tuple[int, int]:
        """Convertit un point monde en pixel framebuffer

        Args:
            x: coordonnée horizontale monde
            y: coordonnée verticale monde
            viewport: Viewport à utiliser (par défaut le viewport courant)
            camera: Camera à utiliser (par défaut la caméra courante)
        """
        coord = self.get_coord()
        with coord.temporary_context(viewport=viewport, camera=camera):
            return coord.world_to_framebuffer(x, y, vector=vector)

    def framebuffer_to_world(self, x: int, y: int, vector: bool = False, viewport: Viewport =  None, camera: Camera = None) -> tuple[float, float]:
        """Convertit un pixel framebuffer en point monde

        Args:
            x: coordonnée horizontale framebuffer
            y: coordonnée verticale framebuffer
            viewport: Viewport à utiliser (par défaut le viewport courant)
            camera: Camera à utiliser (par défaut la caméra courante)
        """
        coord = self.get_coord()
        with coord.temporary_context(viewport=viewport, camera=camera):
            return coord.framebuffer_to_world(x, y, vector=vector)

    # ======================================== UTILITAIRES ========================================
    def visible_world_rect(self) -> tuple[float, float, float, float]:
        """Renvoie ``(x_min, y_min, x_max, y_max)`` du frustum visible en coordonnées monde"""
        return self.get_coord().get_frustum_aabb()

    def scale_to_framebuffer(self, width: float | None = None, height: float | None = None) -> float | tuple[float, float]:
        """Convertit une taille monde en taille framebuffer
        
        Args:
            width: largeur monde
            height: hauteur monde
        """
        w = width if width is not None else 0
        h = height if height is not None else 0
        fb_w, fb_h = self.get_coord().world_to_framebuffer(w, h, vector=True)
        if width is None:
            return fb_h
        if height is None:
            return fb_w
        return fb_w, fb_h
    
    @contextmanager
    def scissor_world(self, wx: float, wy: float, ww: float, wh: float, viewport: Viewport = None, camera: Camera = None):
        """Context manager appliquant un scissor test en coordonnées monde

        Args:
            wx: x monde du coin bas-gauche
            wy: y monde du coin bas-gauche
            ww: largeur monde
            wh: hauteur monde
        """
        x0, y0 = self.world_to_framebuffer(wx, wy, viewport=viewport, camera=camera)
        x1, y1 = self.world_to_framebuffer(wx + ww, wy + wh, viewport=viewport, camera=camera)

        left = int(min(x0, x1))
        top = int(min(y0, y1))
        width = int(abs(x0 - x1))
        height = int(abs(y0 - y1))

        was_enabled = (gl.GLboolean * 1)()
        prev_box = (c_int * 4)()
        gl.glGetBooleanv(gl.GL_SCISSOR_TEST, was_enabled)
        gl.glGetIntegerv(gl.GL_SCISSOR_BOX, prev_box)

        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(left, top, width, height)
        try:
            yield
        finally:
            gl.glScissor(*prev_box)
            if not was_enabled[0]:
                gl.glDisable(gl.GL_SCISSOR_TEST)

    @contextmanager
    def scissor_framebuffer(self, x: float, y: float, w: float, h: float):
        """Context manager appliquant un scissor test en coordonnées Framebuffer

        Args:
            x: coordonnée horizontale coin bas-gauche
            y: coordonnée verticale du coin bas-gauche
            w: largeur
            h: hauteur
        """
        was_enabled = (gl.GLboolean * 1)()
        prev_box = (c_int * 4)()
        gl.glGetBooleanv(gl.GL_SCISSOR_TEST, was_enabled)
        gl.glGetIntegerv(gl.GL_SCISSOR_BOX, prev_box)

        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(x, y, w, h)
        try:
            yield
        finally:
            gl.glScissor(*prev_box)
            if not was_enabled[0]:
                gl.glDisable(gl.GL_SCISSOR_TEST)
        
    # ======================================== INTERNALS ========================================
    def _get_temp_fbo(self, fbo: Framebuffer) -> Framebuffer:
        """Renvoie le FrameBuffer temporaire"""
        if self._temp_fbo is None:
            self._temp_fbo = Framebuffer(fbo.width, fbo.height)
        elif self._temp_fbo.width != fbo.width or self._temp_fbo.height != fbo.height:
            self._temp_fbo.resize(fbo.width, fbo.height)
        return self._temp_fbo

# ======================================== CONTEXT ========================================
@dataclass(slots=True)
class _PipelineContext:
    # Binding
    scene: Scene = None
    layer: Layer = None

    # Configuration OpenGl
    gl_viewport: tuple = None
    fbo: Framebuffer = None
    batch: Batch = None
    z_groups: dict[int, Group] = None

    # Espaces
    viewport: Viewport = None
    main_camera: Camera = None
    camera: Camera = None
    
    # Matrices
    viewport_matrix: Mat4 = None
    projection_matrix: Mat4 = None
    view_matrix: Mat4 = None
    static_matrix: Mat4 = None

    main_projection: Mat4 = None
    main_view: Mat4 = None
    main_static_matrix: Mat4 = None

    pipeline_matrix: Mat4 = None
    inv_pipeline_matrix: Mat4 = None

    def clear(self) -> None:
        """Nettoie le contexte"""
        for attr in self.__slots__:
            setattr(self, attr, None)