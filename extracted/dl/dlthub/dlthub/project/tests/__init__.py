"""A minimal set of fixtures and pytest-dlt adapters to facilitate testing for dlthub projects

Note that you must add pytest-dlt and pytest to your dev dependencies.
"""

from .fixtures import (
    auto_test_access_profile,
    dpt_project_config,
    dpt_project_context,
)

__all__ = [
    "auto_test_access_profile",
    "dpt_project_config",
    "dpt_project_context",
]
