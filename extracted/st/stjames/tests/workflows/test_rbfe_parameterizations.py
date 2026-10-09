"""Persistence of exact endpoint parameters in RBFE workflow payloads."""

from stjames import Atom, Molecule
from stjames.forcefield import LigandParameterizationResult, MangoParameterSetV1, NonbondedParameter
from stjames.workflows.relative_binding_free_energy_perturbation import (
    RBFEGraph,
    RBFEGraphEdge,
    RelativeBindingFreeEnergyPerturbationWorkflow,
    TMDRBFESettings,
)


def test_endpoint_parameters_and_diagnostics_survive_workflow_json() -> None:
    """Workflow serialization retains numerical parameters and nested fit diagnostics."""
    molecule = Molecule(charge=0, multiplicity=1, atoms=[Atom(atomic_number=2, position=(0, 0, 0))], smiles="[He]")
    workflow = RelativeBindingFreeEnergyPerturbationWorkflow(
        ligands={"a": molecule, "b": molecule},
        graph=RBFEGraph(edges=[RBFEGraphEdge(ligand_a="a", ligand_b="b")]),
        target="00000000-0000-0000-0000-000000000001",
        protein="00000000-0000-0000-0000-000000000001",
        settings=TMDRBFESettings(),
    )
    assert workflow.ligand_parameterizations == workflow.small_molecule_parameterizations == {}
    parameters = MangoParameterSetV1(
        mapped_smiles="[He:1]",
        nonbonded=[NonbondedParameter(atom_map=1, charge=0, sigma_angstrom=2.123456789012345, epsilon_kj_mol=0.031234567890123)],
        bonds=[],
        angles=[],
        proper_torsions=[],
        improper_torsions=[],
        release_id="mango-2.0.0",
    )
    result = LigandParameterizationResult(
        outcome="mango",
        parameter_set=parameters,
        diagnostics={"rounds": [{"bound_hits": 2, "coefficients": [0.123456789012345]}], "fitted": True},
    )
    workflow.ligand_parameterizations["a"] = result
    workflow.small_molecule_parameterizations["COF"] = result
    restored = RelativeBindingFreeEnergyPerturbationWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.ligand_parameterizations["a"] == result
    assert restored.small_molecule_parameterizations["COF"] == result


def test_failed_parameterization_retains_error() -> None:
    """Failed endpoints retain their error and diagnostics."""
    failure = LigandParameterizationResult(outcome="failed", error="reference failed", diagnostics={"stage": "reference"})
    assert LigandParameterizationResult.model_validate_json(failure.model_dump_json()) == failure
