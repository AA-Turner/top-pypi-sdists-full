# ======================================== IMPORTS ========================================
from __future__ import annotations

from ..._internal import expect
from ...abc import Component, Request
from ...asset import Animation, Image

from dataclasses import dataclass
from typing import Callable, ClassVar

# ======================================== REQUEST ========================================
@dataclass(frozen=True)
class AnimationRequest(Request):
    """Requête d'animation

    Args:
        animation: animation à activer
        loop: répétition de l'animation
        cutable: supprimer / reset si elle perd la main
        priority: niveau de priorité de l'animation
        tag: label de l'animation
        condition: condition d'activation de l'animation
        on_start): fonction de début d'animation
        on_end: fonction de fin d'animation
    """
    animation: Animation
    loop: bool = False
    cutable: bool = True
    priority: int = 0
    tag: str | None = None
    condition: Callable[[], bool] | None = None
    on_start: Callable[[], None] | None = None
    on_end: Callable[[], None] | None = None

# ======================================== COMPONENT ========================================
class Animator(Component):
    """Composant gérant l'animation d'une entité

    Ce composant est manipulé par ``AnimationSystem``.

    Args:
        idle: animation par défaut
    """
    __slots__ = (
        "_idle",
        "_current_request", "_current_animation", "_frame", "_elapsed",  "_requests",
    )

    requires: ClassVar[tuple[str, ...]] = ("SpriteRenderer",)

    AnimationRequest: ClassVar[type[AnimationRequest]] = AnimationRequest

    def __init__(self, idle: Animation = None):
        # Vérifications
        if __debug__:
            expect(idle, (Animation, None))

        # Attributs publiques
        self._idle: Animation = idle

        # Attributs internes
        self._requests: list[AnimationRequest] = []
        self._current_request: AnimationRequest | None = None
        self._current_animation: Animation | None = self._idle
        self._frame: int = 0
        self._elapsed: float = 0.0
    
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation de l'animateur"""
        return f"Animator(current={self._current_animation}, frame={self._frame})"
    
    def get_attributes(self) -> tuple:
        """Renvoie les attributs du composant"""
        return (self._idle, self._requests, self._current_request, self._current_animation, self._frame, self._elapsed)
    
    def copy(self) -> Animator:
        """Renvoie une copie du composant"""
        new = Animator(self._idle)
        return new

    # ======================================== PROPERTIES ========================================
    @property
    def idle(self) -> Animation:
        """Renvoie l'animation par défaut"""
        return self._idle
    
    @property
    def current_request(self) -> AnimationRequest | None:
        """Renvoie la requête en cours de traitement"""
        return self._current_request

    @property
    def current_animation(self) -> Animation | None:
        """Renvoie l'animation actuelle"""
        return self._current_animation
    
    @property
    def current_index(self) -> int:
        """Renvoie l'indice courant"""
        return self._frame

    @property
    def current_frame(self) -> Image | None:
        """Renvoie la frame actuelle"""
        return self._current_animation[self._frame] if self._current_animation else None
    
    @property
    def requests(self) -> list[AnimationRequest]:
        """Renvoie la liste courante des requêtes"""
        return self._requests
    
    # ======================================== SETTERS ========================================
    @idle.setter
    def idle(self, value: Animation | None) -> None:
        """Fixe l'animation par défaut"""
        self._idle = expect(value, (Animation, None))

    # ======================================== PUBLIC ========================================
    def register(self, request: AnimationRequest) -> None:
        """Enregistre une requête d'animation

        Args:
            request: requête d'animation à enregistrer
        """
        self._requests.append(expect(request, AnimationRequest))

    def unregister(self, request: AnimationRequest) -> None:
        """Retire une requête d'animation

        Args:
            request: requête d'animation à retirer
        """
        self._requests.remove(request)
    
    def unregister_tag(self, tag: str) -> None:
        """Retire les requêtes d'animation avec un certain label

        Args:
            tag: label des requêtes à supprimer
        """
        self._requests = [request for request in self._requests if request.tag != tag]

# ======================================== EXPORTS ========================================
__all__ = [
    "AnimationRequest",
    "Animator",
]