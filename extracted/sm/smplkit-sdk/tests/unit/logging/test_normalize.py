"""Tests for logger name normalization."""

from smplkit.logging._normalize import normalize_logger_name


class TestNormalizeLoggerName:
    def test_slash_replaced_with_dot(self):
        assert normalize_logger_name("a/b/c") == "a.b.c"

    def test_colon_replaced_with_dot(self):
        assert normalize_logger_name("a:b:c") == "a.b.c"

    def test_lowercased(self):
        assert normalize_logger_name("ABC") == "abc"

    def test_combined(self):
        assert normalize_logger_name("ABC/Def:Ghi") == "abc.def.ghi"

    def test_already_normalized(self):
        assert normalize_logger_name("com.example.sql") == "com.example.sql"

    def test_mixed_separators(self):
        assert normalize_logger_name("APP/Module:Sub.Name") == "app.module.sub.name"

    def test_empty_string(self):
        assert normalize_logger_name("") == ""

    def test_single_name(self):
        assert normalize_logger_name("ROOT") == "root"
