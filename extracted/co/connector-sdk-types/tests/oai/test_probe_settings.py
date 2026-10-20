"""Test cases for `ProbeSettings`, the connector-facing probe configuration."""

import pytest
from connector_sdk_types.generated import ProbeCheckName
from connector_sdk_types.oai.modules.probe_module_types import (
    DEFAULT_PROBE_CHECK_ORDER,
    ProbeSettings,
)
from connector_sdk_types.oai.probe import ProbeCheckSpec
from pydantic import ValidationError


def test_default_covers_every_check_with_no_runner():
    """`default()` is the whole point of the module: every check, all done by the SDK."""
    settings = ProbeSettings.default()

    assert [spec.check for spec in settings.checks] == list(DEFAULT_PROBE_CHECK_ORDER)
    assert all(spec.run is None for spec in settings.checks)
    assert all(spec.required for spec in settings.checks)


def test_disabled_and_manual_both_stand_the_module_down():
    """Both keep the module from registering, and they say different things: `manual()` means
    the connector registers its own, `disabled()` means there is no probe here at all."""
    assert ProbeSettings.disabled().register_probe_capability is False
    assert ProbeSettings.manual().register_probe_capability is False


def test_disabled_configures_no_checks():
    """Nothing to run: a disabled probe must not look like a configured one."""
    assert ProbeSettings.disabled().checks == []


def test_no_checks_by_default():
    """Bare `ProbeSettings()` configures nothing, so the module fills every check in."""
    assert ProbeSettings().checks == []


def test_a_duplicated_check_is_rejected():
    """A second entry for the same check would be silently ignored, so refuse it instead."""
    with pytest.raises(ValidationError, match="Duplicate probe check configuration for: accounts"):
        ProbeSettings(
            checks=[
                ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS),
                ProbeCheckSpec(check=ProbeCheckName.ENTITLEMENTS),
                ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS),
            ]
        )


def test_every_duplicated_check_is_named():
    with pytest.raises(ValidationError, match="accounts, entitlements"):
        ProbeSettings(
            checks=[
                ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS),
                ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS),
                ProbeCheckSpec(check=ProbeCheckName.ENTITLEMENTS),
                ProbeCheckSpec(check=ProbeCheckName.ENTITLEMENTS),
            ]
        )


def test_distinct_checks_are_accepted():
    settings = ProbeSettings(
        checks=[ProbeCheckSpec(check=check) for check in DEFAULT_PROBE_CHECK_ORDER]
    )
    assert len(settings.checks) == len(DEFAULT_PROBE_CHECK_ORDER)


@pytest.mark.parametrize("page_size", [0, -1])
def test_page_size_must_read_something(page_size: int):
    with pytest.raises(ValidationError):
        ProbeSettings(page_size=page_size)


def test_per_check_timeout_must_be_positive():
    with pytest.raises(ValidationError):
        ProbeSettings(per_check_timeout_seconds=0)


def _check_config(probe, session):
    raise NotImplementedError


def test_capability_config_is_not_a_default_check():
    """The SDK cannot perform it for a connector, so connectors only get it by asking."""
    assert ProbeCheckName.CAPABILITY_CONFIG not in DEFAULT_PROBE_CHECK_ORDER
    assert ProbeCheckName.CAPABILITY_CONFIG not in {
        spec.check for spec in ProbeSettings.default().checks
    }


def test_a_check_the_sdk_cannot_perform_needs_a_runner():
    """Leaving `run` unset would otherwise only fail on the first probe call."""
    with pytest.raises(ValidationError, match="runner is required for: capability_config"):
        ProbeSettings(checks=[ProbeCheckSpec(check=ProbeCheckName.CAPABILITY_CONFIG)])


def test_a_check_the_sdk_cannot_perform_is_accepted_with_a_runner():
    settings = ProbeSettings(
        checks=[
            ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS),
            ProbeCheckSpec(
                check=ProbeCheckName.CAPABILITY_CONFIG, run=_check_config, required=False
            ),
        ]
    )
    assert [spec.check for spec in settings.checks] == [
        ProbeCheckName.ACCOUNTS,
        ProbeCheckName.CAPABILITY_CONFIG,
    ]


def test_manual_declares_the_checks_of_a_hand_written_probe():
    """Declared for `x-probe-checks` only: the module still stands down."""
    specs = (
        ProbeCheckSpec(check=ProbeCheckName.ACCOUNTS, run=_check_config),
        ProbeCheckSpec(check=ProbeCheckName.CAPABILITY_CONFIG, run=_check_config),
    )
    settings = ProbeSettings.manual(checks=specs)

    assert settings.register_probe_capability is False
    assert [spec.check for spec in settings.checks] == [
        ProbeCheckName.ACCOUNTS,
        ProbeCheckName.CAPABILITY_CONFIG,
    ]


def test_manual_without_checks_declares_nothing():
    assert ProbeSettings.manual().checks == []
