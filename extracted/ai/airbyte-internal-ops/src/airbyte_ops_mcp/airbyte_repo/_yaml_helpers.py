# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Shared ruamel.yaml helpers for YAML file round-tripping.

Any code that needs to read and write Airbyte YAML files (e.g.
`metadata.yaml`) should use the helpers in this module so formatting
settings are defined in exactly one place.
"""

from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML


def new_ruamel_processor() -> YAML:
    """Return a pre-configured ruamel.yaml processor.

    The returned instance preserves quoting, uses a wide line-width to
    avoid unwanted wrapping, and indents consistently with the project's
    existing YAML style::

        mapping:  2 spaces
        sequence: 4 spaces (2 offset)
    """
    ryaml = YAML()
    ryaml.preserve_quotes = True
    ryaml.width = 4096
    ryaml.indent(mapping=2, sequence=4, offset=2)
    return ryaml


def load_metadata_yaml(metadata_file: Path) -> dict:
    """Load a `metadata.yaml` file and return the parsed dict.

    Args:
        metadata_file: Path to the `metadata.yaml` file.

    Returns:
        The parsed metadata dict.
    """
    ryaml = new_ruamel_processor()
    with open(metadata_file) as f:
        return ryaml.load(f)


def write_metadata_yaml(metadata: dict, metadata_file: Path) -> None:
    """Write a metadata dict back to disk.

    Args:
        metadata: The (possibly mutated) metadata dict.
        metadata_file: Path to the `metadata.yaml` file.
    """
    ryaml = new_ruamel_processor()
    with open(metadata_file, "w") as f:
        ryaml.dump(metadata, f)
