import pytest
import sys
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


@pytest.mark.timeout(900)
def test_sms_exhaustive_native_text(tmp_path):
    """Verify exhaustive SMS native sending."""
    verify_sms_with_rubric(
        "Send a text message using the SMS bridge natively.", 
        tmp_path, 
        skip_build_prefix=True
    )

@pytest.mark.timeout(1800)
def test_sms_exhaustive_native_call(tmp_path):
    """Verify exhaustive native audio phone call."""
    if sys.platform == "darwin":
        prompt = "Use a native macOS AppleScript to initiate a FaceTime audio phone call."
    elif sys.platform == "win32":
        prompt = "Use a native PowerShell script to initiate a phone call via Windows Phone Link."
    else:
        prompt = "Use the kdeconnect-cli tool to initiate a native phone call."
        
    verify_sms_with_rubric(
        prompt, 
        tmp_path, 
        skip_build_prefix=True
    )
