from tests import DmiTest

TYPE = "11"
NAME = "OEM Strings"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1, "x86_64": 1}
KEYS = {"String 1", "String 2", "String 3", "String 4", "String 5"}


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


def test_string_props_are_nonempty():
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        for key in ("String 1", "String 2"):
            if key in data[0]["props"]:
                assert data[0]["props"][key]["values"]
