# -*- coding: utf-8 -*-

from boto_session_manager.sentinel import NOTHING
from boto_session_manager.sentinel import resolve_kwargs


def test_nothing():
    assert repr(NOTHING) == "NOTHING"
    assert bool(NOTHING) is False
    assert NOTHING is not None


def test_resolve_kwargs():
    """
    NOTHING means "not passed" and is dropped; None is a real value and is kept.
    """
    assert resolve_kwargs(a=1, b=NOTHING, c=None) == {"a": 1, "c": None}


def test_resolve_kwargs_with_mapper():
    kwargs = resolve_kwargs(
        _mapper={"role_arn": "RoleArn"},
        role_arn="arn",
        external_id=NOTHING,
    )
    assert kwargs == {"RoleArn": "arn"}


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.sentinel",
        preview=False,
    )
