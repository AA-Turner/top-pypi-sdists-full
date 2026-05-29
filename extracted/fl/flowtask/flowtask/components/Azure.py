# Back-compat shim — FEAT-023 relocated Azure to flowtask/interfaces/.
# Old path: flowtask.components.Azure
# New path: flowtask.interfaces.azure_component
from flowtask.interfaces.azure_component import Azure  # noqa: F401
