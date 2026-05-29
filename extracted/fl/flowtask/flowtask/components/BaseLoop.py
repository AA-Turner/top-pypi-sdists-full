# Back-compat shim — FEAT-023 relocated BaseLoop to flowtask/interfaces/.
# Old path: flowtask.components.BaseLoop
# New path: flowtask.interfaces.base_loop
from flowtask.interfaces.base_loop import BaseLoop  # noqa: F401
