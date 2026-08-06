from tests import DmiTest

TYPE = "13"
NAMES = {"BIOS Language Information", "Firmware Language Information"}
COUNT = {"sw_64": 1, "x86_64": 1}
KEYS = {"Currently Installed Language", "Installable Languages", "Language Description Format"}


def test_section_count():
    for arch in DmiTest.arches_with(TYPE):
        assert COUNT[arch] == len(DmiTest.load(arch, TYPE))


def test_section_name():
    for arch in DmiTest.arches_with(TYPE):
        assert all(d["name"] in NAMES for d in DmiTest.load(arch, TYPE))


def test_handle_type():
    for arch in DmiTest.arches_with(TYPE):
        for d in DmiTest.load(arch, TYPE):
            assert TYPE == d["handle"]["type"]
            assert {"id", "type", "bytes"} == set(d["handle"].keys())


def test_props_within_keyset():
    for arch in DmiTest.arches_with(TYPE):
        for d in DmiTest.load(arch, TYPE):
            assert set(d["props"].keys()) <= KEYS


def test_installable_languages_value_and_subitems():
    """'Installable Languages: 1' has value '1' AND sub-item(s) following."""
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        vals = data[0]["props"]["Installable Languages"]["values"]
        assert len(vals) >= 2


def test_currently_installed_language():
    for arch in DmiTest.arches_with(TYPE):
        data = DmiTest.load(arch, TYPE)
        assert data[0]["props"]["Currently Installed Language"]["values"]
