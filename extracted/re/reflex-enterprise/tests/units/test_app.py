"""Unit tests for app."""

import pytest

from reflex_enterprise.app import AppEnterprise
from reflex_enterprise.config import ConfigEnterprise
from reflex_enterprise.proxy import proxy_middleware


def test_app(app: AppEnterprise):
    """Test app."""
    assert proxy_middleware not in app.lifespan_tasks


@pytest.mark.parametrize(
    "user_tier, allowed",
    [
        ("free", False),
        ("pro", False),
        ("team", True),
        ("enterprise", True),
    ],
)
def test_init_app_with_proxy(mocker, user_tier: str, allowed: bool):
    """Test app with proxy."""
    mocker.patch(
        "reflex_base.config._get_config",
        return_value=ConfigEnterprise(
            app_name="app_with_proxy_enabled",
            use_single_port=allowed,
        ),
    )
    mocker.patch(
        "reflex_enterprise.utils.get_user_tier",
        return_value=user_tier,
    )
    app_proxy = AppEnterprise()

    if allowed:
        assert proxy_middleware in app_proxy.lifespan_tasks
    else:
        assert proxy_middleware not in app_proxy.lifespan_tasks
