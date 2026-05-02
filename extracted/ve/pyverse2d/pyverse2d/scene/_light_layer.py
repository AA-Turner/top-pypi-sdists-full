# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._rendering import Pipeline, Camera
from .._flag import Activity
from ..asset import Color
from ..abc import Layer, LightSource
from ..fx import LightRenderer, PointLight, ConeLight

from numbers import Real

# ======================================== LAYER ========================================
class LightLayer(Layer):
    """Layer gérant la lumière

    Args:
        ambient: luminosité ambiante *[0, 1]*
        ambient_color: teinte ambiante
        gamma: facteur de luminosité global *[0, 1]*
        exposure: facteur d'intensité des lumières *[0, inf[*
        tint: couleur d'accentuation *(RGB)*
        tint_strength: intensité de la teinte
        vignette: active la vignette
        vignette_strength: intensité de la vignette *[0, 1]*
        vignette_radius: rayon de la zone centrale non affectée *[0, 1]*
        vignette_color: couleur de la vignette *(RGB)*
        camera: caméra locale
    """
    __slots__ = (
        "_ambient", "_ambient_color", "_gamma", "_exposure", "_tint", "_tint_strength",
        "_vignette", "_vignette_strength", "_vignette_radius", "_vignette_color",
        "_sources", "_active_points", "_active_cones",
        "_renderer",
    )

    _IS_FX = True

    def __init__(
            self,
            ambient: Real = 1.0,
            ambient_color: Color = (255, 255, 255),
            gamma: Real = 1.0,
            exposure: Real = 1.0,
            tint: Color = (255, 255, 255),
            tint_strength: Real = 0.0,
            vignette: bool = False,
            vignette_strength: Real = 0.5,
            vignette_radius: Real = 0.6,
            vignette_color: Color = (0, 0, 0),
            camera: Camera = None
        ):
        # Initialisation du layer
        super().__init__(camera)

        # Paramètres publiques
        self._ambient: float = float(ambient)
        self._ambient_color = Color(ambient_color)
        self._gamma: float = float(gamma)
        self._exposure: float = float(exposure)
        self._tint: Color = Color(tint)
        self._tint_strength: float = float(tint_strength)
        self._vignette: bool = bool(vignette)
        self._vignette_strength: float = float(vignette_strength)
        self._vignette_radius: float = float(vignette_radius)
        self._vignette_color: Color = Color(vignette_color)

        if __debug__:
            if not 0.0 <= self._ambient <= 1.0: raise ValueError(f"ambient must be within 0.0 and 1.0, got {self._ambient}")
            if self._gamma < 0.0: raise ValueError(f"gamma must be positive, got {self._gamma}")
            if self._exposure < 0.0: raise ValueError(f"exposure must be positive, got {self._exposure}")
            if not 0.0 <= self._tint_strength <= 1.0: raise ValueError(f"tint_strength must be within 0.0 and 1.0, got {self._tint_strength}")
            if not 0.0 <= self._vignette_strength <= 1.0: raise ValueError(f"vignette_strength must be within 0.0 and 1.0, got {self._vignette_strength}")
            if not 0.0 <= self._vignette_radius <= 1.0: raise ValueError(f"vignette_radius must be within 0.0 and 1.0, got {self._vignette_radius}")

        # Paramètres internes
        self._renderer: LightRenderer = LightRenderer()
        self._sources: set[LightSource] = set()
        self._active_points: list[PointLight] = []
        self._active_cones: list[ConeLight] = []

    # ======================================== PROPERTIES ========================================
    @property
    def ambient(self) -> float:
        """Luminosité ambiante

        La luminosité doit être un ``Réel`` compris dans l'intervalle *[0, 1]*.
        Mettre cette propriété à 1.0 pour une luminosité maximale.
        """
        return self._ambient
    
    @ambient.setter
    def ambient(self, value: Real) -> None:
        value = float(value)
        assert 0 <= value <= 1.0, ValueError(f"ambient must be within 0 and 1, got {value}")
        self._ambient = value

    @property
    def ambient_color(self) -> Color:
        """Teinte ambiante

        La couleur ambiante peut être un objet ``Color`` ou n'importe quel tuple ``(r, g, b)``.
        Mettre cette propriété à (255, 255, 255) pour une couleur ambiante par défaut.
        """
        return self._ambient_color
    
    @ambient_color.setter
    def ambient_color(self, value: Color) -> None:
        self._ambient_color = Color(value)

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
        assert value >= 0.0, f"gamma ({value}) must be positive"
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
        assert value >= 0.0, f"exposure must be positive, got {value}"

    @property
    def tint(self) -> Color:
        """Couleur d'accentuation

        La couleur peut être un objet ``Color`` ou un tuple ``(r, g, b)``.
        Le canal alpha n'est pas pris en considération dans la teinte.
        """
        return self._tint
    
    @tint.setter
    def tint(self, value: Color) -> None:
        self._tint = Color(value)

    @property
    def tint_strength(self) -> float:
        """Itensité de la couleur d'accentuation

        Le facteur force doit être un ``Réel`` compris dans l'intervalle *[0, 1]*.
        Mettre cette propriété à 0.0 pour ne pas appliquer la couleur d'accentuation.
        """
        return self._tint_strength
    
    @tint_strength.setter
    def tint_strength(self, value: Real) -> None:
        value = float(value)
        assert 0 <= value <= 1.0, ValueError(f"tint_strength must be within 0 and 1, got {value}")
        self._tint_strength = value

    @property
    def vignette(self) -> bool:
        """Active ou désactive la vignette"""
        return self._vignette

    @vignette.setter
    def vignette(self, value: bool) -> None:
        self._vignette = bool(value)

    @property
    def vignette_strength(self) -> float:
        """Intensité de la vignette

        Le facteur doit être un ``Réel`` compris dans l'intervalle *[0, 1]*.
        Mettre cette propriété à 0.0 pour ne pas appliquer la vignette.
        """
        return self._vignette_strength

    @vignette_strength.setter
    def vignette_strength(self, value: Real) -> None:
        value = float(value)
        assert 0 <= value <= 1.0, ValueError(f"vignette_strength must be within 0 and 1, got {value}")
        self._vignette_strength = value

    @property
    def vignette_radius(self) -> float:
        """Rayon de la zone centrale non affectée par la vignette

        Le rayon doit être un ``Réel`` compris dans l'intervalle *[0, 1]*.
        """
        return self._vignette_radius

    @vignette_radius.setter
    def vignette_radius(self, value: Real) -> None:
        value = float(value)
        assert 0 <= value <= 1.0, ValueError(f"vignette_radius must be within 0 and 1, got {value}")
        self._vignette_radius = value

    @property
    def vignette_color(self) -> Color:
        """Couleur de la vignette

        La couleur peut être un objet ``Color`` ou un tuple ``(r, g, b)``.
        """
        return self._vignette_color

    @vignette_color.setter
    def vignette_color(self, value: Color) -> None:
        self._vignette_color = Color(value)

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
        self._renderer.render_ambient(pipeline, self._ambient, self._exposure, self._active_points, self._active_cones, ambient_color=self._ambient_color.rgb, gamma=self._gamma)
        self._renderer.render_tint(pipeline, self._tint.rgb, self._tint_strength)
        if self._vignette:
            self._renderer.render_vignette(pipeline, self._vignette_strength, self._vignette_radius, self._vignette_color.rgb)

    # ======================================== INTERNALS ========================================
    def _get_active_list(self, source: LightSource) -> list:
        """Renvoie la liste active correspondant au type de source"""
        match source:
            case PointLight(): return self._active_points
            case ConeLight():  return self._active_cones