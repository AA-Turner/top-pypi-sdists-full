"""
Call runtime_xfail() to mark running test as xfail.
"""
import pytest

@pytest.fixture()
def runtime_xfail(request):
    """
    Call runtime_xfail() to mark running test as xfail.
    """
    def _xfail(reason=''):
        request.node.add_marker(pytest.mark.xfail(reason=reason))
    return _xfail