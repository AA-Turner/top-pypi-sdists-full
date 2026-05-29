# Back-compat shim — FEAT-023 relocated flow interfaces to flowtask/interfaces/.
# Old path: flowtask.components.flow
# New path: flowtask.interfaces.flow / flowtask.interfaces.abstract
from flowtask.interfaces.abstract import AbstractFlow  # noqa: F401
from flowtask.interfaces.flow import FlowComponent  # noqa: F401
