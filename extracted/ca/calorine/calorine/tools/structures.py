from typing import List
import numpy as np
from ase import Atoms
from ase.filters import FrechetCellFilter
from ase.optimize import BFGS, LBFGS, FIRE, GPMin
from ase.optimize.sciopt import SciPyFminBFGS
from ase.units import GPa

try:
    import spglib
    spglib_available = True
except ImportError:  # pragma: no cover
    spglib_available = False


def relax_structure(structure: Atoms,
                    fmax: float = 0.001,
                    steps: int = 500,
                    minimizer: str = 'bfgs',
                    constant_cell: bool = False,
                    constant_volume: bool = False,
                    scalar_pressure: float = 0.0,
                    **kwargs) -> None:
    """Relaxes the given structure.

    Parameters
    ----------
    structure
        Atomic configuration to relax.
    fmax
        Stop relaxation if the absolute force for all atoms falls below this value.
    steps
        Maximum number of relaxation steps the minimizer is allowed to take.
    minimizer
        Minimizer to use; possible values: 'bfgs', 'lbfgs', 'fire', 'gpmin', 'bfgs-scipy'.
    constant_cell
        If True do not relax the cell or the volume.
    constant_volume
        If True relax the cell shape but keep the volume constant.
    kwargs
        Keyword arguments to be handed over to the minimizer; possible arguments can be found
        in the `ASE documentation <https://wiki.fysik.dtu.dk/ase/ase/optimize.html>`_
    scalar_pressure
        External pressure in GPa.
    """
    if structure.calc is None:
        raise ValueError('Structure has no attached calculator object')
    if constant_cell:
        ucf = structure
    else:
        ucf = FrechetCellFilter(
            structure, constant_volume=constant_volume, scalar_pressure=scalar_pressure * GPa)
    kwargs['logfile'] = kwargs.get('logfile', None)
    if minimizer == 'bfgs':
        dyn = BFGS(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'lbfgs':
        dyn = LBFGS(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'bfgs-scipy':
        dyn = SciPyFminBFGS(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'fire':
        dyn = FIRE(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    elif minimizer == 'gpmin':
        dyn = GPMin(ucf, **kwargs)
        dyn.run(fmax=fmax, steps=steps)
    else:
        raise ValueError(f'Unknown minimizer: {minimizer}')


def get_spacegroup(
    structure: Atoms,
    symprec: float = 1e-5,
    angle_tolerance: float = -1.0,
    style: str = 'international',
) -> str:
    """Returns the space group of a structure using spglib.
    This is a convenience interface to the :func:`get_spacegroup`
    function of spglib that works directly with ase Atoms objects.

    Parameters
    ----------
    structure
        Input atomic structure.
    symprec
        Tolerance imposed when analyzing the symmetry.
    angle_tolerance
        Tolerance imposed when analyzing angles.
    style
        Space group notation to be used. Can be ``'international'`` for the
        interational tables of crystallography (ITC) style (Hermann-Mauguin
        and ITC number) or ``'Schoenflies'`` for the Schoenflies notation.
    """
    if not spglib_available:
        raise ImportError('\
                spglib must be available in order for this function to work.')  # pragma: no cover

    if style == 'international':
        symbol_type = 0
    elif style == 'Schoenflies':
        symbol_type = 1
    else:
        raise ValueError(f'Unknown value for style: {style}')

    structure_tuple = (
        structure.get_cell(),
        structure.get_scaled_positions(),
        structure.numbers)
    spg = spglib.get_spacegroup(
        structure_tuple, symprec=symprec,
        angle_tolerance=angle_tolerance, symbol_type=symbol_type)

    return spg


def get_primitive_structure(
    structure: Atoms,
    no_idealize: bool = True,
    to_primitive: bool = True,
    symprec: float = 1e-5,
) -> Atoms:
    """Returns the primitive structure using spglib.
    This is a convenience interface to the :func:`standardize_cell`
    function of spglib that works directly with ase Atoms objects.

    Parameters
    ----------
    structure
        Input atomic structure.
    no_idealize
        If ``True`` lengths and angles are not idealized.
    to_primitive
        If ``True`` convert to primitive structure.
    symprec
        Tolerance imposed when analyzing the symmetry.
    """
    if not spglib_available:
        raise ImportError('\
                spglib must be available in order for this function to work.')  # pragma: no cover

    structure_tuple = (
        structure.get_cell(),
        structure.get_scaled_positions(),
        structure.numbers)
    result = spglib.standardize_cell(
        structure_tuple, to_primitive=to_primitive,
        no_idealize=no_idealize, symprec=symprec)
    if result is None:
        raise ValueError('spglib failed to find the primitive cell, maybe caused by large symprec.')
    lattice, scaled_positions, numbers = result
    scaled_positions = [np.round(pos, 12) for pos in scaled_positions]
    structure_prim = Atoms(scaled_positions=scaled_positions,
                           numbers=numbers, cell=lattice, pbc=True)
    structure_prim.wrap()

    return structure_prim


def get_wyckoff_sites(
        structure: Atoms,
        map_occupations: List[List[str]] = None,
        symprec: float = 1e-5,
        include_representative_atom_index: bool = False,
) -> List[str]:
    """Returns the Wyckoff symbols of the input structure.
    The Wyckoff labels can be conveniently attached as an array to the
    structure object as demonstrated in the examples section below.

    By default the occupation of the sites is part of the symmetry
    analysis. If a chemically disordered structure is provided this
    will usually reduce the symmetry substantially. If one is
    interested in the symmetry of the underlying structure one can
    control how occupations are handled. To this end, one can provide
    the :attr:`map_occupations` keyword argument. The latter must be a
    list, each entry of which is a list of species that should be
    treated as indistinguishable. As a shortcut, if *all* species
    should be treated as indistinguishable one can provide an empty
    list. Examples that illustrate the usage of the keyword are given
    below.

    Parameters
    ----------
    structure
        Input structure. Note that the occupation of the sites is
        included in the symmetry analysis.
    map_occupations
        Each sublist in this list specifies a group of chemical
        species that shall be treated as indistinguishable for the
        purpose of the symmetry analysis.
    symprec
        Tolerance imposed when analyzing the symmetry using spglib.
    include_representative_atom_index
        If True the index of the first atom in the structure that is
        representative of the Wyckoff site is included in the symbol.
        This is in particular useful in cases when there are multiple
        Wyckoff sites sites with the same Wyckoff letter.

    Examples
    --------
    Wyckoff sites of a hexagonal-close packed structure::

        >>> from ase.build import bulk
        >>> structure = bulk('Ti')
        >>> wyckoff_sites = get_wyckoff_sites(structure)
        >>> print(wyckoff_sites)
        ['2d', '2d']


    The Wyckoff labels can also be attached as an array to the
    structure, in which case the information is also included when
    storing the Atoms object::

        >>> from ase.io import write
        >>> structure.new_array('wyckoff_sites', wyckoff_sites, str)
        >>> write('structure.xyz', structure)

    The function can also be applied to supercells::

        >>> structure = bulk('GaAs', crystalstructure='zincblende', a=3.0).repeat(2)
        >>> wyckoff_sites = get_wyckoff_sites(structure)
        >>> print(wyckoff_sites)
        ['4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c',
         '4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c']

    Now assume that one is given a supercell of a (Ga,Al)As
    alloy. Applying the function directly yields much lower symmetry
    since the symmetry of the original structure is broken::

        >>> structure.set_chemical_symbols(
        ...        ['Ga', 'As', 'Al', 'As', 'Ga', 'As', 'Al', 'As',
        ...         'Ga', 'As', 'Ga', 'As', 'Al', 'As', 'Ga', 'As'])
        >>> print(get_wyckoff_sites(structure))
        ['8g', '8i', '4e', '8i', '8g', '8i', '2c', '8i',
         '2d', '8i', '8g', '8i', '4e', '8i', '8g', '8i']

    Since Ga and Al occupy the same sublattice, they should, however,
    be treated as indistinguishable for the purpose of the symmetry
    analysis, which can be achieved via the :attr:`map_occupations`
    keyword::

        >>> print(get_wyckoff_sites(structure, map_occupations=[['Ga', 'Al'], ['As']]))
        ['4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c',
         '4a', '4c', '4a', '4c', '4a', '4c', '4a', '4c']

    If occupations are to ignored entirely, one can simply provide an
    empty list. In the present case, this turns the zincblende lattice
    into a diamond lattice, on which case there is only one Wyckoff
    site::

        >>> print(get_wyckoff_sites(structure, map_occupations=[]))
        ['8a', '8a', '8a', '8a', '8a', '8a', '8a', '8a',
         '8a', '8a', '8a', '8a', '8a', '8a', '8a', '8a']
    """
    if not spglib_available:
        raise ImportError('\
                spglib must be available in order for this function to work.')  # pragma: no cover

    structure_copy = structure.copy()
    if map_occupations is not None:
        if len(map_occupations) > 0:
            new_symbols = []
            for symb in structure_copy.get_chemical_symbols():
                for group in map_occupations:  # pragma: no cover - because of the break
                    if symb in group:
                        new_symbols.append(group[0])
                        break
        else:
            new_symbols = len(structure) * ['H']
        structure_copy.set_chemical_symbols(new_symbols)
    structure_tuple = (
        structure_copy.get_cell(),
        structure_copy.get_scaled_positions(),
        structure_copy.numbers)
    dataset = spglib.get_symmetry_dataset(structure_tuple, symprec=symprec)
    n_unitcells = np.linalg.det(dataset.transformation_matrix)

    equivalent_atoms = list(dataset.equivalent_atoms)
    wyckoffs = {}
    for index in set(equivalent_atoms):
        multiplicity = list(dataset.equivalent_atoms).count(index) / n_unitcells
        multiplicity = int(round(multiplicity))
        wyckoff = '{}{}'.format(multiplicity, dataset.wyckoffs[index])
        if include_representative_atom_index:
            wyckoff += f'-{index}'
        wyckoffs[index] = wyckoff

    return [wyckoffs[equivalent_atoms[a.index]] for a in structure_copy]
