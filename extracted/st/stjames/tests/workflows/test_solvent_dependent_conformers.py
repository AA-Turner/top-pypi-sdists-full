"""Test solvent-dependent conformer energy precision and component serialization."""

from pytest import approx

from stjames.solvent import Solvent
from stjames.workflows.solvent_dependent_conformers import SolventDependentConformer


def test_energy_components_preserve_microhartree_precision() -> None:
    """Preserve sub-millihartree differences and individual energy components through JSON."""
    conformer = SolventDependentConformer(
        free_energy_by_solvent={Solvent.WATER: -100.11790015, Solvent.HEXANE: -100.11760015},
        singlepoint_energy=-100.1234567,
        rrho_correction=0.01234567,
        solvation_free_energy_by_solvent={Solvent.WATER: -0.00678912, Solvent.HEXANE: -0.00648912},
        relative_free_energy_by_solvent={Solvent.WATER: 0.123456, Solvent.HEXANE: 0.654321},
        population_by_solvent={Solvent.WATER: 0.876543, Solvent.HEXANE: 0.345678},
    )
    restored = SolventDependentConformer.model_validate_json(conformer.model_dump_json())
    assert restored.free_energy_by_solvent == {Solvent.WATER: -100.117900, Solvent.HEXANE: -100.117600}
    assert restored.free_energy_by_solvent[Solvent.HEXANE] - restored.free_energy_by_solvent[Solvent.WATER] == approx(0.0003)
    assert restored.singlepoint_energy == -100.123457
    assert restored.rrho_correction == 0.012346
    assert restored.solvation_free_energy_by_solvent == {Solvent.WATER: -0.006789, Solvent.HEXANE: -0.006489}
    assert restored.relative_free_energy_by_solvent == {Solvent.WATER: 0.123, Solvent.HEXANE: 0.654}
    assert restored.population_by_solvent == {Solvent.WATER: 0.877, Solvent.HEXANE: 0.346}
