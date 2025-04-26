import os
import shutil
import uuid
from unittest import TestCase

import pandas
import pyarrow
from deltalake.writer import write_deltalake

import tecton_core.tecton_pendulum as pendulum
from tecton_core import conf
from tecton_core.data_processing_utils import _calculate_split_count
from tecton_core.data_processing_utils import _even_split_pyarrow
from tecton_core.data_processing_utils import _get_total_row_number
from tecton_core.data_processing_utils import split_spine


pandas_df = pandas.DataFrame({"join_key": ["abc", "abd", "dbc", "dbe", "ace", "xyz", "xya", "xzz"]})
spine_pyarrow_table = pyarrow.table({"join_key": ["abc", "abd", "dbc", "dbe", "ace", "xyz", "xya", "xzz"]})
join_keys = ["join_key"]


class SpineSplitTest(TestCase):
    def test_spine_split_even(self):
        conf.set("DUCKDB_SPINE_SPLIT_STRATEGY", "even")
        conf.set("DUCKDB_SPINE_SPLIT_COUNT", 3)

        split_dfs = split_spine(pandas_df, join_keys)

        assert pandas.DataFrame.equals(split_dfs[0], pandas.DataFrame({"join_key": ["abc", "abd", "ace"]}))
        assert pandas.DataFrame.equals(split_dfs[1], pandas.DataFrame({"join_key": ["dbc", "dbe", "xya"]}))
        assert pandas.DataFrame.equals(split_dfs[2], pandas.DataFrame({"join_key": ["xyz", "xzz"]}))

    def test_spine_split_minimize_distance(self):
        conf.set("DUCKDB_SPINE_SPLIT_STRATEGY", "minimize_distance")
        conf.set("DUCKDB_SPINE_SPLIT_COUNT", 3)

        split_dfs = split_spine(pandas_df, join_keys)

        assert pandas.DataFrame.equals(split_dfs[0], pandas.DataFrame({"join_key": ["abc", "abd", "ace"]}))
        assert pandas.DataFrame.equals(split_dfs[1], pandas.DataFrame({"join_key": ["dbc", "dbe"]}))
        assert pandas.DataFrame.equals(split_dfs[2], pandas.DataFrame({"join_key": ["xya", "xyz", "xzz"]}))

    def test_spine_split_agglomerative_clustering(self):
        conf.set("DUCKDB_SPINE_SPLIT_STRATEGY", "agglomerative_clustering")
        conf.set("DUCKDB_SPINE_SPLIT_COUNT", 3)

        split_dfs = split_spine(pandas_df, join_keys)

        assert pandas.DataFrame.equals(split_dfs[0], pandas.DataFrame({"join_key": ["xyz", "xya", "xzz"]}))
        assert pandas.DataFrame.equals(split_dfs[1], pandas.DataFrame({"join_key": ["abc", "abd", "ace"]}))
        assert pandas.DataFrame.equals(split_dfs[2], pandas.DataFrame({"join_key": ["dbc", "dbe"]}))

    def test_spine_split_even_pyarrow(self):
        split_tables = _even_split_pyarrow(spine_pyarrow_table, join_keys, split_count=3)

        assert split_tables[0].equals(pyarrow.table({"join_key": ["abc", "abd", "ace"]}))
        assert split_tables[1].equals(pyarrow.table({"join_key": ["dbc", "dbe", "xya"]}))
        assert split_tables[2].equals(pyarrow.table({"join_key": ["xyz", "xzz"]}))

    def test_get_total_row_number(self):
        delta_table_path = f"/tmp/test_spine_split/delta_table_{uuid.uuid4()}"
        _set_up_delta_table(delta_table_path)

        total_row_number = _get_total_row_number(
            delta_table_path, pendulum.period(pendulum.parse("2023-09-17"), pendulum.parse("2023-09-19"))
        )

        assert total_row_number == 13

        _tear_down_delta_table(delta_table_path)

    def test_calculate_split_count(self):
        delta_table_path = f"/tmp/test_spine_split/delta_table_{uuid.uuid4()}"
        _set_up_delta_table(delta_table_path)

        split_count = _calculate_split_count(
            delta_table_path, pendulum.period(pendulum.parse("2023-09-17"), pendulum.parse("2023-09-19")), 4
        )

        assert split_count == 4

        _tear_down_delta_table(delta_table_path)


def _set_up_delta_table(delta_table_path):
    # fmt: off
    df = pandas.DataFrame(
        {
            "value": [
                1, 2, 3,
                1, 2,
                1, 2, 3, 4, 5, 6, 7,
                1, 2, 3, 4,
                1, 2,
                1, 2,
            ],
            "time_partition": [
                "2023-09-15", "2023-09-15", "2023-09-15",
                "2023-09-16", "2023-09-16",
                "2023-09-17", "2023-09-17", "2023-09-17", "2023-09-17", "2023-09-17", "2023-09-17", "2023-09-17",
                "2023-09-18", "2023-09-18", "2023-09-18", "2023-09-18",
                "2023-09-19", "2023-09-19",
                "2023-09-20", "2023-09-20",
            ],
        }
    )
    # fmt: on
    write_deltalake(delta_table_path, df, partition_by=["time_partition"])


def _tear_down_delta_table(delta_table_path):
    if os.path.exists(delta_table_path):
        shutil.rmtree(delta_table_path)
        print(f"Deleted Delta table at: {delta_table_path}")
