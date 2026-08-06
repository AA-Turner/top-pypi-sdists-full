from tests import DmiTest

TYPE = "45"
NAME = "Firmware Inventory Information"
COUNT = {"x86_64": 1}
KEYS = {
    "Associated Components",
    "Characteristics",
    "Firmware Component Name",
    "Firmware ID",
    "Firmware Version",
    "Image Size",
    "Lowest Supported Firmware Version",
    "Manufacturer",
    "Release Date",
    "State",
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


def test_characteristics_empty_value_with_subitems():
    """'Characteristics:' has an empty value followed by sub-items."""
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        chars = data[0]["props"]["Characteristics"]["values"]
        assert len(chars) > 0
