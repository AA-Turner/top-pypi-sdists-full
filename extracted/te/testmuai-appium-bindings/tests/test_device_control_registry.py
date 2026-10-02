"""Registry contract for DRIVER-mode device control."""

from testmu_appium._helpers.device_control import KINDS, KindSpec, PlatformOps


def test_ios_gaps_are_exactly_the_declared_set():
    """The seam's coverage guard, moved here from test_platform_adapters.

    Every kind android serves and iOS does not is a decision, not an
    accident. A new kind fails here until its ios row is filled or its
    absence is added to this declaration.
    """
    declared_ios_absent = {
        # Appium's setConnectivity / shell channels are Android-only.
        "wifi", "flight_mode", "mobile_data", "bluetooth", "location",
        "brightness", "dnd",
        # No iOS notification shade: XCUITest exposes no open_notifications,
        # and dismissing it relies on the BACK key iOS does not have.
        "notification",
        # The shared hide_keyboard row lied on iOS (taps "done", reports
        # success either way); refused until the verified implementation
        # (b73806a..c818598) passes device validation.
        "hide_keyboard",
    }
    ios_absent = {
        kind for kind, spec in KINDS.items() if "ios" not in spec.platforms
    }
    assert ios_absent == declared_ios_absent, (
        f"undeclared iOS gaps: {sorted(ios_absent ^ declared_ios_absent)}"
    )


def test_existing_device_control_kinds_are_described_by_platform_ops():
    """The three shipped controls are data, not device_control branches."""
    assert set(KINDS) == {
        "orientation",
        "wifi",
        "flight_mode",
        "mobile_data",
        "bluetooth",
        "location",
        "dark_mode",
        "brightness",
        "dnd",
        "volume",
        "hide_keyboard",
        "notification",
    }

    for spec in KINDS.values():
        assert isinstance(spec, KindSpec)
        assert spec.description
        assert spec.platforms
        for ops in spec.platforms.values():
            assert isinstance(ops, PlatformOps)
            if ops.setter is not None:
                assert ops.value_domain is not None or spec.kind == "hide_keyboard"


def test_registry_only_exposes_getters_with_a_canonical_set_domain():
    for spec in KINDS.values():
        for ops in spec.platforms.values():
            if ops.getter is not None:
                assert ops.setter is not None
                assert ops.value_domain is not None


def test_canonical_domain_descriptions_keep_the_registry_order():
    assert KINDS["orientation"].platforms["android"].value_domain.describe() == (
        "portrait|landscape"
    )
    assert KINDS["wifi"].platforms["android"].value_domain.describe() == "on|off"
    assert KINDS["notification"].platforms["android"].value_domain.describe() == (
        "show|hide"
    )
