"""
Test parser
"""

import os
import pytest
from castepinput.parser import PlainParser, Parser
from castepinput.parser import Block

current_path = os.path.split(__file__)[0]

# pylint:disable=protected-access

lines_example = [
    "fix_all_cell:True",
    "kpoints_mp_grid=4 4 4 # Foo",
    "cut_off_Energy 300   #Bar",
    "xc_functional :  pbesol",
    "SYMMETRY_GENERATE",
    "fixed_occupancy : false",
]

expected_lines = [
    "fix_all_cell:True",
    "kpoints_mp_grid=4 4 4",
    "cut_off_Energy 300",
    "xc_functional :  pbesol",
    "SYMMETRY_GENERATE",
    "fixed_occupancy : false",
]

expected_comments = ["Foo", "Bar"]

block_lines = ["%BLOCK SPECIES_POT", "O C9", "%ENDBLOCK SPECIES_POT"]

expected_kw_dict = {
    "fix_all_cell": "True",
    "kpoints_mp_grid": "4 4 4",
    "cut_off_energy": "300",
    "xc_functional": "pbesol",
    "symmetry_generate": "",
    "fixed_occupancy": "false",
}

expected_block_dict = {"species_pot": Block(["O C9"])}


@pytest.fixture
def base_parser():
    return PlainParser(lines_example)


@pytest.fixture
def parser():
    return Parser(lines_example)


def test_base_clean_up(base_parser):
    """
    Test cleaning up of the lines
    """
    lines, comments = base_parser._clean_up_lines()
    assert lines == expected_lines
    assert comments == expected_comments


def test_base_blocks(base_parser):
    """
    Test parsing the blocks
    """
    base_parser._raw_lines += block_lines
    base_parser._clean_up_lines()
    blocks, kwlines = base_parser._split_block_kw()
    assert "species_pot" in blocks
    assert kwlines == expected_lines
    assert base_parser._blocks == expected_block_dict


def test_base_outputs(base_parser):
    """
    Test parsing keyword value pairs and final output
    """
    base_parser._raw_lines += block_lines
    base_parser.parse()
    assert base_parser._keywords == expected_kw_dict

    res_dict = expected_kw_dict.copy()
    res_dict.update(expected_block_dict)
    assert base_parser.get_dict() == res_dict


def test_cell_parser(parser):
    """Test the cell parser"""
    parser.parse()

    out_dict = parser.get_dict()
    assert out_dict["kpoints_mp_grid"] == [4, 4, 4]
    assert "Foo" in parser.comments
    assert out_dict["fixed_occupancy"] is False
    assert out_dict["fix_all_cell"] is True
    assert out_dict["cut_off_energy"] == 300
    assert out_dict["xc_functional"] == "pbesol"
    assert out_dict["symmetry_generate"] == ""
