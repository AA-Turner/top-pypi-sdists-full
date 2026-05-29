# Back-compat shim — FEAT-023 relocated TableBase to flowtask/interfaces/.
# Old path: flowtask.components.TableBase
# New path: flowtask.interfaces.table_base
from flowtask.interfaces.table_base import TableBase  # noqa: F401
