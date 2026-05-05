# ======================================== IMPORTS ========================================
from __future__ import annotations

# ======================================== ABSTRACT CLASS ========================================
from __future__ import annotations

import numpy as np
from abc import abstractmethod
from numbers import Real

# ======================================== ABSTRACT CLASS ========================================
class ParticleModifier:
    """Modificateur de particules (ABC)
    
    Appliqué chaque frame sur les particules vivantes d'un émetteur.
    Peut être attaché à un ``ParticleEmitter`` ou un ``ParticleLayer``.
    """
    __slots__ = tuple()

    @abstractmethod
    def apply(self, dt: float, alive: np.ndarray, positions: np.ndarray, velocities: np.ndarray) -> None:
        """Applique le modificateur sur les particules vivantes

        Args:
            dt: delta time en secondes
            alive: masque booléen des particules vivantes
            positions: tableau (n, 2) des positions
            velocities: tableau (n, 2) des vélocités
        """