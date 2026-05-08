"""Root conftest.py for the feat-012-add-syntax-check-task worktree.

Stubs out compiled Cython extension modules that are not built inside
this worktree so that test imports succeed without a full build step.

For the syntax checker tests, the parsers need to behave like real async
parsers (accepting content= and providing an async parse() method).
"""
import asyncio
import sys
from unittest.mock import MagicMock

import yaml
import orjson

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

from flowtask.exceptions import TaskParseError


# ---------------------------------------------------------------------------
# Real async parser implementations for use in tests
# These mirror the Cython parser behaviour without requiring compilation.
# ---------------------------------------------------------------------------

class _YAMLParser:
    """Minimal async YAML parser stub matching the Cython YAMLParser API."""
    def __init__(self, content=None, filename=None, **kwargs):
        self.content = content
        self.filename = filename

    async def parse(self, content: str):
        try:
            return yaml.safe_load(content)
        except Exception as err:
            raise TaskParseError(
                f"Task parsing Error on {self.filename!s} with Error: {err!s}."
            )


class _JSONParser:
    """Minimal async JSON parser stub matching the Cython JSONParser API."""
    def __init__(self, content=None, filename=None, **kwargs):
        self.content = content
        self.filename = filename

    async def parse(self, content: str):
        try:
            return orjson.loads(content)
        except Exception as err:
            raise TaskParseError(
                f"Task parsing Error on {self.filename!s} with Error: {err!s}."
            )


class _TOMLParser:
    """Minimal async TOML parser stub matching the Cython TOMLParser API."""
    def __init__(self, content=None, filename=None, **kwargs):
        self.content = content
        self.filename = filename

    async def parse(self, content: str):
        try:
            return tomllib.loads(content)
        except Exception as err:
            raise TaskParseError(
                f"Task parsing Error on {self.filename!s} with Error: {err!s}."
            )


# ---------------------------------------------------------------------------
# Stub modules for Cython extensions
# ---------------------------------------------------------------------------

# Build module stubs for Cython extensions
_yaml_stub = MagicMock()
_yaml_stub.YAMLParser = _YAMLParser

_json_stub = MagicMock()
_json_stub.JSONParser = _JSONParser

_toml_stub = MagicMock()
_toml_stub.TOMLParser = _TOMLParser

_base_stub = MagicMock()

# Register stubs
if "flowtask.parsers._yaml" not in sys.modules:
    sys.modules["flowtask.parsers._yaml"] = _yaml_stub
if "flowtask.parsers.json" not in sys.modules:
    sys.modules["flowtask.parsers.json"] = _json_stub
if "flowtask.parsers.toml" not in sys.modules:
    sys.modules["flowtask.parsers.toml"] = _toml_stub
if "flowtask.parsers.base" not in sys.modules:
    sys.modules["flowtask.parsers.base"] = _base_stub

# Type stubs referenced transitively by parsers
if "flowtask.types.typedefs" not in sys.modules:
    sys.modules["flowtask.types.typedefs"] = MagicMock()

# Utils modules that import Cython types
if "flowtask.utils.parserqs" not in sys.modules:
    _pqs = MagicMock()
    _pqs.is_parseable = MagicMock(return_value=None)
    _pqs.parse_arguments = MagicMock(return_value=({}, {}))
    sys.modules["flowtask.utils.parserqs"] = _pqs
else:
    _pqs = sys.modules["flowtask.utils.parserqs"]
    if not hasattr(_pqs, "is_parseable"):
        _pqs.is_parseable = MagicMock(return_value=None)
    if not hasattr(_pqs, "parse_arguments"):
        _pqs.parse_arguments = MagicMock(return_value=({}, {}))
