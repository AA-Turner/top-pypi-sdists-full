# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, clamped
from .._rendering import Pipeline, Camera
from ..gui import RenderContext
from ..abc import Widget, Layer
from ..math import Point

from bisect import insort
from numbers import Real

# ======================================== LAYER ========================================
class GuiLayer(Layer):
    """Layer contenant des composants Gui

    Args:
        opacity: opacité du layer
        camera: caméra locale
    """
    __slots__ = ("_wrappers", "_opacity")

    def __init__(self, opacity: Real = 1.0, camera: Camera = None):
        super().__init__(camera)
        self._wrappers: list[WidgetWrapper] = []
        self._opacity: float = clamped(float(expect(opacity, Real)))
    
    # ======================================== PROPERTIES ========================================
    @property
    def widgets(self) -> tuple[Widget]:
        """Ensemble des composants"""
        return tuple(wrapper.widget for wrapper in self._wrappers)
            
    @property
    def opacity(self) -> float:
        """Opacité du layer"""
        return self._opacity
    
    @opacity.setter
    def opacity(self, value: Real):
        self._opacity = clamped(float(expect(value, Real)))

    # ======================================== COLLECTIONS ========================================
    def add(self, widget: Widget, name: str = None, z: int = 0) -> None:
        """Ajoute un composant

        Args:
            widget(Widget): composant à ajouter
        """
        if widget.parent is not None:
            raise ValueError("Cannot add a child widget directly, try to add its parent")
        if widget._layer is not None:
            raise ValueError(f"This widget {widget} is already in a scene")
        widget._switch_layer(self)
        wrapper = WidgetWrapper(widget, name, z)
        insort(self._wrappers, wrapper)
    
    def remove(self, widget: Widget) -> None:
        """Retire un composant

        Args:
            widget(Widget): composant à ajouter
        """
        if widget in self._wrappers:
            widget._switch_layer(None)
            self._wrappers.remove(widget)

    def remove_by_name(self, name: str) -> None:
        """Retire un composant par son identifiant

        Args:
            name(str): nom du composant à dissocier
        """
        to_remove = []
        for wrapper in self._wrappers:
            if wrapper.name == name:
                to_remove.append(wrapper.widget)
        for widget in to_remove:
            widget._switch_layer(None)
            self._wrappers.remove(widget)

    def reorder(self, widget: Widget, z: int) -> None:
        """Modifie le Zorder d'un composant

        Args:
            widget(Widget): composant
            z(int): ordre de rendu
        """
        wrapper = self._get_wrapper(expect(widget, Widget))
        if wrapper.z != z:
            wrapper.z = z
            self._wrappers.remove(widget)
            insort(self._wrappers, wrapper)
    
    def __getitem__(self, key: str) -> Widget:
        """Renvoie un composant par son nom"""
        for wrapper in self._wrappers:
            if wrapper.name == key:
                return wrapper.widget

    def __len__(self) -> int:
        """Renvoie le nombre de composants"""
        return len(self._wrappers)

    # ======================================== HOOKS ========================================
    def on_start(self) -> None:
        """Activation du layer"""
        ...

    def on_stop(self) -> None:
        """Désactivation du layer"""
        ...

    # ======================================== LIFE CYCLE ========================================
    def _preload(self) -> None:
        """Préchargement"""
        pass

    def _update(self, dt: float) -> None:
        """Actualisation du layer"""
        for wrapper in reversed(self._wrappers):
            wrapper.widget.update(dt)

    def _draw(self, pipeline: Pipeline) -> None:
        """Affichage du layer"""
        context = self._generate_context(pipeline)
        for wrapper in self._wrappers:
            wrapper.widget.draw(pipeline, context)

    # ======================================== INTERNALS ========================================
    def _get_wrapper(self, widget: Widget) -> WidgetWrapper:
        """Récupère le wrapper d'un composant"""
        for wrapper in self._wrappers:
            if wrapper.widget == widget:
                return wrapper
        raise ValueError(f"This layer has not widget {widget}")
    
    def _generate_context(self, pipeline: Pipeline) -> RenderContext:
        """Génère un contexte de rendu"""
        return RenderContext(
            pipeline=pipeline,
            x = 0.0,
            y = 0.0,
            scale = 1.0,
            rotation = 0.0,
            opacity = self._opacity,
            z = 0,
            group = None,
        )

# ======================================== WRAPPER ========================================
class WidgetWrapper:
    """Wrapper des composants Gui"""
    __slots__ = ("_widget", "name", "z")

    def __init__(self, widget: Widget, name: str, z: int):
        self._widget: Widget = widget
        self.name: str = name
        self.z: int = z
    
    @property
    def widget(self) -> Widget:
        return self._widget

    def __eq__(self, other: Widget | WidgetWrapper) -> bool:
        """Vérifie la correspondance des composants"""
        if isinstance(other, Widget):
            return self._widget == other
        elif isinstance(other, WidgetWrapper):
            return self._widget == other._widget
        return NotImplemented

    def __lt__(self, other: WidgetWrapper) -> bool:
        """Comparaison inférieure"""
        return self.z < other.z