"""Test nmr behavior and validation."""

from pytest import fixture, raises

from stjames import Molecule
from stjames.solvent import ALPB_SOLVENTS, CPCMX_SOLVENTS, Solvent, SolventModel
from stjames.workflows import NMRSpectroscopyWorkflow
from stjames.workflows.nmr import NMR_SOLVENT_MODELS, NMR_SUPPORTED_SOLVENTS, NMRCoupling


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


def test_basic(water: Molecule) -> None:
    """Choose NMR calculation settings for each accuracy mode."""
    nmr = NMRSpectroscopyWorkflow(initial_molecule=water)

    assert nmr.solvent == Solvent.CHLOROFORM

    nmr.per_conformer_chemical_shifts = [
        [0.0, 10.0, 20.0],
        [6.0, 12.0, 24.0],
    ]

    nmr.chemical_shifts = [3.0, 11.0, 22.0]

    assert len(nmr.chemical_shifts) == 3
    assert len(nmr.per_conformer_chemical_shifts) == 2


def test_supported_solvent(water: Molecule) -> None:
    """Verify supported solvent."""
    for solvent in NMR_SOLVENT_MODELS:
        assert NMRSpectroscopyWorkflow(initial_molecule=water, solvent=solvent).solvent == solvent


def test_unsupported_solvent(water: Molecule) -> None:
    """Verify unsupported solvent."""
    with raises(ValueError, match="not supported for NMR prediction"):
        NMRSpectroscopyWorkflow(initial_molecule=water, solvent=Solvent.HEXANE)


def test_solvent_model_derivation() -> None:
    """Verify solvent model derivation."""
    assert set(NMR_SOLVENT_MODELS) == NMR_SUPPORTED_SOLVENTS
    for solvent, model in NMR_SOLVENT_MODELS.items():
        assert solvent in (CPCMX_SOLVENTS if model == SolventModel.CPCMX else ALPB_SOLVENTS)
        if solvent in CPCMX_SOLVENTS:
            assert model == SolventModel.CPCMX


def test_predicted_couplings(water: Molecule) -> None:
    """Verify predicted couplings."""
    coupling = NMRCoupling(
        atom_pairs=[(0, 2)],
        bond_distance=2,
        coupling_hz=7.12345,
        conformer_sd_hz=0.45678,
        uncertainty_hz=0.98765,
        model="test-model",
    )
    nmr = NMRSpectroscopyWorkflow(initial_molecule=water, predicted_couplings=[coupling])

    assert coupling.nuclei == (1, 1)
    assert coupling.coupling_hz == 7.123
    assert coupling.conformer_sd_hz == 0.457
    assert coupling.uncertainty_hz == 0.988
    assert nmr.predicted_couplings == [coupling]
