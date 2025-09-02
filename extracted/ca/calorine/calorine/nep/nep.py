import contextlib
import os
import warnings
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
from ase import Atoms

import _nepy
from calorine.nep.model import _get_nep_contents


def _get_atomic_properties(
    structure: Atoms,
) -> Tuple[List[float], List[str], List[float]]:
    """Fetches cell, symbols and positions for a structure. Since NEP_CPU requires a cell, if the
    structure has no cell a default cubic cell with a side of 100 Å will be used.

    Parameters
    ----------
    structure
        Atoms object representing the structure.

    Returns
    -------
    List[float]
        Cell vectors
    List[str]
        Atomic species
    List[float]
        Atom positions
    List[float]
        Atom masses
    """
    if structure.cell.rank == 0:
        warnings.warn('Using default unit cell (cubic with side 100 Å).')
        set_default_cell(structure)

    c = structure.get_cell(complete=True).flatten()
    cell = [c[0], c[3], c[6], c[1], c[4], c[7], c[2], c[5], c[8]]

    symbols = structure.get_chemical_symbols()
    positions = list(
        structure.get_positions().T.flatten()
    )  # [x1, ..., xN, y1, ... yN,...]
    masses = structure.get_masses()
    return cell, symbols, positions, masses


def _setup_nepy(
    model_filename: str,
    natoms: int,
    cell: List[float],
    symbols: List[str],
    positions: List[float],
    masses: List[float],
    debug: bool,
) -> _nepy.NEPY:
    """Sets up an instance of the NEPY pybind11 interface to NEP_CPU.

    Parameters
    ----------
    model_filename
        Path to model.
    natoms:
        Number of atoms in the structure.
    cell:
        Cell vectors.
    symbols:
        Atom species.
    positions:
        Atom positions.
    masses:
        Atom masses.
    debug:
        Flag to control if the output from NEP_CPU will be printed.

    Returns
    -------
    NEPY
        NEPY interface
    """
    # Ensure that `model_filename` exists to avoid segfault in pybind11 code
    if not os.path.isfile(model_filename):
        raise ValueError(f'{Path(model_filename)} does not exist')

    # Disable output from C++ code by default
    if debug:
        nepy = _nepy.NEPY(model_filename, natoms, cell, symbols, positions, masses)
    else:
        with open(os.devnull, 'w') as f:
            with contextlib.redirect_stdout(f):
                with contextlib.redirect_stderr(f):
                    nepy = _nepy.NEPY(
                        model_filename, natoms, cell, symbols, positions, masses
                    )
    return nepy


def set_default_cell(structure: Atoms, box_length: float = 100):
    """Adds a cubic box to an Atoms object. Atoms object is edited in-place.

    Parameters
    ----------
    structure
        Structure to add box to
    box_length
        Cubic box side length in Å, by default 100
    """
    structure.set_cell([[box_length, 0, 0], [0, box_length, 0], [0, 0, box_length]])
    structure.center()


def get_descriptors(
    structure: Atoms, model_filename: Optional[str] = None, debug: bool = False
) -> np.ndarray:
    """Calculates the NEP descriptors for a given structure. A NEP model defined by a nep.txt
    can additionally be provided to get the NEP3 model specific descriptors.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format. Defaults to ``None``.
    debug
        Flag to toggle debug mode. Makes the generated dummy NEP2 model available
        in a local tmp directory, as well as prints GPUMD output. Defaults to ``False``.

    Returns
    -------
    Descriptors for the supplied structure, with shape (number_of_atoms, descriptor components)
    """
    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)

    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )
    all_descriptors = nepy.get_descriptors()
    descriptors_per_atom = np.array(all_descriptors).reshape(-1, natoms).T
    return descriptors_per_atom


def get_latent_space(
    structure: Atoms, model_filename: Union[str, None] = None, debug: bool = False
) -> np.ndarray:
    """Calculates the latent space representation of a structure, i.e, the activiations in
    the hidden layer. A NEP model defined by a `nep.txt` file needs to be provided.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model. Defaults to None.
    debug
        Flag to toggle debug mode. Prints GPUMD output. Defaults to False.

    Returns
    -------
    Activation with shape `(natoms, N_neurons)`
    """
    if model_filename is None:
        raise ValueError('Model is undefined')
    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)

    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )

    latent = nepy.get_latent_space()
    latent = np.array(latent).reshape(-1, natoms).T
    return latent


def get_potential_forces_and_virials(
    structure: Atoms, model_filename: Optional[str] = None, debug: bool = False
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculates the per-atom potential, forces and virials for a given structure.
    A NEP model defined by a `nep.txt` file needs to be provided.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model. Defaults to None.
    debug
        Flag to toggle debug mode. Prints GPUMD output. Defaults to False.

    Returns
    -------
    potential with shape `(natoms,)`
    forces with shape `(natoms, 3)`
    virials with shape `(natoms, 9)`
    """
    if model_filename is None:
        raise ValueError('Model is undefined')

    model_type = _get_nep_contents(model_filename)[0]['model_type']
    if model_type != 'potential':
        raise ValueError(
            'A NEP model trained for predicting energies and forces must be used.'
        )

    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)

    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )

    energies, forces, virials = nepy.get_potential_forces_and_virials()
    forces_per_atom = np.array(forces).reshape(-1, natoms).T
    virials_per_atom = np.array(virials).reshape(-1, natoms).T
    return np.array(energies), forces_per_atom, virials_per_atom


def get_polarizability(
    structure: Atoms,
    model_filename: Optional[str] = None,
    debug: bool = False,
) -> np.ndarray:
    """Calculates the polarizability tensor for a given structure. A NEP model defined
    by a ``nep.txt`` file needs to be provided. The model must be trained to predict the
    polarizability.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format. Defaults to ``None``.
    debug
        Flag to toggle debug mode. Prints GPUMD output. Defaults to ``False``.

    Returns
    -------
    polarizability with shape ``(3, 3)``
    """
    if model_filename is None:
        raise ValueError('Model is undefined')

    model_type = _get_nep_contents(model_filename)[0]['model_type']
    if model_type != 'polarizability':
        raise ValueError(
            'A NEP model trained for predicting polarizability must be used.'
        )

    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)

    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )
    # Components are in order xx yy zz xy yz zx.
    pol = nepy.get_polarizability()
    polarizability = np.array([
        [pol[0], pol[3], pol[5]],
        [pol[3], pol[1], pol[4]],
        [pol[5], pol[4], pol[2]]
    ])

    return polarizability


def get_dipole(
    structure: Atoms,
    model_filename: Optional[str] = None,
    debug: bool = False,
) -> np.ndarray:
    """Calculates the dipole for a given structure. A NEP model defined by a
    ``nep.txt`` file needs to be provided.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format. Defaults to ``None``.
    debug
        Flag to toggle debug mode. Prints GPUMD output. Defaults to ``False``.

    Returns
    -------
    dipole with shape ``(3,)``
    """
    if model_filename is None:
        raise ValueError('Model is undefined')

    model_type = _get_nep_contents(model_filename)[0]['model_type']
    if model_type != 'dipole':
        raise ValueError('A NEP model trained for predicting dipoles must be used.')

    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)

    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )
    dipole = np.array(nepy.get_dipole())

    return dipole


def get_dipole_gradient(
    structure: Atoms,
    model_filename: Optional[str] = None,
    backend: str = 'c++',
    method: str = 'central difference',
    displacement: float = 0.01,
    charge: float = 1.0,
    nep_command: str = 'nep',
    debug: bool = False,
) -> np.ndarray:
    """Calculates the dipole gradient for a given structure using finite differences.
    A NEP model defined by a `nep.txt` file needs to be provided.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format. Defaults to ``None``.
    backend
        Backend to use for computing dipole gradient with finite differences.
        One of ``'c++'`` (CPU), ``'python'`` (CPU) and ``'nep'`` (GPU).
        Defaults to ``'c++'``.
    method
        Method for computing gradient with finite differences.
        One of 'forward difference' and 'central difference'.
        Defaults to 'central difference'
    displacement
        Displacement in Å to use for finite differences. Defaults to ``0.01``.
    charge
        System charge in units of the elemental charge.
        Used for correcting the dipoles before computing the gradient.
        Defaults to ``1.0``.
    nep_command
        Command for running the NEP executable. Defaults to ``'nep'``.
    debug
        Flag to toggle debug mode. Prints GPUMD output (if applicable). Defaults to ``False``.


    Returns
    -------
        dipole gradient with shape ``(N, 3, 3)``
    """
    if model_filename is None:
        raise ValueError('Model is undefined')

    model_type = _get_nep_contents(model_filename)[0]['model_type']
    if model_type != 'dipole':
        raise ValueError('A NEP model trained for predicting dipoles must be used.')

    local_structure = structure.copy()

    if backend == 'c++':
        dipole_gradient = _dipole_gradient_cpp(
            local_structure,
            model_filename,
            displacement=displacement,
            method=method,
            charge=charge,
            debug=debug,
        )
    elif backend == 'python':
        dipole_gradient = _dipole_gradient_python(
            local_structure,
            model_filename,
            displacement=displacement,
            charge=charge,
            method=method,
        )
    elif backend == 'nep':
        dipole_gradient = _dipole_gradient_nep(
            local_structure,
            model_filename,
            displacement=displacement,
            method=method,
            charge=charge,
            nep_command=nep_command,
        )
    else:
        raise ValueError(f'Invalid backend {backend}')
    return dipole_gradient


def _dipole_gradient_cpp(
    structure: Atoms,
    model_filename: str,
    method: str = 'central difference',
    displacement: float = 0.01,
    charge: float = 1.0,
    debug: bool = False,
) -> np.ndarray:
    """Calculates the dipole gradient with finite differences, using NEP_CPU.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format.
    method
        Method for computing gradient with finite differences.
        One of ``'forward difference'`` and ``'central difference'``.
        Defaults to ``'central difference'``
    displacement
        Displacement in Å to use for finite differences. Defaults to ``0.01``.
    charge
        System charge in units of the elemental charge.
        Used for correcting the dipoles before computing the gradient.
        Defaults to ``1.0``.

    Returns
    -------
        dipole gradient with shape ``(N, 3, 3)``
    """
    if displacement <= 0:
        raise ValueError('Displacement must be > 0 Å')

    implemented_methods = {
        'forward difference': 0,
        'central difference': 1,
        'second order central difference': 2,
    }

    if method not in implemented_methods.keys():
        raise ValueError(f'Invalid method {method} for calculating gradient')

    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)
    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )
    dipole_gradient = np.array(
        nepy.get_dipole_gradient(displacement, implemented_methods[method], charge)
    ).reshape(natoms, 3, 3)
    return dipole_gradient


def _dipole_gradient_python(
    structure: Atoms,
    model_filename: str,
    method: str = 'central difference',
    displacement: float = 0.01,
    charge: float = 1.0,
) -> np.ndarray:
    """Calculates the dipole gradient with finite differences, using the Python and get_dipole().

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format.
    method
        Method for computing gradient with finite differences.
        One of ``'forward difference'`` and ``'central difference'``.
        Defaults to ``'central difference'``
    displacement
        Displacement in Å to use for finite differences. Defaults to ``0.01``.
    charge
        System charge in units of the elemental charge.
        Used for correcting the dipoles before computing the gradient.
        Defaults to ``1.0``.

    Returns
    -------
        dipole gradient with shape ``(N, 3, 3)``
    """
    if displacement <= 0:
        raise ValueError('Displacement must be > 0 Å')

    N = len(structure)
    if method == 'forward difference':
        # Correct all dipole by the permanent dipole, charge * center of mass
        d = (
            get_dipole(structure, model_filename)
            + charge * structure.get_center_of_mass()
        )
        d_forward = np.zeros((N, 3, 3))
        for atom in range(N):
            for cartesian in range(3):
                copy = structure.copy()
                positions = copy.get_positions()
                positions[atom, cartesian] += displacement
                copy.set_positions(positions)
                d_forward[atom, cartesian, :] = (
                    get_dipole(copy, model_filename)
                    + charge * copy.get_center_of_mass()
                )
        gradient = (d_forward - d[None, None, :]) / displacement

    elif method == 'central difference':
        d_forward = np.zeros((N, 3, 3))
        d_backward = np.zeros((N, 3, 3))
        for atom in range(N):
            for cartesian in range(3):
                # Forward displacements
                copy_forward = structure.copy()
                positions_forward = copy_forward.get_positions()
                positions_forward[atom, cartesian] += displacement
                copy_forward.set_positions(positions_forward)
                d_forward[atom, cartesian, :] = (
                    get_dipole(copy_forward, model_filename)
                    + charge * copy_forward.get_center_of_mass()
                )
                # Backwards displacement
                copy_backward = structure.copy()
                positions_backward = copy_backward.get_positions()
                positions_backward[atom, cartesian] -= displacement
                copy_backward.set_positions(positions_backward)
                d_backward[atom, cartesian, :] = (
                    get_dipole(copy_backward, model_filename)
                    + charge * copy_backward.get_center_of_mass()
                )
        gradient = (d_forward - d_backward) / (2 * displacement)
    elif method == 'second order central difference':
        # Coefficients from
        # https://en.wikipedia.org/wiki/Finite_difference_coefficient#Central_finite_difference
        d_forward_one_h = np.zeros((N, 3, 3))
        d_forward_two_h = np.zeros((N, 3, 3))
        d_backward_one_h = np.zeros((N, 3, 3))
        d_backward_two_h = np.zeros((N, 3, 3))
        for atom in range(N):
            for cartesian in range(3):
                copy = structure.copy()
                positions = copy.get_positions()
                # Forward displacements
                positions[atom, cartesian] += displacement  # + h
                copy.set_positions(positions)
                d_forward_one_h[atom, cartesian, :] = (
                    get_dipole(copy, model_filename)
                    + charge * copy.get_center_of_mass()
                )
                positions[atom, cartesian] += displacement  # + 2h total
                copy.set_positions(positions)
                d_forward_two_h[atom, cartesian, :] = (
                    get_dipole(copy, model_filename)
                    + charge * copy.get_center_of_mass()
                )
                # Backwards displacement
                positions[atom, cartesian] -= 3 * displacement  # 2h - 3h = -h
                copy.set_positions(positions)
                d_backward_one_h[atom, cartesian, :] = (
                    get_dipole(copy, model_filename)
                    + charge * copy.get_center_of_mass()
                )
                positions[atom, cartesian] -= displacement  # - 2h total
                copy.set_positions(positions)
                d_backward_two_h[atom, cartesian, :] = (
                    get_dipole(copy, model_filename)
                    + charge * copy.get_center_of_mass()
                )
            c0 = -1.0 / 12.0
            c1 = 2.0 / 3.0
            gradient = (
                c0 * d_forward_two_h
                + c1 * d_forward_one_h
                - c1 * d_backward_one_h
                - c0 * d_backward_two_h
            ) / displacement
    else:
        raise ValueError(f'Invalid method {method} for calculating gradient')
    return gradient


def _dipole_gradient_nep(
    structure: Atoms,
    model_filename: str,
    method: str = 'central difference',
    displacement: float = 0.01,
    charge: float = 1.0,
    nep_command: str = 'nep',
) -> np.ndarray:
    """Calculates the dipole gradient with finite differences, using the NEP executable.

    Parameters
    ----------
    structure
        Input structure
    model_filename
        Path to NEP model in ``nep.txt`` format.
    method
        Method for computing gradient with finite differences.
        One of ``'forward difference'`` and ``'central difference'``.
        Defaults to ``'central difference'``
    displacement
        Displacement in Å to use for finite differences. Defaults to 0.01 Å.
        Note that results are possibly unreliable for displacemen < 0.01,
        which might be due to rounding errors.
    charge
        System charge in units of the elemental charge.
        Used for correcting the dipoles before computing the gradient.
        Defaults to 1.0.
    nep_command
        Command for running the NEP executable. Defaults to ``'nep'``.


    Returns
    -------
        dipole gradient with shape ``(N, 3, 3)``
    """
    if displacement <= 0:
        raise ValueError('Displacement must be > 0 Å')

    if displacement < 1e-2:
        warnings.warn(
            'Dipole gradients with nep are unstable for displacements < 0.01 Å.'
        )

    N = len(structure)
    if method == 'forward difference':
        structure = _set_dummy_energy_forces(structure)
        structures = [structure]  # will hold 3N+1 structures
        # Correct for the constant dipole, by adding charge * center of mass
        corrections = np.zeros((3 * N + 1, 3))
        corrections[0] = charge * structure.get_center_of_mass()
        for atom in range(N):
            for cartesian in range(3):
                copy = structure.copy()
                positions = copy.get_positions()
                positions[atom, cartesian] += displacement
                copy.set_positions(positions)
                copy = _set_dummy_energy_forces(copy)
                structures.append(copy)
                corrections[1 + atom * 3 + cartesian] = (
                    charge * copy.get_center_of_mass()
                )

        dipoles = (
            _predict_dipole_batch(structures, model_filename, nep_command) * N
        )  # dipole/atom, shape (3N+1, 3)
        dipoles += corrections

        d = dipoles[0, :]
        d_forward = dipoles[1:].reshape(N, 3, 3)
        gradient = (d_forward - d[None, None, :]) / displacement

    elif method == 'central difference':
        structures_forward = []  # will hold 3N structures
        structures_backward = []  # will hold 3N structures

        # Correct for the constant dipole, by adding charge * center of mass
        corrections_forward = np.zeros((3 * N, 3))
        corrections_backward = np.zeros((3 * N, 3))

        for atom in range(N):
            for cartesian in range(3):
                # Forward displacements
                copy_forward = structure.copy()
                positions_forward = copy_forward.get_positions()
                positions_forward[atom, cartesian] += displacement
                copy_forward.set_positions(positions_forward)
                copy_forward = _set_dummy_energy_forces(copy_forward)
                structures_forward.append(copy_forward)
                corrections_forward[atom * 3 + cartesian] = (
                    charge * copy_forward.get_center_of_mass()
                )

                # Backwards displacement
                copy_backward = structure.copy()
                positions_backward = copy_backward.get_positions()
                positions_backward[atom, cartesian] -= displacement
                copy_backward.set_positions(positions_backward)
                copy_backward = _set_dummy_energy_forces(copy_backward)
                structures_backward.append(copy_backward)
                corrections_backward[atom * 3 + cartesian] = (
                    charge * copy_backward.get_center_of_mass()
                )

        structures = structures_forward + structures_backward
        dipoles = (
            _predict_dipole_batch(structures, model_filename, nep_command) * N
        )  # dipole/atom, shape (6N, 3)
        d_forward = dipoles[: 3 * N, :]
        d_backward = dipoles[3 * N :, :]

        d_forward += corrections_forward
        d_backward += corrections_backward

        d_forward = d_forward.reshape(N, 3, 3)
        d_backward = d_backward.reshape(N, 3, 3)

        gradient = (d_forward - d_backward) / (2 * displacement)
    else:
        raise ValueError(f'Invalid method {method} for calculating gradient')
    return gradient


def _set_dummy_energy_forces(structure: Atoms) -> Atoms:
    """Sets the energies and forces of structure to zero.

    Parameters
    ----------
    structure
        Input structure


    Returns
    ------- Copy of structure, with SinglePointCalculator with zero energy and force.
    """
    from ase.calculators.singlepoint import SinglePointCalculator

    copy = structure.copy()
    N = len(copy)
    energy = 0

    forces = np.zeros((N, 3))
    dummy = SinglePointCalculator(copy, **{'energy': energy, 'forces': forces})
    copy.calc = dummy
    return copy


def _predict_dipole_batch(
    structures: List[Atoms], model_filename: str, nep_command: str = 'nep'
) -> np.ndarray:
    """Predicts dipoles for a set of structures using the NEP executable
    Note that the units are in (dipole units)/atom.

    Parameters
    ----------
    structure
        Input structures
    model_filename
        Path to NEP model in ``nep.txt`` format.
    nep_command
        Command for running the NEP executable. Defaults to ``'nep'``.


    Returns
    ------- Predicted dipoles, with shape (len(structures), 3).
    """
    import shutil
    from os.path import join as join_path
    from subprocess import run
    from tempfile import TemporaryDirectory

    from calorine.nep import read_model, write_nepfile, write_structures

    with TemporaryDirectory() as directory:
        shutil.copy2(model_filename, join_path(directory, 'nep.txt'))
        model = read_model(model_filename)

        parameters = dict(
            prediction=1,
            mode=1,
            version=model.version,
            n_max=[model.n_max_radial, model.n_max_angular],
            cutoff=[model.radial_cutoff, model.angular_cutoff],
            basis_size=[model.n_basis_radial, model.n_basis_radial],
            l_max=[model.l_max_3b, model.l_max_4b, model.l_max_5b],
            neuron=model.n_neuron,
            type=[len(model.types), *model.types],
        )

        write_nepfile(parameters, directory)
        file = join_path(directory, 'train.xyz')
        write_structures(file, structures)

        # Execute nep
        completed = run([nep_command], cwd=directory, capture_output=True)
        completed.check_returncode()

        # Read results
        dipoles = np.loadtxt(join_path(directory, 'dipole_train.out'))
        if len(dipoles.shape) == 1:
            dipoles = dipoles.reshape(1, -1)
        return dipoles[:, :3]


def _check_components_polarizability_gradient(component: Union[str, List[str]]) -> List[int]:
    """
    Verifies that the selected components are ok.
    """
    allowed_components = {
            'x': 0,
            'y': 1,
            'z': 2,
    }

    # Check if chosen components are ok
    if component == 'full':
        components_to_compute = [0, 1, 2]
    else:
        components_list = [component] if isinstance(component, str) else component
        components_to_compute = []
        for c in components_list:
            if c in allowed_components.keys():
                components_to_compute.append(allowed_components[c])
            elif c == 'full':
                raise ValueError('Write ``component="full"`` to get all components.')
            else:
                raise ValueError(f'Invalid component {c}')
        assert len(components_list) == len(components_to_compute), \
            'Number of components to compute does not match.'
    return components_to_compute


def get_polarizability_gradient(
    structure: Atoms,
    model_filename: Optional[str] = None,
    displacement: float = 0.01,
    component: Union[str, List[str]] = 'full',
    debug: bool = False,
) -> np.ndarray:
    """Calculates the dipole gradient for a given structure using finite differences.
    A NEP model defined by a ``nep.txt`` file needs to be provided.
    This function computes the derivatives using the second-order central difference
    method with a C++ backend.

    Parameters
    ----------
    structure
        Input structure.
    model_filename
        Path to NEP model in ``nep.txt`` format. Defaults to ``None``.
    displacement
        Displacement in Å to use for finite differences. Defaults to ``0.01``.
    component
        Component or components of the polarizability tensor that the gradient
        should be computed for.
        The following components are available: ``x`, ``y``, ``z``, ``full``.
        Option ``full`` computes the derivative whilst moving the atoms in each Cartesian
        direction, which yields a tensor of shape ``(N, 3, 6)``.
        Multiple components may be specified.
        Defaults to ``full``.
    debug
        Flag to toggle debug mode. Prints GPUMD output (if applicable). Defaults to ``False``.


    Returns
    -------
        polarizability gradient with shape ``(N, C, 6)`` where ``C``
        is the number of components chosen.
    """
    if model_filename is None:
        raise ValueError('Model is undefined')

    model_type = _get_nep_contents(model_filename)[0]['model_type']
    if model_type != 'polarizability':
        raise ValueError('A NEP model trained for predicting polarizability must be used.')

    components_to_compute = _check_components_polarizability_gradient(component)

    local_structure = structure.copy()
    polarizability_gradient = _polarizability_gradient_cpp(
        local_structure,
        model_filename,
        displacement=displacement,
        components=components_to_compute,
        debug=debug,
    )
    return polarizability_gradient


def _polarizability_gradient_to_3x3(natoms, pg):
    """
    Converts a polarizability gradient tensor with
    shape (Natoms, 3, 6) to (Natoms, 3, 3, 3).
    The 6 items in the polarizability gradient have
    the following order from GPUMD: xx, yy, zz, xy, yz, zx.
    """
    gpumd_to_3x3_indices = np.array([
        [0, 3, 5],
        [3, 1, 4],
        [5, 4, 2]
    ])
    polgrad_3x3 = np.zeros((natoms, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            index = gpumd_to_3x3_indices[i, j]
            polgrad_3x3[:, :, i, j] = pg[:, :, index]
    return polgrad_3x3


def _polarizability_gradient_cpp(
    structure: Atoms,
    model_filename: str,
    displacement: float,
    components: List[int],
    debug: bool = False,
) -> np.ndarray:
    """Calculates the polarizability gradient with finite differences, using NEP_CPU.

    Parameters
    ----------
    structure
        Input structure.
    model_filename
        Path to NEP model in ``nep.txt`` format.
    displacement
        Displacement in Å to use for finite differences. Defaults to ``0.01``.
    components
        List of components to compute. Integer values from 0 to 2 that corresponds
        to indices in the ordered list [x, y, z]. Index 1 corresponds to the
        derivative with regards to only the y positions of the atoms, and so forth.

    Returns
    -------
        dipole gradient with shape ``(N, len(components), 3, 3)``
    """
    if displacement <= 0:
        raise ValueError('Displacement must be > 0 Å')
    # TODO possibly use components later to only move atoms in one cartesian direction
    local_structure = structure.copy()
    natoms = len(local_structure)
    cell, symbols, positions, masses = _get_atomic_properties(local_structure)
    nepy = _setup_nepy(
        model_filename, natoms, cell, symbols, positions, masses, debug
    )
    pg = np.array(
        nepy.get_polarizability_gradient(displacement, components)
        ).reshape(natoms, 3, 6)
    # Convert to 3x3
    polarizability_gradient = _polarizability_gradient_to_3x3(natoms, pg)
    return polarizability_gradient[:, components, :, :]  # Only return the relevant components
