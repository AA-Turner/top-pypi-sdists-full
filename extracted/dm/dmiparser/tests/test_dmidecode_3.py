from tests import DmiTest

TYPE = "3"
NAME = "Chassis Information"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1, "x86_64": 1}
KEYS = {
    "Asset Tag",
    "Boot-up State",
    "Contained Elements",
    "Height",
    "Lock",
    "Manufacturer",
    "Number Of Power Cords",
    "OEM Information",
    "Power Supply State",
    "SKU Number",
    "Security Status",
    "Serial Number",
    "Thermal State",
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


def test_contained_elements_empty_value_with_subitems():
    """'Contained Elements:' (when present) has an empty value followed by sub-items."""
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        ce = data[0]["props"].get("Contained Elements")
        if ce:
            assert len(ce["values"]) > 0
