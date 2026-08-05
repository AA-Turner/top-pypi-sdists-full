from tests.conftest import arches_with, load

TYPE = "28"
NAME = "Temperature Probe"
COUNT = {"loongarch64": 1}
KEYS = {
    "Accuracy",
    "Description",
    "Location",
    "Maximum Value",
    "Minimum Value",
    "Nominal Value",
    "OEM-specific Information",
    "Resolution",
    "Status",
    "Tolerance",
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
