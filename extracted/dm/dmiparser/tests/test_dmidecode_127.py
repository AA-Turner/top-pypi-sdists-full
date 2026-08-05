from tests.conftest import arches_with, load

TYPE = "127"
NAME = "End Of Table"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1, "x86_64": 1}


def test_section_count():
    for arch in arches_with(TYPE):
        assert COUNT[arch] == len(load(arch, TYPE))


def test_section_name():
    for arch in arches_with(TYPE):
        assert all(NAME == d["name"] for d in load(arch, TYPE))


def test_handle_type():
    for arch in arches_with(TYPE):
        for d in load(arch, TYPE):
            assert TYPE == d["handle"]["type"]
            assert {"id", "type", "bytes"} == set(d["handle"].keys())


def test_empty_props():
    """End Of Table has no props (boundary: empty-props section)."""
    for arch in arches_with(TYPE):
        for d in load(arch, TYPE):
            assert {} == d["props"]
