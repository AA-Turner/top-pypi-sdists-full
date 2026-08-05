from tests.conftest import arches_with, load

TYPE = "19"
NAME = "Memory Array Mapped Address"
COUNT = {"aarch64": 39, "loongarch64": 1, "sw_64": 1, "x86_64": 5}
KEYS = {
    "Ending Address",
    "Partition Width",
    "Physical Array Handle",
    "Range Size",
    "Starting Address",
}


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


def test_props_within_keyset():
    for arch in arches_with(TYPE):
        for d in load(arch, TYPE):
            assert set(d["props"].keys()) <= KEYS
