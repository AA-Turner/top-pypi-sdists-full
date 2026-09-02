# Back-compat shim — FEAT-023 relocated tPandas to flowtask/interfaces/.
# Old path: flowtask.components.tPandas
# New path: flowtask.interfaces.t_pandas
from flowtask.interfaces.t_pandas import tPandas  # noqa: F401
