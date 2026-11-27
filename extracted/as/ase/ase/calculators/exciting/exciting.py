"""ASE Calculator for the ground state exciting DFT code.

Exciting calculator class in this file allow for writing exciting input
files using ASE Atoms object that allow for the compiled exciting binary
to run DFT on the geometry/material defined in the Atoms object. Also gives
access to developer to a lightweight parser (lighter weight than NOMAD or
the exciting parser in the exciting repository) to capture ground state
properties.

Note: excitingtools must be installed using `pip install excitingtools` to
use this calculator.
"""

from collections.abc import Mapping
from os import PathLike
from pathlib import Path
from typing import Any

import ase.io.exciting
from ase.calculators.calculator import PropertyNotImplementedError
from ase.calculators.exciting.runner import (
    SimpleBinaryRunner,
    SubprocessRunResults,
)
from ase.calculators.genericfileio import (
    BaseProfile,
    CalculatorTemplate,
    GenericFileIOCalculator,
)


class ExcitingProfile(BaseProfile):
    """Defines all quantities that are configurable for a given machine.

    Follows the generic pattern BUT currently not used by our calculator as:
       * species_path is part of the input file in exciting.
       * OnlyTypo fix part of the profile used in the base class is the run
         method, which is part of the BinaryRunner class.
    """

    configvars = {'species_path'}

    def __init__(self, command, species_path=None, **kwargs):
        super().__init__(command, **kwargs)

        self.species_path = species_path

    def version(self):
        """Return exciting version."""
        # TARP No way to get the version for the binary in use
        return

    # Machine specific config files in the config
    # species_file goes in the config
    # binary file in the config.
    # options for that, parallel info dictionary.
    # Number of threads and stuff like that.

    def get_calculator_command(self, input_file):
        """Returns command to run binary as a list of strings."""
        # input_file unused for exciting, it looks for input.xml in run
        # directory.
        if input_file is None:
            return []
        else:
            return [str(input_file)]


class ExcitingGroundStateTemplate(CalculatorTemplate):
    """Template for Ground State Exciting Calculator

    Abstract methods inherited from the base class:
        * write_input
        * execute
        * read_results
    """

    parser = {'info.xml': ase.io.exciting.parse_output}
    output_names = list(parser)
    # Use frozenset since the CalculatorTemplate enforces it.
    implemented_properties = frozenset(['energy', 'forces'])
    _label = 'exciting'

    def __init__(self):
        super().__init__('exciting', self.implemented_properties)
        self.errorname = f'{self._label}.err'

    @staticmethod
    def _require_forces(input_parameters):
        """Expect ASE always wants forces, enforce setting in input_parameters.

        Parameters
        ----------
        input_parameters : dict | ExcitingGroundStateInput
            Exciting ground state input parameters.

        Returns
        -------
        ExcitingGroundStateInput
            Ground state input parameters, with "compute forces" set to true.

        """
        from excitingtools import ExcitingGroundStateInput

        input_parameters = ExcitingGroundStateInput(input_parameters)
        input_parameters.tforce = True
        return input_parameters

    def write_input(
        self,
        profile: ExcitingProfile,  # ase test linter enforces method signatures
        # be consistent with the
        # abstract method that it implements
        directory: PathLike,
        atoms: ase.Atoms,
        parameters: dict,
        properties=None,
    ):
        """Write an exciting input.xml file based on the input args.

        Parameters
        ----------
        profile : ExcitingProfile
            Exciting code profile.
        directory : PathLike
            Directory in which to run calculator.
        atoms : Atoms
            ASE Atoms object.
        parameters : dict
            Exciting ground state input parameters, in a dictionary.
            Expect species_path, title and ground_state data,
            either in an object or as dict.
        properties : None
            Base method's API expects the physical properties
            expected from a ground state calculation, for example energies
            and forces. For us this is not used.

        """
        # Create a copy of the parameters dictionary so we don't
        # modify the callers dictionary.
        parameters_dict = parameters
        required_keys = {'title', 'species_path', 'ground_state_input'}
        assert required_keys <= set(parameters_dict)
        file_name = Path(directory) / 'input.xml'
        species_path = parameters_dict.pop('species_path')
        title = parameters_dict.pop('title')
        # We can also pass additional parameters which are actually called
        # properties in the exciting input xml. We don't use this term
        # since ASE use properties to refer to results of a calculation
        # (e.g. force, energy).
        if 'properties_input' not in parameters_dict:
            parameters_dict['properties_input'] = None

        ase.io.exciting.write_input_xml_file(
            file_name=file_name,
            atoms=atoms,
            ground_state_input=parameters_dict['ground_state_input'],
            species_path=species_path,
            title=title,
            properties_input=parameters_dict['properties_input'],
        )

    def execute(self, directory: PathLike, profile) -> SubprocessRunResults:
        """Given an exciting calculation profile, execute the calculation.

        When executing an exciting calculation, you need to call run on an
        exciting binary runner which is stored as the profile variable. The
        binary runner at initialization will set all of the directory
        information so we don't use this variable again here.

        Parameters
        ----------
        directory : PathLike
            Not used but comes from the base class.
        profile
            This name comes from the superclass CalculatorTemplate.
            It should be an instance of an exciting.runner.SimpleBinaryRunner.

        Returns
        -------
        SubprocessRunResults
            Results of the subprocess.run command.

        """
        return profile.run()

    def read_results(self, directory: PathLike) -> Mapping[str, Any]:
        """Parse results from each ground state output file.

        Note we allow for the ability for there to be multiple output files.

        Parameters
        ----------
        directory : PathLike
            Directory path to output file from exciting simulation.

        Returns
        -------
        Mapping[str, Any]
            dictionary of results. This can be fed into
            ExcitingGroundStateResults if the user wants to access properties
            more easily.

        """
        results = {}
        for file_name in self.output_names:
            full_file_path = Path(directory) / file_name
            result: dict = self.parser[file_name](full_file_path)
            results.update(result)
        return results

    def load_profile(self, cfg, **kwargs):
        """ExcitingProfile can be created via a config file.

        Alternative to this method the profile can be created with it's
        init method. This method allows for more settings to be passed.
        """
        return ExcitingProfile.from_config(cfg, self.name, **kwargs)


class ExcitingGroundStateResults:
    """Exciting Ground State Results."""

    def __init__(self, results: dict) -> None:
        self.results = results
        self.final_scl_iteration = list(results['scl'].keys())[-1]

    def total_energy(self) -> float:
        """Return total energy of system."""
        # TODO(Alex) We should a common list of keys somewhere
        # such that parser -> results -> getters are consistent
        return float(
            self.results['scl'][self.final_scl_iteration]['Total energy']
        )

    def band_gap(self) -> float:
        """Return the estimated fundamental gap from the exciting sim."""
        return float(
            self.results['scl'][self.final_scl_iteration][
                'Estimated fundamental gap'
            ]
        )

    def forces(self):
        """Return forces present on the system.

        Currently, not all exciting simulations return forces. We leave this
        definition for future revisions.
        """
        raise PropertyNotImplementedError

    def stress(self):
        """Get the stress on the system.

        Right now exciting does not yet calculate the stress on the system so
        this won't work for the time being.
        """
        raise PropertyNotImplementedError


class ExcitingGroundStateCalculator(GenericFileIOCalculator):
    """Class for the ground state calculation.

    Parameters
    ----------
    runner : SimpleBinaryRunner
        Binary runner that will execute an exciting calculation and
        return a result.
    ground_state_input : dict | ExcitingGroundStateInput
        Dictionary of ground state settings for example
        {'rgkmax': 8.0, 'autormt': True} or an object of type
        ExcitingGroundStateInput.
    directory : str
        Directory in which to run the job.
    species_path : str
        Path to the location of exciting's species files.
    title : str, default: 'ASE-generated input'
        Job name written to input.xml.

    Examples
    --------
    >>> atoms: Atoms
    >>> gs_calculator = ExcitingGroundState(runner, ground_state_input)
    >>> results: ExcitingGroundStateResults = gs_calculator.calculate(atoms)

    """

    def __init__(
        self,
        *,
        runner: SimpleBinaryRunner,
        ground_state_input,
        directory='./',
        species_path='./',
        title='ASE-generated input',
        parameters: dict[str, Any] | None = None,
    ):
        self.runner = runner
        # Package data to be passed to
        # ExcitingGroundStateTemplate.write_input(..., input_parameters, ...)
        # Structure not included, as it's passed when one calls .calculate
        # method directly.
        required_params = {
            'title': title,
            'species_path': species_path,
            'ground_state_input': ground_state_input,
        }
        # Set parameters to an empty dict if it is None (or Falsey). This
        # is needed for the next line.
        parameters = parameters or {}
        # Add key, value paris from required_params if they are not defined
        # in parmaters.
        parameters = required_params | parameters
        # GenericFileIOCalculator expects a `profile`
        # containing machine-specific settings, however, in exciting's case,
        # the species file are defined in the input XML (hence passed in the
        # parameters argument) and the only other machine-specific setting is
        # the BinaryRunner. Furthermore, in GenericFileIOCalculator.calculate,
        # profile is only used to provide a run method. We therefore pass the
        # BinaryRunner in the place of a profile.
        super().__init__(
            profile=runner,
            template=ExcitingGroundStateTemplate(),
            directory=directory,
            parameters=parameters,
        )
