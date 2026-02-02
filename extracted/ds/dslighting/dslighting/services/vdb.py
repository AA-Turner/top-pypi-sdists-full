"""
DSLighting Vector Database Service

Re-export dsat.services.vdb.VDBService.
"""
try:
    from dsat.services.vdb import VDBService
except ImportError:
    VDBService = None

__all__ = ["VDBService"]
