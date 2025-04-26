# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

from snowflake import _legacy

import pytest

# 2023-09-07(bwarsaw): These tests are missing an important check that the snowflake.pth file gets installed
# correctly, and that it properly injects the legacy functions into the `snowflake` namespace.  It's actually
# tricky to write that test, we assume -- backed by manual testing and if need be, a test external to the unit
# tests -- that it does.

def test_snowflake(monkeypatch, tmp_path):
    snowflake_file = tmp_path / 'snowflake'
    with snowflake_file.open('w') as fp:
        # The contents don't matter as it is not validated.
        fp.write('snowflake uuid')
    monkeypatch.setattr(_legacy, 'SNOWFLAKE_FILE', str(snowflake_file))
    assert _legacy.snowflake() == 'snowflake uuid'


def test_snowflake_with_arg(tmp_path):
    snowflake_file = tmp_path / 'snowflake'
    with snowflake_file.open('w') as fp:
        # The contents don't matter as it is not validated.
        fp.write('snowflake uuid')
    assert _legacy.snowflake(snowflake_file=snowflake_file) == 'snowflake uuid'


def test_snowflake_filenotfound(monkeypatch, tmp_path):
    snowflake_file = tmp_path / 'snowflake'
    with pytest.raises(FileNotFoundError):
        _legacy.snowflake()


def test_make_snowflake_notimplemented():
    with pytest.raises(NotImplementedError):
        _legacy.make_snowflake()
