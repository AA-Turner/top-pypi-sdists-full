# ======================================== IMPORTS ========================================
from __future__ import annotations

from ...._internal import expect
from ....abc import System
from ...._core import Geometry

from ..._world import World

from ._spatial_hash import SpatialHash
from ._resolve import CachedContact
from ._update import UpdateContext, update_processor
from ._constants import ConstantsDataset

from numbers import Real, Integral

# ======================================== SYSTEM ========================================
class CollisionSystem(System):
    """Système de détection et résolution des collisions

    Args:
        broadphase: utilisation du spatial hash
        slop: pénétration tolérée avant correction
        max_position_correction: correction de position maximale par frame
        iterations: nombre d'itérations de la convergence
        extra_iterations_threshold: profondeur de pénétration à partir de laquelle des itérations supplémentaires sont ajoutées
        extra_iterations: nombre d'itérations supplémentaires
        restitution_theshold: seuil minimale de restitution
        restitution_max_velocity: vélocité maximale de la restitution
        vel_along_wake_treshold: vitesse de rapprochement minimale pour réveiller les entités
    """
    __slots__ = (
        "_slop", "_max_position_correction",
        "_iterations", "_extra_iterations_threshold", "_extra_iterations",
        "_restitution_threshold", "_restitution_max_velocity",
        "_vel_along_wake_treshold",
        "_hash",
        "_cache", "_geometry_cache", "_geometry_keys",
        "_C",
    )
    order = 70
    exclusive = True
    requires = ("PhysicsSystem",)

    def __init__(
            self,
            broadphase: bool = True,
            slop: Real = 0.5,
            max_position_correction: Real = 8.0,
            iterations: Integral = 6,
            extra_iterations_threshold: Real = 4.0,
            extra_iterations: Integral = 4,
            restitution_threshold: Real = 1.0,
            restitution_max_velocity: Real = 10.0,
            vel_along_wake_treshold: Real = 0.1,
        ):
        # Transtypage
        slop = float(slop)
        max_position_correction = float(max_position_correction)
        iterations = int(iterations)
        extra_iterations_threshold = float(extra_iterations_threshold)
        extra_iterations = int(extra_iterations)
        restitution_threshold = float(restitution_threshold)
        restitution_max_velocity = float(restitution_max_velocity)
        vel_along_wake_treshold = float(vel_along_wake_treshold)

        if __debug__:
            expect(broadphase, bool)

        # Attributs publiques
        self._slop: float = slop
        self._max_position_correction: float = max_position_correction
        self._iterations: int = max(1, iterations)
        self._extra_iterations_threshold: float = extra_iterations_threshold
        self._extra_iterations: int = max(0, extra_iterations)
        self._restitution_threshold: float = restitution_threshold
        self._restitution_max_velocity: float = restitution_max_velocity
        self._vel_along_wake_treshold: float = vel_along_wake_treshold

        # Attributs internes
        self._hash: SpatialHash | None = SpatialHash() if broadphase else None
        self._cache: dict[tuple[int, int], CachedContact] = {}
        self._geometry_cache: dict[int, Geometry] = {}
        self._geometry_keys: dict[int, tuple] = {}
        self._C: ConstantsDataset = ConstantsDataset(
            self._slop, self._max_position_correction,
            self._iterations, self._extra_iterations_threshold, self._extra_iterations,
            self._restitution_threshold, self._restitution_max_velocity,
            self._vel_along_wake_treshold,
        )
    
    # ======================================== CONTRACT ========================================
    def __repr__(self) -> str:
        """Renvoie une représentation du système"""
        return f"CollisionSystem(broadphase={self._hash is not None}, slop={self._slop}, iterations={self._iterations})"
    
    # ======================================== PROPERTIES ========================================
    @property
    def slop(self) -> float:
        """Profondeur de pénétration tolérée"""
        return self._slop
    
    @property
    def max_position_correction(self) -> float:
        """Correcttion maximale instantannée"""
        return self._max_position_correction
    
    @property
    def iterations(self) -> int:
        """Nombre d'itérations par frame"""
        return self._iterations
    
    @property
    def extra_iterations_treshold(self) -> float:
        """Seuil de profondeur de pénétration pour activer les itérations supplémentaires"""
        return self._extra_iterations_threshold
    
    @property
    def extra_iterations(self) -> int:
        """Nombre d'itérations supplémentaires"""
        return self._extra_iterations
    
    @property
    def restitution_treshold(self) -> float:
        """Restitution minimale considérée"""
        return self._restitution_threshold
    
    @property
    def restitution_max_velocity(self) -> float:
        """Velocité maximale engendrée par la restitution"""
        return self.restitution_max_velocity
    
    @property
    def vel_along_wake_treshold(self) -> float:
        """Seuil de vélocité arrivante pour réveiller l'entité"""
        return self._vel_along_wake_treshold

    # ======================================== LIFE CYCLE ========================================
    def update(self, world: World, dt: float):
        """
        Détecte et résout les collisions pour toutes les entités actives

        Args:
            world(World): monde courant
            dt(float): delta temps
        """
        ctx = UpdateContext.build(world, dt, self._hash, self._cache, self._geometry_cache, self._geometry_keys, self._C)
        update_processor(ctx)

    # ======================================== INTERFACE ========================================
    def reset_calibration(self) -> None:
        """Réinitialise la calibration du spatial hash"""
        if self._hash is not None:
            self._hash._cell_size = None
            self._hash.clear_static()

    def clear_cache(self) -> None:
        """Vide le cache d'impulsions"""
        self._cache.clear()

    def clear_geometry(self) -> None:
        """Nettoie le cache géométrique"""
        self._geometry_cache.clear()
        self._geometry_keys.clear()