# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...asset import Color

import numpy as np

from numbers import Real
from typing import Tuple

# ======================================== EMITTER ========================================
class ParticleEmitter:
    __slots__ = (
        "x", "y",
        "_rate",
        "_lifetime_min", "_lifetime_max",
        "_speed_min", "_speed_max",
        "_angle_min", "_angle_max",
        "_size_min", "_size_max", "_size_end",
        "_angular_vel_min", "_angular_vel_max",
        "_color_start", "_color_end",
        "_active", "_accumulator",
        "_max",
        "_positions", "_velocities",
        "_rotations", "_angular_velocities",
        "_lifetimes", "_max_lifetimes",
        "_sizes", "_sizes_end",
        "_colors_start", "_colors_end",
    )

    def __init__(
        self,
        x: Real = 0.0,
        y: Real = 0.0,
        *,
        max_particles: int = 500,
        rate: Real = 50.0,
        lifetime: Tuple[Real, Real] = (1.0, 2.0),
        speed: Tuple[Real, Real] = (50.0, 150.0),
        angle: Tuple[Real, Real] = (0.0, 360.0),
        size: Tuple[Real, Real] = (5.0, 10.0),
        size_end: Real = 0.0,
        angular_velocity: Tuple[Real, Real] = (-180.0, 180.0),
        color_start: Color = Color(255, 255, 255, 255),
        color_end: Color = Color(255, 255, 255, 0),
    ):
        self.x = float(x)
        self.y = float(y)
        self._rate = float(rate)
        self._lifetime_min, self._lifetime_max = float(lifetime[0]), float(lifetime[1])
        self._speed_min,    self._speed_max    = float(speed[0]),    float(speed[1])
        self._angle_min,    self._angle_max    = float(angle[0]),    float(angle[1])
        self._size_min,     self._size_max     = float(size[0]),     float(size[1])
        self._size_end                         = float(size_end)
        self._angular_vel_min, self._angular_vel_max = float(angular_velocity[0]), float(angular_velocity[1])
        self._color_start = Color(color_start)
        self._color_end   = Color(color_end)
        self._active      = True
        self._accumulator = 0.0

        n = int(max_particles)
        self._max                = n
        self._positions          = np.zeros((n, 2), dtype=np.float32)
        self._velocities         = np.zeros((n, 2), dtype=np.float32)
        self._rotations          = np.zeros(n,      dtype=np.float32)
        self._angular_velocities = np.zeros(n,      dtype=np.float32)
        self._lifetimes          = np.zeros(n,      dtype=np.float32)
        self._max_lifetimes      = np.ones(n,       dtype=np.float32)
        self._sizes              = np.zeros(n,      dtype=np.float32)
        self._sizes_end          = np.zeros(n,      dtype=np.float32)
        self._colors_start       = np.zeros((n, 4), dtype=np.float32)
        self._colors_end         = np.zeros((n, 4), dtype=np.float32)

    # ======================================== INTERFACE ========================================
    @property
    def rate(self) -> float:
        return self._rate

    @rate.setter
    def rate(self, value: Real) -> None:
        self._rate = float(value)

    def start(self) -> None:
        self._active = True

    def stop(self) -> None:
        self._active = False

    def burst(self, count: int) -> None:
        self._spawn(int(count))

    # ======================================== LIFECYCLE ========================================
    def update(self, dt: float) -> None:
        """Actualisation CPU du pool"""
        if self._active and self._rate > 0.0:
            self._accumulator += self._rate * dt
            count = int(self._accumulator)
            if count > 0:
                self._accumulator -= count
                self._spawn(count)

        alive = self._lifetimes > 0.0
        if not alive.any():
            return
        self._lifetimes[alive]  -= dt
        self._positions[alive]  += self._velocities[alive] * dt
        self._rotations[alive]  += self._angular_velocities[alive] * dt

    def collect(self) -> tuple | None:
        """Renvoie (positions, rotations, sizes, colors) des particules vivantes"""
        alive = self._lifetimes > 0.0
        if not alive.any():
            return None

        t  = np.clip(1.0 - self._lifetimes[alive] / self._max_lifetimes[alive], 0.0, 1.0)
        t4 = t[:, np.newaxis]

        sizes  = (self._sizes[alive]  * (1.0 - t)  + self._sizes_end[alive]  * t ).astype(np.float32)
        colors = (self._colors_start[alive] * (1.0 - t4) + self._colors_end[alive] * t4).astype(np.float32)

        return self._positions[alive], self._rotations[alive], sizes, colors

    # ======================================== INTERNALS ========================================
    def _spawn(self, count: int) -> None:
        dead = np.where(self._lifetimes <= 0.0)[0]
        if not len(dead):
            return
        n   = min(count, len(dead))
        idx = dead[:n]

        lt = np.random.uniform(self._lifetime_min, self._lifetime_max, n).astype(np.float32)
        self._lifetimes[idx]     = lt
        self._max_lifetimes[idx] = lt

        self._positions[idx, 0] = self.x
        self._positions[idx, 1] = self.y

        speeds = np.random.uniform(self._speed_min, self._speed_max, n)
        angles = np.radians(np.random.uniform(self._angle_min, self._angle_max, n))
        self._velocities[idx, 0] = (speeds * np.cos(angles)).astype(np.float32)
        self._velocities[idx, 1] = (speeds * np.sin(angles)).astype(np.float32)

        self._rotations[idx] = np.radians(np.random.uniform(0.0, 360.0, n)).astype(np.float32)
        self._angular_velocities[idx] = np.radians(
            np.random.uniform(self._angular_vel_min, self._angular_vel_max, n)
        ).astype(np.float32)

        self._sizes[idx]     = np.random.uniform(self._size_min, self._size_max, n).astype(np.float32)
        self._sizes_end[idx] = self._size_end

        self._colors_start[idx] = np.array(self._color_start, dtype=np.float32)
        self._colors_end[idx]   = np.array(self._color_end,   dtype=np.float32)