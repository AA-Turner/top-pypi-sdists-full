from tests.conftest import arches_with, load

TYPE = "1"
NAME = "System Information"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1, "x86_64": 1}
KEYS = {
    "Family",
    "Manufacturer",
    "Product Name",
    "SKU Number",
    "Serial Number",
    "UUID",
    "Version",
    "Wake-up Type",
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


def test_uuid_value_contains_dashes():
    """UUID value contains dashes (e.g. '62259285-0007-3ea1-d110-068975ca1c21')."""
    for arch in arches_with(TYPE):
        data = load(arch, TYPE)
        uuid = data[0]["props"]["UUID"]["values"][0]
        assert "-" in uuid
