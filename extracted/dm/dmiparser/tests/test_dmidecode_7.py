from tests.conftest import arches_with, load

TYPE = "7"
NAME = "Cache Information"
COUNT = {"aarch64": 4, "loongarch64": 12, "sw_64": 4, "x86_64": 6}
KEYS = {
    "Associativity",
    "Configuration",
    "Error Correction Type",
    "Installed SRAM Type",
    "Installed Size",
    "Location",
    "Maximum Size",
    "Operational Mode",
    "Socket Designation",
    "Speed",
    "Supported SRAM Types",
    "System Type",
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
