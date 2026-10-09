"""Spin-state prediction workflow."""

from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field, PositiveInt, field_validator

from ..base import round_float
from ..types import UUID
from .multistage_opt import MultiStageOptMixin
from .workflow import MoleculeWorkflow


class SpinState(BaseModel):
    """The result of a SpinState calculation.

    Attributes:
        multiplicity: multiplicity of the SpinState
        energy: energy of the optimized Molecule
        calculation: UUIDs of Calculations that produced this SpinState

    Examples:
    >>> from stjames.molecule import Atom, Molecule
    >>> He = Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=2, position=[0, 0, 0])])
    >>> SpinState(multiplicity=3, energy=-13.4291, calculation=['8a031a27-30d2-4ac7-8ade-efae9e9fc94a'])
    <SpinState 3 -13.429>
    """

    multiplicity: PositiveInt
    energy: Annotated[float, AfterValidator(round_float(6))]
    calculation: list[UUID | None]

    def __str__(self) -> str:
        """Return the workflow representation as text."""
        return repr(self)

    def __repr__(self) -> str:
        """Represent SpinState with its multiplicity and energy."""
        return f"<{type(self).__name__} {self.multiplicity} {self.energy:.3f}>"


class SpinStatesWorkflow(MoleculeWorkflow, MultiStageOptMixin):
    """Workflow for computing spin states of molecules.

    Uses the modes from MultiStageOptSettings.

    Influenced by:
    [Performance of Quantum Chemistry Methods for Benchmark Set of Spin–State
    Energetics Derived from Experimental Data of 17 Transition Metal Complexes
    (SSE17)](https://chemrxiv.org/engage/chemrxiv/article-details/66a8b15cc9c6a5c07a792487)

    Inherited

    Attributes:
        initial_molecule: Molecule of interest
        mode: Mode for workflow
        multistage_opt_settings: settings for optimization and singlepoint

        states: multiplicities of the spin states targeted
        spin_states: resulting spin states data

    Examples:
    >>> from stjames.molecule import Atom, Molecule
    >>> from stjames.workflows.multistage_opt import MultiStageOptSettings
    >>> from stjames.settings import Settings
    >>> from stjames.method import Method
    >>> He = Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=2, position=[0, 0, 0])])
    >>> msos = MultiStageOptSettings(optimization_settings=[Settings(method=Method.GFN2_XTB)], singlepoint_settings=Settings(method=Method.R2SCAN3C))
    >>> ss = SpinStatesWorkflow(initial_molecule=He, states=[1, 3, 5], multistage_opt_settings=msos)
    >>> str(ss)
    '<SpinStatesWorkflow [1, 3, 5] r2scan_3c//gfn2_xtb>'
    """

    states: list[PositiveInt]

    # Results
    spin_states: list[SpinState] = Field(default_factory=list)

    def __repr__(self) -> str:
        """Represent SpinStatesWorkflow with its spin states and level of theory."""
        return f"<{type(self).__name__} {self.states} {self.level_of_theory}>"

    def __len__(self) -> int:
        """Return the number of spin states."""
        return len(self.states)

    @property
    def level_of_theory(self) -> str:
        """Report the optimization level of theory.

        Returns:
            level-of-theory label
        """
        return self.multistage_opt_settings.level_of_theory

    @field_validator("states")
    @classmethod
    def validate_states(cls, states: list[PositiveInt]) -> list[PositiveInt]:
        """Confirm that all spin states are valid.

        Args:
            states: spin states to validate
        """
        if not states:
            raise ValueError("Expected at least one spin state.")

        if any((states[0] - mult) % 2 for mult in states):
            raise ValueError(f"Inconsistent multiplicities found: {states}")

        return states

    def str_results(self) -> str:
        """Format the multiplicity and energy of each spin state.

        Returns:
            readable summary of spin-state energies
        """
        return "SpinStatesResults\n" + "\n".join(f"  {ss.multiplicity}: {ss.energy:>5.2f}" for ss in self.spin_states)

    @property
    def energies(self) -> list[float]:
        """Collect the energies of all spin states.

        Returns:
            spin-state energies in result order
        """
        return [ss.energy for ss in self.spin_states]

    @field_validator("spin_states")
    @classmethod
    def validate_spin_states(cls, spin_states: list[SpinState]) -> list[SpinState]:
        """Ensure that all spin states have consistent results.

        Args:
            spin_states: spin-state results to validate
        """
        mults = [ss.multiplicity for ss in spin_states]

        if len(mults) != len(set(mults)):
            raise ValueError(f"Duplicate multiplicities found: {mults}")

        if any((mults[0] - mult) % 2 for mult in mults[1:]):
            raise ValueError(f"Inconsistent multiplicities found: {mults}")

        return spin_states
