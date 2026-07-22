from abc import ABC, abstractmethod

class Preconditioner(ABC):
    
    def __init__(self, SMatrix):
        self.SMatrix = SMatrix
    
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