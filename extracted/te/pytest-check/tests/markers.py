import importlib.util

import pytest
from packaging import version


require_pytest_7_3 = pytest.mark.skipif(
    version.parse(pytest.__version__) < version.parse("7.3.0"),
    reason="summary message only supported on pytest7.3+",
)

require_pytest_reportlog = pytest.mark.skipif(
    importlib.util.find_spec("pytest_reportlog") is None,
    reason="requires pytest-reportlog",
)
