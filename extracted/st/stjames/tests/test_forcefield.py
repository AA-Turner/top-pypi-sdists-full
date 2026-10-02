import pytest
from pydantic import ValidationError

from stjames.forcefield import (
    AngleParameter,
    BondParameter,
    LigandParameterizationResult,
    MangoParameterSetV1,
    NonbondedParameter,
    PeriodicTorsionTerm,
    TorsionParameter,
)
from stjames.method import FF_METHODS, FORCE_FIELD_METHODS, Method


def parameter_set() -> MangoParameterSetV1:
    return MangoParameterSetV1(
        mapped_smiles="[C:1]([H:2])([H:3])([H:4])[H:5]",
        nonbonded=[
            NonbondedParameter(
                atom_map=atom_map,
                charge=-0.4 if atom_map == 1 else 0.1,
                sigma_angstrom=3.0,
                epsilon_kj_mol=0.1,
            )
            for atom_map in range(1, 6)
        ],
        bonds=[
            BondParameter(
                atom_maps=(1, atom_map),
                length_angstrom=1.09,
                force_constant_kj_mol_angstrom2=300.0,
            )
            for atom_map in range(2, 6)
        ],
        angles=[
            AngleParameter(
                atom_maps=(2, 1, 3),
                angle_radians=1.91,
                force_constant_kj_mol_radian2=50.0,
            )
        ],
        proper_torsions=[
            TorsionParameter(
                atom_maps=(2, 1, 3, 4),
                terms=[
                    PeriodicTorsionTerm(
                        periodicity=3,
                        phase_radians=0.0,
                        force_constant_kj_mol=0.25,
                    )
                ],
            )
        ],
        improper_torsions=[],
        release_id="mango-1.0.0",
        manifest_sha256="a" * 64,
    )


def test_parameter_set_round_trip_preserves_discriminator_and_maps() -> None:
    original = parameter_set()
    restored = MangoParameterSetV1.model_validate_json(original.model_dump_json())

    assert restored == original
    assert restored.parameter_set_type == "mango_parameter_set_v1"
    assert [parameter.atom_map for parameter in restored.nonbonded] == [1, 2, 3, 4, 5]


def test_result_round_trip_and_invariants() -> None:
    original = LigandParameterizationResult(
        outcome="mango",
        parameter_set=parameter_set(),
    )
    assert LigandParameterizationResult.model_validate_json(original.model_dump_json()) == original
    with pytest.raises(ValidationError, match="must include an error"):
        LigandParameterizationResult(outcome="failed")
    with pytest.raises(ValidationError, match="must contain a parameter set"):
        LigandParameterizationResult(outcome="mango")


def test_force_fields_route_to_openff_engine() -> None:
    assert Method("mango_1_0_0") is Method.MANGO_1_0_0
    assert Method.MANGO_1_0_0 in FF_METHODS
    for method in FORCE_FIELD_METHODS:
        assert method.default_engine().value == "openff"


def test_parameter_set_requires_complete_valid_atom_maps() -> None:
    data = parameter_set().model_dump()
    data["nonbonded"].append(data["nonbonded"][0])
    with pytest.raises(ValidationError, match="unique and contiguous"):
        MangoParameterSetV1.model_validate(data)

    data = parameter_set().model_dump()
    data["bonds"][0]["atom_maps"] = (1, 6)
    with pytest.raises(ValidationError, match="unknown atom map"):
        MangoParameterSetV1.model_validate(data)
