from tests.conftest import arches_with, load

TYPE = "4"
NAME = "Processor Information"
COUNT = {"aarch64": 2, "loongarch64": 4, "sw_64": 2, "x86_64": 2}
KEYS = {
    "Asset Tag",
    "Characteristics",
    "Core Count",
    "Core Enabled",
    "Current Speed",
    "External Clock",
    "Family",
    "Flags",
    "ID",
    "L1 Cache Handle",
    "L2 Cache Handle",
    "L3 Cache Handle",
    "Manufacturer",
    "Max Speed",
    "Part Number",
    "Serial Number",
    "Signature",
    "Socket Designation",
    "Status",
    "Thread Count",
    "Type",
    "Upgrade",
    "Version",
    "Voltage",
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


def test_characteristics_empty_value_with_subitems():
    for arch in arches_with(TYPE):
        for d in load(arch, TYPE):
            if "Characteristics" in d["props"]:
                chars = d["props"]["Characteristics"]["values"]
                assert len(chars) > 0
