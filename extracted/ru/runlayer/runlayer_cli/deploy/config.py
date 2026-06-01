"""
Configuration parser for runlayer.yaml deployment configuration.

Note: This module only reads/parses YAML locally for Docker build parameters.
All validation happens in the backend.
"""

import re
from pathlib import Path
from typing import Any

import yaml


def load_config(config_path: str) -> dict[str, Any]:
    """
    Load deployment configuration from YAML file.

    Note: This does NO validation - just parses the YAML.
    Backend handles all validation.

    Args:
        config_path: Path to runlayer.yaml file

    Returns:
        Dictionary with parsed YAML data

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If YAML is invalid or empty
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        if not data:
            raise ValueError("Configuration file is empty")

        return data
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax: {e}")
    except Exception as e:
        raise ValueError(f"Failed to parse configuration: {e}")


def load_config_raw(config_path: str) -> str:
    """
    Load raw YAML file content as string.

    Args:
        config_path: Path to runlayer.yaml file

    Returns:
        Raw YAML content as string

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    return path.read_text()


def update_config_id(config_path: str, deployment_id: str) -> None:
    """
    Update the deployment ID in the configuration file.

    Uses string replacement to preserve formatting and comments.

    Args:
        config_path: Path to runlayer.yaml file
        deployment_id: UUID of the created deployment
    """
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    content = path.read_text()

    # Replace or add the id field
    # Pattern matches: "id: <value>" or "id: null" or "id:" at start of line
    id_pattern = re.compile(r"^id:\s*.*$", re.MULTILINE)

    if id_pattern.search(content):
        # Replace existing id
        new_content = id_pattern.sub(f"id: {deployment_id}", content)
    else:
        # Add id after the comment header (if present) or at the top
        lines = content.split("\n")
        insert_pos = 0

        # Find position after comment block
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith("#"):
                insert_pos = i
                break

        lines.insert(insert_pos, f"id: {deployment_id}")
        new_content = "\n".join(lines)

    path.write_text(new_content)
