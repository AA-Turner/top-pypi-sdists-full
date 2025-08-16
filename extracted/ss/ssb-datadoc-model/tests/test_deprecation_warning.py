import importlib

import pytest

import datadoc_model.all_optional  # noqa: F401
import datadoc_model.model
import datadoc_model.required  # noqa: F401


def test_import_deprecated_module():
    with pytest.warns(DeprecationWarning):
        importlib.reload(datadoc_model.model)


def test_import_all_optional_module(recwarn):
    importlib.reload(datadoc_model.all_optional)

    assert len(recwarn) == 0


def test_import_required_module(recwarn):
    importlib.reload(datadoc_model.required)
    assert len(recwarn) == 0
