"""Tests for fray.stats — payload database statistics."""

import json
import os
import tempfile
from pathlib import Path

import pytest

from fray.stats import (
    CategoryStats,
    PayloadStats,
    _count_json_payloads,
    _count_txt_payloads,
    collect_stats,
)


# ── Fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def payload_tree(tmp_path):
    """Create a realistic payload directory tree for testing."""
    # xss/ — 2 JSON files + 1 TXT
    xss = tmp_path / "xss"
    xss.mkdir()
    (xss / "basic.json").write_text(json.dumps({
        "payloads": [
            {"id": 1, "payload": "<script>alert(1)</script>"},
            {"id": 2, "payload": "<img src=x onerror=alert(1)>"},
            {"id": 3, "payload": "<svg/onload=alert(1)>"},
        ]
    }))
    (xss / "advanced.json").write_text(json.dumps([
        {"payload": "<details open ontoggle=alert(1)>"},
        {"payload": "<body onpageshow=alert(1)>"},
    ]))
    (xss / "xss_basic.txt").write_text(
        "<script>alert(1)</script>\n"
        "<img src=x onerror=alert(1)>\n"
        "# comment line\n"
        "\n"
        "<svg onload=alert(1)>\n"
    )

    # sqli/ — 1 JSON file
    sqli = tmp_path / "sqli"
    sqli.mkdir()
    (sqli / "general.json").write_text(json.dumps({
        "payloads": [
            {"id": 1, "payload": "' OR 1=1--"},
            {"id": 2, "payload": "1 UNION SELECT NULL--"},
        ]
    }))

    # empty/ — directory with no payload files
    empty = tmp_path / "empty_cat"
    empty.mkdir()

    # hidden/ — should be skipped
    hidden = tmp_path / ".hidden"
    hidden.mkdir()
    (hidden / "secret.json").write_text(json.dumps({"payloads": [{"id": 1}]}))

    return tmp_path


# ── _count_json_payloads ─────────────────────────────────────────────────

class TestCountJsonPayloads:
    def test_dict_with_payloads_key(self, tmp_path):
        fp = tmp_path / "test.json"
        fp.write_text(json.dumps({"payloads": [1, 2, 3]}))
        assert _count_json_payloads(fp) == 3

    def test_list_format(self, tmp_path):
        fp = tmp_path / "test.json"
        fp.write_text(json.dumps([{"a": 1}, {"b": 2}]))
        assert _count_json_payloads(fp) == 2

    def test_empty_list(self, tmp_path):
        fp = tmp_path / "test.json"
        fp.write_text(json.dumps([]))
        assert _count_json_payloads(fp) == 0

    def test_empty_dict(self, tmp_path):
        fp = tmp_path / "test.json"
        fp.write_text(json.dumps({}))
        assert _count_json_payloads(fp) == 0

    def test_corrupt_json(self, tmp_path):
        fp = tmp_path / "bad.json"
        fp.write_text("{broken json!!")
        assert _count_json_payloads(fp) == 0

    def test_missing_file(self, tmp_path):
        fp = tmp_path / "nonexistent.json"
        assert _count_json_payloads(fp) == 0


# ── _count_txt_payloads ──────────────────────────────────────────────────

class TestCountTxtPayloads:
    def test_basic(self, tmp_path):
        fp = tmp_path / "test.txt"
        fp.write_text("payload1\npayload2\npayload3\n")
        assert _count_txt_payloads(fp) == 3

    def test_skip_blanks_and_comments(self, tmp_path):
        fp = tmp_path / "test.txt"
        fp.write_text("payload1\n\n# comment\n  \npayload2\n")
        assert _count_txt_payloads(fp) == 2

    def test_empty_file(self, tmp_path):
        fp = tmp_path / "empty.txt"
        fp.write_text("")
        assert _count_txt_payloads(fp) == 0

    def test_missing_file(self, tmp_path):
        fp = tmp_path / "nonexistent.txt"
        assert _count_txt_payloads(fp) == 0


# ── CategoryStats ────────────────────────────────────────────────────────

class TestCategoryStats:
    def test_total(self):
        cs = CategoryStats(name="xss", json_payloads=100, txt_payloads=50)
        assert cs.total == 150

    def test_files(self):
        cs = CategoryStats(name="xss", json_files=3, txt_files=2)
        assert cs.files == 5

    def test_defaults(self):
        cs = CategoryStats(name="empty")
        assert cs.total == 0
        assert cs.files == 0
        assert cs.subcategories == []


# ── PayloadStats ─────────────────────────────────────────────────────────

class TestPayloadStats:
    def test_totals(self):
        ps = PayloadStats(categories=[
            CategoryStats(name="xss", json_payloads=100, txt_payloads=50, json_files=2, txt_files=1),
            CategoryStats(name="sqli", json_payloads=80, json_files=1),
        ])
        assert ps.total_payloads == 230
        assert ps.total_files == 4
        assert ps.total_categories == 2

    def test_empty(self):
        ps = PayloadStats()
        assert ps.total_payloads == 0
        assert ps.total_files == 0
        assert ps.total_categories == 0

    def test_to_dict(self):
        ps = PayloadStats(
            payloads_dir="/test",
            categories=[
                CategoryStats(name="xss", json_payloads=10, txt_payloads=5,
                              json_files=1, txt_files=1, subcategories=["basic"]),
            ],
        )
        d = ps.to_dict()
        assert d["total_payloads"] == 15
        assert d["total_files"] == 2
        assert d["total_categories"] == 1
        assert d["categories"][0]["name"] == "xss"
        assert d["categories"][0]["total"] == 15
        assert d["categories"][0]["subcategories"] == ["basic"]


# ── collect_stats ────────────────────────────────────────────────────────

class TestCollectStats:
    def test_basic(self, payload_tree):
        stats = collect_stats(payload_tree)
        assert stats.total_categories == 2  # xss + sqli (empty_cat excluded)
        assert stats.total_payloads == 10   # 3+2+3 xss + 2 sqli
        assert stats.total_files == 4       # 2 json + 1 txt (xss) + 1 json (sqli)

    def test_sorted_descending(self, payload_tree):
        stats = collect_stats(payload_tree)
        assert stats.categories[0].name == "xss"  # 8 > 2
        assert stats.categories[1].name == "sqli"

    def test_xss_breakdown(self, payload_tree):
        stats = collect_stats(payload_tree)
        xss = stats.categories[0]
        assert xss.json_payloads == 5   # 3 + 2
        assert xss.txt_payloads == 3    # 3 non-blank, non-comment lines
        assert xss.json_files == 2
        assert xss.txt_files == 1

    def test_hidden_dirs_skipped(self, payload_tree):
        stats = collect_stats(payload_tree)
        names = [c.name for c in stats.categories]
        assert ".hidden" not in names

    def test_empty_category_excluded(self, payload_tree):
        stats = collect_stats(payload_tree)
        names = [c.name for c in stats.categories]
        assert "empty_cat" not in names

    def test_nonexistent_dir(self, tmp_path):
        stats = collect_stats(tmp_path / "nope")
        assert stats.total_payloads == 0
        assert stats.total_categories == 0

    def test_to_dict_roundtrip(self, payload_tree):
        stats = collect_stats(payload_tree)
        d = stats.to_dict()
        assert isinstance(d, dict)
        assert d["total_payloads"] == stats.total_payloads
        assert len(d["categories"]) == stats.total_categories


# ── print_stats (smoke test) ─────────────────────────────────────────────

class TestPrintStats:
    def test_smoke(self, payload_tree, capsys):
        stats = collect_stats(payload_tree)
        from fray.stats import print_stats
        print_stats(stats)
        # Just verify it doesn't crash and produces output
        captured = capsys.readouterr()
        # Rich writes to its own console, so check it ran without error

    def test_empty(self, capsys):
        stats = PayloadStats()
        from fray.stats import print_stats
        print_stats(stats)
