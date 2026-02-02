"""Simple sync interfaces for doing one-off requests."""

from pyreqwest._pyreqwest.simple.sync_request import (
    pyreqwest_delete,
    pyreqwest_get,
    pyreqwest_head,
    pyreqwest_patch,
    pyreqwest_post,
    pyreqwest_put,
    pyreqwest_request,
)

__all__ = [
    "pyreqwest_request",
    "pyreqwest_get",
    "pyreqwest_post",
    "pyreqwest_put",
    "pyreqwest_patch",
    "pyreqwest_delete",
    "pyreqwest_head",
]
