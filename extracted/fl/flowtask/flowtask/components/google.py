# Back-compat shim — FEAT-023 relocated GoogleBase to flowtask/interfaces/.
# Old path: flowtask.components.google
# New path: flowtask.interfaces.google_base
from flowtask.interfaces.google_base import GoogleBase  # noqa: F401
