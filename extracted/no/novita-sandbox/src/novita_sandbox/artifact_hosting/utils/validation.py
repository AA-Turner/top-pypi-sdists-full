"""Validation utilities for Artifact Hosting SDK."""

import re
from typing import Dict


# Environment variable key name pattern: must start with letter or underscore,
# followed by letters, numbers, or underscores
ENV_VAR_KEY_PATTERN = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def validate_environment_variables(env_vars: Dict[str, str]) -> None:
    """Validate environment variable keys.
    
    Validates that all environment variable keys:
    - Are non-empty
    - Match the pattern: ^[a-zA-Z_][a-zA-Z0-9_]*$
    - Start with a letter or underscore
    - Contain only letters, numbers, and underscores
    
    Does NOT validate values (they can be any string).
    
    Args:
        env_vars: Dictionary of environment variables to validate.
    
    Raises:
        ValueError: If any environment variable key is invalid.
    """
    if not env_vars:
        return
    
    for key, value in env_vars.items():
        if not key:
            raise ValueError("Environment variable key cannot be empty")
        
        if not ENV_VAR_KEY_PATTERN.match(key):
            raise ValueError(
                f"Invalid environment variable key '{key}': "
                "must start with a letter or underscore and contain only "
                "letters, numbers, and underscores"
            )


def validate_project_name(name: str) -> None:
    """Validate project name format.
    
    Project name must:
    - Be 3-63 characters long
    - Start with a lowercase letter
    - Contain only lowercase letters, numbers, and hyphens
    - Match pattern: ^[a-z][a-z0-9-]{2,62}$
    
    Args:
        name: Project name to validate.
    
    Raises:
        ValueError: If project name is invalid.
    """
    if not name:
        raise ValueError("Project name cannot be empty")
    
    if len(name) < 3 or len(name) > 63:
        raise ValueError(
            f"Project name '{name}' must be between 3 and 63 characters long"
        )
    
    if not re.match(r"^[a-z][a-z0-9-]{2,62}$", name):
        raise ValueError(
            f"Invalid project name '{name}': "
            "must start with a lowercase letter and contain only "
            "lowercase letters, numbers, and hyphens"
        )
