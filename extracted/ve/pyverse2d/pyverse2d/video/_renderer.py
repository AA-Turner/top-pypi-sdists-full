# ======================================== IMPORTS ========================================
from __future__ import annotations

from ._player import VideoPlayer

import pyglet.sprite as _sprite

# ======================================== RENDERER ========================================
class VideoRenderer:
    """Rendu d'un ``VideoPlayer`` dans le batch monde du layer courant"""

    @staticmethod
    def attach(player: VideoPlayer, batch, group) -> _sprite.Sprite:
        """Crée et retourne le sprite monde associé au player

        Args:
            player: ``VideoPlayer`` source
            batch: batch du layer courant
            group: group z-order du layer courant
        """
        texture = player.texture
        if texture is None:
            return None
        sprite = _sprite.Sprite(texture, x=player.x, y=player.y, batch=batch, group=group)
        sprite.scale_x = player.width / texture.width
        sprite.scale_y = player.height / texture.height
        return sprite

    @staticmethod
    def update(player: VideoPlayer, sprite: _sprite.Sprite) -> None:
        """Met à jour la frame courante du sprite

        Args:
            player: ``VideoPlayer`` source
            sprite: sprite monde associé
        """
        if sprite is None:
            return
        texture = player.texture
        if texture is not None:
            sprite.image = texture
            sprite.x = player.x
            sprite.y = player.y
            sprite.scale_x = player.width / texture.width
            sprite.scale_y = player.height / texture.height