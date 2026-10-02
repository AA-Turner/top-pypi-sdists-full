"""utils-level fixes from the 2026-09-30 audit.

- ``compute_h_index`` returned the h-th largest VALUE, not h.
- ``to_db`` swallowed every non-lock write error, so a run could finish
  "complete" with zero rows for the affected chunk.
- ``local_now`` is the single source of the pipeline's reference date
  (America/New_York) for every "is this month complete" decision.
"""
import sqlite3

import arrow as ar
import pandas as pd
import pytest

from geocif import utils


def test_h_index_is_a_count_not_a_value():
    # four values are >= 4 but only three are >= 5 -> h = 4 (the old code
    # returned 4 here by coincidence of the value; the next cases separate
    # the two readings).
    assert utils.compute_h_index([10, 8, 5, 4, 3]) == 4
    # three values >= 3 -> 3, whereas the 3rd largest value is 9
    assert utils.compute_h_index([30, 20, 9]) == 3
    assert utils.compute_h_index([1, 1, 1]) == 1
    assert utils.compute_h_index([0.5, 0.2]) == 0
    assert utils.compute_h_index([]) == 0


def test_local_now_is_new_york_time():
    now = utils.local_now()
    assert now.utcoffset().total_seconds() in (-4 * 3600, -5 * 3600)
    assert abs((ar.utcnow() - now).total_seconds()) < 5


def test_to_db_writes_rows(tmp_path):
    df = pd.DataFrame({"a": [1, 2]})
    df.index.name = "Index"
    db = tmp_path / "ok.db"
    utils.to_db(db, "t", df)
    with sqlite3.connect(db) as con:
        assert con.execute("select count(*) from t").fetchone()[0] == 2


def test_to_db_raises_instead_of_swallowing_write_errors(tmp_path):
    df = pd.DataFrame({"a": [1]})
    df.index.name = "Index"
    missing_dir = tmp_path / "no_such_dir" / "x.db"
    with pytest.raises(RuntimeError, match="to_db failed"):
        utils.to_db(missing_dir, "t", df, max_retries=1)
