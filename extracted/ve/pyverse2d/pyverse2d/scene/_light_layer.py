# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, expect_subclass, positive
from .._rendering import Pipeline, Camera
from .._flag import Activity
from ..abc import Layer, LightSource, LightEffect
from ..fx import (
    PointLight, ConeLight,
    Ambient, Bloom, Tint, Vignette,
    LightRenderer,
)

from numbers import Real
from typing import Type

# ======================================== CONSTANTS ========================================
_SUPPORTED_EFFECT: frozenset[Type[LightEffect]] = frozenset({Ambient, Bloom, Tint, Vignette})

# ======================================== LAYER ========================================
class LightLayer(Layer):
    """Layer gérant la lumière

    Args:
        effects: effets lumineux
        gamma: facteur de luminosité global
        exposure: facteur d'intensité des sources lumineuses
        camera: caméra locale
    """
    __slots__ = (
        "_gamma", "_exposure",
        "_sources", "_active_points", "_active_cones",
        "_ambient", "_bloom", "_tint", "_vignette",
        "_renderer",
    )

    _IS_FX = True

    _DEFAULT_AMBIENT: Ambient = Ambient(level=1.0, shade=(1.0, 1.0, 1.0))

    def __init__(
            self,
            *effects: LightEffect,
            gamma: Real = 1.0,
            exposure: Real = 1.0,
            camera: Camera = None
        ):
        # Transtypage
        gamma = float(gamma)
        exposure = float(exposure)

        if __debug__:
            positive(gamma)
            positive(exposure)

        # Initialisation du layer
        super().__init__(camera)

        # Attributs publiques
        self._gamma: float = gamma
        self._exposure: float = exposure

        # Sources lumineuses
        self._active_points: list[PointLight] = []
        self._active_cones: list[ConeLight] = []
        self._sources: set[LightSource] = set()

        # Effets
        self._ambient: Ambient | None = None
        self._bloom: Bloom | None = None
        self._tint: Tint | None = None
        self._vignette: Vignette | None = None

        for effect in effects:
            self.add_effect(effect)

        # Renderer
        self._renderer: LightRenderer = LightRenderer()

    # ======================================== PROPERTIES ========================================
    @property
    def gamma(self) -> float:
        """Facteur de luminosité global

        Le gamma doit être un ``Réel`` positif.
        Mettre cette propriété à 1.0 pour une luminosité normale.
        """
        return self._gamma
    
    @gamma.setter
    def gamma(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._gamma = value

    @property
    def exposure(self) -> float:
        """Facteur d'intensité des lumières

        Le facteur doit être un ``Réel`` positif.
        Mettre cette propriété à 1.0 pour un éclairage par défaut.
        """
        return self._exposure
    
    @exposure.setter
    def exposure(self, value: Real) -> None:
        value = float(value)
        if __debug__:
            positive(value)
        self._exposure = value

    # ======================================== SOURCES ========================================
    def add_source(self, source: LightSource) -> None:
        """Ajoute une source de lumière

        Args:
            source: source à ajouter
        """
        assert isinstance(source, LightSource), f"source must be a LightSource, got {source}"
        self._sources.add(source)
        if source.is_enabled():
            self._get_active_list(source).append(source)

    def remove_source(self, source: LightSource) -> None:
        """Retire une source de lumière

        Args:
            source: source à retirer
        """
        if source.is_enabled():
            self._get_active_list(source).remove(source)
        self._sources.discard(source)

    def get_sources(self) -> set[LightSource]:
        """Renvoie l'ensemble des sources de lumière"""
        return self._sources
    
    # ======================================== EFFECTS ========================================
    def add_effect(self, effect: LightEffect) -> None:
        """Ajoute un effect lumineux
        
        Args:
            effect: effet à ajouter
        """
        id_ = self._effect_id(type(effect))
        if getattr(self, id_, None) is not None:
            raise RuntimeError(f"This layer has already an effect {type(effect).__name__}")
        setattr(self, id_, effect)

    def remove_effect(self, effect_type: Type[LightEffect]) -> LightEffect:
        """Supprime un effet

        Args:
            effect_type: type de l'effet à retirer

        Returns:
            LightEffect: effet retiré
        """
        id_ = self._effect_id(effect_type)
        effect = getattr(self, id_, None)
        if effect is None:
            raise RuntimeError(f"This layer has no effect {effect_type.__name__}")
        setattr(self, id_, None)
        return effect

    def get_effect(self, effect_type: Type[LightEffect]) -> LightEffect | None:
        """Renvoie un effet

        Args:
            effect_type: type de l'effet
        """
        id_ = self._effect_id(effect_type)
        return getattr(self, id_, None)
    
    def get_all_effects(self) -> tuple[LightEffect, ...]:
        """Renvoie l'ensemble des effets du ``LightLayer``"""
        return tuple(effect for effect_type in _SUPPORTED_EFFECT if (effect := getattr(self, f"_{effect_type.id()}")) is not None)

    def has_effect(self, effect_type: Type[LightEffect]) -> bool:
        """Vérifie la présence d'un effet

        Args:
            effect_type: type de l'effet à vérifier

        Returns:
            bool: présence
        """
        id_ = self._effect_id(effect_type)
        return getattr(self, id_, None) is None

    @property
    def ambient(self) -> Ambient | None:
        """Effet d'ambiance"""
        return self._ambient
    
    @ambient.setter
    def ambient(self, value: Ambient | None) -> None:
        if __debug__:
            expect(value, Ambient)
        self._ambient = value

    @property
    def bloom(self) -> Bloom | None:
        """Effet de saignement"""
        return self._bloom
    
    @bloom.setter
    def bloom(self, value: Bloom | None) -> None:
        if __debug__:
            expect(value, Bloom)
        self._bloom = value

    @property
    def tint(self) -> Tint | None:
        """Effet de teinte"""
        return self._tint
    
    @tint.setter
    def tint(self, value: Tint | None) -> None:
        if __debug__:
            expect(value, Tint)
        self._tint = value

    @property
    def vignette(self) -> Vignette | None:
        """Effet de réducation de vision"""
        return self._vignette
    
    @vignette.setter
    def vignette(self, value: Vignette | None) -> None:
        if __debug__:
            expect(value, Vignette)
        self._vignette = value

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
        pass

    def _update(self, dt: float) -> None:
        """Actualisation"""
        for source in self._sources:
            state: Activity = source.update(dt)
            if state is Activity.DEFAULT:
                continue
            if state is Activity.ENABLED:
                self._get_active_list(source).append(source)
            elif state is Activity.DISABLED:
                self._get_active_list(source).remove(source)

    def _draw(self, pipeline: Pipeline) -> None:
        """Affichage"""
        self._renderer.render_ambient(pipeline, self._ambient or self._DEFAULT_AMBIENT, self._active_points, self._active_cones, gamma=self._gamma, exposure=self._exposure)
        if self._bloom:
            self._renderer.render_bloom(pipeline, self._bloom)
        if self._tint:
            self._renderer.render_tint(pipeline, self._tint)
        if self._vignette:
            self._renderer.render_vignette(pipeline, self._vignette)

    # ======================================== INTERNALS ========================================
    def _get_active_list(self, source: LightSource) -> list:
        """Renvoie la liste active correspondant au type de source"
        
        Args:
            source: source à vérifier
        """
        match source:
            case PointLight(): return self._active_points
            case ConeLight():  return self._active_cones

    def _effect_id(self, effect_type: Type[LightEffect]) -> str:
        """Vérifie le support d'un type d'effet

        Args:
            effect_type: type de l'effet
        """
        if __debug__:
            if not effect_type in _SUPPORTED_EFFECT: raise RuntimeError(f"This Layer does not support {effect_type.__name__} effect")
        return f"_{effect_type.id()}"