# Back-compat shim — FEAT-023 relocated AbstractFlow to flowtask/interfaces/.
# Old path: flowtask.components.abstract
# New path: flowtask.interfaces.abstract
from flowtask.interfaces.abstract import AbstractFlow  # noqa: F401
