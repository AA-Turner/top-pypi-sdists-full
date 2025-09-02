from __future__ import annotations

import contextlib
import os
from tempfile import TemporaryFile
from typing import List, Union

import numpy as np
from ase import Atoms
from ase.calculators.calculator import Calculator, all_changes
from ase.stress import full_3x3_to_voigt_6_stress

import _nepy
from calorine.nep.model import _get_nep_contents
from calorine.nep.nep import _check_components_polarizability_gradient, \
        _polarizability_gradient_to_3x3


class CPUNEP(Calculator):
    """This class provides an ASE calculator for `nep_cpu`,
    the in-memory CPU implementation of GPUMD.

    Parameters
    ----------
    model_filename : str
        Path to file in ``nep.txt`` format with model parameters
    atoms : Atoms
        Atoms to attach the calculator to
    label : str
        Label for this calclator
    debug : bool, optional
        Flag to toggle debug mode. Prints GPUMD output. Defaults to False.

    Raises
    ------
    FileNotFoundError
        Raises :class:`FileNotFoundError` if :attr:`model_filename` does not point to a valid file.
    ValueError
        Raises :class:`ValueError` atoms are not defined when trying to get energies and forces.
    Example
    -------

    >>> calc = CPUNEP('nep.txt')
    >>> atoms.calc = calc
    >>> atoms.get_potential_energy()
    """

    implemented_properties = [
        'energy',
        'energies',
        'forces',
        'stress',
    ]
    debug = False
    nepy = None

    def __init__(
        self,
        model_filename: str,
        atoms: Atoms | None = None,
        label: str | None = None,
        debug: bool = False,
    ):
        self.debug = debug

        if not os.path.exists(model_filename):
            raise FileNotFoundError(f'{model_filename} does not exist.')
        self.model_filename = str(model_filename)

        # Get model type from first row in nep.txt
        header, _ = _get_nep_contents(self.model_filename)
        self.model_type = header['model_type']
        self.supported_species = set(header['types'])
        self.nep_version = header['version']

        if self.model_type == 'dipole':
            # Only available for dipole models
            self.implemented_properties = ['dipole']
        elif self.model_type == 'polarizability':
            # Only available for polarizability models
            self.implemented_properties = ['polarizability']

        # Initialize atoms, results and nepy - note that this is also done in Calculator.__init__()
        if atoms is not None:
            self.set_atoms(atoms)
        parameters = {'model_filename': model_filename}
        Calculator.__init__(self, label=label, atoms=atoms, **parameters)
        if atoms is not None:
            self._setup_nepy()

    def __str__(self) -> str:
        def indent(s: str, i: int) -> str:
            s = '\n'.join([i * ' ' + line for line in s.split('\n')])
            return s

        parameters = '\n'.join(
            [f'{key}: {value}' for key, value in self.parameters.items()]
        )
        parameters = indent(parameters, 4)
        using_debug = '\nIn debug mode' if self.debug else ''

        s = f'{self.__class__.__name__}\n{parameters}{using_debug}'
        return s

    def _setup_nepy(self):
        """
        Creates an instance of the NEPY class and attaches it to the calculator object.
        The output from `nep.cpp` is only written to STDOUT if debug == True
        """
        if self.atoms is None:
            raise ValueError('Atoms must be defined when calculating properties.')
        if self.atoms.cell.rank == 0:
            raise ValueError('Atoms must have a defined cell.')

        natoms = len(self.atoms)
        self.natoms = natoms
        c = self.atoms.get_cell(complete=True).flatten()
        cell = [c[0], c[3], c[6], c[1], c[4], c[7], c[2], c[5], c[8]]
        symbols = self.atoms.get_chemical_symbols()
        positions = list(
            self.atoms.get_positions().T.flatten()
        )  # [x1, ..., xN, y1, ... yN,...]
        masses = self.atoms.get_masses()

        # Disable output from C++ code by default
        if self.debug:
            self.nepy = _nepy.NEPY(
                self.model_filename, self.natoms, cell, symbols, positions, masses
            )
        else:
            with TemporaryFile('w') as f:
                with contextlib.redirect_stdout(f):
                    self.nepy = _nepy.NEPY(
                        self.model_filename,
                        self.natoms,
                        cell,
                        symbols,
                        positions,
                        masses,
                    )

    def set_atoms(self, atoms: Atoms):
        """Updates the Atoms object.

        Parameters
        ----------
        atoms : Atoms
            Atoms to attach the calculator to
        """
        species_in_atoms_object = set(np.unique(atoms.get_chemical_symbols()))
        if not species_in_atoms_object.issubset(self.supported_species):
            raise ValueError('Structure contains species that are not supported by the NEP model.')
        self.atoms = atoms
        self.results = {}
        self.nepy = None

    def _update_symbols(self):
        """Update atom symbols in NEPY."""
        symbols = self.atoms.get_chemical_symbols()
        self.nepy.set_symbols(symbols)

    def _update_masses(self):
        """Update atom masses in NEPY"""
        masses = self.atoms.get_masses()
        self.nepy.set_masses(masses)

    def _update_cell(self):
        """Update cell parameters in NEPY."""
        c = self.atoms.get_cell(complete=True).flatten()
        cell = [c[0], c[3], c[6], c[1], c[4], c[7], c[2], c[5], c[8]]
        self.nepy.set_cell(cell)

    def _update_positions(self):
        """Update atom positions in NEPY."""
        positions = list(
            self.atoms.get_positions().T.flatten()
        )  # [x1, ..., xN, y1, ... yN,...]
        self.nepy.set_positions(positions)

    def calculate(
        self,
        atoms: Atoms = None,
        properties: List[str] = None,
        system_changes: List[str] = all_changes,
    ):
        """Calculate energy, per atom energies, forces, stress and dipole.

        Parameters
        ----------
        atoms : Atoms, optional
            System for which to calculate properties, by default None
        properties : List[str], optional
            Properties to calculate, by default None
        system_changes : List[str], optional
            Changes to the system since last call, by default all_changes
        """
        if properties is None:
            properties = self.implemented_properties

        Calculator.calculate(self, atoms, properties, system_changes)

        if self.nepy is None:
            # Create new NEPY interface
            self._setup_nepy()
        # Update existing NEPY interface
        for change in system_changes:
            if change == 'positions':
                self._update_positions()
            elif change == 'numbers':
                self._update_symbols()
                self._update_masses()
            elif change == 'cell':
                self._update_cell()

        if 'dipole' in properties:
            dipole = np.array(self.nepy.get_dipole())
            self.results['dipole'] = dipole
        elif 'polarizability' in properties:
            pol = np.array(self.nepy.get_polarizability())
            polarizability = np.array([
                    [pol[0], pol[3], pol[5]],
                    [pol[3], pol[1], pol[4]],
                    [pol[5], pol[4], pol[2]]
                ])
            self.results['polarizability'] = polarizability
        elif 'descriptors' in properties:
            descriptors = np.array(self.nepy.get_descriptors())
            descriptors_per_atom = descriptors.reshape(-1, self.natoms).T
            self.results['descriptors'] = descriptors_per_atom
        else:
            energies, forces, virials = self.nepy.get_potential_forces_and_virials()
            energies_per_atom = np.array(energies)
            energy = energies_per_atom.sum()
            forces_per_atom = np.array(forces).reshape(-1, self.natoms).T
            virials_per_atom = np.array(virials).reshape(-1, self.natoms).T
            stress = -(np.sum(virials_per_atom, axis=0) / self.atoms.get_volume()).reshape((3, 3))
            stress = full_3x3_to_voigt_6_stress(stress)

            self.results['energy'] = energy
            self.results['forces'] = forces_per_atom
            self.results['stress'] = stress

    def get_dipole_gradient(
        self,
        displacement: float = 0.01,
        method: str = 'central difference',
        charge: float = 1.0,
    ):
        """Calculates the dipole gradient using finite differences.

        Parameters
        ----------
        displacement
            Displacement in Å to use for finite differences. Defaults to 0.01 Å.
        method
            Method for computing gradient with finite differences.
            One of 'forward difference' and 'central difference'.
            Defaults to 'central difference'
        charge
            System charge in units of the elemental charge.
            Used for correcting the dipoles before computing the gradient.
            Defaults to 1.0.

        Returns
        -------
        dipole gradient with shape `(N, 3, 3)` where ``N`` are the number of atoms.
        """
        if 'dipole' not in self.implemented_properties:
            raise ValueError('Dipole gradients are only defined for dipole NEP models.')

        if displacement <= 0:
            raise ValueError('displacement must be > 0 Å')

        implemented_methods = {
            'forward difference': 0,
            'central difference': 1,
            'second order central difference': 2,
        }

        if method not in implemented_methods.keys():
            raise ValueError(f'Invalid method {method} for calculating gradient')

        if self.nepy is None:
            # Create new NEPY interface
            self._setup_nepy()

        dipole_gradient = np.array(
            self.nepy.get_dipole_gradient(
                displacement, implemented_methods[method], charge
            )
        ).reshape(self.natoms, 3, 3)
        return dipole_gradient

    def get_polarizability(
        self,
        atoms: Atoms = None,
        properties: List[str] = None,
        system_changes: List[str] = all_changes,
    ) -> np.ndarray:
        """Calculates the polarizability tensor for the current structure.
        The model must have been trained to predict the polarizability.
        This is a wrapper function for :func:`calculate`.

        Parameters
        ----------
        atoms : Atoms, optional
            System for which to calculate properties, by default None
        properties : List[str], optional
            Properties to calculate, by default None
        system_changes : List[str], optional
            Changes to the system since last call, by default all_changes

        Returns
        -------
        polarizability with shape ``(3, 3)``
        """
        if properties is None:
            properties = self.implemented_properties

        if 'polarizability' not in properties:
            raise ValueError('Polarizability is only defined for polarizability NEP models.')
        self.calculate(atoms, properties, system_changes)
        return self.results['polarizability']

    def get_polarizability_gradient(
        self,
        displacement: float = 0.01,
        component: Union[str, List[str]] = 'full',
    ) -> np.ndarray:
        """Calculates the dipole gradient for a given structure using finite differences.
        This function computes the derivatives using the second-order central difference
        method with a C++ backend.

        Parameters
        ----------
        displacement
            Displacement in Å to use for finite differences. Defaults to ``0.01``.
        component
            Component or components of the polarizability tensor that the gradient
            should be computed for.
            The following components are available: `x`, `y`, `z`, `full`
            Option ``full`` computes the derivative whilst moving the atoms in each Cartesian
            direction, which yields a tensor of shape ``(N, 3, 3, 3)``,
            where ``N`` is the number of atoms.
            Multiple components may be specified.
            Defaults to ``full``.

        Returns
        -------
        polarizability gradient with shape ``(N, C, 3, 3)`` with ``C`` components chosen.
        """
        if 'polarizability' not in self.implemented_properties:
            raise ValueError('Polarizability gradients are only defined'
                             ' for polarizability NEP models.')

        if displacement <= 0:
            raise ValueError('displacement must be > 0 Å')

        if self.nepy is None:
            # Create new NEPY interface
            self._setup_nepy()

        component_array = _check_components_polarizability_gradient(component)

        pg = np.array(
            self.nepy.get_polarizability_gradient(
                displacement, component_array
            )
        ).reshape(self.natoms, 3, 6)
        polarizability_gradient = _polarizability_gradient_to_3x3(self.natoms, pg)
        return polarizability_gradient[:, component_array, :, :]

    def get_descriptors(
        self,
        atoms: Atoms = None,
        properties: List[str] = None,
        system_changes: List[str] = all_changes,
    ) -> np.ndarray:
        """Calculates the descriptor tensor for the current structure.
        This is a wrapper function for :func:`calculate`.

        Parameters
        ----------
        atoms : Atoms, optional
            System for which to calculate properties, by default None
        properties : List[str], optional
            Properties to calculate, by default None
        system_changes : List[str], optional
            Changes to the system since last call, by default all_changes

        Returns
        -------
        descriptors with shape ``(number_of_atoms, descriptor_components)``
        """
        self.calculate(atoms, ['descriptors'], system_changes)
        return self.results['descriptors']
