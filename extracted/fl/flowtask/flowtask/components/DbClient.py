# Back-compat shim — FEAT-023 relocated DbClient to flowtask/interfaces/.
# Old path: flowtask.components.DbClient
# New path: flowtask.interfaces.db_client
from flowtask.interfaces.db_client import DbClient  # noqa: F401
