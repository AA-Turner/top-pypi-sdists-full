# Back-compat shim — FEAT-023 relocated CopyToFileBase to flowtask/interfaces/.
# Old path: flowtask.components.CopyToFileBase
# New path: flowtask.interfaces.copy_to_file_base
from flowtask.interfaces.copy_to_file_base import CopyToFileBase  # noqa: F401
