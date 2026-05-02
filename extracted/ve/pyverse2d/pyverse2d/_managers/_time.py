# ======================================== IMPORTS ========================================
from __future__ import annotations

from .._internal import expect, over, positive, clamped
from ..abc import Manager, Request

from ._context import ContextManager

import pyglet
from collections import deque
from typing import Callable, Any
from numbers import Real
from dataclasses import dataclass

# ======================================== CONSTANTS ========================================
_FPS_MIN = 15
_DT_MAX = 1 / _FPS_MIN

# ======================================== REQUEST ========================================
@dataclass(slots=True)
class _TimerRequest(Request):
    """Requête d'appel de fonction avec timer"""
    callback: Callable
    elapsed: float
    interval: float
    remaining: int | None

# ======================================== GESTIONNAIRE ========================================
class TimeManager(Manager):
    """Gestionnaire du temps"""
    __slots__ = (
        "_clock",
        "_raw_dt", "_dt", "_eff_dt",
        "_target_fps", "_fps", "_fps_buffer",
        "_time_scale",
        "_scheduling", "_timers",
    )

    _ID: str = "time"

    def __init__(self, context_manager: ContextManager):
        # Initialisation du gestionnaire
        super().__init__(context_manager)

        # Horloge
        self._clock: float = 0.0

        # Delta time
        self._raw_dt: float = 0.0
        self._dt: float = 0.0
        self._eff_dt: float = 0.0

        # Frame-rate
        self._fps: float = 0.0
        self._fps_buffer: deque[float] = deque(maxlen=50)
        self._target_fps: int = 60

        # Effects
        self._time_scale: float = 1.0

        # Handlers
        self._scheduling: list[Callable[[float], None]] = []
        self._timers: list[_TimerRequest] = []

    # ======================================== PROPERTIES ========================================
    @property
    def timer(self) -> float:
        """Temps écoulé depuis le début de l'éxécution"""
        return self._clock

    @property
    def raw_dt(self) -> float:
        """Delta-time brute"""
        return self._raw_dt
    
    @property
    def dt(self) -> float:
        """Delta-time affiné"""
        return self._dt
    
    @property
    def eff_dt(self) -> float:
        """Delta-time utilisé"""
        return self._eff_dt
    
    @property
    def target_dt(self) -> float:
        """Delta-time cible

        Le delta-time doit être un ``float`` compris dans l'invervalle ]0, 0.66].
        Mettre à ``None`` pour ne pas limiter le delta-time.
        """
        return (1 / self._target_fps) if self._target_fps is not None else 0.0
    
    @target_dt.setter
    def target_dt(self, value: float | None) -> None:
        self._target_fps = int(1 / clamped(expect(value, float), min=0, max=_DT_MAX, include_min=False, include_max=True)) if value is not None else None
        self._update_framerate()
    
    @property
    def fps(self) -> float:
        """Frame-rate"""
        return self._fps
    
    @property
    def smooth_fps(self) -> float:
        """Frame-rate lissé"""
        return  sum(self._fps_buffer) / len(self._fps_buffer) if self._fps_buffer else 0.0
    
    @property
    def target_fps(self) -> float | None:
        """Frame-rate cible

        Le frame-rate doit être un ``int`` positif non nul supérieur ou égale à 15.
        Mettre à ``None`` pour ne pas limiter les fps.
        """
        return self._target_fps
    
    @target_fps.setter
    def target_fps(self, value: int | None) -> None:
        self._target_fps = over(expect(value, int), _FPS_MIN, arg="target_fps") if value is not None else None
        self._update_framerate()

    @property
    def time_scale(self) -> float:
        """Facteur d'écoulement du temps

        Le facteur doit être un ``Réel`` positif.
        """
        return self._time_scale
    
    @time_scale.setter
    def time_scale(self, value: Real) -> None:
        self._time_scale = positive(float(expect(value, Real)))

    # ======================================== COLLECTIONS ========================================
    def schedule(self, func: Callable) -> None:
        """Lance une boucle sur une fonction
        
        Args:
            func: fonction à lancer
        """
        self._scheduling.append(func)
        if self._target_fps is None:
            pyglet.clock.schedule(func)
        else:
            pyglet.clock.schedule_interval(func, self.target_dt)
    
    def scale(self, value: Real) -> Real:
        """Convertit une valeur en unité/s

        Args:
            value: valeur à convertir
        """
        return value * self._eff_dt
    
    def elapsed(self, origin: float) -> float:
        """Renvoie le temps écoulé depuis un point du temps antérieur

        Args:
            origin: point du temps de départ
        """
        return self._clock - origin
    
    def after(self, interval: float, callback: Callable[[], Any]) -> None:
        """Appel une fonction en différé

        Args:
            interval: délai avant appel *(en secondes)*
            callback: fonction à appeler
        """
        self._timers.append(_TimerRequest(callback=callback, elapsed=0, interval=interval, remaining=1))

    def every(self, interval: float, callback: Callable[[], Any], limit: int = None) -> None:
        """Appel une fonction à un intervalle donné

        Args:
            interval: délai entre chaque appel *(en secondes)*
            callback: fonction à appeler
            limit: limite de répétitions
        """
        self._timers.append(_TimerRequest(callback=callback, elapsed=0, interval=interval, remaining=limit))

    # ======================================== LIFE CYCLE ========================================
    def tick(self, raw_dt: float) -> float:
        """Calcul le delta-time affiné
        
        Args:
            raw_dt: delta-time brut
        """
        self._clock += raw_dt
        self._raw_dt = raw_dt
        self._dt = min(_DT_MAX, raw_dt)
        self._fps = 1 / max(self._dt, 10e-8)
        self._fps_buffer.append(self._fps)
        self._eff_dt = self._dt * self._time_scale
        return self._eff_dt
    
    def update(self, dt: float) -> None:
        """Actualisation
        
        Args:
            dt: delta-time
        """
        for timer in list(self._timers):
            timer.elapsed += dt
            if timer.elapsed >= timer.interval:
                timer.elapsed = 0
                timer.callback()
                if timer.remaining is not None:
                    timer.remaining -= 1
                    if timer.remaining == 0:
                        self._timers.remove(timer)

    def flush(self) -> None:
        """Nettoyage"""
        pass

    # ======================================== INTERNALES ========================================
    def _update_framerate(self) -> None:
        """Actualise le taux de rafraichissement"""
        target_dt = self.target_dt
        for func in self._scheduling:
            pyglet.clock.unschedule(func)
            if target_dt == 0.0:
                pyglet.clock.schedule(func)
            else:
                pyglet.clock.schedule_interval(func, self.target_dt)
    
        if pyglet.app.event_loop.is_running:
            pyglet.clock.unschedule(pyglet.app.event_loop._redraw_windows)
            if target_dt == 0.0:
                pyglet.clock.schedule(pyglet.app.event_loop._redraw_windows)
            else:
                pyglet.clock.schedule_interval(pyglet.app.event_loop._redraw_windows, self.target_dt)

# ======================================== EXPORTS ========================================
__all__ = [
    "TimeManager",
]