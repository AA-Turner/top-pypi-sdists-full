"""Exhaustive utility test for sms, command /models."""
import pytest
from sage.tests.rubric_checker import verify_utility_command

def test_sms_cmd_models_kdeconnect(tmp_path):
    verify_utility_command("sms", "/models", tmp_path, delivery="kdeconnect")
