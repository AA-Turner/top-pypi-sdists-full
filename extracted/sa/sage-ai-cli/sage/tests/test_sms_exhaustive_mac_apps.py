import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_mac_apps(tmp_path):
    """Verify exhaustive macOS app operations (osascript system config and Messages setup) via SMS."""
    prompts = [
        "Open the Messages app on my Mac and prepare a text.",
        "Use osascript to change my system volume and toggle dark mode."
    ]
    for prompt in prompts:
        verify_sms_with_rubric(prompt, tmp_path)
