"""Front door of `events.py` and `surfaces.py`, which `python -m probe_contracts.codegen` GENERATES:
never edit them."""

from .events import Event
from .surfaces import ProductSurface

__all__ = ["Event", "ProductSurface"]
