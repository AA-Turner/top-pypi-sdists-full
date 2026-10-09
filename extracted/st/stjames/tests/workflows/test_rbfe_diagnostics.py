"""Test rbfe diagnostics behavior and validation."""

from stjames.workflows.relative_binding_free_energy_perturbation import (
    RBFEAnalysisError,
    RBFEConvergenceDiagnostics,
    RBFEConvergencePoint,
    RBFECycle,
    RBFEDiagnostics,
    RBFEEdgeDiagnostics,
    RBFEGraphEdge,
    RBFELegDiagnostics,
    RBFEMixingDiagnostics,
    RBFEOverlapDiagnostics,
)


def test_complex_overlap_analyses_remain_independent() -> None:
    """Final-production diagnostics do not overwrite the legacy reconstructed overlap."""
    overlap = RBFEOverlapDiagnostics(
        lambda_values=[0.0, 0.5001, 1.0],
        overlap_matrix=[[0.8, 0.2, 0.0], [0.2, 0.6, 0.2], [0.0, 0.2, 0.8]],
        adjacent_overlaps=[0.2, 0.2],
        minimum_adjacent_overlap=0.2,
        minimum_adjacent_lambda_pair=(0.0, 0.5),
        nonfinite_energy_count=1,
    )
    edge = RBFEGraphEdge(
        ligand_a="a",
        ligand_b="b",
        complex_lambda_values=[0.0, 1.0],
        complex_overlap_matrix=[[0.9, 0.1], [0.1, 0.9]],
        diagnostics=RBFEEdgeDiagnostics(complex=RBFELegDiagnostics(overlap=overlap)),
    )
    payload = edge.model_dump()
    assert payload["complex_lambda_values"] == [0.0, 1.0]
    assert payload["complex_overlap_matrix"] == [[0.9, 0.1], [0.1, 0.9]]
    assert payload["diagnostics"]["complex"]["overlap"]["lambda_values"] == [0.0, 0.5, 1.0]
    assert payload["diagnostics"]["complex"]["overlap"]["overlap_matrix"] == overlap.overlap_matrix

    restored = RBFEGraphEdge.model_validate_json(edge.model_dump_json())
    restored_payload = restored.model_dump()
    assert restored_payload["complex_lambda_values"] == [0.0, 1.0]
    assert restored_payload["complex_overlap_matrix"] == [[0.9, 0.1], [0.1, 0.9]]
    assert restored.diagnostics is not None
    assert restored.diagnostics.complex is not None
    assert restored.diagnostics.complex.overlap == overlap
    properties = RBFEGraphEdge.model_json_schema()["properties"]
    assert properties["complex_lambda_values"]["deprecated"] is True
    assert properties["complex_overlap_matrix"]["deprecated"] is True
    assert "legacy TMD bisection/reconstruct_ukln" in properties["complex_lambda_values"]["description"]
    assert "legacy TMD reconstruct_ukln" in properties["complex_overlap_matrix"]["description"]

    final_production_only = RBFEGraphEdge(
        ligand_a="a",
        ligand_b="b",
        diagnostics=RBFEEdgeDiagnostics(complex=RBFELegDiagnostics(overlap=overlap)),
    )
    final_production_payload = RBFEGraphEdge.model_validate_json(final_production_only.model_dump_json()).model_dump()
    assert "complex_lambda_values" not in final_production_payload
    assert "complex_overlap_matrix" not in final_production_payload

    legacy_with_empty_diagnostics = RBFEGraphEdge(
        ligand_a="a",
        ligand_b="b",
        complex_lambda_values=[0.0, 1.0],
        complex_overlap_matrix=[[0.9, 0.1], [0.1, 0.9]],
        diagnostics=RBFEEdgeDiagnostics(complex=RBFELegDiagnostics()),
    )
    assert legacy_with_empty_diagnostics.diagnostics is not None
    assert legacy_with_empty_diagnostics.diagnostics.complex is not None
    assert legacy_with_empty_diagnostics.diagnostics.complex.overlap is None


def test_leg_and_ddg_diagnostics_round_trip() -> None:
    """The schema preserves the three leg metrics and combined DDG convergence."""
    point = RBFEConvergencePoint(
        fraction=0.5001,
        frame_count=100,
        estimate=1.2345,
        uncertainty=0.1234,
    )
    convergence = RBFEConvergenceDiagnostics(
        forward_convergence=[point],
        reverse_convergence=[point],
    )
    mixing = RBFEMixingDiagnostics(
        neighbor_exchange_acceptance_rates=[0.8123, 0.7234],
        replicas_visiting_both_endpoints=3,
        complete_round_trip_count=2,
    )
    diagnostics = RBFEEdgeDiagnostics(
        complex=RBFELegDiagnostics(convergence=convergence, mixing=mixing),
        solvent=RBFELegDiagnostics(convergence=convergence, mixing=mixing),
        ddg=convergence,
        analysis_errors=[
            RBFEAnalysisError(
                family="overlap",
                leg="complex",
                explanation="production energies unavailable",
            )
        ],
    )

    restored = RBFEEdgeDiagnostics.model_validate_json(diagnostics.model_dump_json())
    assert restored == diagnostics


def test_normalized_cycle_closure_round_trip() -> None:
    """Normalized cycle closure survives graph-diagnostics serialization."""
    cycle = RBFECycle(
        ligands=["a", "b", "c"],
        closure_error=1.0,
        closure_error_uncertainty=0.5,
    )
    assert cycle.normalized_closure_error == 2.0
    diagnostics = RBFEDiagnostics(cycles=[cycle])
    restored = RBFEDiagnostics.model_validate_json(diagnostics.model_dump_json())
    assert restored == diagnostics
