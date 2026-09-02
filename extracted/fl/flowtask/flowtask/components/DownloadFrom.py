# Back-compat shim — FEAT-023 relocated DownloadFromBase to flowtask/interfaces/.
# Old path: flowtask.components.DownloadFrom
# New path: flowtask.interfaces.download_from
from flowtask.interfaces.download_from import DownloadFromBase  # noqa: F401
