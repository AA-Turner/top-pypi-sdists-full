# Back-compat shim — FEAT-023 relocated CopyFromBase to flowtask/interfaces/.
# Old path: flowtask.components.CopyFromBase
# New path: flowtask.interfaces.copy_from_base
from flowtask.interfaces.copy_from_base import CopyFromBase  # noqa: F401
