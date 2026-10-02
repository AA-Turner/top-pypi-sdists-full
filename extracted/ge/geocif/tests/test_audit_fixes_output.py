"""``output.store`` must re-raise a failed results write (2026-09-30 audit,
A10): it used to print the error and return, so the run reported success
with the chunk's rows missing from the DB.
"""
import sqlite3

import pandas as pd
import pytest

from geocif import utils
from geocif.ml import output


def test_store_reraises_db_failure(monkeypatch, tmp_path):
    def boom(*args, **kwargs):
        raise sqlite3.OperationalError("disk I/O error")

    monkeypatch.setattr(utils, "to_db", boom)
    df = pd.DataFrame({"Best Hyperparameters": [{"depth": 4}], "x": [1.0]})
    with pytest.raises(sqlite3.OperationalError):
        output.store(tmp_path / "x.db", "exp", df, None, "catboost")


def test_store_writes_when_db_is_healthy(tmp_path):
    df = pd.DataFrame({"Best Hyperparameters": [{"depth": 4}], "x": [1.0]})
    df.index.name = "Index"
    output.store(tmp_path / "ok.db", "exp", df, None, "catboost")
    with sqlite3.connect(tmp_path / "ok.db") as con:
        assert con.execute("select count(*) from exp").fetchone()[0] == 1
