# Back-compat shim — FEAT-023 relocated GroupComponent to flowtask/interfaces/.
# Old path: flowtask.components.group
# New path: flowtask.interfaces.group
from flowtask.interfaces.group import GroupComponent  # noqa: F401
