"""A captured image is stored under the name its caller gives it, never "master.png" (2026-10-08)."""

from matrx_ai.tools.image_outputs import _master_stem


def test_caller_name_becomes_the_stem():
    assert _master_stem("Binary cards screenshot.png", "png") == "Binary cards screenshot"


def test_no_name_keeps_master():
    assert _master_stem(None, "png") == "master"
    assert _master_stem("   ", "png") == "master"


def test_a_name_never_becomes_a_path():
    assert "/" not in _master_stem("../../etc/passwd", "png")
    assert "/" not in _master_stem("a/b/c.png", "png")
    assert _master_stem('we"ird|<name>?.png', "png") == "weirdname"
