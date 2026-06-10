"""Unit tests for app."""

import pytest
from reflex.constants import CompileContext

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


@pytest.mark.parametrize(
    "compile_context, prod_mode, user_tier, allowed",
    [
        # `reflex export` is restricted to paid tiers.
        (CompileContext.EXPORT, False, "anonymous", False),
        (CompileContext.EXPORT, False, "free", False),
        (CompileContext.EXPORT, False, "pro", True),
        (CompileContext.EXPORT, False, "team", True),
        (CompileContext.EXPORT, False, "enterprise", True),
        # `reflex run --env prod` is restricted to paid tiers.
        (CompileContext.RUN, True, "anonymous", False),
        (CompileContext.RUN, True, "free", False),
        (CompileContext.RUN, True, "pro", True),
        (CompileContext.RUN, True, "team", True),
        (CompileContext.RUN, True, "enterprise", True),
        # `reflex run` (dev mode) is free for everyone.
        (CompileContext.RUN, False, "free", True),
        (CompileContext.RUN, False, "anonymous", True),
        # Cloud deploy is handled separately and not restricted here.
        (CompileContext.DEPLOY, True, "free", True),
    ],
)
def test_check_paid_tier_for_command(
    mocker,
    compile_context: CompileContext,
    prod_mode: bool,
    user_tier: str,
    allowed: bool,
):
    """Test that export and run-prod are limited to non-free users."""
    mocker.patch(
        "reflex.utils.exec.get_compile_context",
        return_value=compile_context,
    )
    mocker.patch("reflex.utils.exec.is_prod_mode", return_value=prod_mode)
    mocker.patch("reflex.utils.exec.is_in_app_harness", return_value=False)
    mocker.patch(
        "reflex_enterprise.utils.get_user_tier",
        return_value=user_tier,
    )

    from reflex_enterprise.utils import check_paid_tier_for_command

    if allowed:
        check_paid_tier_for_command()
    else:
        with pytest.raises(SystemExit):
            check_paid_tier_for_command()
