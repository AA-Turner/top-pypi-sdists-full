import pytest

from g3hardware.api import HardwareModuleConfig


@pytest.mark.parametrize(
    "input_type, expected_output",
    [
        ("x20cbb80", "X20cBB80"),  # normal case
        ("x20cai4622", "X20cAI4622"),  # normal case
        ("X20CAT4222  ", "X20cAT4222"),  # normal case (with spaces)
        ("X20c SI9100", "X20c SI9100"),  # wrong (spaces in the middle)
        ("x20cbb90", "x20cbb90"),  # wrong (unknown module type)
        ("foo", "foo"),  # wrong (unknown module type)
    ]
)
def test_format_type(input_type, expected_output):
    assert HardwareModuleConfig.format_type(input_type) == expected_output


@pytest.mark.parametrize(
    "input_type, expected_tb",
    [
        ("x20cai4622", "X20TB12"),  # normal case
        ("x20csl8101", "X20TB52"),  # normal case
        ("x20csl8100", "X20TB52"),  # normal case
        ("x20cmk0213", None),  # normal case (module without TB)
        ("foo", None),  # wrong (unknown module type)
    ]
)
def test_get_tb(input_type, expected_tb):
    assert HardwareModuleConfig.get_tb(input_type).value == expected_tb


@pytest.mark.parametrize(
    "input_type, expected_bm",
    [
        ("x20cai4622", "X20cBM11"),  # normal case
        ("x20csl8101", None),  # normal case (module without BM)
        ("x20csl8100", None),  # normal case (module without BM)
        ("foo", None),  # wrong (unknown module type)
    ]
)
def test_get_bm(input_type, expected_bm):
    assert HardwareModuleConfig.get_bm(input_type).value == expected_bm


@pytest.mark.parametrize(
    "input_type, expected_settings",
    [
        (  # normal case
            "x20cai4622",
            """<Parameter ID="InputFilter" Value="level 16"/>
<Parameter ID="InputLimitation" Value="255"/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
        ("X20TB12", None),  # normal case (module without BM)
        ("foo", None),  # wrong (unknown module type)
    ]
)
def test_get_settings(input_type, expected_settings):
    settings = HardwareModuleConfig.get_settings(input_type).value
    assert settings == expected_settings
