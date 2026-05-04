from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod
from numbers import Real
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...fx import Particle

# ======================================== ABC ========================================
class ParticleEmitter(ABC):
    """Classe abstraite des émetteur de particules

    Args:
        particle: pattern de particule
        max_particles: nombre maximum de particules simultanées
        rate: taux d'émission en particules/seconde
    """
    __slots__ = (
        "x", "y",
        "_particle", "_max", "_rate",
        "_active", "_accumulator",
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
        particle: Particle = None,
        max_particles: int = 500,
        rate: Real = 50.0,
    ):
        self.x: float = float(x)
        self.y: float = float(y)

        from ...fx import Particle
        self._particle: Particle = particle or Particle()
        self._max: int = int(max_particles)
        self._rate: float = float(rate)
        self._active: bool = True
        self._accumulator: float = 0.0

        n = self._max
        self._positions = np.zeros((n, 2), dtype=np.float32)
        self._velocities = np.zeros((n, 2), dtype=np.float32)
        self._rotations = np.zeros(n, dtype=np.float32)
        self._angular_velocities = np.zeros(n, dtype=np.float32)
        self._lifetimes = np.zeros(n, dtype=np.float32)
        self._max_lifetimes = np.ones(n, dtype=np.float32)
        self._sizes = np.zeros(n, dtype=np.float32)
        self._sizes_end = np.zeros(n, dtype=np.float32)
        self._colors_start = np.zeros((n, 4), dtype=np.float32)
        self._colors_end = np.zeros((n, 4), dtype=np.float32)

    # ======================================== PROPERTIES ========================================
    @property
    def particle(self) -> Particle:
        """Configuration des particules"""
        return self._particle

    @particle.setter
    def particle(self, value: Particle) -> None:
        assert isinstance(value, Particle), f"particle must be a Particle, got {value}"
        self._particle = value

    @property
    def rate(self) -> float:
        """Taux d'émission"""
        return self._rate

    @rate.setter
    def rate(self, value: Real) -> None:
        self._rate = float(value)

    # ======================================== INTERFACE ========================================
    def start(self) -> None:
        """Active l'émission continue"""
        self._active = True

    def stop(self) -> None:
        """Désactive l'émission continue"""
        self._active = False

    def burst(self, count: int) -> None:
        """Emet un nombre défini de particules instantanément"""
        self._spawn(int(count))

    def clear(self) -> None:
        """Supprime toutes les particules vivantes"""
        self._lifetimes[:] = 0.0

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

        self._lifetimes[alive] -= dt
        self._positions[alive] += self._velocities[alive] * dt
        self._rotations[alive] += self._angular_velocities[alive] * dt

    def collect(self) -> tuple | None:
        """Renvoie (positions, rotations, sizes, colors) des particules vivantes"""
        alive = self._lifetimes > 0.0
        if not alive.any():
            return None

        t  = np.clip(1.0 - self._lifetimes[alive] / self._max_lifetimes[alive], 0.0, 1.0)
        t4 = t[:, np.newaxis]

        sizes  = (self._sizes[alive] * (1.0 - t) + self._sizes_end[alive] * t ).astype(np.float32)
        colors = (self._colors_start[alive] * (1.0 - t4) + self._colors_end[alive] * t4).astype(np.float32)

        return self._positions[alive], self._rotations[alive], sizes, colors

    # ======================================== INTERNALS ========================================
    def _spawn(self, count: int) -> None:
        dead = np.where(self._lifetimes <= 0.0)[0]
        if not len(dead):
            return

        p = self._particle
        n = min(count, len(dead))
        idx = dead[:n]

        lt = np.random.uniform(p.lifetime[0], p.lifetime[1], n).astype(np.float32)
        self._lifetimes[idx] = lt
        self._max_lifetimes[idx] = lt

        spawn_pos, spawn_vel = self._emit(n)
        self._positions[idx] = spawn_pos
        self._velocities[idx] = spawn_vel

        self._rotations[idx] = np.radians(
            np.random.uniform(0.0, 360.0, n)
        ).astype(np.float32)
        self._angular_velocities[idx] = np.radians(
            np.random.uniform(p.angular_velocity[0], p.angular_velocity[1], n)
        ).astype(np.float32)

        self._sizes[idx] = np.random.uniform(p.size[0], p.size[1], n).astype(np.float32)
        self._sizes_end[idx] = p.size_end

        self._colors_start[idx] = np.array(p.color_start, dtype=np.float32)
        self._colors_end[idx] = np.array(p.color_end, dtype=np.float32)

    @abstractmethod
    def _emit(self, count: int) -> tuple[np.ndarray, np.ndarray]:
        """Renvoie (positions, velocities) pour ``count`` nouvelles particules

        Args:
            count: nombre de particules à spawner
        
        Returns:
            positions: (n, 2) float32
            velocities: (n, 2) float32
        """