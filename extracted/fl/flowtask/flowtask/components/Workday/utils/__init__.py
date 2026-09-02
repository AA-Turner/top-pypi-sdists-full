"""Backward-compatibility shim — re-exports from new interface home (TASK-102)."""
from flowtask.interfaces.workday.utils import safe_serialize, extract_by_type, first, ensure_list

__all__ = ["safe_serialize", "extract_by_type", "first", "ensure_list"]
