"""
The ``io.shengBTE`` module provides functions for reading and writing data
files in shengBTE format.
"""

import numpy as np
from itertools import product
from collections import namedtuple
from ..core.structures import Supercell
import hiphive


def read_shengBTE_fc3(filename, prim, supercell, symprec=1e-5):
    """Reads third-order force constants file in shengBTE format.

    Parameters
    ----------
    filename : str
        input file name
    prim : ase.Atoms
        primitive cell for the force constants
    supercell : ase.Atoms
        supercell onto which to map force constants
    symprec : float
        structural symmetry tolerance

    Returns
    -------
    fcs : ForceConstants
        third order force constants for the specified supercell
    """

    raw_sheng = _read_raw_sheng(filename)

    sheng = _raw_to_fancy(raw_sheng, prim.cell)

    fcs = _sheng_to_fcs(sheng, prim, supercell, symprec)

    return fcs


def write_shengBTE_fc3(filename, fcs, prim, symprec=1e-5, cutoff=np.inf,
                       fc_tol=1e-8):
    """Writes third-order force constants file in shengBTE format.

    Parameters
    -----------
    filename : str
        input file name
    fcs : ForceConstants
        force constants; the supercell associated with this object must be
        based on prim
    prim : ase.Atoms
        primitive configuration (must be equivalent to structure used in the
        shengBTE calculation)
    symprec : float
        structural symmetry tolerance
    cutoff : float
        all atoms in cluster must be within this cutoff
    fc_tol : float
        if the absolute value of the largest entry in a force constant is less
        than fc_tol it will not be written
    """

    sheng = _fcs_to_sheng(fcs, prim, symprec, cutoff, fc_tol)

    raw_sheng = _fancy_to_raw(sheng)

    _write_raw_sheng(raw_sheng, filename)


def _read_raw_sheng(filename):
    """ Read shengBTE fc3 file.

    Parameters
    ----------
    filename : str
        input file name

    Returns
    -------
    list
        list with shengBTE block entries, where an entry consist of
        [i, j, k, cell_pos2, cell_pos3, fc3]
    """
    lines_per_fc_block = 32

    fc3_data_shengBTE = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        num_fcs = int(lines[0])
        lind = 2
        for i in range(1, num_fcs+1):
            # sanity check
            assert int(lines[lind]) == i, (int(lines[lind]), i)

            # read cell poses
            cell_pos2 = np.array([float(fld) for fld in lines[lind+1].split()])
            cell_pos3 = np.array([float(fld) for fld in lines[lind+2].split()])

            # read basis indices
            i, j, k = (int(fld) for fld in lines[lind+3].split())

            # read fc
            fc3_ijk = np.zeros((3, 3, 3))
            for n in range(27):
                x, y, z = [int(fld) - 1 for fld in lines[lind+4+n].split()[:3]]
                fc3_ijk[x, y, z] = float(lines[lind+4+n].split()[-1])

            # append entry
            entry = [i, j, k, cell_pos2, cell_pos3, fc3_ijk]
            fc3_data_shengBTE.append(entry)
            lind += lines_per_fc_block

    return fc3_data_shengBTE


_ShengEntry = namedtuple('Entry', ['site_0', 'site_1', 'site_2', 'pos_1',
                                   'pos_2', 'fc', 'offset_1', 'offset_2'])


def _raw_to_fancy(raw_sheng, cell):
    """
    Converts force constants as read from shengBTE file to the namedtuple
    format defined above (_ShengEntry).
    """
    sheng = []
    for raw_entry in raw_sheng:
        p1, p2 = raw_entry[3:5]
        offset_1 = np.linalg.solve(cell.T, p1).round(0).astype(int)
        offset_2 = np.linalg.solve(cell.T, p2).round(0).astype(int)
        entry = _ShengEntry(*(i - 1 for i in raw_entry[:3]), *raw_entry[3:],
                            offset_1, offset_2)
        sheng.append(entry)
    return sheng


def _fancy_to_raw(sheng):
    """
    Converts force constants namedtuple format defined above (_ShengEntry) to
    format used for writing shengBTE files.
    """
    raw_sheng = []
    for entry in sheng:
        raw_entry = list(entry[:6])
        raw_entry[0] += 1
        raw_entry[1] += 1
        raw_entry[2] += 1
        raw_sheng.append(raw_entry)

    return raw_sheng


def _write_raw_sheng(raw_sheng, filename):
    """ See corresponding read function. """

    with open(filename, 'w') as f:
        f.write('{}\n\n'.format(len(raw_sheng)))

        for index, fc3_row in enumerate(raw_sheng, start=1):
            i, j, k, cell_pos2, cell_pos3, fc3_ijk = fc3_row

            f.write('{:5d}\n'.format(index))

            f.write((3*'{:14.10f} '+'\n').format(*cell_pos2))
            f.write((3*'{:14.10f} '+'\n').format(*cell_pos3))
            f.write((3*'{:5d}'+'\n').format(i, j, k))

            for x, y, z in product(range(3), repeat=3):
                f.write((3*' {:}').format(x+1, y+1, z+1))
                f.write('    {:14.10f}\n'.format(fc3_ijk[x, y, z]))
            f.write('\n')


def _fcs_to_sheng(fcs, prim, symprec, cutoff, fc_tol):
    """ Produces a list containing fcs in shengBTE format

    prim and fcs.supercell must be aligned.
    """

    supercell = Supercell(fcs.supercell, prim, symprec)
    assert all(fcs.supercell.pbc) and all(prim.pbc)

    n_atoms = len(supercell)

    D = fcs.supercell.get_all_distances(mic=False, vector=True)
    D_mic = fcs.supercell.get_all_distances(mic=True, vector=True)
    M = np.eye(n_atoms, dtype=bool)
    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            M[i, j] = (np.allclose(D[i, j], D_mic[i, j], atol=symprec, rtol=0)
                       and np.linalg.norm(D[i, j]) < cutoff)
            M[j, i] = M[i, j]

    data = {}
    for a0 in supercell:
        for a1 in supercell:
            if not M[a0.index, a1.index]:
                continue
            for a2 in supercell:
                if not (M[a0.index, a2.index] and M[a1.index, a2.index]):
                    continue

                offset_1 = np.subtract(a1.offset, a0.offset)
                offset_2 = np.subtract(a2.offset, a0.offset)

                sites = (a0.site, a1.site, a2.site)

                key = sites + tuple(offset_1) + tuple(offset_2)

                ijk = (a0.index, a1.index, a2.index)

                fc = fcs[ijk]

                if key in data:
                    assert np.allclose(data[key], fc, atol=fc_tol)
                else:
                    data[key] = fc

    sheng = []
    for k, fc in data.items():
        if np.max(np.abs(fc)) < fc_tol:
            continue
        offset_1 = k[3:6]
        pos_1 = np.dot(offset_1, prim.cell)
        offset_2 = k[6:9]
        pos_2 = np.dot(offset_2, prim.cell)
        entry = _ShengEntry(*k[:3], pos_1, pos_2, fc, offset_1, offset_2)
        sheng.append(entry)

    return sheng


def _sheng_to_fcs(sheng, prim, supercell, symprec):
    supercell_map = Supercell(supercell, prim, symprec)
    fc_array = np.zeros((len(supercell),) * 3 + (3,) * 3)
    mapped_clusters = np.zeros((len(supercell),) * 3, dtype=bool)

    for atom in supercell_map:
        i = atom.index
        for entry in sheng:
            if atom.site != entry.site_0:
                continue
            j = supercell_map.index(entry.site_1, entry.offset_1 + atom.offset)
            k = supercell_map.index(entry.site_2, entry.offset_2 + atom.offset)
            ijk = (i, j, k)
            if mapped_clusters[ijk]:
                raise Exception('Ambiguous force constant.'
                                ' Supercell is too small')
            fc_array[ijk] = entry.fc
            mapped_clusters[ijk] = True

    fcs = hiphive.force_constants.ForceConstants.from_arrays(
        supercell, fc3_array=fc_array)
    return fcs
