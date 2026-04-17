"""
Test module for the inputs
"""
import os
import pytest
import numpy as np

from castepinput.inputs import CastepInput, CellInput
from castepinput.inputs import Block, parse_pos_line, construct_pos_line

current_path = os.path.split(__file__)[0]

# pylint: disable=invalid-name


@pytest.fixture
def basic_input():
    """Test the basics"""
    c = CastepInput()
    c["a"] = "a"
    c["b"] = Block(["a", "b"])
    c["c"] = 5
    c["d"] = [2, 2, 2]
    c["e"] = ""
    c["f"] = True
    c["g"] = False
    return c


@pytest.fixture
def cell_input():
    """Test using CellInput"""
    c = CellInput()
    c["symmetry_generate"] = True
    return c


def test_input_gen(basic_input):
    """
    Test basic function of generate inputs
    """

    def split_line(line):
        return [tmp.strip() for tmp in line.split(":")]

    lines = basic_input.get_file_lines()
    assert lines[0].split(":")[0].strip() == "a"
    assert lines[0].split(":")[1].strip() == "a"
    assert lines[1].startswith("%")
    assert lines[4].startswith("%")
    assert split_line(lines[5]) == ["c", "5"]
    assert split_line(lines[6]) == ["d", "2 2 2"]
    assert split_line(lines[7]) == ["e"]
    assert split_line(lines[8]) == ["f", "True"]
    assert split_line(lines[9]) == ["g", "False"]


def test_header(basic_input):
    """
    Test adding header
    """
    basic_input.header = ["Hello World"]
    lines = basic_input.get_file_lines()
    assert lines[0] == "# Hello World"

    basic_input.header = ["#Hello World"]
    lines = basic_input.get_file_lines()
    assert lines[0] == "#Hello World"


def test_unit(basic_input):
    """
    Test the unit system
    """
    basic_input.units["a"] = "eV"
    basic_input.units["b"] = "eV"
    lines = basic_input.get_file_lines()
    assert lines[0].split(":")[1].strip()[-2:] == "eV"
    assert lines[2].strip() == "eV"


def test_string(basic_input):
    lines = basic_input.get_file_lines()
    assert "\n".join(lines) + "\n" == basic_input.get_string()


def test_save(basic_input, tmpdir):
    outname = str(tmpdir.join("test.in"))
    basic_input.save(outname)
    os.remove(outname)


def test_save_read(basic_input, tmpdir):
    """Test saving and raeding"""
    outname = str(tmpdir.join("test.in"))
    basic_input.save(outname)
    input2 = CastepInput.from_file(outname)
    assert dict(input2) == dict(basic_input)

    # Test round trip with Plain mode
    input2 = CastepInput.from_file(outname, plain=True)
    input2.save(outname)
    input3 = CastepInput.from_file(outname, plain=True)
    assert input2 == input3
    # Check if all parsed values are string/Block
    assert all(isinstance(s, (str, Block)) for s in input3.values())

    # Test unit system
    basic_input.units["a"] = "eV"
    basic_input.save(outname)
    input3 = CastepInput.from_file(outname)
    assert input3["a"] == "a eV"


# Tests for CellInputs
def test_pos_lines():
    """
    Rest construction and presing of positions lines
    """

    line = "Ce 1.23 2.34 2.6 SPIN=1 LABEL=Ce1 MIX=(1 1)"
    elem, pos, tags = parse_pos_line(line)
    assert elem == "Ce"
    assert pos == [1.23, 2.34, 2.6]
    assert tags == "SPIN=1 LABEL=Ce1 MIX=(1 1)"
    lines = construct_pos_line(elem, pos, tags)
    r = parse_pos_line(lines)
    for a in zip(r, [elem, pos, tags]):
        assert a[0] == a[1]


def test_input_pos_lines(cell_input):
    """
    Rest construction and presing of positions lines
    """
    line = "Ce 1.23 2.34 2.6 SPIN=1 LABEL=Ce1 MIX=(1 1)"
    cell_input["positions_abs"] = Block([line] * 3)
    elem, pos, tags = cell_input.get_positions()
    assert elem == ["Ce"] * 3
    assert np.all(pos == np.array([[1.23, 2.34, 2.6]] * 3))
    assert tags == ["SPIN=1 LABEL=Ce1 MIX=(1 1)"] * 3
    cell_input.set_positions(elem, pos, tags)

    nelem, npos, ntags = cell_input.get_positions()
    assert nelem == elem
    assert np.all(npos == pos)
    assert ntags == tags


def visual_inspect(inp):
    print("\n\nSTART OF Visual inspection:")
    print(inp.get_string())
    print("\n\nEND OF Visual inspection")


def test_set_cell(cell_input):
    """
    Test set_cell method
    """

    # Both 3x3 or 3 array should be supported
    cin = [[1.0, 0, 0], [0, 1.5, 0], [0, 0, 1.0]]
    cell_input.set_cell(cin)
    assert np.all(cell_input.get_cell() == cin)
    visual_inspect(cell_input)

    cin = [3, 3, 3]
    cell_input.set_cell(cin)
    assert np.all(cell_input.get_cell() == np.diag(cin))

    with pytest.raises(ValueError):
        cell_input.set_cell([[0, 0, 0], [1, 1, 1]])

    with pytest.raises(ValueError):
        cell_input.set_cell([1, 2, 3, 4])


def test_set_pos(cell_input):
    """
    Test set_positions method
    """
    p = [[0, 0, 0], [1, 0, 0]]
    cell_input.set_positions(["O", "O"], p)
    r = cell_input.get_positions()
    assert r[0] == ["O", "O"]
    assert np.all(r[1] == p)
    visual_inspect(cell_input)


@pytest.mark.parametrize(
    "data, expected",
    [
        [1, {"pos": [[1, 1, 1], [2, 2, 2]], "cell": [[4, 0, 0], [0, 4, 0], [0, 0, 4]]}],
        [2, {"pos": [[0, 0, 0], [1, 1, 1]], "cell": [[2, 0, 0], [0, 2, 0], [0, 0, 2]]}],
    ],
)
def test_cell_and_pos(data, expected):
    """test reading cell lattice vectors and positions"""
    cin = CellInput.from_file(os.path.join(current_path, f"data/cell_example_{data}.cell"))
    assert cin.get_cell().tolist() == expected["cell"]
    assert cin.get_positions()[1].tolist() == expected["pos"]


def test_input_serialization():
    """Test serialization and deserialization of CellInput"""
    cin = CellInput.from_file(os.path.join(current_path, "data/cell_example_1.cell"))
    sdict = cin.as_dict()
    cin_2 = CellInput.from_dict(sdict)
    assert cin == cin_2
    assert cin.to_json() == cin_2.to_json()


def test_block_serialization():
    """Test serialization and deserialization of Block"""
    b = Block(["a", "b", "c"])
    b_new = Block.from_dict(b.as_dict())
    assert list(b) == list(b_new)


def test_block_assertion():
    """Test that Block rejects non-string items"""
    with pytest.raises(AssertionError):
        Block([1, 2, 3])


def test_unit_line_skipping(tmpdir):
    """Test that unit lines in lattice and position blocks are skipped"""
    cell_content = """\
%BLOCK LATTICE_CART
angs
4 0 0
0 4 0
0 0 4
%ENDBLOCK LATTICE_CART

%BLOCK POSITIONS_ABS
ang
O 1 1 1
Ce 2 2 2
%ENDBLOCK POSITIONS_ABS
"""
    fname = str(tmpdir.join("test.cell"))
    with open(fname, "w") as f:
        f.write(cell_content)
    cin = CellInput.from_file(fname)
    assert cin.get_cell().tolist() == [[4, 0, 0], [0, 4, 0], [0, 0, 4]]
    elems, pos, _ = cin.get_positions()
    assert elems == ["O", "Ce"]
    assert pos.tolist() == [[1, 1, 1], [2, 2, 2]]


def test_set_cell_clears_abc(cell_input):
    """Test that set_cell removes lattice_abc if present"""
    cell_input["lattice_abc"] = Block(["10 10 10 90 90 90"])
    cell_input.set_cell([[4, 0, 0], [0, 4, 0], [0, 0, 4]])
    assert "lattice_abc" not in cell_input
    assert "lattice_cart" in cell_input


def test_set_positions_clears_other(cell_input):
    """Test that set_positions removes the other type of positions block"""
    cell_input["positions_frac"] = Block(["O 0 0 0"])
    cell_input.set_positions(["Ce"], [[1, 1, 1]])
    assert "positions_frac" not in cell_input
    assert "positions_abs" in cell_input

    cell_input.set_positions(["O"], [[0, 0, 0]], frac=True)
    assert "positions_abs" not in cell_input
    assert "positions_frac" in cell_input


def test_serialization_preserves_header_and_units():
    """Test that header and units survive serialization round-trip"""
    cin = CellInput(cut_off_energy=300, header=["A comment"], units={"lattice_cart": "ang"})
    cin["lattice_cart"] = Block(["4 0 0", "0 4 0", "0 0 4"])
    sdict = cin.as_dict()
    cin_2 = CellInput.from_dict(sdict)
    assert cin_2.header == ["A comment"]
    assert cin_2.units == {"lattice_cart": "ang"}


def test_init_with_positional_dict():
    """Test that CastepInput accepts a positional dict for backward compat"""
    d = {"cut_off_energy": 300, "task": "singlepoint"}
    cin = CastepInput(d)
    assert cin["cut_off_energy"] == 300
    assert cin["task"] == "singlepoint"


def test_get_cell_from_abc(tmpdir):
    """Test get_cell using lattice_abc format"""
    cell_content = """\
%BLOCK LATTICE_ABC
4 4 4 90 90 90
%ENDBLOCK LATTICE_ABC

%BLOCK POSITIONS_FRAC
O 0.0 0.0 0.0
O 0.5 0.5 0.5
%ENDBLOCK POSITIONS_FRAC
"""
    fname = str(tmpdir.join("test.cell"))
    with open(fname, "w") as f:
        f.write(cell_content)
    cin = CellInput.from_file(fname)
    expected = [[4, 0, 0], [0, 4, 0], [0, 0, 4]]
    assert np.allclose(cin.get_cell(), expected)


def test_get_positions_frac(tmpdir):
    """Test get_positions with fractional positions converted to Cartesian"""
    cell_content = """\
%BLOCK LATTICE_CART
4 0 0
0 4 0
0 0 4
%ENDBLOCK LATTICE_CART

%BLOCK POSITIONS_FRAC
O 0.0 0.0 0.0
O 0.5 0.5 0.5
%ENDBLOCK POSITIONS_FRAC
"""
    fname = str(tmpdir.join("test.cell"))
    with open(fname, "w") as f:
        f.write(cell_content)
    cin = CellInput.from_file(fname)
    elems, pos, _ = cin.get_positions()
    assert elems == ["O", "O"]
    assert np.allclose(pos[0], [0, 0, 0])
    assert np.allclose(pos[1], [2, 2, 2])


def test_get_positions_no_positions(cell_input):
    """Test that get_positions raises when no positions are defined"""
    with pytest.raises(RuntimeError, match="No positions defined"):
        cell_input.get_positions()


def test_parse_pos_line_invalid():
    """Test that parse_pos_line raises on malformed input"""
    with pytest.raises(ValueError, match="Cannot understand line"):
        parse_pos_line("badline")


def test_write_lattice_cart_with_units():
    """Test that self.units adds unit lines to lattice_cart block output"""
    cin = CellInput()
    cin.units["lattice_cart"] = "ang"
    cin.set_cell([[4, 0, 0], [0, 4, 0], [0, 0, 4]])
    lines = cin.get_file_lines()
    # %BLOCK lattice_cart, then unit line, then 3 vector lines
    block_start = next(i for i, ln in enumerate(lines) if ln.startswith("%BLOCK"))
    assert lines[block_start + 1] == "ang"
    assert lines[block_start + 2].strip().split() == [
        "4.0000000000",
        "0.0000000000",
        "0.0000000000",
    ]


def test_write_positions_abs_with_units():
    """Test that self.units adds unit lines to positions_abs block output"""
    cin = CellInput()
    cin.units["positions_abs"] = "ang"
    cin.set_positions(["O", "Ce"], [[1, 1, 1], [2, 2, 2]])
    lines = cin.get_file_lines()
    block_start = next(i for i, ln in enumerate(lines) if ln.startswith("%BLOCK"))
    assert lines[block_start + 1] == "ang"


def test_read_lattice_abc_with_units(tmpdir):
    """Test reading lattice_abc block with a unit line"""
    cell_content = """\
%BLOCK LATTICE_ABC
ang
4 4 4
90 90 90
%ENDBLOCK LATTICE_ABC
"""
    fname = str(tmpdir.join("test.cell"))
    with open(fname, "w") as f:
        f.write(cell_content)
    cin = CellInput.from_file(fname)
    expected = [[4, 0, 0], [0, 4, 0], [0, 0, 4]]
    assert np.allclose(cin.get_cell(), expected)


def test_round_trip_lattice_cart_with_units(tmpdir):
    """Test round-trip of lattice_cart with units: read → write → read"""
    cell_content = """\
%BLOCK LATTICE_CART
ang
4 0 0
0 4 0
0 0 4
%ENDBLOCK LATTICE_CART

%BLOCK POSITIONS_ABS
O 1 1 1
Ce 2 2 2
%ENDBLOCK POSITIONS_ABS
"""
    fname = str(tmpdir.join("test.cell"))
    with open(fname, "w") as f:
        f.write(cell_content)
    cin = CellInput.from_file(fname)

    # Write back and read again
    fname2 = str(tmpdir.join("test2.cell"))
    cin.save(fname2)
    cin2 = CellInput.from_file(fname2)

    assert np.allclose(cin2.get_cell(), [[4, 0, 0], [0, 4, 0], [0, 0, 4]])
    elems, pos, _ = cin2.get_positions()
    assert elems == ["O", "Ce"]
    assert np.allclose(pos, [[1, 1, 1], [2, 2, 2]])


def test_round_trip_positions_with_units(tmpdir):
    """Test round-trip of positions_abs with units: read → write → read"""
    cell_content = """\
%BLOCK LATTICE_CART
4 0 0
0 4 0
0 0 4
%ENDBLOCK LATTICE_CART

%BLOCK POSITIONS_ABS
bohr
O 1 1 1
Ce 2 2 2
%ENDBLOCK POSITIONS_ABS
"""
    fname = str(tmpdir.join("test.cell"))
    with open(fname, "w") as f:
        f.write(cell_content)
    cin = CellInput.from_file(fname)

    fname2 = str(tmpdir.join("test2.cell"))
    cin.save(fname2)
    cin2 = CellInput.from_file(fname2)

    elems, pos, _ = cin2.get_positions()
    assert elems == ["O", "Ce"]
    assert np.allclose(pos, [[1, 1, 1], [2, 2, 2]])
