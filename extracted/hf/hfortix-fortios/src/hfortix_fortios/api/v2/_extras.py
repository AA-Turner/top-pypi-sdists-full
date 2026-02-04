"""
Extra methods for generated endpoint classes.

This file contains custom methods that are NOT auto-generated and should be
preserved when running the generator. The generator will NEVER modify this file.

These methods are attached to the appropriate endpoint classes at import time.

Usage:
    Methods defined here follow the pattern:
    
    def <endpoint_path>__<method_name>(self, ...):
        '''Method that gets attached to the endpoint class.'''
        ...
    
    EXTRA_METHODS = {
        "<endpoint_path>": {
            "<method_name>": <function>,
        }
    }
"""

from __future__ import annotations


# Registry of extra methods to attach to endpoint classes
# Format: "endpoint.path" -> {"method_name": function}
EXTRA_METHODS: dict[str, dict[str, object]] = {
    # Add custom methods here when needed
    # Example:
    # "monitor.system.config_revision": {
    #     "diff": config_revision__diff,
    # },
}


def apply_extra_methods(endpoint_path: str, cls: type) -> None:
    """
    Apply extra methods from this module to an endpoint class.
    
    This should be called by the endpoint's __init__.py after the class is defined.
    
    Args:
        endpoint_path: Dot-separated path like "monitor.system.config_revision"
        cls: The endpoint class to attach methods to
    """
    if endpoint_path in EXTRA_METHODS:
        for method_name, method_func in EXTRA_METHODS[endpoint_path].items():
            setattr(cls, method_name, method_func)
