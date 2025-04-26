import importlib.metadata

from .slip10 import SLIP10, InvalidInputError, PrivateDerivationError
from .utils import HARDENED_INDEX, SLIP10DerivationError

__version__ = importlib.metadata.version(__package__ or __name__)

__all__ = [
    "SLIP10",
    "SLIP10DerivationError",
    "PrivateDerivationError",
    "InvalidInputError",
    "HARDENED_INDEX",
]
