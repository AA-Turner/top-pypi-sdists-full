# Back-compat shim — FEAT-023 relocated UploadToBase to flowtask/interfaces/.
# Old path: flowtask.components.UploadTo
# New path: flowtask.interfaces.upload_to
from flowtask.interfaces.upload_to import UploadToBase  # noqa: F401
