"""
DSLighting Utils - Dynamic Import

Re-export dsat.utils.dynamic_import.import_workflow_from_string.
"""
try:
    from dsat.utils.dynamic_import import import_workflow_from_string
except ImportError:
    import_workflow_from_string = None

__all__ = ["import_workflow_from_string"]
