"""Test ion mobility behavior and validation."""

from pytest import fixture, raises

from stjames import Molecule
from stjames.workflows import IonMobilityWorkflow
from stjames.workflows.ion_mobility import IonMobilityForcefieldElement


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


def test_basic(water: Molecule) -> None:
    """Initialize ion mobility workflows with supported accuracy modes."""
    wf = IonMobilityWorkflow(
        initial_molecule=water,
        forcefield=[
            IonMobilityForcefieldElement(name="oxygen", atomic_number=8, mass=16.00, sigma=0.5, epsilon=0.5),
            IonMobilityForcefieldElement(name="hydrogen", atomic_number=1, mass=1.01, sigma=0.5, epsilon=0.5),
        ],
    )

    assert wf.forcefield is not None
    assert len(wf.forcefield) == 2

    with raises(ValueError):
        IonMobilityWorkflow(
            initial_molecule=water,
            forcefield=[
                IonMobilityForcefieldElement(name="oxygen", atomic_number=8, mass=16.00, sigma=0.5, epsilon=0.5),
            ],
        )
