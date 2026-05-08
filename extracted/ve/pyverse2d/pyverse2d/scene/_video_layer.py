# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..abc import Layer
from ..video import VideoPlayer, VideoRenderer

import pyglet.sprite as _sprite

# ======================================== RENDERER ========================================
class VideoLayer(Layer):
    """Layer portant des ``VideoPlayer``

    Les players sont créés indépendamment et ajoutés via ``add()``.
    Le layer orchestre leur update et leur rendu dans le viewport de la scène parente,
    via le batch monde — les players sont ainsi observés par la caméra du layer.
    """
    __slots__ = ("_players", "_sprites")

    def __init__(self):
        super().__init__()
        self._players: list[VideoPlayer] = []
        self._sprites: dict[VideoPlayer, _sprite.Sprite] = {}

    # ======================================== INTERFACE ========================================
    def add(self, player: VideoPlayer) -> None:
        """Ajoute un player au layer

        Args:
            player: ``VideoPlayer`` à ajouter
        """
        if player not in self._players:
            self._players.append(player)

    def remove(self, player: VideoPlayer) -> None:
        """Retire un player du layer

        Args:
            player: ``VideoPlayer`` à retirer
        """
        player.stop()
        sprite = self._sprites.pop(player, None)
        if sprite is not None:
            sprite.delete()
        self._players.remove(player)

    def clear(self) -> None:
        """Arrête et retire tous les players"""
        for player in self._players:
            player.stop()
        for sprite in self._sprites.values():
            sprite.delete()
        self._players.clear()
        self._sprites.clear()

    @property
    def players(self) -> tuple[VideoPlayer, ...]:
        """Players actifs *(lecture seule)*"""
        return tuple(self._players)

    # ======================================== CYCLE DE VIE ========================================
    def update(self, dt: float) -> None:
        """Actualisation des frames courantes

        Args:
            dt: delta-time
        """
        for player in self._players:
            sprite = self._sprites.get(player)
            if sprite is not None:
                VideoRenderer.update(player, sprite)

    def draw(self, pipeline) -> None:
        """Rendu de tous les players via le batch monde du pipeline

        Les sprites sont attachés au batch/group du layer courant à la première
        frame de rendu, puis mis à jour chaque frame via ``VideoRenderer``.

        Args:
            pipeline: pipeline de rendu courant
        """
        batch = pipeline.batch
        group = pipeline.get_group(z=0)

        for player in self._players:
            if player not in self._sprites:
                sprite = VideoRenderer.attach(player, batch, group)
                if sprite is not None:
                    self._sprites[player] = sprite