# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import CallbackList, positive, expect, expect_callable
from ...abc import Component, Request
from ...asset import Sound
from ...math.easing import EasingFunc, linear
from ..._managers._audio import SoundHandle

from numbers import Real, Integral
from dataclasses import dataclass

# ======================================== COMPONENT ========================================
class SoundEmitter(Component):
    """Composant permettant d'émettre des sons et musiques

    Ce composant est manipulé par ``SoundSystem``.

    Args:
        volume: volume de l'émetteur
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
        # Transtypage et vérifications
        volume = float(volume)
        inner_radius = abs(float(inner_radius))
        outer_radius = abs(float(outer_radius))

        if __debug__:
            positive(volume)
            expect_callable(falloff)

        # Attributs publiques
        self._volume: float = volume
        self._inner_radius: float = inner_radius
        self._outer_radius: float = outer_radius
        self._falloff: EasingFunc = falloff

        # Hooks
        self._on_start: CallbackList | None = None
        self._on_end: CallbackList | None = None

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
        """Volume propre du composant

        Le volume doit être un ``Réel`` positif.
        """
        return self._volume
    
    @volume.setter
    def volume(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._volume = value

    @property
    def inner_radius(self) -> float:
        """Portée du son à plein volume

        Cette propriété fixe un rayon dans lequel le son est au volume normal.
        """
        return self._inner_radius
    
    @inner_radius.setter
    def inner_radius(self, value: Real) -> None:
        value = abs(float(value))
        self._inner_radius = value

    @property
    def outer_radius(self) -> float:
        """Portée maximale du son

        Cette propriété fixe un rayon au-delà duquel le son n'est pas audible.
        Mettre cette propriété à ``0.0`` pour une portée infinie.
        """
        return self._outer_radius
    
    @outer_radius.setter
    def outer_radius(self, value: Real) -> None:
        value = abs(float(value))
        self._outer_radius = value

    @property
    def falloff(self) -> EasingFunc:
        """Fonction d'atténuation

        L'atténuation se fait uniquement en inner_radius et outer_radius.
        Ne fonctionne pas avec un rayon infinie.
        """
        return self._falloff
    
    @falloff.setter
    def falloff(self, value: EasingFunc) -> None:
        if __debug__:
            expect_callable(value)
        self._falloff = value

    # ======================================== HOOKS ========================================
    @property
    def on_start(self) -> CallbackList:
        """Début de lecture d'un son"""
        if self._on_start is None:
            self._on_start = CallbackList()
        return self._on_start
    
    @property
    def on_end(self) -> CallbackList:
        """Fin de lecture d'un son"""
        if self._on_end is None:
            self._on_end = CallbackList()
        return self._on_end
    
    # ======================================== REGSITRY ========================================
    def register(self, sound: Sound, name: str) -> None:
        """Enregistre un son

        Args:
            sound: son à enregistrer
            name: nom du son
        """
        if __debug__:
            expect(sound, Sound)
        self._registry[name] = sound

    def unregister(self, name: str) -> None:
        """Supprime l'enregistrement d'un son

        Args:
            name: nom du son
        """
        del self._registry[name]

    def __getitem__(self, name: str) -> Sound:
        """Renvoie un son pré-enregistrer

        Args:
            name: nom du son

        Raises:
            ValueError: si le son n'est pas présent dans le registre
        """
        return self._registry[name]

    def get(self, name: str) -> Sound | None:
        """Renvoie un son pré-enregistrer

        Args:
            name: nom du son
        """
        return self._registry.get(name)
    
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
        limit: Integral | None = None,
    ) -> None:
        """Joue un son pré-enregistrer
        
        Args:
            name: nom du son
        """
        self.play(self[name], loop=loop, limit=limit)

    def play(
        self,
        sound: Sound,
        loop: bool = False,
        limit: Integral | None = None,
    ) -> None:
        """Joue un son inconnu

        Args:
            sound: son à jouer
        """
        # Transtypage et vérifications
        loop = bool(loop)
        limit = int(limit) if limit is not None else None

        if __debug__:
            expect(sound, Sound)

        # Demande de lecture
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
        if self._on_start:
            self._on_start.trigger()

    def _remove_handle(self, handle: SoundHandle) -> None:
        """Retire un ``SoundHandle`` de la liste des sons en cours de lecture"""
        self._playing.discard(handle)
        if self._on_end:
            self._on_end.trigger()
    
    def _clear_handles(self) -> None:
        """Vide la liste des sons en cours de lecture"""
        self._playing.clear()
        if self._on_end:
            self._on_end.trigger()

# ======================================== REQUESTS ========================================
@dataclass(slots=True, frozen=True)
class AudioRequest(Request):
    """Requête de lecture d'un son
    
    Args:
        son: ``Sound`` asset à lire
        loop: lecture en boucle
        limit: limite de répétitions
    """
    sound: Sound
    loop: bool = False
    limit: int | None = None

# ======================================== EXPORTS ========================================
__all__ = [
    "SoundEmitter",
    "AudioRequest",
]