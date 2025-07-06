"""
Utilities package for Matrice Deploy.

This package contains utility modules for the Matrice deployment system.
"""

# Import post_processing module components for easy access
from . import post_processing

# Re-export commonly used items from post_processing for convenience
from .post_processing import (
    PostProcessor,
    create_config_from_template,
    create_people_counting_config,
    process_simple,
    list_available_usecases,
    validate_config
)

__all__ = [
    'post_processing',
    'PostProcessor',
    'create_config_from_template',
    'create_people_counting_config',
    'process_simple',
    'list_available_usecases',
    'validate_config'
] 