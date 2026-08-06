from tests import DmiTest

TYPE = "2"
NAME = "Base Board Information"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1, "x86_64": 1}
KEYS = {
    "Asset Tag",
    "Chassis Handle",
    "Contained Object Handles",
    "Features",
    "Location In Chassis",
    "Manufacturer",
    "Product Name",
    "Serial Number",
    "Type",
    "Version",
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


def test_features_empty_value_with_subitems():
    """'Features:' has an empty value followed by sub-items."""
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        feats = data[0]["props"]["Features"]["values"]
        assert len(feats) > 0
