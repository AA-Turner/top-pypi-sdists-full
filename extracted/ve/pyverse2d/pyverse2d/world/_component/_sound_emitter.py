# ======================================== IMPORTS ========================================
from __future__ import annotations

from pyverse2d._managers._audio import SoundHandle

from ..._internal import CallbackList, positive
from ...abc import Component, Request
from ...asset import Sound
from ...math.easing import EasingFunc, is_easing, linear

from numbers import Real
from dataclasses import dataclass
from typing import Callable

# ======================================== COMPONENT ========================================
class SoundEmitter(Component):
    """Composant permettant d'émettre des sons et musiques

    Ce composant est manipulé par ``SoundSystem``.

    Args:
        inner_radius: portée du son à plein volume
        outer_radius: portée absolue du son
        falloff: fonction d'atténuation du son
    """
    __slots__ = (
        "_volume", "_inner_radius", "_outer_radius", "_falloff",
        "_on_start", "_on_end",
        "_to_play", "_playing",
        "_registry",
    )

    def __init__(
            self,
            volume: Real = 1.0,
            inner_radius: Real = 0.0,
            outer_radius: Real = 0.0,
            falloff: EasingFunc = linear,
        ):
        # Attributs publiques
        self._volume: float = float(volume)
        self._inner_radius: float = abs(float(inner_radius))
        self._outer_radius: float = abs(float(outer_radius))
        self._falloff: EasingFunc = falloff

        if __debug__:
            positive(self._volume)
            if not is_easing(self._falloff): raise ValueError(f"falloff ({self._falloff}) must be an EasingFunc from math module")

        # Hooks
        self._on_start: CallbackList = CallbackList()
        self._on_end: CallbackList = CallbackList()

        # Buffer
        self._to_play: list[AudioRequest] = []
        self._playing: set[SoundHandle] = set()

        # Registry
        self._registry: dict[str, Sound] = {}

    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du composant"""
        return f"SoundEmitter(volume={self._volume}, inner_radius={self._inner_radius}, outer_radius={self._outer_radius})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._volume, self._inner_radius, self._outer_radius, self._falloff)
    
    def copy(self) -> SoundEmitter:
        """Renvoie une copie du composant"""
        new = SoundEmitter(
            volume = self._volume,
            inner_radius = self._inner_radius,
            outer_radius = self._outer_radius,
            falloff = self._falloff,
        )
        new._on_start._inject(self._on_start._exctract())
        new._on_end._inject(self._on_end._exctract())
        return new

    # ======================================== PROPERTIES ========================================
    @property
    def volume(self) -> float:
        """Volume propre du comosant

        Le volume doit être un ``Réel`` positif.
        """
        return self._volume
    
    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        assert value >= 0.0, f"volume ({value}) must be positive"
        self._volume = value

    @property
    def inner_radius(self) -> float:
        """Portée du son à plein volume

        Cette propriété fixe un rayon dans lequel le son est au volume normal.
        """
        return self._inner_radius
    
    @inner_radius.setter
    def inner_radius(self, value: Real) -> None:
        self._inner_radius = abs(float(value))

    @property
    def outer_radius(self) -> float:
        """Portée maximale du son

        Cette propriété fixe un rayon au-delà duquel le son n'est pas audible.
        Mettre cette propriété à ``0.0`` pour une portée infinie.
        """
        return self._outer_radius
    
    @outer_radius.setter
    def outer_radius(self, value: Real) -> None:
        self._outer_radius = abs(float(value))

    @property
    def falloff(self) -> EasingFunc:
        """Fonction d'atténuation

        L'atténuation se fait uniquement en inner_radius et outer_radius.
        Ne fonctionne pas avec un rayon infinie.
        """
        return self._falloff
    
    @falloff.setter
    def falloff(self, value: EasingFunc | None) -> None:
        assert value is None or is_easing(value), f"falloff ({value}) must be an EasingFunc from math module"
        self._falloff = value or linear

    # ======================================== HOOKS ========================================
    @property
    def on_start(self) -> CallbackList:
        """Début de lecture d'un son"""
        return self._on_start
    
    @property
    def on_end(self) -> CallbackList:
        """Fin de lecture d'un son"""
        return self._on_end
    
    # ======================================== REGSITRY ========================================
    def register(self, sound: Sound, name: str) -> None:
        """Enregistre un son

        Args:
            sound: son à enregistrer
            name: nom du son
        """
        self._registry[name] = sound

    def unregister(self, name: str) -> None:
        """Supprime l'enregistrement d'un son

        Args:
            name: nom du son
        """
        del self._registry[name]

    def get(self, name: str) -> Sound | None:
        """Renvoie un son pré-enregistrer

        Args:
            name: nom du son

        Raises:
            ValueError: si le son n'est pas présent dans le registre
        """
        return self._registry[name]
    
    def has(self, name: str) -> bool:
        """Vérifie la présence d'un son dans le registre
        
        Args:
            name: nom du son
        """
        return name in self._registry

    # ======================================== INTERFACE ========================================
    def emit(
            self,
            name: str,
            loop: bool = False,
            limit: int | None = None,
        ) -> None:
        """Joue un son pré-enregistrer
        
        Args:
            name: nom du son
        """
        self.play(self.get(name), loop=loop, limit=limit)

    def play(
            self,
            sound: Sound,
            loop: bool = False,
            limit: int | None = None,
        ) -> None:
        """Joue un son inconnu

        Args:
            sound: son à jouer
        """
        self._to_play.append(
            AudioRequest(
                sound = sound,
                loop = loop,
                limit = limit,
            )
        )

    def resume(self) -> None:
        """Reprend la lecture des sons"""
        for handle in self._playing:
            handle.resume()

    def pause(self) -> None:
        """Met en pause la lecture des sons"""
        for handle in self._playing:
            handle.pause()

    def stop(self) -> None:
        """Arrête la lecture des sons"""
        for handle in self._playing:
            handle.stop()

    # ======================================== INTERNALS ========================================
    def _add_handle(self, handle: SoundHandle) -> None:
        """Ajoute un ``SoundHandle`` à la liste des sons en cours de lecture"""
        self._playing.add(handle)
        self._on_start.trigger()

    def _remove_handle(self, handle: SoundHandle) -> None:
        """Retire un ``SoundHandle`` de la liste des sons en cours de lecture"""
        self._playing.discard(handle)
        self._on_end.trigger()
    
    def _clear_handles(self) -> None:
        """Vide la liste des sons en cours de lecture"""
        self._playing.clear()
        self._on_end.trigger()

# ======================================== REQUESTS ========================================
@dataclass(slots=True, frozen=True)
class AudioRequest(Request):
    """Reqûete de lecture d'un son"""
    sound: Sound
    loop: bool = False
    limit: int | None = None