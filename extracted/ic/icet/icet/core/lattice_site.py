"""
This module provides a Python interface to the LatticeSite class.
"""

from _icet import LatticeSite


def __latticeSite_str(self):
    return '{} : {}'.format(self.index, self.unitcell_offset)


LatticeSite.__str__ = __latticeSite_str
