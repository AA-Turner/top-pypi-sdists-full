"""Commands module for Runlayer CLI.

This package intentionally does NOT eagerly re-export submodules. The
`aiwatch` scan-only binary depends on being able to import specific command
modules (`scan`, `auth`, `logs`, `org_api_key`) without loading the heavy
dependencies (fastmcp, docker, mcp) that the full CLI needs. Python runs
this `__init__.py` before loading any submodule, so any top-level import
here is paid by `aiwatch` on startup — which would break the packaged
binary. Import submodules directly at call sites instead.
"""
