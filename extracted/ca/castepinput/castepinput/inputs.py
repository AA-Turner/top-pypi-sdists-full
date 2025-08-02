"""
Classes for .param and .cell files
"""
import os
import tempfile
import re
from collections import OrderedDict

import numpy as np
from .parser import Parser, PlainParser
from .common import Block, cell_abcs_to_vec


class CastepInput(OrderedDict):
    """
    Class for storing key - values pairs of CASTEP inputs
    This class can be used for .param, .cell and also other CASTEP style
    inputs such as OptaDos's odi file

    ``self.get_file_lines`` is used for getting a list of strings as
    lines to be written to the file

    ``self.get_string`` is used for getting the content to be passed
    to ``write`` function of a file-like object

    sepecial properties:
    * ``header`` a list of lines to be put into the header
    * ``units`` a dictionary of the units
    """

    def __init__(self, *args, **kwargs):
        """Instantiate the object"""
        super().__init__(*args, **kwargs)
        self.header = []
        self.units = {}

    def get_file_lines(self):
        """
        Return a list of strings to be write out to the files
        """
        lines = []
        for hline in self.header:
            if not hline.startswith("#"):
                lines.append("# " + hline)
            else:
                lines.append(hline)

        for key, value in self.items():
            if isinstance(value, Block):
                lines.append(f"%BLOCK {key}")
                # Add units
                if key in self.units:
                    lines.append(str(self.units[key]))
                # Append each line
                for val in value:
                    lines.append(val)
                lines.append(f"%ENDBLOCK {key}\n")
            else:
                # If a list/tuple is passed join into a string
                if isinstance(value, (tuple, list)):
                    value = " ".join(map(str, value))
                # None and "" are treats as simple flag line e.g. SYMMETRY_GENERATE
                if value is not None and value != "":
                    this_line = f"{key:<20}: {value}"
                else:
                    this_line = key
                if key in self.units:
                    this_line = this_line + " " + self.units[key]
                lines.append(this_line)

        return lines

    def get_string(self):
        """Return the string representing the input file"""
        return "\n".join(self.get_file_lines()) + "\n"

    def save(self, fname):
        """Save the input as a file"""
        with open(fname, "w", encoding="utf-8") as fhandle:
            fhandle.write(self.get_string())

    @classmethod
    def from_file(cls, fname, plain=False):
        """
        Constrant an instance from the file
        """
        out = cls()
        out.load_file(fname, plain)
        return out

    def load_file(self, fname, plain=False):
        """
        Load from the file
        """
        with open(fname, encoding="utf-8") as fhandle:
            lines = fhandle.readlines()
        if plain:
            parser = PlainParser(lines)
        else:
            parser = Parser(lines)
        dict_out = parser.get_dict()
        for k, value in dict_out.items():
            self.__setitem__(k, value)

    def test_read_write(self, basic_input):
        """
        Adhoc test of readin and writing
        """
        outname = os.path.join(tempfile.mkdtemp(), "test.in")
        self.save(outname)
        input2 = type(self)()
        input2.load_file(outname)
        assert dict(input2) == dict(basic_input)


class ParamInput(CastepInput):
    pass


class CellInput(CastepInput):
    """
    Representation for the content in `<seed>.cell` file.
    """

    def get_cell(self):
        """Return cell vectors"""

        cell = []
        if "lattice_cart" in self:
            cell_lines = self["lattice_cart"]

            for line in cell_lines:
                cell.append([float(val) for val in line.split()])

        elif "lattice_abc" in self:
            abc_lines = self["lattice_abc"]

            abc = []
            for line in abc_lines:
                abc.extend([float(val) for val in line.split()])
            assert len(abc) == 6, "Problem in lattice_abc block"

            cell = cell_abcs_to_vec(abc)

        return np.asarray(cell)

    def get_positions(self):
        """
        Positions of ions

        :returns elements: A list of elements
        :returns pos: A list of list of floats of the positions
        :returns tags: A dictionary of tags e.g spin, mixture, label etc
        """
        is_frac = False
        pos_lines = self.get("positions_abs")
        if not pos_lines:
            pos_lines = self.get("positions_frac")
            is_frac = True
        if not pos_lines:
            raise RuntimeError("No positions defined")

        elems = []
        pos = []
        tags = []
        for line in pos_lines:
            elem, parser, tag = parse_pos_line(line)
            elems.append(elem)
            pos.append(parser)
            tags.append(tag)

        pos = np.array(pos)

        if is_frac:
            # We need to multiple the positions with cells
            cell = self.get_cell()
            pos = np.dot(pos, cell)

        return elems, pos, tags

    def set_cell(self, cell):
        """
        Set cell. Accept a length 3 list/array or 3x3 list/array.
        """
        cell_lines = Block()
        cell = np.asarray(cell)
        if cell.shape == (3,):
            cell = np.diag(cell)
        if cell.shape != (3, 3):
            raise ValueError(f"Cell must be a 3x3 matrix. But {cell} is given")

        for coord in cell:
            cell_lines.append(f"{coord[0]:.10f}  {coord[1]:.10f}  {coord[2]:.10f}")

        self["lattice_cart"] = Block(cell_lines)

    def set_positions(self, elements, positions, tags=None, frac=False):
        """
        Set positions
        """
        if frac:
            bname = "positions_frac"
        else:
            bname = "positions_abs"

        pos_lines = Block()
        if not tags:
            tags = [""] * len(elements)
        for elem, parser, tag in zip(elements, positions, tags):
            pos_lines.append(construct_pos_line(elem, parser, tag))

        self[bname] = Block(pos_lines)


def parse_pos_line(cell_line):
    """
    Parse single line in the cell block.
    Return element, coorindates and a dictionary of tags
    """

    cell_line = cell_line.strip()
    tokens = re.split(r"[\s]+", cell_line, maxsplit=4)
    if len(tokens) < 4:
        raise ValueError(f"Cannot understand line: {cell_line}")
    # There are trailing tags here
    if len(tokens) == 5:
        tags = tokens[-1]
    else:
        tags = ""

    elem = tokens[0].capitalize()
    coor = list(map(float, tokens[1:4]))

    return elem, coor, tags


def construct_pos_line(elem, coor, tags):
    """
    Do the opposite of the parse_pos_line
    """
    return f"{elem}  {coor[0]:.10f} {coor[1]:.10f} {coor[2]:.10f} {tags}"
