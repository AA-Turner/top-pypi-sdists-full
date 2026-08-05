from tests.conftest import arches_with, load

TYPE = "17"
NAME = "Memory Device"
COUNT = {"aarch64": 32, "loongarch64": 16, "sw_64": 32, "x86_64": 32}
KEYS = {
    "Array Handle",
    "Asset Tag",
    "Bank Locator",
    "Cache Size",
    "Configured Memory Speed",
    "Configured Voltage",
    "Data Width",
    "Error Information Handle",
    "Firmware Version",
    "Form Factor",
    "Locator",
    "Logical Size",
    "Manufacturer",
    "Maximum Voltage",
    "Memory Operating Mode Capability",
    "Memory Subsystem Controller Manufacturer ID",
    "Memory Subsystem Controller Product ID",
    "Memory Technology",
    "Minimum Voltage",
    "Module Manufacturer ID",
    "Module Product ID",
    "Non-Volatile Size",
    "Part Number",
    "Rank",
    "Serial Number",
    "Set",
    "Size",
    "Speed",
    "Total Width",
    "Type",
    "Type Detail",
    "Volatile Size",
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
