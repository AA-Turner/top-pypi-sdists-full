"""
Fixtures for preview feature filtering tests.

These tests validate that the code generator correctly filters out
preview endpoints and models based on x-sf-enabling-parameter.
"""

import sys
from pathlib import Path

import pytest
from unittest.mock import Mock

# Add codegen folder to path so 'tests.preview_test._generated' imports work
_codegen_dir = Path(__file__).parent.parent
if str(_codegen_dir) not in sys.path:
    sys.path.insert(0, str(_codegen_dir))

_GENERATED_CODE_MISSING_MSG = """
Generated test code not found.

Error: {error}
"""


@pytest.fixture(scope="module")
def mock_root():
    return Mock()


@pytest.fixture(scope="module")
def mock_resource_class():
    return Mock()


@pytest.fixture(scope="module")
def mock_sproc_client():
    return Mock()


@pytest.fixture(scope="module")
def default_api(mock_root, mock_resource_class, mock_sproc_client):
    try:
        from tests.preview_test._generated.api.default_api import DefaultApi

        return DefaultApi(root=mock_root, resource_class=mock_resource_class, sproc_client=mock_sproc_client)
    except ImportError as e:
        pytest.fail(_GENERATED_CODE_MISSING_MSG.format(error=e))


@pytest.fixture(scope="module")
def default_api_class():
    try:
        from tests.preview_test._generated.api.default_api import DefaultApi

        return DefaultApi
    except ImportError as e:
        pytest.fail(_GENERATED_CODE_MISSING_MSG.format(error=e))


@pytest.fixture(scope="module")
def models_module():
    try:
        from tests.preview_test._generated import models

        return models
    except ImportError as e:
        pytest.fail(_GENERATED_CODE_MISSING_MSG.format(error=e))
