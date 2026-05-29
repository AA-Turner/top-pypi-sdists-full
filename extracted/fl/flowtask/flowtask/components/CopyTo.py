# Back-compat shim — FEAT-023 relocated CopyTo to flowtask/interfaces/.
# Old path: flowtask.components.CopyTo
# New path: flowtask.interfaces.copy_to
from flowtask.interfaces.copy_to import CopyTo  # noqa: F401
