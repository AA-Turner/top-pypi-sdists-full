import os
import shutil
import warnings
import tempfile
from collections.abc import Iterable
from typing import Any, List, Tuple, Union

import numpy as np
from ase import Atoms
from ase.calculators.calculator import FileIOCalculator, OldShellProfile, all_changes
from ase.io import read as ase_read
from ase.units import GPa

from calorine.nep.model import _get_nep_contents
from ..gpumd import write_xyz


class GPUMDShellProfile(OldShellProfile):
    """This class provides an ASE calculator for NEP calculations with
    GPUMD.

    Parameters
    ----------
    command : str
        Command to run GPUMD with.
        Default: ``gpumd``
    gpu_identifier_index : int, None
        Index that identifies the GPU that GPUNEP should be run with.
        Typically, NVIDIA GPUs are enumerated with integer indices.
        See https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars.
        Set to None in order to use all available GPUs. Note that GPUMD exit with an error
        when running with more than one GPU if your system is not large enough.
        Default: None
    """
    def __init__(self, command : str, gpu_identifier_index: Union[int, None]):
        if gpu_identifier_index is not None:
            # Do not set a specific device to use = use all available GPUs
            self.cuda_environment_variables = f'CUDA_VISIBLE_DEVICES={gpu_identifier_index}'
            command_with_gpus = f'export {self.cuda_environment_variables} && ' + command
        else:
            command_with_gpus = command
        super().__init__(command_with_gpus)


class GPUNEP(FileIOCalculator):
    """This class provides an ASE calculator for NEP calculations with
    GPUMD.

    This calculator writes files that are input to the `gpumd`
    executable. It is thus likely to be slow if many calculations
    are to be performed.

    Parameters
    ----------
    model_filename : str
        Path to file in ``nep.txt`` format with model parameters.
    directory : str
        Directory to run GPUMD in. If None, a temporary directory
        will be created and removed once the calculations are finished.
        If specified, the directory will not be deleted. In the latter
        case, it is advisable to do no more than one calculation with
        this calculator (unless you know exactly what you are doing).
    label : str
        Label for this calculator.
    atoms : Atoms
        Atoms to attach to this calculator.
    command : str
        Command to run GPUMD with.
        Default: ``gpumd``
    gpu_identifier_index : int
        Index that identifies the GPU that GPUNEP should be run with.
        Typically, NVIDIA GPUs are enumerated with integer indices.
        See https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#env-vars.
        Set to None in order to use all available GPUs. Note that GPUMD exit with an error
        when running with more than one GPU if your system is not large enough.
        Default: 0


    Example
    -------

    >>> calc = GPUNEP('nep.txt')
    >>> atoms.calc = calc
    >>> atoms.get_potential_energy()
    """

    command = 'gpumd'
    base_implemented_properties = ['energy', 'forces', 'stress']
    discard_results_on_any_change = True

    # We use list of tuples to define parameters for
    # MD simulations. Looks like a dictionary, but sometimes
    # we want to repeat the same keyword.
    base_single_point_parameters = [('dump_thermo', 1),
                                    ('dump_force', 1),
                                    ('dump_position', 1),
                                    ('velocity', 1e-24),
                                    ('time_step', 1e-6),  # 1 zeptosecond
                                    ('ensemble', 'nve'),
                                    ('run', 1)]

    def __init__(self,
                 model_filename: str,
                 directory: str = None,
                 label: str = 'GPUNEP',
                 atoms: Atoms = None,
                 command: str = command,
                 gpu_identifier_index: Union[int, None] = 0
                 ):
        if not os.path.exists(model_filename):
            raise FileNotFoundError(f'{model_filename} does not exist.')
        self.model_filename = str(model_filename)

        # Get model type from first row in nep.txt
        header, _ = _get_nep_contents(self.model_filename)
        self.model_type = header['model_type']
        self.supported_species = set(header['types'])
        self.nep_version = header['version']
        self.model_filename = model_filename

        self.implemented_properties = list(self.base_implemented_properties)
        self.single_point_parameters = self.base_single_point_parameters
        if 'charge' in self.model_type:
            # Only available for charge models
            self.implemented_properties.extend(
                ['charges', 'born_effective_charges'])
            qnep_parameters = [('dump_xyz', (-1, 1, 1, 'charges_and_bec.xyz', 'charge', 'bec'))]
            self.single_point_parameters = qnep_parameters + self.base_single_point_parameters

        # Determine run command
        # Determine whether to save stdout or not
        if directory is None and '>' not in command:
            # No need to save stdout if we run in temporary directory
            command += ' > /dev/null'
        elif '>' not in command:
            command += ' > stdout'
        self.command = command

        # Determine directory to run in
        self._use_temporary_directory = directory is None
        self._directory = directory
        if self._use_temporary_directory:
            self._make_new_tmp_directory()
        else:
            self._potential_path = os.path.relpath(
                os.path.abspath(self.model_filename), self._directory)

        # Override the profile in ~/.config/ase/config.ini.
        # See https://wiki.fysik.dtu.dk/ase/ase/
        #            calculators/calculators.html#calculator-configuration
        profile = GPUMDShellProfile(command, gpu_identifier_index)
        FileIOCalculator.__init__(self,
                                  directory=self._directory,
                                  label=label,
                                  atoms=atoms,
                                  profile=profile)

    def run_custom_md(
        self,
        parameters: List[Tuple[str, Any]],
        return_last_atoms: bool = False,
        only_prepare: bool = False,
    ):
        """
        Run a custom MD simulation.

        Parameters
        ----------
        parameters
            Parameters to be specified in the run.in file.
            The potential keyword is set automatically, all other
            keywords need to be set via this argument.
            Example::

                    [('dump_thermo', 100),
                     ('dump_position', 1000),
                     ('velocity', 300),
                     ('time_step', 1),
                     ('ensemble', ['nvt_ber', 300, 300, 100]),
                     ('run', 10000)]

        return_last_atoms
            If ``True`` the last saved snapshot will be returned.
        only_prepare
            If ``True`` the necessary input files will be written
             but the MD run will not be executed.

        Returns
        -------
            The last snapshot if :attr:`return_last_atoms` is ``True``.
        """
        if self._use_temporary_directory:
            self._make_new_tmp_directory()

        if self._use_temporary_directory and not return_last_atoms:
            raise ValueError('Refusing to run in temporary directory '
                             'and not returning atoms; all results will be gone.')

        if self._use_temporary_directory and only_prepare:
            raise ValueError('Refusing to only prepare in temporary directory, '
                             'all files will be removed.')

        # Write files and run
        FileIOCalculator.write_input(self, self.atoms)
        self._write_runfile(parameters)
        write_xyz(filename=os.path.join(self._directory, 'model.xyz'),
                  structure=self.atoms)

        if only_prepare:
            return None

        # Execute the calculation.
        self.execute()

        # Extract last snapshot if needed
        if return_last_atoms:
            last_atoms = ase_read(os.path.join(self._directory, 'movie.xyz'),
                                  format='extxyz', index=-1)

        if self._use_temporary_directory:
            self._clean()

        if return_last_atoms:
            return last_atoms
        else:
            return None

    def write_input(self, atoms, properties=None, system_changes=None):
        """
        Write the input files necessary for a single-point calculation.
        """
        if self._use_temporary_directory:
            self._make_new_tmp_directory()
        FileIOCalculator.write_input(self, atoms, properties, system_changes)
        self._write_runfile(parameters=self.single_point_parameters)
        write_xyz(filename=os.path.join(self._directory, 'model.xyz'),
                  structure=atoms)

    def _write_runfile(self, parameters):
        """Write run.in file to define input parameters for MD simulation.

        Parameters
        ----------
        parameters : dict
            Defines all key-value pairs used in run.in file
            (see GPUMD documentation for a complete list).
            Values can be either floats, integers, or lists/tuples.
        """
        if len(os.listdir(self._directory)) > 0:
            warnings.warn(f'{self._directory} is not empty.')

        with open(os.path.join(self._directory, 'run.in'), 'w') as f:
            # Custom potential is allowed but normally it can be deduced
            if 'potential' not in [keyval[0] for keyval in parameters]:
                f.write(f'potential {self._potential_path} \n')
            # Write all keywords with parameter(s)
            for key, val in parameters:
                f.write(f'{key} ')
                if isinstance(val, Iterable) and not isinstance(val, str):
                    for v in val:
                        f.write(f'{v} ')
                else:
                    f.write(f'{val}')
                f.write('\n')

    def get_potential_energy_and_stresses_from_file(self):
        """
        Extract potential energy (third column of last line in thermo.out) and stresses
        from thermo.out
        """
        data = np.loadtxt(os.path.join(self._directory, 'thermo.out'))
        if len(data.shape) == 1:
            line = data
        else:
            line = data[-1, :]

        # Energy
        energy = line[2]

        # Stress
        stress = [v for v in line[3:9]]
        stress = -GPa * np.array(stress)  # to eV/A^3

        if np.any(np.isnan(stress)) or np.isnan(energy):
            raise ValueError(f'Failed to extract energy and/or stresses:\n {line}')
        return energy, stress

    def _read_potential_energy_and_stresses(self):
        """Reads potential energy and stresses."""
        self.results['energy'], self.results['stress'] = \
            self.get_potential_energy_and_stresses_from_file()

    def get_forces_from_file(self):
        """
        Extract forces (in eV/A) from last snapshot in force.out
        """
        data = np.loadtxt(os.path.join(self._directory, 'force.out'))
        return data[-len(self.atoms):, :]

    def _read_forces(self):
        """Reads forces (the last snapshot in force.out) in eV/A"""
        self.results['forces'] = self.get_forces_from_file()

    def get_charges_and_becs_from_file(self):
        """Extract charges and Born Effective Charges from last
        snapshot in `charges_and_bec.xyz`"""
        structure = ase_read(os.path.join(self._directory, 'charges_and_bec.xyz'), '-1')
        charges = structure.get_charges()
        becs = structure.get_array('bec')
        return charges, becs

    def _read_charges_and_becs(self):
        """Reads charges and Born Effective Charges from file."""
        charges, becs = self.get_charges_and_becs_from_file()
        self.results['charges'] = charges
        self.results['born_effective_charges'] = becs

    def read_results(self):
        """
        Read results from last step of MD calculation.
        """
        self._read_potential_energy_and_stresses()
        self._read_forces()

        if 'charge' in self.model_type:
            self._read_charges_and_becs()
        if self._use_temporary_directory:
            self._clean()

    def _clean(self):
        """
        Remove directory with calculations.
        """
        shutil.rmtree(self._directory)

    def _make_new_tmp_directory(self):
        """
        Create a new temporary directory.
        """
        # We do not need to create a new temporary directory
        # if the current one is empty
        if self._directory is None or \
           (os.path.isdir(self._directory) and len(os.listdir(self._directory)) > 0):
            self._directory = tempfile.mkdtemp()
        self._potential_path = os.path.relpath(os.path.abspath(self.model_filename),
                                               self._directory)

    def set_atoms(self, atoms):
        """
        Set Atoms object.
        Used also when attaching calculator to Atoms object.
        """
        self.atoms = atoms
        self.results = {}

    def set_directory(self, directory):
        """
        Set path to a new directory. This makes it possible to run
        several calculations with the same calculator while saving
        all results
        """
        self._directory = directory
        self._use_temporary_directory = False
        self._potential_path = os.path.relpath(os.path.abspath(self.model_filename),
                                               self._directory)

    def get_born_effective_charges(
        self,
        atoms: Atoms = None,
        properties: List[str] = None,
        system_changes: List[str] = all_changes,
    ) -> np.ndarray:
        """Calculates (if needed) and returns the Born effective charges.
        Note that this requires a qNEP model.

        Parameters
        ----------
        atoms
            System for which to calculate properties, by default `None`.
        properties
            Properties to calculate, by default `None`.
        system_changes
            Changes to the system since last call, by default all_changes.
        """
        if 'born_effective_charges' not in self.implemented_properties:
            raise ValueError(
                'This model does not support the calculation of Born effective charges.')
        self.calculate(atoms, properties, system_changes)
        return self.results['born_effective_charges']
