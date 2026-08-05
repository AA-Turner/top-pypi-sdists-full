import json

import pytest

from dmiparser import DmiParser
from tests.conftest import ARCHES, load

FULL_COUNT = {"aarch64": 92, "loongarch64": 56, "sw_64": 59, "x86_64": 88}


def test_full_section_counts():
    for arch in ARCHES:
        assert FULL_COUNT[arch] == len(load(arch, "full"))


def test_every_section_has_valid_structure():
    for arch in ARCHES:
        for sect in load(arch, "full"):
            assert {"handle", "name", "props"} == set(sect.keys())
            assert {"id", "type", "bytes"} == set(sect["handle"].keys())


def test_empty_props_sections():
    """Each arch full dump has exactly one empty-props section: End Of Table."""
    for arch in ARCHES:
        data = load(arch, "full")
        empty = [d for d in data if not d["props"]]
        assert 1 == len(empty)
        assert "End Of Table" == empty[0]["name"]


def test_last_section_is_end_of_table():
    for arch in ARCHES:
        data = load(arch, "full")
        assert "End Of Table" == data[-1]["name"]
        assert "127" == data[-1]["handle"]["type"]


def test_indent_lv_counts_only_leading_tabs():
    assert 0 == DmiParser._indent_lv("")
    assert 0 == DmiParser._indent_lv("no tab")
    assert 1 == DmiParser._indent_lv("\tfoo")
    assert 2 == DmiParser._indent_lv("\t\tfoo")
    # spaces are not tabs
    assert 0 == DmiParser._indent_lv("    foo")
    # stops at the first non-tab character
    assert 1 == DmiParser._indent_lv("\t \tfoo")


def test_typeerror_on_non_str():
    for bad in (123, b"bytes", None, 1.5, ["list"]):
        with pytest.raises(TypeError):
            DmiParser(bad)


def test_valueerror_malformed_handle_line():
    """A line starting 'Handle' and ending 'bytes' that doesn't match the regex raises."""
    with pytest.raises(ValueError):
        DmiParser("Handle 0x0001 bytes\n")


def test_valueerror_property_line_without_colon():
    """A property line (indented) with no ':' in GET_PROP state raises."""
    with pytest.raises(ValueError):
        DmiParser("Handle 0x0001, DMI type 1, 27 bytes\n" "System Information\n" "\tNoColonHere\n")


def test_empty_input_yields_empty_list():
    assert [] == json.loads(str(DmiParser("")))


def test_header_only_no_handles_yields_empty_list():
    assert [] == json.loads(str(DmiParser("# dmidecode 3.0\nSMBIOS 2.7 present.\n")))


def test_no_trailing_newline_flushes_last_section():
    text = "Handle 0x0001, DMI type 1, 27 bytes\n" "System Information\n" "\tManufacturer: Foo"
    data = json.loads(str(DmiParser(text)))
    assert 1 == len(data)
    assert ["Foo"] == data[0]["props"]["Manufacturer"]["values"]


def test_kwargs_pass_through_to_json_dumps():
    text = "Handle 0x0001, DMI type 1, 27 bytes\nSystem Information\n\tStatus: OK\n"
    out = str(DmiParser(text, sort_keys=True, indent=2))
    assert "\n" in out
    assert ["OK"] == json.loads(out)[0]["props"]["Status"]["values"]


def test_one_handle_many_sections():
    """One Handle yields multiple sections sharing the handle (type 10 style).

    No new arch data exercises one-handle-to-many-sections; this inline snippet
    preserves coverage of that parser boundary condition.
    """
    text = (
        "Handle 0x005F, DMI type 10, 20 bytes\n"
        "On Board Device 1 Information\n"
        "\tType: Video\n"
        "\tStatus: Enabled\n"
        "\tDescription: ServerEngines Pilot III\n"
        "On Board Device 2 Information\n"
        "\tType: Ethernet\n"
        "\tStatus: Enabled\n"
        "\tDescription: Intel I350\n"
    )
    data = json.loads(str(DmiParser(text)))
    assert 2 == len(data)
    assert ["On Board Device 1 Information", "On Board Device 2 Information"] == [d["name"] for d in data]
    assert all("0x005F" == d["handle"]["id"] for d in data)
    assert all("10" == d["handle"]["type"] for d in data)


def test_subitem_leading_space_stripped():
    """Sub-items with a leading space are stripped (' 1.80.10802' -> '1.80.10802').

    No new arch data exercises leading-space stripping of sub-items; this inline
    snippet preserves coverage of that parser boundary condition.
    """
    text = (
        "Handle 0x0066, DMI type 148, 48 bytes\n"
        "OEM-specific Type\n"
        "\tStrings:\n"
        "\t\tSE5C610.86B.01.01.0022.062820171903\n"
        "\t\t 1.80.10802\n"
        "\t\t3.1.3.43\n"
    )
    data = json.loads(str(DmiParser(text)))
    strings = data[0]["props"]["Strings"]["values"]
    assert "1.80.10802" in strings
    assert " 1.80.10802" not in strings
