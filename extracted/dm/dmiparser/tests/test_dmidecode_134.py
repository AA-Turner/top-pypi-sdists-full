from tests.conftest import arches_with, load

TYPE = "134"
NAME = "OEM-specific Type"
COUNT = {"x86_64": 1}
KEYS = {"Header and Data"}


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


def test_header_and_data_multiline():
    """Header and Data spans multiple lines (each line a hex-byte value)."""
    for arch in arches_with(TYPE):
        data = load(arch, TYPE)
        hd = data[0]["props"]["Header and Data"]["values"]
        assert len(hd) >= 1
        assert all(v for v in hd)
