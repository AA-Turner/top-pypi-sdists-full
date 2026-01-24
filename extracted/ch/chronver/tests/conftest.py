"""Set up for chronver tests

:copyright: Copyright (c) 2024 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_protocol(*args, **kwargs):
    import pathlib, sys

    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
