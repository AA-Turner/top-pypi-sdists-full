"""Unit tests for DDL generation — no Doris connection required.

DDL order verified on Doris 4.0.2:

    CREATE TABLE name (columns)
    ENGINE = OLAP
    KEY_TYPE KEY(cols)
    COMMENT 'text'
    [PARTITION BY ...]
    DISTRIBUTED BY HASH(col) BUCKETS N
    PROPERTIES ("k" = "v")
"""
import pytest
from sqlalchemy import MetaData, Table, Column, Integer, String, Float
from sqlalchemy.schema import CreateTable

from pydoris.sqlalchemy.dialect import DorisDialect
from pydoris.sqlalchemy.datatype import TINYINT, LARGEINT, DOUBLE, BITMAP, HLL


@pytest.fixture()
def dialect():
    return DorisDialect()


def _compile(table, dialect):
    return str(CreateTable(table).compile(dialect=dialect))


# ───────────────────────────────────────────────────────────────────────────
# KEY model: DUPLICATE / UNIQUE / AGGREGATE
# ───────────────────────────────────────────────────────────────────────────
class TestKeyModel:

    def test_duplicate_key_explicit(self, dialect):
        t = Table("t", MetaData(),
                  Column("id", Integer), Column("v", String(50)),
                  pydoris_key_type="DUPLICATE", pydoris_key_columns=["id"])
        ddl = _compile(t, dialect)
        assert "DUPLICATE KEY(`id`)" in ddl

    def test_duplicate_key_multi_columns(self, dialect):
        t = Table("t", MetaData(),
                  Column("a", Integer), Column("b", Integer), Column("c", String(50)),
                  pydoris_key_type="DUPLICATE", pydoris_key_columns=["a", "b"])
        ddl = _compile(t, dialect)
        assert "DUPLICATE KEY(`a`, `b`)" in ddl

    def test_unique_key(self, dialect):
        t = Table("t", MetaData(),
                  Column("id", Integer), Column("name", String(50)),
                  pydoris_key_type="UNIQUE", pydoris_key_columns=["id", "name"])
        ddl = _compile(t, dialect)
        assert "UNIQUE KEY(`id`, `name`)" in ddl

    def test_aggregate_key(self, dialect):
        t = Table("t", MetaData(),
                  Column("id", Integer), Column("pv", Integer),
                  pydoris_key_type="AGGREGATE", pydoris_key_columns=["id"])
        ddl = _compile(t, dialect)
        assert "AGGREGATE KEY(`id`)" in ddl

    def test_auto_detect_key_from_pk(self, dialect):
        """When no key_type/key_columns given, derive DUPLICATE KEY from primary_key."""
        t = Table("t", MetaData(),
                  Column("uid", Integer, primary_key=True),
                  Column("val", String(100)))
        ddl = _compile(t, dialect)
        assert "DUPLICATE KEY(`uid`)" in ddl

    def test_auto_detect_key_multi_pk(self, dialect):
        t = Table("t", MetaData(),
                  Column("a", Integer, primary_key=True),
                  Column("b", Integer, primary_key=True),
                  Column("v", String(50)))
        ddl = _compile(t, dialect)
        assert "DUPLICATE KEY(`a`, `b`)" in ddl

    def test_no_key_when_no_pk_and_no_opts(self, dialect):
        t = Table("t", MetaData(),
                  Column("a", Integer), Column("b", String(10)))
        ddl = _compile(t, dialect)
        assert "KEY(" not in ddl


# ───────────────────────────────────────────────────────────────────────────
# Suppress MySQL-specific DDL that Doris rejects
# ───────────────────────────────────────────────────────────────────────────
class TestSuppressedMySQLFeatures:

    def test_no_auto_increment(self, dialect):
        t = Table("t", MetaData(),
                  Column("id", Integer, primary_key=True), Column("v", Integer))
        ddl = _compile(t, dialect)
        assert "AUTO_INCREMENT" not in ddl

    def test_no_primary_key_constraint(self, dialect):
        t = Table("t", MetaData(),
                  Column("id", Integer, primary_key=True))
        ddl = _compile(t, dialect)
        assert "PRIMARY KEY" not in ddl

    def test_no_foreign_key_constraint(self, dialect):
        m = MetaData()
        Table("parent", m, Column("id", Integer, primary_key=True))
        child = Table("child", m,
                      Column("id", Integer, primary_key=True),
                      Column("pid", Integer))
        ddl = _compile(child, dialect)
        assert "FOREIGN KEY" not in ddl

    def test_no_unique_constraint(self, dialect):
        from sqlalchemy import UniqueConstraint
        t = Table("t", MetaData(),
                  Column("id", Integer, primary_key=True),
                  Column("email", String(100)),
                  UniqueConstraint("email"))
        ddl = _compile(t, dialect)
        assert "UNIQUE" not in ddl or "UNIQUE KEY" in ddl  # only as Doris KEY model

    def test_no_unsigned(self, dialect):
        t = Table("t", MetaData(),
                  Column("a", TINYINT), Column("b", LARGEINT), Column("c", Integer))
        ddl = _compile(t, dialect)
        assert "UNSIGNED" not in ddl

    def test_no_zerofill(self, dialect):
        t = Table("t", MetaData(), Column("a", Integer))
        ddl = _compile(t, dialect)
        assert "ZEROFILL" not in ddl


# ───────────────────────────────────────────────────────────────────────────
# ENGINE
# ───────────────────────────────────────────────────────────────────────────
class TestEngine:

    def test_engine_olap(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer), pydoris_engine="OLAP")
        ddl = _compile(t, dialect)
        assert "ENGINE = OLAP" in ddl

    def test_no_engine_by_default(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer))
        ddl = _compile(t, dialect)
        assert "ENGINE" not in ddl


# ───────────────────────────────────────────────────────────────────────────
# DISTRIBUTED BY
# ───────────────────────────────────────────────────────────────────────────
class TestDistribution:

    def test_hash_with_buckets(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer),
                  pydoris_distributed_by='HASH(`id`)', pydoris_buckets=16)
        ddl = _compile(t, dialect)
        assert "DISTRIBUTED BY HASH(`id`) BUCKETS 16" in ddl

    def test_hash_without_buckets(self, dialect):
        """Omitting BUCKETS lets Doris use AUTO sizing."""
        t = Table("t", MetaData(), Column("id", Integer),
                  pydoris_distributed_by='HASH(`id`)')
        ddl = _compile(t, dialect)
        assert "DISTRIBUTED BY HASH(`id`)" in ddl
        assert "BUCKETS" not in ddl

    def test_random_distribution(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer),
                  pydoris_distributed_by='RANDOM', pydoris_buckets='AUTO')
        ddl = _compile(t, dialect)
        assert "DISTRIBUTED BY RANDOM BUCKETS AUTO" in ddl

    def test_hash_multi_columns(self, dialect):
        t = Table("t", MetaData(), Column("a", Integer), Column("b", Integer),
                  pydoris_distributed_by='HASH(`a`, `b`)', pydoris_buckets=8)
        ddl = _compile(t, dialect)
        assert "DISTRIBUTED BY HASH(`a`, `b`) BUCKETS 8" in ddl


# ───────────────────────────────────────────────────────────────────────────
# PARTITION BY
# ───────────────────────────────────────────────────────────────────────────
class TestPartition:

    def test_range_partition(self, dialect):
        part = ("PARTITION BY RANGE(`dt`) ("
                "PARTITION p202501 VALUES LESS THAN ('2025-02-01'), "
                "PARTITION p202502 VALUES LESS THAN ('2025-03-01'))")
        t = Table("t", MetaData(), Column("dt", Integer), Column("id", Integer),
                  pydoris_partition_by=part)
        ddl = _compile(t, dialect)
        assert "PARTITION BY RANGE" in ddl
        assert "VALUES LESS THAN" in ddl

    def test_list_partition(self, dialect):
        part = ("PARTITION BY LIST(`city`) ("
                "PARTITION p_cn VALUES IN ('beijing', 'shanghai'), "
                "PARTITION p_us VALUES IN ('new york'))")
        t = Table("t", MetaData(), Column("city", String(50)), Column("id", Integer),
                  pydoris_partition_by=part)
        ddl = _compile(t, dialect)
        assert "PARTITION BY LIST" in ddl


# ───────────────────────────────────────────────────────────────────────────
# PROPERTIES
# ───────────────────────────────────────────────────────────────────────────
class TestProperties:

    def test_single_property(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer),
                  pydoris_properties={"replication_num": "1"})
        ddl = _compile(t, dialect)
        assert 'PROPERTIES ("replication_num" = "1")' in ddl

    def test_multiple_properties(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer),
                  pydoris_properties={"replication_num": "3", "storage_format": "V2"})
        ddl = _compile(t, dialect)
        assert '"replication_num" = "3"' in ddl
        assert '"storage_format" = "V2"' in ddl


# ───────────────────────────────────────────────────────────────────────────
# COMMENT
# ───────────────────────────────────────────────────────────────────────────
class TestComment:

    def test_table_comment(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer), comment="my test table")
        ddl = _compile(t, dialect)
        assert "COMMENT 'my test table'" in ddl

    def test_comment_with_single_quote(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer), comment="it's a table")
        ddl = _compile(t, dialect)
        assert "COMMENT 'it\\'s a table'" in ddl

    def test_comment_before_distributed(self, dialect):
        """Doris requires: ... COMMENT '...' DISTRIBUTED BY ..."""
        t = Table("t", MetaData(), Column("id", Integer),
                  comment="test",
                  pydoris_distributed_by='HASH(`id`)', pydoris_buckets=1)
        ddl = _compile(t, dialect)
        comment_pos = ddl.index("COMMENT")
        dist_pos = ddl.index("DISTRIBUTED")
        assert comment_pos < dist_pos

    def test_comment_before_partition(self, dialect):
        t = Table("t", MetaData(), Column("id", Integer),
                  comment="test",
                  pydoris_partition_by="PARTITION BY RANGE(`id`) (PARTITION p1 VALUES LESS THAN ('100'))")
        ddl = _compile(t, dialect)
        comment_pos = ddl.index("COMMENT")
        part_pos = ddl.index("PARTITION")
        assert comment_pos < part_pos


# ───────────────────────────────────────────────────────────────────────────
# DDL clause ordering: ENGINE → KEY → COMMENT → PARTITION → DISTRIBUTED → PROPERTIES
# ───────────────────────────────────────────────────────────────────────────
class TestDDLOrdering:

    def test_full_ordering(self, dialect):
        t = Table("t", MetaData(),
                  Column("dt", Integer), Column("id", Integer), Column("v", String(50)),
                  pydoris_engine="OLAP",
                  pydoris_key_type="DUPLICATE", pydoris_key_columns=["dt", "id"],
                  comment="ordering test",
                  pydoris_partition_by="PARTITION BY RANGE(`dt`) (PARTITION p1 VALUES LESS THAN ('100'))",
                  pydoris_distributed_by='HASH(`id`)', pydoris_buckets=8,
                  pydoris_properties={"replication_num": "1"})
        ddl = _compile(t, dialect)

        positions = {
            "ENGINE": ddl.index("ENGINE"),
            "KEY": ddl.index("DUPLICATE KEY"),
            "COMMENT": ddl.index("COMMENT"),
            "PARTITION": ddl.index("PARTITION BY"),
            "DISTRIBUTED": ddl.index("DISTRIBUTED"),
            "PROPERTIES": ddl.index("PROPERTIES"),
        }
        order = sorted(positions, key=positions.get)
        assert order == ["ENGINE", "KEY", "COMMENT", "PARTITION", "DISTRIBUTED", "PROPERTIES"]


# ───────────────────────────────────────────────────────────────────────────
# Doris-specific column types in DDL output
# ───────────────────────────────────────────────────────────────────────────
class TestColumnTypeDDL:

    @pytest.mark.parametrize("col_type, expected_str", [
        (TINYINT,  "TINYINT"),
        (LARGEINT, "LARGEINT"),
        (DOUBLE,   "DOUBLE"),
        (BITMAP,   "BITMAP"),
        (HLL,      "HLL"),
    ])
    def test_doris_type_in_ddl(self, dialect, col_type, expected_str):
        t = Table("t", MetaData(), Column("a", col_type))
        ddl = _compile(t, dialect)
        assert expected_str in ddl


# ───────────────────────────────────────────────────────────────────────────
# Full realistic DDL (matches what Doris actually accepts)
# ───────────────────────────────────────────────────────────────────────────
class TestRealisticDDL:

    def test_duplicate_model_table(self, dialect):
        t = Table(
            "user_events", MetaData(),
            Column("event_date", Integer),
            Column("user_id", Integer),
            Column("event_type", String(50)),
            Column("amount", DOUBLE),
            pydoris_engine="OLAP",
            pydoris_key_type="DUPLICATE",
            pydoris_key_columns=["event_date", "user_id"],
            comment="user event log",
            pydoris_distributed_by='HASH(`user_id`)',
            pydoris_buckets=32,
            pydoris_properties={"replication_num": "3"},
        )
        ddl = _compile(t, dialect)

        assert "CREATE TABLE user_events" in ddl
        assert "ENGINE = OLAP" in ddl
        assert "DUPLICATE KEY(`event_date`, `user_id`)" in ddl
        assert "COMMENT 'user event log'" in ddl
        assert "DISTRIBUTED BY HASH(`user_id`) BUCKETS 32" in ddl
        assert '"replication_num" = "3"' in ddl
        assert "AUTO_INCREMENT" not in ddl
        assert "PRIMARY KEY" not in ddl

    def test_unique_model_table(self, dialect):
        t = Table(
            "users", MetaData(),
            Column("id", Integer),
            Column("name", String(100)),
            Column("email", String(200)),
            pydoris_key_type="UNIQUE",
            pydoris_key_columns=["id"],
            pydoris_distributed_by='HASH(`id`)',
            pydoris_buckets=16,
            pydoris_properties={"replication_num": "1",
                                "enable_unique_key_merge_on_write": "true"},
        )
        ddl = _compile(t, dialect)
        assert "UNIQUE KEY(`id`)" in ddl
        assert '"enable_unique_key_merge_on_write" = "true"' in ddl

    def test_aggregate_model_table(self, dialect):
        t = Table(
            "site_metrics", MetaData(),
            Column("dt", Integer),
            Column("site_id", Integer),
            Column("pv", Integer),
            pydoris_key_type="AGGREGATE",
            pydoris_key_columns=["dt", "site_id"],
            pydoris_distributed_by='HASH(`site_id`)',
            pydoris_buckets=8,
            pydoris_properties={"replication_num": "1"},
        )
        ddl = _compile(t, dialect)
        assert "AGGREGATE KEY(`dt`, `site_id`)" in ddl
