from abc import ABC, abstractmethod
import numpy as np

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False

class Preconditioner(ABC):
    
    def __init__(self, SMatrix):
        self.SMatrix = SMatrix

    def get_array_module(self):
        """
        Returns the appropriate array module (numpy or cupy) based on the SMatrix device.
        """
        if CUPY_AVAILABLE and isinstance(getattr(self.SMatrix, 'device', None), str) and "gpu" in self.SMatrix.device:
            return cp
        else:
            return np
    
    @abstractmethod
    def get_name(self):
        """Return the name of the preconditioner."""
        pass

    @abstractmethod
    def build(self):
        """Build internal data."""
        pass

    @abstractmethod
    def apply_inverse(self, x):
        """
        Compute M^{-1}x.
        """
        pass