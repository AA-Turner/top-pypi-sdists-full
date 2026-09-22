import builtins

import pytest

from public import install, private, public


@pytest.fixture
def cleanup_builtins():
    # We have to run this at the start of the test because when this package
    # is installed into the test environment, of course the public.pth file
    # gets evaluate, which installs the names into builtins!
    builtins.__dict__.pop('public', None)
    builtins.__dict__.pop('private', None)
    yield
    # Remove public and private from builtins after each test.
    builtins.__dict__.pop('public', None)
    builtins.__dict__.pop('private', None)


def test_install(cleanup_builtins):
    assert not hasattr(builtins, 'public')
    assert not hasattr(builtins, 'private')
    install()
    assert builtins.public is public
    assert builtins.private is private
