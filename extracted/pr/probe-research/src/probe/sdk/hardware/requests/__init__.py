"""Request-bound device observations for serving integrations."""

from .groups import GpuRequestGroups
from .requests import GpuRequests

__all__ = ["GpuRequestGroups", "GpuRequests"]
