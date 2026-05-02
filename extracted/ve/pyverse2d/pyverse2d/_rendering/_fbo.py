from __future__ import annotations

import pyglet.image
import pyglet.image.buffer
import pyglet.gl as gl


class Framebuffer:
    """Wrapper FBO"""
    __slots__ = ("_fbo", "_texture")

    def __init__(self, width: int, height: int):
        self._texture = pyglet.image.Texture.create(
            width, height,
            min_filter=gl.GL_LINEAR,
            mag_filter=gl.GL_LINEAR,
        )
        self._fbo = pyglet.image.buffer.Framebuffer()
        self._fbo.attach_texture(self._texture, attachment=gl.GL_COLOR_ATTACHMENT0)

    # ======================================== PROPRIÉTÉS ========================================

    @property
    def width(self) -> int:
        """Largeur du Framebuffer"""
        return self._texture.width

    @property
    def height(self) -> int:
        """Hauteur du Framebuffer"""
        return self._texture.height

    @property
    def texture_id(self) -> int:
        """Identifiant de la texture"""
        return self._texture.id

    # ======================================== INTERFACE ========================================

    def bind(self) -> None:
        """Rend dans ce FBO"""
        self._fbo.bind()

    def unbind(self) -> None:
        """Revient au framebuffer principal"""
        self._fbo.unbind()

    def clear(self) -> None:
        """Efface le contenu du FBO (doit être bindé)"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def resize(self, width: int, height: int) -> None:
        """Recrée la texture aux nouvelles dimensions et la réattache"""
        self._fbo.delete()
        self._texture = pyglet.image.Texture.create(
            width, height,
            min_filter=gl.GL_LINEAR,
            mag_filter=gl.GL_LINEAR,
        )
        self._fbo = pyglet.image.buffer.Framebuffer()
        self._fbo.attach_texture(self._texture, attachment=gl.GL_COLOR_ATTACHMENT0)

    def delete(self) -> None:
        """Libère les ressources GPU"""
        self._fbo.delete()