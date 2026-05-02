# ======================================== IMPORTS ========================================
from __future__ import annotations

from pyglet import media as _media

from typing import Callable, Any
from abc import ABC, abstractmethod

# ======================================== ABSTRACT CLASS ========================================
class AudioHandle(ABC):
    """Classe abstraite des tokens audio"""
    __slots__ = (
        "source", "player", "on_stop",
        "_active", "_base_volume", "_play_volume",
        "__weakref__",
    )

    def __init__(self, source: _media.StaticSource, player: _media.Player, on_stop: Callable[[AudioHandle], Any] = None):
        # Attributs publiques
        self.source: _media.StreamingSource = source
        self.player: _media.Player = player
        self.on_stop: Callable[[AudioHandle], Any] = on_stop

        # Attributs internes
        self._active: bool = True
        self._base_volume: float = 1.0
        self._play_volume: float = 1.0

        # Configuration du player
        self.player.push_handlers(on_player_eos=self.on_eos)

    # ======================================== PROPERTIES ========================================
    @property
    def base_volume(self) -> float:
        """Volume de base
        
        Le volume doit être un ``Réel`` positif.
        """
        return self._base_volume
    
    @base_volume.setter
    def base_volume(self, value: float) -> None:
        self._base_volume = value
        self._refresh_volume()
    
    @property
    def play_volume(self) -> float:
        """Volume ponctuel
        Le volume doit être un ``Réel`` positif.
        """
        return self._play_volume
    
    @play_volume.setter
    def play_volume(self, value: float) -> None:
        self._play_volume = value
        self._refresh_volume()

    # ======================================== GETTERS ========================================
    def get_volume(self) -> float:
        """Renvoie le volume de lecture"""
        return self._base_volume * self._play_volume
    
    # ======================================== SETTERS ========================================
    def set_volumes(self, base: float, play: float) -> None:
        """Fixe les deux types de volumes
        
        Args:
            base: volume de base
            play: volume de lecture
        """
        self._base_volume = base
        self._play_volume = play
        self._refresh_volume()
    
    # ======================================== PREDICATES ========================================
    def is_active(self) -> bool:
        """Vérifie que le handle soit actif"""
        return self._active

    def is_playing(self) -> bool:
        """Vérifie que le handle soit en cours de lecture"""
        return self._active and self.player.playing
    
    # ======================================== HOOKS ========================================
    @abstractmethod
    def on_eos(self) -> None: ...

    # ======================================== INTERFACE ========================================
    @abstractmethod
    def resume(self) -> None: ...

    @abstractmethod
    def pause(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    def delete(self) -> None:
        """Supprime le player sans déclencher les événements d'arrêt"""
        if self._active:
            self.player.pause()
            self.player.delete()
            self._active = False
            if self.on_stop:
                self.on_stop(self)
    
    # ======================================== INTERNALS ========================================
    def _refresh_volume(self) -> None:
        """Actualise le volume du player"""
        if self._active:
            self.player.volume = self.get_volume()