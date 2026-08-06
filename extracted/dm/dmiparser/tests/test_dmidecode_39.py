from tests import DmiTest

TYPE = "39"
NAME = "System Power Supply"
COUNT = {"loongarch64": 1}
KEYS = {
    "Asset Tag",
    "Hot Replaceable",
    "Input Voltage Range Switching",
    "Location",
    "Manufacturer",
    "Max Power Capacity",
    "Model Part Number",
    "Name",
    "Plugged",
    "Power Unit Group",
    "Revision",
    "Serial Number",
    "Status",
    "Type",
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


def test_status_value_contains_comma():
    """Status value contains a comma (e.g. 'Full, OK')."""
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        status = data[0]["props"]["Status"]["values"][0]
        assert "," in status
