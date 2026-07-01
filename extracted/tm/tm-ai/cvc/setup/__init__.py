"""cvc.setup — Single source of truth for the first-run setup experience.

Public API:
    from cvc.setup import (
        list_provider_specs, list_provider_specs_all,
        get_provider_spec, list_feature_specs, registry_snapshot,
    )

Why this exists:
    Historically the wizard had hardcoded provider lists in cvc/cli.py:setup() and
    cvc/setup_wizard.py:PROVIDERS that drifted from the actual capabilities (NVIDIA NIM,
    Copilot OAuth, etc.). This package provides ONE registry that both CLIs and the
    dashboard read from, so any new provider or feature lights up everywhere.

``list_provider_specs_all`` returns the union of hand-written specs AND the
Hermes-catalog providers wrapped via ``cvc.providers.hermes_catalog`` — so
``cvc setup`` shows z.ai/GLM, Kimi, StepFun, etc. without a separate submenu.
"""

from cvc.setup.registry import (
    ProviderSpec,
    list_provider_specs,
    list_provider_specs_all,
    get_provider_spec,
    registry_snapshot,
    PROVIDER_SPECS_WITH_CATALOG,
)
from cvc.setup.features import (
    FeatureSpec,
    list_feature_specs,
    get_feature_spec,
)

__all__ = [
    "ProviderSpec",
    "FeatureSpec",
    "PROVIDER_SPECS_WITH_CATALOG",
    "list_provider_specs",
    "list_provider_specs_all",
    "get_provider_spec",
    "list_feature_specs",
    "get_feature_spec",
    "registry_snapshot",
]  # type: ignore[list-item]  # noqa: F822
