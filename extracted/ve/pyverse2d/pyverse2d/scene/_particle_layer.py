# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, profile_section, over
from .._rendering import Pipeline, Camera
from ..abc import Layer, ParticleEmitter, ParticleModifier
from ..fx import ParticleRenderer

from typing import Type, ClassVar
from numbers import Real
from contextlib import nullcontext

# ======================================== LAYER ========================================
class ParticleLayer(Layer):
    """Layer gérant les particules

    Args:
        additive: blending additif ou alpha classique
        scissor: rect de limitation du rendu ``(x, y, width, height)``
        camera: caméra locale
    """
    __slots__ = (
        "_additive", "_scissor",
        "_emitters", "_modifiers",
        "_renderer",
    )

    _IS_FX: ClassVar[bool] = True

    def __init__(self, additive: bool = True, camera: Camera = None):
        # Transtypage
        additive = bool(additive)

        # Initialisation du layer
        super().__init__(camera)

        # Attributs publiques
        self._additive: bool = additive
        self._scissor: tuple[float, float, float, float] = None

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
        value = bool(value)
        self._additive = value

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
    
    # ======================================== SCISSOR ========================================
    def set_scissor(self, x: Real, y: Real, width: Real, height: Real) -> None:
        """Fixe le rect de rendu

        Args:
            x: position horizontale
            y: position verticale
            width: largeur
            height: hauteur
        """
        # Transtypage et vérifications
        x = float(x)
        y = float(y)
        width = float(width)
        height = float(height)

        if __debug__:
            over(width, 0, include=False)
            over(height, 0, include=False)

        # Application
        self._scissor = (x, y, width, height)

    def clear_scissor(self) -> None:
        """Retire la limitation du rendu"""
        self._scissor = None

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

    @profile_section("scene.particle_layer.update")
    def _update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        for emitter in self._emitters:
            emitter.update(dt, modifiers=(self._modifiers or None))

    @profile_section("scene.particle_layer.draw")
    def _draw(self, pipeline: Pipeline) -> None:
        """Affichage
        
        Args:
            pipeline: ``Pipeline`` de rendu courante
        """
        ctx = pipeline.scissor_world(*self._scissor) if self._scissor else nullcontext()
        with ctx:
            self._renderer.render(pipeline, self._emitters, self._additive)

# ======================================== EXPORTS ========================================
__all__ = [
    "ParticleLayer",
]