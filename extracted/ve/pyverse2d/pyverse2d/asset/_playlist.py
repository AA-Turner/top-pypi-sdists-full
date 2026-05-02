# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, positive
from ..abc import Asset

from ._music import Music

from numbers import Real
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .._managers._audio import AudioManager

# ======================================== ASSET ========================================
class Playlist(Asset):
    """Playlist de musiques à jouer successivement
    
    Args:
        musics: liste des musiques
        shuffle: lecture aléatoire
        loop: lecture en boucle
        fade_in: fondu en ouverture *(en secondes)*
        fade_out: fondu en fermeture *(en secondes)*
        delay: délai entre chaque musique *(en secondes)*
        cross_fade: fondu de transition entre chaque musique *(en secondes)*
    """
    __slots__ = (
        "_musics",
        "_shuffle", "_loop",
        "_fade_in", "_fade_out",
        "_delay", "_cross_fade",
        "_order",
    )

    _AUDIO_MANAGER: AudioManager = None

    @classmethod
    def _get_audio_manager(cls) -> AudioManager:
        """Renvoie le gestionnaire audio"""
        if cls._AUDIO_MANAGER is None:
            from .._managers._audio import AudioManager
            cls._AUDIO_MANAGER = AudioManager.get_instance()
        return cls._AUDIO_MANAGER
    
    def __init__(
            self,
            musics: list[Music],
            shuffle: bool = False,
            loop: bool = False,
            fade_in: Real = 0.0,
            fade_out: Real = 0.0,
            delay: Real = 0.0,
            cross_fade: Real = 0.0,
        ):
        # Attributs publiques
        self._musics: list[Music] = musics
        self._shuffle: bool = shuffle
        self._loop: bool = loop
        self._fade_in: float = float(fade_in)
        self._fade_out: float= float(fade_out)
        self._delay: float = float(delay)
        self._cross_fade: float = float(cross_fade)

        if __debug__:
            expect(self._musics, list[Music])
            expect(self._shuffle, bool)
            expect(self._loop, bool)
            positive(self._fade_in)
            positive(self._fade_out)
            positive(self._delay)
            positive(self._cross_fade)

        # Attributs internes
        self._order: list[int] = None
        self._refresh_order()

    # ======================================== PROPERTIES ========================================
    @property
    def musics(self) -> list[Music]:
        """Renvoie la liste des musiques *(lecture seule)*"""
        return self._musics

    @property
    def order(self) -> list[int]:
        """Renvoie l'ordre de lecture des musiques *(lecture seule)*"""
        return self._order

    @property
    def shuffle(self) -> bool:
        """Lecture aléatoire"""
        return self._shuffle
    
    @shuffle.setter
    def shuffle(self, value: bool) -> None:
        assert isinstance(value, bool), f"shuffle ({value}) must be a boolean"
        if value == self._shuffle:
            return
        self._shuffle = value
        if self._shuffle:
            random.shuffle(self._order)

    @property
    def loop(self) -> bool:
        """Lecture en boucle"""
        return self._loop
    
    @loop.setter
    def loop(self, value: bool) -> None:
        assert isinstance(value, bool), f"loop ({value}) must be a boolean"
        self._loop = value

    @property
    def fade_in(self) -> float:
        """Fondu en ouverture

        Cette propriété fixe la durée *en secondes* d'augmentation progressive du son à la lecture.
        """
        return self._fade_in
    
    @fade_in.setter
    def fade_in(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"fade_in ({value}) must be positive"
        self._fade_in = value

    @property
    def fade_out(self) -> float:
        """Fondu en fermeture

        Cette propriété fixe la durée *en secondes* de réduction progressive du son à la fin de lecture.
        """
        return self._fade_out
    
    @fade_out.setter
    def fade_out(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"fade_out ({value}) must be positive"
        self._fade_out = value

    @property
    def delay(self) -> float:
        """Délai entre chaque musique

        Cette propriété fixe le temps d'attente entre chaque musique.
        La durée est *en secondes*.
        """
        return self._delay
    
    @delay.setter
    def delay(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"delay ({value}) must be positive"
        self._delay = value

    @property
    def cross_fade(self) -> float:
        """Fondu de transition

        Cette propriété fixe la durée *en secondes* de fondu entre chaque musique.
        """
        value = float(value)
        assert value >= 0.0, f"cross_fade ({value}) must be positive"
        self._cross_fade = value

    @cross_fade.setter
    def cross_fade(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"cross_fade ({value}) must be positive"
        self._cross_fade = value

    # ======================================== MUSICS ========================================
    def add(self, music: Music, index: int = -1) -> None:
        """Ajoute une musique à la liste

        Args:
            music: asset ``Music`` à ajouter
            index: indice d'insertion *(par défaut en dernier)*
        """
        if __debug__:
            expect(music, Music)
        if index < 0:
            self._musics.append(music)
        else:
            self._musics.insert(music, index)
        self._refresh_order()

    def remove(self, music: Music) -> None:
        """Supprime une musique de la liste
        
        Args:
            music: asset ``Music`` à supprimer
        """
        self._musics.remove(music)
        self._refresh_order()

    def pop(self, index: int) -> Music:
        """Supprime une musique de la liste par son indice

        Args:
            index: indice à supprimer

        Returns:
            music: l'asset ``Music`` supprimé de la liste
        """
        music = self._musics.pop(index)
        self._refresh_order()
        return music
    
    def get(self, index: int) -> Music:
        """Renvoie la musique à un indice donné
        
        Args:
            index: indice à vérifier
        """
        return self._musics[index]
    
    def clear(self) -> None:
        """Vide la liste des musiques"""
        self._musics.clear()
        self._order.clear()

    # ======================================== INTERFACE ========================================    
    def play(self) -> None:
        """Joue la playlist"""
        self._get_audio_manager().play_playlist(self)
    
    def resume(self) -> None:
        """Reprend la playlist"""
        if self._get_audio_manager().current_playlist != self:
            return
        self._get_audio_manager().resume_playlist()

    def pause(self) -> None:
        """Met pause à la playlist"""
        if self._get_audio_manager().current_playlist != self:
            return
        self._get_audio_manager().pause_playlist()

    def stop(self) -> None:
        """Arrête la playlist"""
        if self._get_audio_manager().current_playlist != self:
            return
        self._get_audio_manager().stop_playlist()
    
    # ======================================== INTERNALS ========================================
    def _refresh_order(self) -> None:
        """Applique la lecture aléatoire"""
        self._order = list(range(len(self._musics)))
        if self._shuffle:
            random.shuffle(self._order)