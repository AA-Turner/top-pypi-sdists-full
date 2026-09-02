# Back-compat shim — FEAT-023 relocated FileBase to flowtask/interfaces/.
# Old path: flowtask.components.FileBase
# New path: flowtask.interfaces.file_base
from flowtask.interfaces.file_base import FileBase  # noqa: F401
