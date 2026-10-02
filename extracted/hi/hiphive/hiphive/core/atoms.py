"""
Collection of functions and classes for handling information concerning atoms
and structures, including the relationship between primitive cell and
supercells that are derived thereof.
"""

import pickle
from ase import Atoms as aseAtoms
import numpy as np
from ..input_output.logging_tools import logger

# TODO: Rename logger
logger = logger.getChild('atoms')


class Atom:
    # TODO: This class should inherit some immutable to make it clear that
    # there is no reference to any other obj
    """Unique representation of an atom in a lattice with a basis

    Class for storing information about the position of an atom in a supercell
    relative to the origin of the underlying primitive cell. This class is used
    for handling the relationship between a primitive cell and supercells
    derived thereof.

    Parameters
    ----------
    site : int
        site index
    offset : list(float) or numpy.ndarray
        must contain three elements, offset_x, offset_y, offset_z
    """
    def __init__(self, site, offset):
        offset = tuple(offset)
        self._site = site
        self._offset = offset

    @property
    def site(self):
        """int : index of corresponding site in the primitive basis"""
        return self._site

    @property
    def offset(self):
        """list(int) : translational offset of the supercell site relative
        to the origin of the primitive cell in units of primitive lattice
        vectors"""
        return self._offset

    def __repr__(self):
        return 'Atom({}, {})'.format(self.site, self.offset)

    def spos(atom, basis):
        return np.add(basis[atom.site], atom.offset)

    def pos(atom, basis, cell):
        spos = atom.spos(basis)
        return np.dot(spos, cell)

    @staticmethod
    def spos_to_atom(spos, basis, tol=None):
        # TODO: Why is this simply duplicated spos_to_atom from helper below?
        if not tol:
            # TODO: Link to config file
            tol = 1e-4
        for site, base in enumerate(basis):
            offset = np.subtract(spos, base)
            diff = offset - np.round(offset, 0)
            if np.linalg.norm(diff) < tol:
                offset = np.round(offset, 0).astype(int)
                atom = Atom(site, offset)
                assert np.linalg.norm(spos - atom.spos(basis)) < tol, (
                    '{} with basis {} != {}'.format(atom, basis, spos))
                return atom

        s = '{} not compatible with {} and tolerance {}'
        raise Exception(s.format(spos, basis, tol))

    def __hash__(self):
        return hash((self._site, *self.offset))

    def __eq__(self, other):
        if not isinstance(other, Atom):
            return False
        return self.site == other.site and self.offset == other.offset


class Atoms(aseAtoms):
    """Minimally augmented version of the ASE Atoms class suitable for handling
    primitive cell information.

    Saves and loads by pickle.
    """
    @property
    def basis(self):
        """numpy.ndarray : scaled coordinates of the sites in the primitive basis
        """
        return self.get_scaled_positions().round(12) % 1

    def write(self, f):
        """ Writes the object to file.

        Note: Only the cell, basis and numbers are stored!

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to write to (file object)
        """
        data = {}
        data['cell'] = self.cell
        data['basis'] = self.basis
        data['numbers'] = self.numbers

        pickle.dump(data, f)

    @staticmethod
    def read(f):
        """ Load an hiPhive Atoms object from file.

        Parameters
        ----------
        f : str or file object
            name of input file (str) or stream to load from (file object)

        Returns
        -------
        hiPhive Atoms object
        """
        data = pickle.load(f)
        atoms = aseAtoms(numbers=data['numbers'],
                         scaled_positions=data['basis'],
                         cell=data['cell'],
                         pbc=True)
        return Atoms(atoms)


def atom_to_spos(atom, basis):
    """Helper function for obtaining the position of a supercell atom in scaled
    coordinates.

    Parameters
    ----------
    atom : hiPhive.Atom
        supercell atom
    basis : list(list(float)) or numpy.ndarray
        positions of sites in the primitive basis

    Returns
    -------
    numpy.ndarray
        scaled coordinates of an atom in a supercell
    """
    return np.add(atom.offset, basis[atom.site])


def spos_to_atom(spos, basis, tol=1e-4):
    """Helper function for transforming a supercell position to the primitive
    basis.

    Parameters
    ----------
    spos : list(list(float)) or numpy.ndarray
        scaled coordinates of an atom in a supercell
    basis : list(list(float)) or numpy.ndarray
        positions of sites in the primitive basis
    tol : float
        a general tolerance

    Returns
    -------
    hiphive.Atom
         supercell atom
    """
    # TODO: Fix tolerance
    # If needed, convert inputs to arrays to make use of numpy vectorization
    spos = np.asarray(spos)
    basis = np.asarray(basis)
    # If the scaled position belongs to this site, the offset is the
    # difference in scaled coordinates and should be integer
    offsets = spos - basis
    # The diff is the difference between the offset vector and the nearest
    # integer vector.
    diffs = offsets - np.round(offsets, 0)
    # It should be close to the null vector if this is the correct site.
    match_indices = np.nonzero(np.linalg.norm(diffs, axis=1) < tol)[0]
    # If no atom was found or more than one atoms were found we throw an error
    if len(match_indices) != 1:
        raise ValueError(f'{spos} not compatible with {basis} and tolerance {tol}')

    # This should be the correct atom
    site = match_indices[0]
    # If the difference is less than the tol make the offset integers
    offset = np.rint(offsets[site])
    atom = Atom(site, offset)
    # Just to be sure we check that the atom actually produces the
    # input spos given the input basis
    s = ('Atom=[{},{}] with basis {} != {}'
         .format(atom.site, atom.offset, basis, spos))
    assert np.linalg.norm(spos - atom_to_spos(atom, basis)) < tol, s
    return atom
