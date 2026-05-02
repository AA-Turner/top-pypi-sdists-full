# ======================================== IMPORTS ========================================
from __future__ import annotations
from ._version import __version__

import pyglet
from typing import Callable

# ======================================== PRIMITIVES ========================================
from . import typing, abc, math, shape, asset

# ======================================== STATE ========================================
from ._rendering import (
    Window, LogicalScreen, Viewport, Camera,
    Pipeline,
)

_pipeline: Pipeline | None = None

# ======================================== MANAGERS ========================================
from ._managers import ContextManager, TimeManager, CoordinatesManager, EventManager, KeyManager, MouseManager, InputsManager, UiManager, AudioManager

_context_manager: ContextManager = ContextManager()

# Time
time: TimeManager = TimeManager(_context_manager)
_context_manager.time = time

# Coordinates
coordinates: CoordinatesManager = CoordinatesManager(_context_manager)
_context_manager.coordinates = coordinates

# Event
event: EventManager = EventManager(_context_manager)
_context_manager.event = event

# Key
key: KeyManager = KeyManager(_context_manager)
_context_manager.key = key

# Mouse
mouse: MouseManager = MouseManager(_context_manager)
_context_manager.mouse = mouse

# Inputs
inputs: InputsManager = InputsManager(_context_manager)
_context_manager.inputs = inputs

# Ui
ui: UiManager = UiManager(_context_manager)
_context_manager.ui = ui

# Audio
audio: AudioManager = AudioManager(_context_manager)
_context_manager.audio = audio

# ======================================== NODES ========================================
from . import world, tile, gui, fx, scene

# ======================================== SETTERS ========================================
def set_window(window: Window):
    """Définit la fenêtre du moteur

    Args:
        window: fenêtre à utiliser
    """
    global _pipeline
    if not isinstance(window, Window):
        raise TypeError("Expected a Window instance")
    _pipeline = Pipeline(window)

    for manager in _context_manager:
        manager.bind(window)

    @_pipeline.window.native.event
    def on_draw():
        """Draw call"""
        _pipeline.window.clear()
        scene.draw(_pipeline)

# ======================================== COLLECTIONS ========================================
def preload(loadable: scene.Scene = None) -> None:
    """Précharge le rendu

    Args:
        loadable: scène spécifique à précharger
    """
    if _pipeline is None:
        raise RuntimeError("Not window set. Please try set_window() before loading") 
    if loadable is None:
        scene._preload(_pipeline)
    else:
        loadable._preload(_pipeline)

def run(on_update: Callable[[float], None] = None, on_draw: Callable[[], None] = None):
    """Démarre le moteur

    Args:
        on_update: hook d'actualisation
        on_draw: hook d'affichage
    """
    if _pipeline is None:
        raise RuntimeError("No window set, try set_window() before run()")

    def _update(raw_dt: float):
        """Boucle interne"""
        # Calcul du delta-time
        dt = time.tick(raw_dt)

        # Actualisation des gestionnaires
        for manager in _context_manager:
            manager.update(dt)

        # Actualisation des scenes
        scene.update(dt)

        # Appel de la fonction externe
        if on_update is not None:
            on_update(dt)

        # Nettoyage
        for manager in _context_manager:
            manager.flush()

    # Draw hook
    if on_draw is not None:
        _pipeline.window.native.push_handlers(on_draw=on_draw)

    # Lancement
    time.schedule(_update)
    pyglet.app.run(time.target_dt if time.target_dt is not None else 1 / 9999)

def stop():
    """Arrête proprement le moteur"""
    global _pipeline
    if _pipeline is None:
        return

    window = _pipeline.window.native

    # Désenregistre les handlers
    window.pop_handlers()

    # Ferme la fenêtre
    window.close()

    # Stop la loop pyglet
    pyglet.app.exit()

    # Reset pipeline
    _pipeline = None

# ======================================== EXPORTS ========================================
__all__ = [
    "Window",
    "LogicalScreen",
    "Viewport",
    "Camera",

    "CoordSpace",
    "world_to_frustum",
    "frustum_to_ndc",
    "ndc_to_nvc",
    "nvc_to_viewport",
    "viewport_to_framebuffer",
    "framebuffer_to_canvas",
    "canvas_to_window",
    "window_to_canvas",
    "canvas_to_framebuffer",
    "framebuffer_to_viewport",
    "viewport_to_nvc",
    "nvc_to_ndc",
    "ndc_to_frustum",
    "frustum_to_world",
    "CoordContext",

    "TimeManager",
    "EventManager",
    "KeyManager",
    "MouseManager",
    "InputsManager",
    "UiManager",

    "time",
    "coordinates",
    "event",
    "key",
    "mouse",
    "inputs",
    "ui",
    "audio",

    "typing",
    "abc",
    "math",
    "shape",
    "asset",
    "world",
    "tile",
    "gui",
    "fx",
    "scene",

    "set_window",
    "preload",
    "run",
    "stop",
]