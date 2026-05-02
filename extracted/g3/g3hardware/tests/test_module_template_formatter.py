import pytest

from g3hardware.api import HardwareModuleSettingsTemplateFormatter


@pytest.fixture
def formatter():
    return HardwareModuleSettingsTemplateFormatter()


@pytest.mark.parametrize(
    "module_type, expected_template_name",
    [
        ("x20cai4622", "X20cAI4622"),  # normal case
        ("  X20cCP1584  ", "X20cCP1584"),  # normal case (with spaces)        
        ("  X20cCP1684  ", "X20cCP1684"),  # normal case (with spaces)
        ("  X20cCP3687X  ", "X20cCP3687X"),  # normal case (with spaces)
        ("foo", "default"),  # unknown module type
    ]
    )
def test_get_template(formatter, module_type, expected_template_name):
    template = formatter.get_template(module_type)
    assert template.name == expected_template_name


@pytest.mark.parametrize(
    "template_name, render_args, expected_content_snippet",
    [
        (  # normal case (no render args)
            "X20cAI4622",
            {},
            """<Parameter ID="InputFilter" Value="level 16"/>
<Parameter ID="InputLimitation" Value="255"/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
        (  # wrong case (render args provided but not needed)
            "X20cAI4622",
            {"safemoduleid": "2"},
            """<Parameter ID="InputFilter" Value="level 16"/>
<Parameter ID="InputLimitation" Value="255"/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
        (  # normal case (with render args)
            "X20cSI4100",
            {"safemoduleid": "2"},
            """<Parameter ID="SafeModuleID" Value="2"/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
        (  # normal case (with render args, empty value)
            "X20cSI4100",
            {"safemoduleid": ""},
            """<Parameter ID="SafeModuleID" Value=""/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
        (  # wrong (no render args)
            "X20cSI4100",
            {},
            """<Parameter ID="SafeModuleID" Value="{{ safemoduleid }}"/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
        (  # wrong case (misspelled render args)
            "X20cSI4100",
            {"SafeModuleID": "2"},
            """<Parameter ID="SafeModuleID" Value="{{ safemoduleid }}"/>
<Parameter ID="Supervision" Value="off"/>"""
        ),
    ]
)
def test_format_template(
    formatter, template_name, render_args, expected_content_snippet
):
    template = formatter.env.get_template(template_name)
    rendered_content = formatter.format_template(template, **render_args)
    assert expected_content_snippet == rendered_content
