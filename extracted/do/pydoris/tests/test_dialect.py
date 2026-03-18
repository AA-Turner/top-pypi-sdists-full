"""Unit tests for DorisDialect properties — no Doris connection required."""
from pydoris.sqlalchemy.dialect import DorisDialect, DorisTypeCompiler, DorisDDLCompiler


class TestDialectAttributes:

    def test_name(self):
        assert DorisDialect.name == "pydoris"

    def test_supports_statement_cache(self):
        assert DorisDialect.supports_statement_cache is True

    def test_type_compiler(self):
        assert DorisDialect.type_compiler is DorisTypeCompiler

    def test_ddl_compiler(self):
        assert DorisDialect.ddl_compiler is DorisDDLCompiler

    def test_construct_arguments_defined(self):
        assert len(DorisDialect.construct_arguments) == 1
        table_cls, defaults = DorisDialect.construct_arguments[0]
        expected_keys = {"engine", "key_type", "key_columns",
                         "distributed_by", "buckets", "partition_by", "properties"}
        assert expected_keys == set(defaults.keys())

    def test_construct_arguments_all_default_none(self):
        _, defaults = DorisDialect.construct_arguments[0]
        for key, val in defaults.items():
            assert val is None, f"{key} should default to None"
