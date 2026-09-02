"""Canary for the test suite's real-keychain guard."""

import os
import subprocess
import sys

import keyring
import keyring.backends.null

_NULL_KEYRING_BACKEND = "keyring.backends.null.Keyring"


def test_real_keychain_access_is_blocked_everywhere():
    assert os.environ["PYTHON_KEYRING_BACKEND"] == _NULL_KEYRING_BACKEND
    assert isinstance(keyring.get_keyring(), keyring.backends.null.Keyring)

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import os; print(os.environ.get('PYTHON_KEYRING_BACKEND', ''))",
        ],
        check=True,
        capture_output=True,
        env={},
        text=True,
    )

    assert result.stdout.strip() == _NULL_KEYRING_BACKEND
