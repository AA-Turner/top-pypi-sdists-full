"""Global Plato settings resolved from environment variables.

All settings use the ``PLATO_`` prefix::

    export PLATO_E2E_TEST_DIR=/extra/e2e-tests
    export PLATO_E2E_TEST_FILTER=test_workspace

Access via ``get_settings()``.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class PlatoSettings(BaseSettings):
    """Global Plato settings shared across all subsystems."""

    model_config = {"env_prefix": "PLATO_"}

    e2e_test_dir: str = Field(
        default="",
        description="Path to e2e test directory. When set, world runs e2e tests after reset() instead of step() loop.",
    )

    e2e_test_filter: str = Field(
        default="",
        description="Only run e2e tests whose names contain this substring.",
    )


_settings: PlatoSettings | None = None


def get_settings() -> PlatoSettings:
    """Get the global Plato settings singleton."""
    global _settings
    if _settings is None:
        _settings = PlatoSettings()
    return _settings
