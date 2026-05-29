# Back-compat shim — FEAT-023 relocated BaseAction to flowtask/interfaces/.
# Old path: flowtask.components.BaseAction
# New path: flowtask.interfaces.base_action
from flowtask.interfaces.base_action import BaseAction  # noqa: F401
