"""
DSLighting Common - Constants

Re-export dsat.common.constants.
"""
try:
    from dsat.common.constants import *
except ImportError:
    # If DSAT is unavailable, define defaults locally.
    DEFAULT_MAX_STEPS = 100
    DEFAULT_TIMEOUT = 300

__all__ = ["DEFAULT_MAX_STEPS", "DEFAULT_TIMEOUT"]
