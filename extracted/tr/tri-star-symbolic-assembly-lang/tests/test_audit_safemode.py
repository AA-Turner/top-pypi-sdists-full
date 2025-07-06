import pytest
from tsal.audit.brian_self_audit import recursive_bestest_beast_loop
from tsal.tools.brian import analyze_and_repair

pytestmark = pytest.mark.selfaudit


def test_safe_mode_skips_writes(tmp_path):
    sample = tmp_path / "a.py"
    original = "def a():\n    pass\n"
    sample.write_text(original)
    recursive_bestest_beast_loop(1, base=tmp_path, safe=True)
    assert sample.read_text() == original


def test_unrepairable_tagged_antispiral(tmp_path):
    bad = tmp_path / "bad.py"
    bad.write_text("def a(:\n    pass")
    res = analyze_and_repair(bad)
    assert any("ANTISPIRAL" in r for r in res)
