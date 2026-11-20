"""Test logP workflow input validation."""

from pytest import mark, raises

from stjames import Molecule
from stjames.workflows.logp import LogPMethod, LogPWorkflow

_PALLADIUM_CHLORIDE = Molecule.from_xyz("3\n\nPd 0 0 0\nCl 2.3 0 0\nCl -2.3 0 0")


@mark.parametrize("method", [LogPMethod.CHEMPROP_SANGSTER2026, LogPMethod.CRIPPEN])
def test_smiles_methods_reject_structure(method: LogPMethod) -> None:
    """Require SMILES for both SMILES-based methods."""
    with raises(ValueError, match="only supported by the COSMO-RS"):
        LogPWorkflow(initial_molecule=_PALLADIUM_CHLORIDE, logp_method=method)


@mark.parametrize(("smiles", "molecule"), [("", None), ("CCO", _PALLADIUM_CHLORIDE)])
def test_cosmors_requires_exactly_one_input(smiles: str, molecule: Molecule | None) -> None:
    """Reject missing or ambiguous COSMO-RS input."""
    with raises(ValueError, match="exactly one"):
        LogPWorkflow(initial_smiles=smiles, initial_molecule=molecule, logp_method=LogPMethod.COSMORS)


def test_cosmors_rejects_periodic_structure() -> None:
    """Reject periodic cells for molecular COSMO-RS."""
    molecule = _PALLADIUM_CHLORIDE.model_copy(update={"cell": ((10, 0, 0), (0, 10, 0), (0, 0, 10))})
    with raises(ValueError, match="nonperiodic"):
        LogPWorkflow(initial_molecule=molecule, logp_method=LogPMethod.COSMORS)
