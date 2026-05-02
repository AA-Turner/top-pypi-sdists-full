"""
DataIntegration parsers.

Navigator can support parsing Tasks from JSON-format, YAML-format and more complex TOML format.
"""
from ._yaml import YAMLParser
from .toml import TOMLParser
from .json import JSONParser


__all__ = (
    "TOMLParser",
    "YAMLParser",
    "JSONParser",
)
