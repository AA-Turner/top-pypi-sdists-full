from tests import DmiTest

TYPE = "42"
NAME = "Management Controller Host Interface"
COUNT = {"x86_64": 2}
KEYS = {"Device Type", "Host Interface Type", "Protocol ID", "idProduct", "idVendor"}


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
