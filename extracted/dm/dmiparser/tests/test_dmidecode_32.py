from tests.conftest import arches_with, load

TYPE = "32"
NAME = "System Boot Information"
COUNT = {"aarch64": 1, "loongarch64": 1, "sw_64": 1}
KEYS = {"Status"}


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


def test_property_structure_is_values_list():
    """Property value is always wrapped in {'values': [...]} structure."""
    for arch in arches_with(TYPE):
        data = load(arch, TYPE)
        assert isinstance(data[0]["props"]["Status"]["values"], list)
        assert len(data[0]["props"]["Status"]["values"]) >= 1
