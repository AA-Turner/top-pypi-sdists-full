from importlib.metadata import PackageNotFoundError, version

from cube_agent.main import cli as main

__all__ = ["main"]

# The installed distribution's version, which hatch-vcs took from the release
# tag at build time. A source tree that was never installed has no metadata;
# "0.0.0" matches pyproject.toml's fallback-version for the same case.
try:
    __version__ = version("edgescaleai-cube-mcp")
except PackageNotFoundError:
    __version__ = "0.0.0"
