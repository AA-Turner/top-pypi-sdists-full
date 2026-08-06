from tests import DmiTest

TYPE = "16"
NAME = "Physical Memory Array"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1, "x86_64": 1}
KEYS = {
    "Error Correction Type",
    "Error Information Handle",
    "Location",
    "Maximum Capacity",
    "Number Of Devices",
    "Use",
}


def test_section_count():
    for arch in DmiTest.arches_with(TYPE):
        assert COUNT[arch] == len(DmiTest.load(arch, TYPE))


def test_section_name():
    for arch in DmiTest.arches_with(TYPE):
        assert all(NAME == d["name"] for d in DmiTest.load(arch, TYPE))


def test_handle_type():
    for arch in DmiTest.arches_with(TYPE):
        for d in DmiTest.load(arch, TYPE):
            assert TYPE == d["handle"]["type"]
            assert {"id", "type", "bytes"} == set(d["handle"].keys())


def test_props_within_keyset():
    for arch in DmiTest.arches_with(TYPE):
        for d in DmiTest.load(arch, TYPE):
            assert set(d["props"].keys()) <= KEYS
