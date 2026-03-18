"""Integration tests — require a running Doris instance (4.0+).

All expectations verified against Doris 4.0.2.  Set DORIS_URI env var or
use the defaults in conftest.py.  Skipped automatically when the database
is unreachable.
"""
import datetime

import pytest
from sqlalchemy import text

from pydoris.sqlalchemy.datatype import parse_sqltype


# ═══════════════════════════════════════════════════════════════════════════
# Fixtures — test tables
# ═══════════════════════════════════════════════════════════════════════════
@pytest.fixture(scope="module")
def setup_tables(doris_engine):
    """Create every table needed by the module, drop on teardown."""
    stmts = [
        # --- all-types table ---
        "DROP TABLE IF EXISTS pydoris_test.all_types",
        """CREATE TABLE pydoris_test.all_types (
            k1 INT NOT NULL,
            c_boolean BOOLEAN,
            c_tinyint TINYINT,
            c_smallint SMALLINT,
            c_int INT,
            c_bigint BIGINT,
            c_largeint LARGEINT,
            c_float FLOAT,
            c_double DOUBLE,
            c_decimalv3 DECIMALV3(18,6),
            c_decimalv3_def DECIMALV3,
            c_char CHAR(50),
            c_varchar VARCHAR(255),
            c_string STRING,
            c_text TEXT,
            c_date DATE,
            c_datetime DATETIME,
            c_datetime3 DATETIME(3),
            c_datetime6 DATETIME(6),
            c_json JSON,
            c_jsonb JSONB,
            c_array ARRAY<INT>,
            c_map MAP<STRING, INT>,
            c_struct STRUCT<name:STRING, age:INT>,
            c_ipv4 IPV4,
            c_ipv6 IPV6,
            c_variant VARIANT
        ) DUPLICATE KEY(k1)
        DISTRIBUTED BY HASH(k1) BUCKETS 1
        PROPERTIES ("replication_num" = "1")""",

        # --- defaults table ---
        "DROP TABLE IF EXISTS pydoris_test.defaults_test",
        """CREATE TABLE pydoris_test.defaults_test (
            k1 INT NOT NULL,
            c_def_null VARCHAR(50) NULL DEFAULT NULL,
            c_def_str VARCHAR(50) NULL DEFAULT 'hello',
            c_def_int INT NULL DEFAULT '100',
            c_no_def VARCHAR(50) NULL
        ) DUPLICATE KEY(k1)
        DISTRIBUTED BY HASH(k1) BUCKETS 1
        PROPERTIES ("replication_num" = "1")""",

        # --- AGGREGATE KEY table ---
        "DROP TABLE IF EXISTS pydoris_test.agg_model",
        """CREATE TABLE pydoris_test.agg_model (
            dt DATE NOT NULL,
            user_id INT NOT NULL,
            pv INT SUM NOT NULL DEFAULT '0',
            uv BITMAP BITMAP_UNION NOT NULL
        ) AGGREGATE KEY(dt, user_id)
        DISTRIBUTED BY HASH(user_id) BUCKETS 1
        PROPERTIES ("replication_num" = "1")""",

        # --- UNIQUE KEY table ---
        "DROP TABLE IF EXISTS pydoris_test.unique_model",
        """CREATE TABLE pydoris_test.unique_model (
            id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            value INT NULL
        ) UNIQUE KEY(id, name)
        DISTRIBUTED BY HASH(id) BUCKETS 1
        PROPERTIES ("replication_num" = "1")""",

        # --- index table ---
        "DROP TABLE IF EXISTS pydoris_test.index_test",
        """CREATE TABLE pydoris_test.index_test (
            k1 INT NOT NULL,
            name VARCHAR(100),
            city VARCHAR(50),
            bio TEXT,
            INDEX idx_name (name) USING INVERTED,
            INDEX idx_bio (bio) USING INVERTED PROPERTIES("parser" = "english")
        ) DUPLICATE KEY(k1)
        DISTRIBUTED BY HASH(k1) BUCKETS 1
        PROPERTIES ("replication_num" = "1")""",

        # --- comment table ---
        "DROP TABLE IF EXISTS pydoris_test.comment_test",
        """CREATE TABLE pydoris_test.comment_test (
            k1 INT NOT NULL COMMENT 'primary id',
            name VARCHAR(100) COMMENT 'user name'
        ) DUPLICATE KEY(k1)
        COMMENT 'table level comment'
        DISTRIBUTED BY HASH(k1) BUCKETS 1
        PROPERTIES ("replication_num" = "1")""",

        # --- view ---
        "DROP VIEW IF EXISTS pydoris_test.test_view",
        "CREATE VIEW pydoris_test.test_view AS SELECT k1, c_int FROM pydoris_test.all_types",

        # --- DISTRIBUTED BY RANDOM ---
        "DROP TABLE IF EXISTS pydoris_test.random_dist",
        """CREATE TABLE pydoris_test.random_dist (k1 INT, v1 STRING)
        DUPLICATE KEY(k1) DISTRIBUTED BY RANDOM BUCKETS AUTO
        PROPERTIES ("replication_num" = "1")""",
    ]
    with doris_engine.connect() as conn:
        for s in stmts:
            conn.execute(text(s))
        conn.commit()

    yield

    with doris_engine.connect() as conn:
        conn.execute(text("DROP VIEW IF EXISTS pydoris_test.test_view"))
        for tbl in ["all_types", "defaults_test", "agg_model", "unique_model",
                     "index_test", "comment_test", "random_dist"]:
            conn.execute(text(f"DROP TABLE IF EXISTS pydoris_test.{tbl}"))
        conn.commit()


# ═══════════════════════════════════════════════════════════════════════════
# 1. Type parsing — verified against real SHOW COLUMNS output
# ═══════════════════════════════════════════════════════════════════════════
class TestTypeMapping:
    """What Doris SHOW COLUMNS reports vs. what parse_sqltype produces."""

    # Mapping: column_name -> (expected_reported_type_prefix, expected_python_class_name)
    EXPECTED = {
        "k1":              ("int",            "INTEGER"),
        "c_boolean":       ("boolean",        "BOOLEAN"),
        "c_tinyint":       ("tinyint",        "TINYINT"),
        "c_smallint":      ("smallint",       "SMALLINT"),
        "c_int":           ("int",            "INTEGER"),
        "c_bigint":        ("bigint",         "BIGINT"),
        "c_largeint":      ("largeint",       "LARGEINT"),
        "c_float":         ("float",          "FLOAT"),
        "c_double":        ("double",         "DOUBLE"),
        "c_decimalv3":     ("decimal(18,6)",  "DECIMAL"),
        "c_decimalv3_def": ("decimal(38,9)",  "DECIMAL"),
        "c_char":          ("char(50)",       "CHAR"),
        "c_varchar":       ("varchar(255)",   "VARCHAR"),
        "c_string":        ("text",           "TEXT"),     # STRING → text
        "c_text":          ("text",           "TEXT"),
        "c_date":          ("date",           "DATE"),
        "c_datetime":      ("datetime",       "DATETIME"),
        "c_datetime3":     ("datetime(3)",    "DATETIME"),
        "c_datetime6":     ("datetime(6)",    "DATETIME"),
        "c_json":          ("json",           "JSON"),
        "c_jsonb":         ("json",           "JSON"),     # JSONB → json
        "c_array":         ("array<int>",     "ARRAY"),
        "c_map":           ("map<text,int>",  "MAP"),
        "c_struct":        ("struct<",        "STRUCT"),
        "c_ipv4":          ("ipv4",           "IPV4"),
        "c_ipv6":          ("ipv6",           "IPV6"),
        "c_variant":       ("variant",        "VARIANT"),
    }

    def test_all_column_types_reported_and_parsed(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SHOW COLUMNS FROM `pydoris_test`.`all_types`"
            )
            checked = set()
            for row in rows:
                col_name, type_str = row[0], row[1]
                if col_name not in self.EXPECTED:
                    continue
                exp_prefix, exp_cls = self.EXPECTED[col_name]

                # Verify what Doris actually reports
                assert type_str.startswith(exp_prefix), (
                    f"{col_name}: expected type to start with '{exp_prefix}', got '{type_str}'")

                # Verify our parse_sqltype handles it
                parsed = parse_sqltype(type_str)
                assert type(parsed).__name__ == exp_cls, (
                    f"{col_name}: parse_sqltype('{type_str}') -> {type(parsed).__name__}, "
                    f"expected {exp_cls}")
                checked.add(col_name)

            assert checked == set(self.EXPECTED.keys()), (
                f"Missing columns: {set(self.EXPECTED.keys()) - checked}")

    def test_varchar_length_preserved(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SHOW COLUMNS FROM `pydoris_test`.`all_types`"
            )
            for row in rows:
                if row[0] == "c_varchar":
                    t = parse_sqltype(row[1])
                    assert t.length == 255
                    return
        pytest.fail("Column 'c_varchar' not found")

    def test_char_length_preserved(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SHOW COLUMNS FROM `pydoris_test`.`all_types`"
            )
            for row in rows:
                if row[0] == "c_char":
                    t = parse_sqltype(row[1])
                    assert t.length == 50
                    return
        pytest.fail("Column 'c_char' not found")

    def test_decimal_precision_scale(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SHOW COLUMNS FROM `pydoris_test`.`all_types`"
            )
            for row in rows:
                if row[0] == "c_decimalv3":
                    t = parse_sqltype(row[1])
                    assert t.precision == 18
                    assert t.scale == 6
                    return
        pytest.fail("Column 'c_decimalv3' not found")

    def test_decimal_default_precision(self, doris_engine, setup_tables):
        """DECIMALV3 without params → decimal(38,9)."""
        with doris_engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SHOW COLUMNS FROM `pydoris_test`.`all_types`"
            )
            for row in rows:
                if row[0] == "c_decimalv3_def":
                    t = parse_sqltype(row[1])
                    assert t.precision == 38
                    assert t.scale == 9
                    return
        pytest.fail("Column 'c_decimalv3_def' not found")


# ═══════════════════════════════════════════════════════════════════════════
# 2. SHOW COLUMNS metadata — nullable, default, key, extra
# ═══════════════════════════════════════════════════════════════════════════
class TestShowColumns:
    """SHOW COLUMNS returns: Field(0), Type(1), Null(2), Key(3), Default(4), Extra(5)."""

    def _columns(self, conn, table):
        rows = conn.exec_driver_sql(
            f"SHOW COLUMNS FROM `pydoris_test`.`{table}`"
        )
        return {r[0]: {"type": r[1], "null": r[2], "key": r[3],
                       "default": r[4], "extra": r[5]} for r in rows}

    # --- nullable ---
    def test_not_null(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "defaults_test")
            assert cols["k1"]["null"] == "NO"

    def test_nullable(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "defaults_test")
            assert cols["c_def_str"]["null"] == "YES"

    # --- default ---
    def test_default_string(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "defaults_test")
            assert cols["c_def_str"]["default"] == "hello"

    def test_default_int(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "defaults_test")
            assert cols["c_def_int"]["default"] == "100"

    def test_default_none_when_no_default(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "defaults_test")
            assert cols["k1"]["default"] is None

    # --- key ---
    def test_key_column_marked(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "all_types")
            assert cols["k1"]["key"] == "YES"
            assert cols["c_int"]["key"] == "NO"

    # --- extra (aggregation type) ---
    def test_aggregate_extra_sum(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "agg_model")
            assert cols["pv"]["extra"] == "SUM"

    def test_aggregate_extra_bitmap_union(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "agg_model")
            assert cols["uv"]["extra"] == "BITMAP_UNION"

    def test_unique_extra_none(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "unique_model")
            assert cols["value"]["extra"] == "NONE"

    def test_duplicate_key_extra_empty(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            cols = self._columns(conn, "all_types")
            assert cols["k1"]["extra"] == ""


# ═══════════════════════════════════════════════════════════════════════════
# 3. SHOW FULL COLUMNS — column comment
# ═══════════════════════════════════════════════════════════════════════════
class TestShowFullColumns:
    """SHOW FULL COLUMNS headers:
    Field(0), Type(1), Collation(2), Null(3), Key(4), Default(5),
    Extra(6), Privileges(7), Comment(8)
    """

    def test_column_comment(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rows = conn.exec_driver_sql(
                "SHOW FULL COLUMNS FROM `pydoris_test`.`comment_test`"
            )
            comments = {r[0]: r[8] for r in rows}
            assert comments["k1"] == "primary id"
            assert comments["name"] == "user name"

    def test_full_columns_has_9_fields(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            res = conn.exec_driver_sql(
                "SHOW FULL COLUMNS FROM `pydoris_test`.`comment_test`"
            )
            desc = [d[0] for d in res.cursor.description]
            assert len(desc) == 9
            assert desc == ["Field", "Type", "Collation", "Null", "Key",
                            "Default", "Extra", "Privileges", "Comment"]


# ═══════════════════════════════════════════════════════════════════════════
# 4. SHOW FULL TABLES — table vs view filtering
# ═══════════════════════════════════════════════════════════════════════════
class TestShowFullTables:

    def _full_tables(self, conn):
        rows = conn.exec_driver_sql("SHOW FULL TABLES FROM `pydoris_test`")
        return {r[0]: r[1] for r in rows}

    def test_base_table_type(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            tables = self._full_tables(conn)
            assert tables["all_types"] == "BASE TABLE"

    def test_view_type(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            tables = self._full_tables(conn)
            assert tables["test_view"] == "VIEW"

    def test_filter_tables_excludes_views(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            tables = self._full_tables(conn)
            base_tables = [n for n, t in tables.items() if t == "BASE TABLE"]
            views = [n for n, t in tables.items() if t in ("VIEW", "SYSTEM VIEW")]
            assert "all_types" in base_tables
            assert "test_view" not in base_tables
            assert "test_view" in views
            assert "all_types" not in views


# ═══════════════════════════════════════════════════════════════════════════
# 5. Table comment via information_schema
# ═══════════════════════════════════════════════════════════════════════════
class TestTableComment:

    def test_table_comment(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.execute(text(
                "SELECT table_comment FROM information_schema.tables "
                "WHERE table_schema = :s AND table_name = :t"
            ), {"s": "pydoris_test", "t": "comment_test"})
            assert rs.scalar() == "table level comment"

    def test_no_comment_returns_empty(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.execute(text(
                "SELECT table_comment FROM information_schema.tables "
                "WHERE table_schema = :s AND table_name = :t"
            ), {"s": "pydoris_test", "t": "all_types"})
            val = rs.scalar()
            assert val == "" or val is None


# ═══════════════════════════════════════════════════════════════════════════
# 6. SHOW INDEX
# ═══════════════════════════════════════════════════════════════════════════
class TestShowIndex:
    """SHOW INDEX headers (13 cols):
    Table, Non_unique, Key_name, Seq_in_index, Column_name,
    Collation, Cardinality, Sub_part, Packed, Null, Index_type,
    Comment, Properties
    """

    def _indexes(self, conn, table):
        rs = conn.exec_driver_sql(
            f"SHOW INDEX FROM `pydoris_test`.`{table}`"
        )
        result = {}
        for row in rs:
            name = row[2]  # Key_name
            if name not in result:
                result[name] = {
                    "columns": [],
                    "index_type": row[10],
                    "properties": row[12] if len(row) > 12 else "",
                }
            result[name]["columns"].append(row[4])
        return result

    def test_inverted_index_exists(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            idxs = self._indexes(conn, "index_test")
            assert "idx_name" in idxs
            assert idxs["idx_name"]["index_type"] == "INVERTED"
            assert "name" in idxs["idx_name"]["columns"]

    def test_inverted_index_with_parser(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            idxs = self._indexes(conn, "index_test")
            assert "idx_bio" in idxs
            assert idxs["idx_bio"]["index_type"] == "INVERTED"
            assert "parser" in idxs["idx_bio"]["properties"]

    def test_index_has_13_columns(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.exec_driver_sql(
                "SHOW INDEX FROM `pydoris_test`.`index_test`"
            )
            desc = [d[0] for d in rs.cursor.description]
            assert len(desc) == 13
            assert "Index_type" in desc
            assert "Properties" in desc


# ═══════════════════════════════════════════════════════════════════════════
# 7. Data model tests (DUPLICATE / UNIQUE / AGGREGATE)
# ═══════════════════════════════════════════════════════════════════════════
class TestDataModels:

    def test_duplicate_key_in_show_create(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.execute(text("SHOW CREATE TABLE pydoris_test.all_types"))
            ddl = rs.fetchone()[1]
            assert "DUPLICATE KEY(`k1`)" in ddl

    def test_unique_key_in_show_create(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.execute(text("SHOW CREATE TABLE pydoris_test.unique_model"))
            ddl = rs.fetchone()[1]
            assert "UNIQUE KEY(`id`, `name`)" in ddl

    def test_aggregate_key_in_show_create(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.execute(text("SHOW CREATE TABLE pydoris_test.agg_model"))
            ddl = rs.fetchone()[1]
            assert "AGGREGATE KEY(`dt`, `user_id`)" in ddl

    def test_random_distribution_in_show_create(self, doris_engine, setup_tables):
        with doris_engine.connect() as conn:
            rs = conn.execute(text("SHOW CREATE TABLE pydoris_test.random_dist"))
            ddl = rs.fetchone()[1]
            assert "DISTRIBUTED BY RANDOM" in ddl


# ═══════════════════════════════════════════════════════════════════════════
# 8. DDL execution — round-trip create / insert / select / drop
# ═══════════════════════════════════════════════════════════════════════════
class TestDDLExecution:

    def test_create_insert_select_drop(self, doris_engine, setup_tables):
        tbl = "pydoris_test.ddl_roundtrip"
        with doris_engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {tbl}"))
            conn.execute(text(f"""
                CREATE TABLE {tbl} (
                    id INTEGER NOT NULL,
                    name VARCHAR(100),
                    score DOUBLE
                )
                ENGINE = OLAP
                DUPLICATE KEY(`id`)
                COMMENT 'roundtrip test'
                DISTRIBUTED BY HASH(`id`) BUCKETS 1
                PROPERTIES ("replication_num" = "1")
            """))
            conn.commit()

            conn.execute(text(f"INSERT INTO {tbl} VALUES (1, 'alice', 3.14)"))
            conn.commit()

            rs = conn.execute(text(f"SELECT * FROM {tbl}"))
            rows = rs.fetchall()
            assert len(rows) == 1
            assert rows[0][0] == 1
            assert rows[0][1] == "alice"

            # Verify comment
            rs = conn.execute(text(
                "SELECT table_comment FROM information_schema.tables "
                "WHERE table_schema='pydoris_test' AND table_name='ddl_roundtrip'"
            ))
            assert rs.scalar() == "roundtrip test"

            conn.execute(text(f"DROP TABLE {tbl}"))
            conn.commit()

    def test_partition_table(self, doris_engine, setup_tables):
        tbl = "pydoris_test.part_roundtrip"
        with doris_engine.connect() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS {tbl}"))
            conn.execute(text(f"""
                CREATE TABLE {tbl} (
                    dt DATE NOT NULL,
                    id INT NOT NULL,
                    val VARCHAR(100)
                )
                DUPLICATE KEY(dt, id)
                PARTITION BY RANGE(dt) (
                    PARTITION p202501 VALUES LESS THAN ('2025-02-01'),
                    PARTITION p202502 VALUES LESS THAN ('2025-03-01')
                )
                DISTRIBUTED BY HASH(id) BUCKETS 1
                PROPERTIES ("replication_num" = "1")
            """))
            conn.commit()

            rs = conn.execute(text(f"SHOW CREATE TABLE {tbl}"))
            ddl = rs.fetchone()[1]
            assert "PARTITION BY RANGE" in ddl

            conn.execute(text(f"DROP TABLE {tbl}"))
            conn.commit()


# ═══════════════════════════════════════════════════════════════════════════
# 9. TIME type — query-result only, not storable
# ═══════════════════════════════════════════════════════════════════════════
class TestTimeType:

    def test_timediff_returns_timedelta(self, doris_engine):
        with doris_engine.connect() as conn:
            rs = conn.execute(text(
                "SELECT TIMEDIFF('2025-01-01 12:00:00', '2025-01-01 10:30:00')"
            ))
            val = rs.scalar()
            assert isinstance(val, datetime.timedelta)
            assert val.total_seconds() == 5400

    def test_time_column_not_supported_for_olap(self, doris_engine):
        """Doris rejects TIME as a column type for OLAP tables."""
        with doris_engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS pydoris_test._time_fail"))
            with pytest.raises(Exception, match="(?i)time.*not supported"):
                conn.execute(text("""
                    CREATE TABLE pydoris_test._time_fail (k1 INT, t TIME)
                    DUPLICATE KEY(k1) DISTRIBUTED BY HASH(k1) BUCKETS 1
                    PROPERTIES ("replication_num" = "1")
                """))
