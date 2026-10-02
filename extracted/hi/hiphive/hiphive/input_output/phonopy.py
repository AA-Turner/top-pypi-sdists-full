"""
This module provides functions for reading and writing data files
in phonopy and phono3py formats.
"""

import os
import warnings
from itertools import product

import hiphive
import numpy as np
from .logging_tools import logger

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', category=FutureWarning)
    import h5py


logger = logger.getChild('io_phonopy')


def _filename_to_format(filename: str) -> str:
    """ Tries to guess the format from the filename """
    basename = os.path.basename(filename)

    if basename == 'FORCE_CONSTANTS':
        return 'text'

    if '.' in basename:
        extension = basename.split('.')[-1]
        if extension == 'hdf5':
            return 'hdf5'
    raise ValueError('Could not guess file format')


def read_phonopy_fc2(filename: str, format: str = None) -> np.ndarray:
    """Parses a second-order force constant file in phonopy format.

    Parameters
    ----------
    filename : str
        input file name
    format : str
       specify the file-format, if None tries to guess the format from filename;
       possible values: "text", "hdf5"

    Returns
    -------
    numpy.ndarray
        second-order force constant matrix (`N,N,3,3` array)
        where `N` is the number of atoms
    """
    fc2_readers = {
        'text': _read_phonopy_fc2_text,
        'hdf5': _read_phonopy_fc2_hdf5
    }

    if format is None:
        format = _filename_to_format(filename)
    if format not in fc2_readers.keys():
        raise ValueError('Did not recognize format {}'.format(format))
    return fc2_readers[format](filename)


def write_phonopy_fc2(filename: str,
                      fc2,
                      format: str = None) -> None:
    """Writes second-order force constant matrix in phonopy format.

    Parameters
    ----------
    filename : str
        output file name
    fc2 : ForceConstants or numpy.ndarray
        second-order force constant matrix
    format : str
       specify the file-format, if None try to guess the format from filename;
       possible values: "text", "hdf5"
     """

    fc2_writers = {
        'text': _write_phonopy_fc2_text,
        'hdf5': _write_phonopy_fc2_hdf5
    }

    # get fc2_array
    if isinstance(fc2, hiphive.ForceConstants):
        fc2_array = fc2.get_fc_array(order=2)
    elif isinstance(fc2, np.ndarray):
        fc2_array = fc2
    else:
        raise TypeError('fc2 should be ForceConstants or NumPy array')

    # check that fc2 has correct shape
    n_atoms = fc2_array.shape[0]
    if fc2_array.shape != (n_atoms, n_atoms, 3, 3):
        raise ValueError('fc2 has wrong shape')

    # write
    if format is None:
        format = _filename_to_format(filename)
    if format not in fc2_writers.keys():
        raise ValueError('Did not recognize format {}'.format(format))
    fc2_writers[format](filename, fc2_array)


def read_phonopy_fc3(filename: str) -> np.ndarray:
    """Parses a third order force constant file in phonopy hdf5 format.

    Parameters
    ----------
    filename : str
        input file name

    Returns
    -------
    numpy.ndarray
        third order force constant matrix
    """
    with h5py.File(filename, 'r') as hf:
        if 'fc3' in hf.keys():
            fc3 = hf['fc3'][:]
        else:
            raise IOError('Could not find fc3 in file {}'.format(filename))
    return fc3


def write_phonopy_fc3(filename: str, fc3) -> None:
    """Writes third order force constant matrix in phonopy hdf5 format.

    Parameters
    ----------
    filename : str
        output file name
    fc3 : ForceConstants or numpy.ndarray
        third order force constant matrix
    """

    if isinstance(fc3, hiphive.ForceConstants):
        fc3_array = fc3.get_fc_array(order=3)
    elif isinstance(fc3, np.ndarray):
        fc3_array = fc3
    else:
        raise TypeError('fc3 should be ForceConstants or NumPy array')

    # check that fc3 has correct shape
    n_atoms = fc3_array.shape[0]
    if fc3_array.shape != (n_atoms, n_atoms, n_atoms, 3, 3, 3):
        raise ValueError('fc3 has wrong shape')

    with h5py.File(filename, 'w') as hf:
        hf.create_dataset('fc3', data=fc3_array, compression='gzip')
        hf.flush()


def _read_phonopy_fc2_text(filename: str) -> np.ndarray:
    """ Reads phonopy-fc2 file in text format. """
    with open(filename, 'r') as f:

        # read shape of force constants
        line = f.readline()
        line_ints = [int(x) for x in line.split()]
        if len(line_ints) == 1:
            n_atoms = line_ints[0]
        elif len(line_ints) == 2:
            assert line_ints[0] == line_ints[1]
            n_atoms = line_ints[0]
        else:
            raise ValueError('Unsupported or incorrect phonopy format')
        fc2 = np.full((n_atoms, n_atoms, 3, 3), np.nan)

        # read force constants
        lines = f.readlines()
        for n, line in enumerate(lines):
            flds = line.split()
            if len(flds) == 2:
                i = int(flds[0]) - 1  # phonopy index starts with 1
                j = int(flds[1]) - 1
                for x in range(3):
                    fc_row = lines[n + x + 1].split()
                    for y in range(3):
                        fc2[i][j][x][y] = float(fc_row[y])
    return fc2


def _read_phonopy_fc2_hdf5(filename: str) -> np.ndarray:
    """ Reads phonopy-fc2 file in hdf5 format. """
    with h5py.File(filename, 'r') as hf:
        if 'force_constants' in hf.keys():
            fc2 = hf['force_constants'][:]
        elif 'fc2' in hf.keys():
            fc2 = hf['fc2'][:]
        else:
            raise IOError('Could not find fc2 in file {}'.format(filename))
    return fc2


def _write_phonopy_fc2_text(filename: str, fc2: np.ndarray) -> None:
    """ Writes second-order force constants to file in text format. """
    n_atoms = fc2.shape[0]
    with open(filename, 'w') as f:
        f.write('{:5d} {:5d}\n'.format(n_atoms, n_atoms))
        for i, j in product(range(n_atoms), repeat=2):
            fc2_ij = fc2[(i, j)]
            if fc2_ij.shape != (3, 3):
                raise ValueError('Invalid shape for fc2[({},{})]'.format(i, j))
            f.write('{:-5d}{:5d}\n'.format(i + 1, j + 1))
            for row in fc2_ij:
                f.write((3*' {:22.15f}'+'\n').format(*tuple(row)))


def _write_phonopy_fc2_hdf5(filename: str, fc2: np.ndarray) -> None:
    """ Writes second-order force constants to file in hdf5 format. """
    with h5py.File(filename, 'w') as hf:
        hf.create_dataset('fc2', data=fc2, compression='gzip')
        hf.flush()
