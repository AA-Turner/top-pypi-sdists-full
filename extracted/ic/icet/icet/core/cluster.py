"""
This module provides the Cluster class.
"""

from _icet import Cluster

__all__ = ['Cluster']


def __str__(self) -> str:
    """ String representation. """

    def right_align(s: str, width: int) -> str:
        """ Right-aligns a string in a field that is widened if it does not fit. """
        return ' ' * max(0, width - len(s)) + s

    # Width of the frame drawn around the table.
    table_width = 77

    padding = '=' * ((table_width - len(' Cluster ')) // 2)

    # General information
    s = [f'{padding} Cluster {padding}']
    s += [f' Order:      {self.order}']
    s += [f' Radius:     {self.radius:g}']
    if self.order > 1:
        s += [' Distances:' + ''.join(f'  {d:g}' for d in self.distances)]

    # Lattice sites
    s += ['-' * table_width]
    s += [' Unitcell index |   Unitcell offset   |    Position']
    s += ['-' * table_width]
    for site, position in zip(self.lattice_sites, self.positions):
        offset = ''.join(f' {right_align(str(x), 5)}' for x in site.unitcell_offset)
        coordinates = ''.join(f' {right_align(f"{x:.6f}", 11)}' for x in position)
        s += [f'{right_align(str(site.index), 14)}  |'
              f'{right_align(offset, 19)}  |'
              f'{right_align(coordinates, 36)}']

    s += ['=' * table_width]
    return '\n'.join(s)


def __repr__(self) -> str:
    """ Representation. """
    s = type(self).__name__ + '('
    s += f'order={self.order}'
    s += f', radius={self.radius:.4f}'
    s += f', sites={[site.index for site in self.lattice_sites]}'
    s += ')'
    return s


Cluster.__str__ = __str__
Cluster.__repr__ = __repr__
