# Back-compat shim — FEAT-023 relocated QSBase to flowtask/interfaces/.
# Old path: flowtask.components.QSBase
# New path: flowtask.interfaces.qs_base
from flowtask.interfaces.qs_base import QSBase  # noqa: F401
