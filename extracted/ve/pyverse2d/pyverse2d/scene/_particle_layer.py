# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect
from .._rendering import Pipeline, Camera
from ..abc import Layer, ParticleEmitter, ParticleModifier
from ..fx import ParticleRenderer

from typing import Type

# ======================================== LAYER ========================================
class ParticleLayer(Layer):
    """Layer gérant les particules

    Args:
        additive: blending additif ou alpha classique
        camera: caméra locale
    """
    __slots__ = (
        "_additive",
        "_emitters", "_modifiers",
        "_renderer",
    )

    def __init__(self, additive: bool = True, camera: Camera = None):
        # Transtypage
        additive = bool(additive)

        # Initialisation du layer
        super().__init__(camera)

        # Attributs publiques
        self._additive: bool = bool(additive)

        # Attributs internes
        self._emitters: set[ParticleEmitter] = []
        self._modifiers: list[ParticleModifier] = []

        # Renderer
        self._renderer: ParticleRenderer = ParticleRenderer()

    # ======================================== PROPERTIES ========================================
    @property
    def additive(self) -> bool:
        """Blending additif ou alpha classique"""
        return self._additive

    @additive.setter
    def additive(self, value: bool) -> None:
        self._additive = bool(value)

    # ======================================== EMITTERS ========================================
    def add_emitter(self, emitter: ParticleEmitter) -> None:
        """Ajoute un émetteur

        Args:
            emitter: émetteur à ajouter
        """
        if __debug__:
            expect(emitter, ParticleEmitter)
        self._emitters.append(emitter)

    def remove_emitter(self, emitter: ParticleEmitter) -> None:
        """Retire un émetteur
        
        Args:
            emitter: émetter à retirer
        """
        self._emitters.discard(emitter)

    def get_emitters(self) -> set[ParticleEmitter]:
        """Renvoie la liste des émetteurs *(lecture seule)*"""
        return self._emitters
    
    # ======================================== MODIIFERS ========================================
    def add_modifier(self, modifier: ParticleModifier) -> None:
        """Ajoute un modifieur
        
        Args:
            modifier: ``ParticleModifier``à ajouter
        """
        if __debug__:
            expect(modifier, ParticleModifier)
        self._modifiers.append(modifier)

    def remove_modifier(self, modifier: ParticleModifier) -> None:
        """Retire un modifieur

        Args:
            modifier: ``ParticleModifier`` à retirer
        """
        self._modifiers.remove(modifier)

    def pop_modifier(self, index: int) -> ParticleModifier:
        """Supprime un modifieur par indice

        Args:
            index: indice du ``ParticleModifier`` à supprimer

        Returns:
            ParticleModifier: le modifieur supprimé
        """
        return self._modifiers.pop(index)

    def get_modifiers(self, modifier_type: Type[ParticleModifier] | None = None) -> list[ParticleModifier]:
        """Renvoie la liste des modifiers *(lecture seule)*"""
        if modifier_type is None:
            return self._modifiers
        return [modifier for modifier in self._modifiers if type(modifier) is modifier_type]
    
    def has_modifier(self, modifier_type: Type[ParticleModifier]) -> bool:
        """Vérifie la présence d'un modifieur
        
        Args:
            modifieur_type: type de modifieur
        """
        for modifier in self._modifiers:
            if type(modifier) is modifier_type:
                return True
        return False

    # ======================================== HOOKS ========================================
    def on_start(self):
        """Activation du layer"""
        pass

    def on_stop(self):
        """Désactivation du layer"""
        pass

    # ======================================== LIFE CYCLE ========================================
    def _preload(self):
        """Préchargement spécialisé"""

    def _update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        for emitter in self._emitters:
            emitter.update(dt, modifiers=(self._modifiers or None))

    def _draw(self, pipeline: Pipeline) -> None:
        """Affichage
        
        Args:
            pipeline: ``Pipeline`` de rendu courante
        """
        self._renderer.render(pipeline, self._emitters, self._additive)