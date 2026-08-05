import json

import pytest

from tests.conftest import arches_with, load
from dmiparser.dmidecoder.dmidecoder import DmiDecoder

TYPE = "9"
NAME = "System Slot Information"
COUNT = {"aarch64": 7, "loongarch64": 6, "x86_64": 18}
KEYS = {
    "Bus Address",
    "Characteristics",
    "Current Usage",
    "Data Bus Width",
    "Data Bus Width (Base)",
    "Designation",
    "Height",
    "ID",
    "Length",
    "Peer Devices",
    "Slot Physical Width",
    "Type",
}


def _decoder(arch):
    """Build a DmiDecoder from type 9 text (no dmidecode binary needed)."""
    data = load(arch, TYPE)
    d = DmiDecoder.__new__(DmiDecoder)
    d._data = data
    d._text = json.dumps(data)
    return d


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


def test_bus_address_value_contains_colon():
    """Bus Address value is split on first ':' only (e.g. '0000:00:03.2')."""
    for arch in arches_with(TYPE):
        data = load(arch, TYPE)
        for d in data:
            bus = d["props"].get("Bus Address")
            if bus:
                assert ":" in bus["values"][0]


def test_characteristics_empty_value_with_subitems():
    for arch in arches_with(TYPE):
        data = load(arch, TYPE)
        chars = data[0]["props"]["Characteristics"]["values"]
        assert len(chars) > 0


def test_decoder_sections():
    for arch in arches_with(TYPE):
        d = _decoder(arch)
        assert COUNT[arch] == len(d.sections)
        assert all(n == NAME for _, n in d.sections)


def test_decoder_get_by_name():
    for arch in arches_with(TYPE):
        d = _decoder(arch)
        designations = d.get("props", "Designation", "values", name=NAME)
        assert len(designations) == COUNT[arch]


def test_decoder_get_missing_key_returns_empty():
    for arch in arches_with(TYPE):
        d = _decoder(arch)
        assert [] == d.get("props", "DoesNotExist", "values")


def test_decoder_get_no_keys_raises_typeerror():
    for arch in arches_with(TYPE):
        d = _decoder(arch)
        with pytest.raises(TypeError):
            d.get()


def test_decoder_text_and_data_consistent():
    for arch in arches_with(TYPE):
        d = _decoder(arch)
        assert d.data == json.loads(d.text)
        assert COUNT[arch] == len(d.data)
