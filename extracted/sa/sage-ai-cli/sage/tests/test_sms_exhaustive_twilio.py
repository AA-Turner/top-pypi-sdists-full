import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_exhaustive_twilio(tmp_path):
    """Verify exhaustive SMS native sending and Twilio voice calls via SMS."""
    prompts = [
        "Send a text message using the SMS bridge natively.",
        "Trigger an API call to Twilio to initiate a phone call."
    ]
    for prompt in prompts:
        verify_sms_with_rubric(prompt, tmp_path)
