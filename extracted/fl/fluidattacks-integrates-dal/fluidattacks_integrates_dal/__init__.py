from fa_purity import (
    Unsafe,
)

from ._logger import (
    set_logger,
)

__version__ = "2.2.0"

Unsafe.compute(set_logger(__name__, __version__))
