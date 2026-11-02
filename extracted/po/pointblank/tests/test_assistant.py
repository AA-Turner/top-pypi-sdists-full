import sys

import pytest
from unittest.mock import patch

from pointblank.validate import load_dataset
from pointblank.assistant import assistant


def test_draft_fail_no_chatlas():
    with patch.dict(sys.modules, {"chatlas": None}):
        with pytest.raises(ImportError):
            assistant(data="data", model="model")


def test_draft_fail_no_shiny():
    with patch.dict(sys.modules, {"shiny": None}):
        with pytest.raises(ImportError):
            assistant(data="data", model="model")


def test_draft_fail_invalid_provider():
    small_table = load_dataset(dataset="small_table")

    with pytest.raises(ValueError):
        assistant(data=small_table, model="invalid:model")
        assistant(data=small_table, tbl_name="small_table", model="invalid:model")
        assistant(model="invalid:model")
