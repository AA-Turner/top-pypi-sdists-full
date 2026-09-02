# Back-compat shim — FEAT-023 relocated UserComponent to flowtask/interfaces/.
# Old path: flowtask.components.user
# New path: flowtask.interfaces.user
from flowtask.interfaces.user import UserComponent  # noqa: F401
