# -*- coding: utf-8 -*-

from boto_session_manager.exc import NoBotocoreCredentialError

import pytest


def test_no_botocore_credential_error():
    with pytest.raises(NoBotocoreCredentialError):
        raise NoBotocoreCredentialError
    assert issubclass(NoBotocoreCredentialError, Exception)


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.exc",
        preview=False,
    )
