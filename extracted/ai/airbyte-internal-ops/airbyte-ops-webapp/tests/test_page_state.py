"""Guardrail tests that keep page `SetState` keys in sync with page-state models.

Prefab addresses state by string key, so a typo in `SetState("lookup_eror", ...)`
or a manually added initial-state key that no page model declares fails silently
in the browser. These tests make such drift fail at test time instead: every
literal `SetState` key used by a page must be a field on that page's typed state
model, and the model must reproduce the page's initial-state keys exactly.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from pydantic import BaseModel

from airbyte_ops_webapp.pages.connector_version_manager._state import (
    ConnectorVersionManagerPageState,
)
from airbyte_ops_webapp.pages.customer_billing._state import CustomerBillingPageState
from airbyte_ops_webapp.pages.motherduck_diagnostics._state import (
    MotherDuckDiagnosticsPageState,
)
from airbyte_ops_webapp.state import OAuthConfigState

_WEBAPP_ROOT = Path(__file__).resolve().parent.parent / "airbyte_ops_webapp"
_SETSTATE_LITERAL = re.compile(r"""SetState\(\s*["']([A-Za-z_][A-Za-z0-9_]*)["']""")


def _sample_oauth_config() -> OAuthConfigState:
    return OAuthConfigState(
        enabled=True,
        issuer="https://issuer.example",
        client_id="client",
        redirect_uri="https://app.example/callback",
        authorization_endpoint="https://issuer.example/auth",
        token_endpoint="https://issuer.example/token",
        session_endpoint="/oauth/session",
        token_exchange_endpoint="/oauth/token",
    )


def _literal_setstate_keys(*package_dirs: Path) -> set[str]:
    """Collect every literal `SetState("key", ...)` key under the given dirs."""
    keys: set[str] = set()
    for package_dir in package_dirs:
        for source in package_dir.rglob("*.py"):
            keys.update(_SETSTATE_LITERAL.findall(source.read_text()))
    return keys


_PAGE_STATE_CASES = [
    pytest.param(
        CustomerBillingPageState,
        (_WEBAPP_ROOT / "pages" / "customer_billing",),
        CustomerBillingPageState.from_env(
            oauth_config=_sample_oauth_config()
        ).to_prefab_state(),
        id="customer_billing",
    ),
    pytest.param(
        MotherDuckDiagnosticsPageState,
        (_WEBAPP_ROOT / "pages" / "motherduck_diagnostics",),
        MotherDuckDiagnosticsPageState.from_env(
            oauth_config=_sample_oauth_config()
        ).to_prefab_state(),
        id="motherduck_diagnostics",
    ),
    pytest.param(
        ConnectorVersionManagerPageState,
        (_WEBAPP_ROOT / "pages" / "connector_version_manager",),
        ConnectorVersionManagerPageState.from_env(
            oauth_config=_sample_oauth_config()
        ).to_prefab_state(),
        id="connector_version_manager",
    ),
]


@pytest.mark.parametrize("model_cls, package_dirs, initial_state", _PAGE_STATE_CASES)
def test_setstate_keys_exist_on_page_state_model(
    model_cls: type[BaseModel],
    package_dirs: tuple[Path, ...],
    initial_state: dict[str, object],
) -> None:
    """Every literal `SetState` key a page uses is a field on its state model."""
    model_fields = set(model_cls.model_fields)
    used_keys = _literal_setstate_keys(*package_dirs)
    unknown = used_keys - model_fields
    assert not unknown, (
        f"{model_cls.__name__} is missing fields for SetState keys: {sorted(unknown)}"
    )


@pytest.mark.parametrize("model_cls, package_dirs, initial_state", _PAGE_STATE_CASES)
def test_initial_state_keys_match_page_state_model(
    model_cls: type[BaseModel],
    package_dirs: tuple[Path, ...],
    initial_state: dict[str, object],
) -> None:
    """The built initial state exposes exactly the model's declared fields."""
    assert set(initial_state) == set(model_cls.model_fields)
