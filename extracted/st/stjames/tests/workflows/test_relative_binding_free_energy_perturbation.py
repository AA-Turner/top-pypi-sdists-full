"""Tests for relative binding free-energy workflow schemas."""

import math
from typing import Literal

import pytest
from pydantic import ValidationError

from stjames import (
    Atom,
    Molecule,
    RBFEEdgeTopology,
    RBFEReceptorAnchorAtom,
    RBFESeparatedTopologyAnchors,
    RBFESeparatedTopologyMetadata,
    RBFESeparatedTopologyTetherAtoms,
    TMDSeparatedTopologySettings,
)
from stjames.workflows.relative_binding_free_energy_perturbation import (
    RBFEGraph,
    RBFEGraphEdge,
    RBFEGraphWorkflow,
    RelativeBindingFreeEnergyPerturbationWorkflow,
    TMDRBFESettings,
)


def _ligands(charge_b: int = 0) -> dict[str, Molecule]:
    """Return minimal ligand mapping accepted by graph workflow validation."""
    ligand = Molecule(
        charge=0,
        multiplicity=1,
        atoms=[Atom(atomic_number=2, position=(0.0, 0.0, 0.0))],
    )
    ligand_b = ligand.model_copy(update={"charge": charge_b, "multiplicity": 2 if charge_b else 1}, deep=True)
    return {"a": ligand, "b": ligand_b}


def test_legacy_edge_defaults_to_single_topology() -> None:
    """Legacy payloads without topology remain single-topology edges."""
    edge = RBFEGraphEdge.model_validate({"ligand_a": "a", "ligand_b": "b"})

    assert edge.topology == RBFEEdgeTopology.SINGLE_TOPOLOGY
    assert edge.model_dump(mode="json")["topology"] == "single_topology"


@pytest.mark.parametrize("topology", list(RBFEEdgeTopology))
def test_edge_topology_round_trip(topology: RBFEEdgeTopology) -> None:
    """Every edge topology serializes and deserializes without loss."""
    edge = RBFEGraphEdge(ligand_a="a", ligand_b="b", topology=topology)

    restored = RBFEGraphEdge.model_validate_json(edge.model_dump_json())

    assert restored == edge
    assert restored.topology is topology


def test_separated_topology_settings_expose_only_supported_controls() -> None:
    """Public settings omit TMD's advanced alchemical schedule knobs."""
    settings = TMDSeparatedTopologySettings()

    assert settings.anchor_selection_method == "baumann_rmsf"
    assert settings.anchor_equilibration.n_eq_steps == 10_000
    assert settings.anchor_equilibration.n_frames == 100
    assert settings.restraints.bond_force_constant == 500.0
    assert settings.restraints.angle_force_constant == 200.0
    assert settings.restraints.dihedral_force_constant == 10.0
    assert set(settings.model_dump()) == {"anchor_selection_method", "anchor_equilibration", "restraints"}


def test_separated_topology_settings_reject_invalid_controls() -> None:
    """Equilibration lengths and restraint constants must be positive."""
    with pytest.raises(ValidationError):
        TMDSeparatedTopologySettings(anchor_equilibration={"n_frames": 0})
    with pytest.raises(ValidationError):
        TMDSeparatedTopologySettings(restraints={"bond_force_constant": 0})


def _separated_topology_metadata() -> RBFESeparatedTopologyMetadata:
    receptor_atoms = tuple(
        RBFEReceptorAnchorAtom(
            index=index,
            chain_id="A",
            residue_name="ALA",
            residue_id=str(index + 10),
            atom_name=atom_name,
        )
        for index, atom_name in enumerate(("CA", "C", "N"))
    )
    return RBFESeparatedTopologyMetadata(
        anchors=RBFESeparatedTopologyAnchors(
            receptor_atoms=receptor_atoms,
            ligand_a_atoms=(1, 2, 3),
            ligand_b_atoms=(4, 5, 6),
        ),
        tether_atoms=RBFESeparatedTopologyTetherAtoms(ligand_a=7, ligand_b=8),
        complex_raw_dg=1.2345,
        restraint_correction_a=0.5124,
        restraint_correction_b=0.8126,
    )


def test_separated_topology_metadata_round_trip() -> None:
    """Resolved atom identities and correction components remain interpretable."""
    edge = RBFEGraphEdge(
        ligand_a="a",
        ligand_b="b",
        topology=RBFEEdgeTopology.SEPARATED_TOPOLOGY,
        separated_topology_metadata=_separated_topology_metadata(),
    )

    restored = RBFEGraphEdge.model_validate_json(edge.model_dump_json())

    assert restored == edge
    assert restored.separated_topology_metadata is not None
    assert restored.separated_topology_metadata.anchors is not None
    assert restored.separated_topology_metadata.anchors.receptor_atoms[0].atom_name == "CA"
    assert restored.separated_topology_metadata.complex_raw_dg == 1.234
    assert restored.separated_topology_metadata.restraint_correction == 0.301


def test_edge_rejects_fields_for_the_other_topology() -> None:
    """Atom maps and separated metadata cannot leak across topology strategies."""
    with pytest.raises(ValueError, match="cannot define an atom-mapping core"):
        RBFEGraphEdge(
            ligand_a="a",
            ligand_b="b",
            topology=RBFEEdgeTopology.SEPARATED_TOPOLOGY,
            core=[(0, 0)],
        )
    with pytest.raises(ValueError, match="requires topology='separated_topology'"):
        RBFEGraphEdge(
            ligand_a="a",
            ligand_b="b",
            separated_topology_metadata=RBFESeparatedTopologyMetadata(),
        )


def test_separated_topology_planning_score_defaults_to_none() -> None:
    """Separated-topology candidates remain opt-in."""
    assert RBFEGraphWorkflow(ligands=_ligands()).separated_topology_planning_score is None


@pytest.mark.parametrize("score", [-1.0, math.inf, -math.inf, math.nan])
def test_separated_topology_planning_score_rejects_invalid_values(score: float) -> None:
    """Separated-topology planning scores must be finite and non-negative."""
    with pytest.raises(ValueError, match="finite and non-negative"):
        RBFEGraphWorkflow(ligands=_ligands(), separated_topology_planning_score=score)


def test_mixed_star_graph_is_rejected() -> None:
    """Separated-topology candidates are supported only by greedy graph construction."""
    with pytest.raises(ValueError, match="only mode='greedy'"):
        RBFEGraphWorkflow(
            ligands=_ligands(),
            mode="star_map",
            hub_compound_id="a",
            separated_topology_planning_score=25.0,
        )


def test_mixed_graph_normalizes_omitted_scorer() -> None:
    """Enabling separated topology changes an omitted default to dummy-atom scoring."""
    workflow = RBFEGraphWorkflow(ligands=_ligands(), separated_topology_planning_score=25.0)

    assert workflow.greedy_scoring == "dummy_atoms"


@pytest.mark.parametrize("scorer", ["best", "jaccard"])
def test_mixed_graph_rejects_explicit_incompatible_scorer(
    scorer: Literal["best", "jaccard"],
) -> None:
    """Explicit non-dummy scorers are not silently replaced in mixed mode."""
    with pytest.raises(ValueError, match="requires greedy_scoring='dummy_atoms'"):
        RBFEGraphWorkflow(
            ligands=_ligands(),
            separated_topology_planning_score=25.0,
            greedy_scoring=scorer,
        )


@pytest.mark.parametrize(
    ("settings", "charge_b", "message"),
    [
        (TMDRBFESettings(legs=["vacuum"]), 0, "only solvent and complex legs"),
        (TMDRBFESettings(), 1, "equal formal charge"),
    ],
)
def test_workflow_validates_separated_topology_constraints(
    settings: TMDRBFESettings,
    charge_b: int,
    message: str,
) -> None:
    """Separated topology has narrower leg and charge support."""
    edge = RBFEGraphEdge(
        ligand_a="a",
        ligand_b="b",
        topology=RBFEEdgeTopology.SEPARATED_TOPOLOGY,
    )
    with pytest.raises(ValueError, match=message):
        RelativeBindingFreeEnergyPerturbationWorkflow(
            ligands=_ligands(charge_b),
            graph=RBFEGraph(edges=[edge]),
            protein="protein-uuid",
            settings=settings,
        )


def _workflow_with_small_molecules(
    small_molecules: dict[str | int, str | None],
) -> RelativeBindingFreeEnergyPerturbationWorkflow:
    """Build a minimal RBFE workflow with fixed receptor-side molecules."""
    return RelativeBindingFreeEnergyPerturbationWorkflow(
        ligands=_ligands(),
        graph=RBFEGraph(edges=[RBFEGraphEdge(ligand_a="a", ligand_b="b")]),
        protein="protein-uuid",
        settings=TMDRBFESettings(),
        small_molecules=small_molecules,
    )


def test_workflow_harmonizes_canonical_protein() -> None:
    """Canonical protein input populates the deprecated target alias."""
    workflow = _workflow_with_small_molecules({})

    assert workflow.protein == "protein-uuid"
    assert workflow.target == "protein-uuid"


def test_workflow_accepts_legacy_target_payload() -> None:
    """Legacy serialized payloads may still supply only target."""
    workflow = RelativeBindingFreeEnergyPerturbationWorkflow.model_validate(
        {
            "ligands": _ligands(),
            "graph": RBFEGraph(edges=[RBFEGraphEdge(ligand_a="a", ligand_b="b")]),
            "target": "protein-uuid",
            "settings": TMDRBFESettings(),
        }
    )

    assert workflow.protein == "protein-uuid"
    assert workflow.target == "protein-uuid"


def test_workflow_accepts_fixed_small_molecules() -> None:
    """Parameterized cofactors and known ions are valid non-candidate inputs."""
    workflow = _workflow_with_small_molecules({"NAD": "NC(=O)c1ccncc1", "ZN": None})

    assert workflow.small_molecules == {"NAD": "NC(=O)c1ccncc1", "ZN": None}


def test_workflow_uses_shared_small_molecule_validation() -> None:
    """RBFE applies the shared non-polymer declaration contract."""
    with pytest.raises(ValidationError, match="non-polymer residue entry"):
        _workflow_with_small_molecules({"NAD": None})


def test_solvent_trajectory_outputs_round_trip_independently() -> None:
    """Both legs retain distinct artifacts; old edges need no solvent fields."""
    old = RBFEGraphEdge(ligand_a="a", ligand_b="b")
    assert old.solvent_trajectories is None
    assert old.solvent_protein_uuid is None
    assert old.solvent_ligand_atom_indices is None
    edge = RBFEGraphEdge.model_validate(
        {
            "ligand_a": "a",
            "ligand_b": "b",
            "complex_trajectories": {"0.0": {"uuid": "00000000-0000-0000-0000-000000000001"}},
            "complex_protein_uuid": "00000000-0000-0000-0000-000000000002",
            "complex_ligand_atom_indices": {"ligand_a": [100, 101], "ligand_b": [102, 103]},
            "solvent_trajectories": {
                "0.0": {"uuid": "00000000-0000-0000-0000-000000000003"},
                "1.0": {"uuid": "00000000-0000-0000-0000-000000000004"},
            },
            "solvent_protein_uuid": "00000000-0000-0000-0000-000000000005",
            "solvent_ligand_atom_indices": {"ligand_a": [30, 31], "ligand_b": [32, 33]},
        }
    )
    restored = RBFEGraphEdge.model_validate_json(edge.model_dump_json())
    assert restored == edge
    assert restored.solvent_trajectories is not None
    assert set(restored.solvent_trajectories) == {0.0, 1.0}
    assert restored.solvent_protein_uuid != restored.complex_protein_uuid


def test_cofactor_indices_survive_json_round_trip() -> None:
    """Restore SDK integer keys and frontend string keys before backend selection."""
    workflow = _workflow_with_small_molecules({100: "OCCO", "EDO": "OCCO", "ZN": None})
    payload = workflow.model_dump(mode="json")
    assert payload["small_molecules"]["100"] == "OCCO"
    assert RelativeBindingFreeEnergyPerturbationWorkflow.model_validate(payload).small_molecules == workflow.small_molecules
    assert RelativeBindingFreeEnergyPerturbationWorkflow.model_validate_json(workflow.model_dump_json()).small_molecules == workflow.small_molecules
