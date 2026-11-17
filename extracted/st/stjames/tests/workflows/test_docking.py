"""Test docking behavior and validation."""

from pydantic import TypeAdapter
from pytest import fixture, mark, raises

from stjames import Molecule
from stjames.pdb import PDB, ResidueAtomRef, ResidueRef, read_pdb
from stjames.workflows.docking import (
    AnalogueDockingWorkflow,
    DockingDistanceRestraint,
    DockingPositionRestraint,
    DockingRestraint,
    DockingSettingsUnion,
    DockingWorkflow,
    GninaSettings,
    HeronSettings,
    InducedFitSettings,
    Score,
    VinaSettings,
)


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


@fixture
def gfp() -> PDB:
    """Green fluorescent protein."""
    return read_pdb("tests/data/1ema.pdb")


def test_raises(water: Molecule, gfp: str) -> None:
    # negative pocket
    """Reject negative docking pocket dimensions and incompatible settings."""
    with raises(ValueError):
        DockingWorkflow(
            initial_molecule=water,
            protein=gfp,
            pocket=((0, 0, 0), (-1, -1, -1)),
        )

    # no protein
    with raises(ValueError):
        DockingWorkflow(  # ty: ignore[missing-argument]
            initial_molecule=water,
            pocket=((0, 0, 0), (-1, -1, -1)),
        )


def test_basic(water: Molecule, gfp: str) -> None:
    """Preserve docking pocket geometry and empty initial score collections."""
    dwf = DockingWorkflow(
        initial_molecule=water,
        protein=gfp,
        pocket=((0, 0, 0), (1, 1, 1)),
    )

    assert not dwf.scores

    assert dwf.pocket == ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0))

    assert isinstance(dwf.target, PDB)
    assert dwf.target.description.code == "1EMA"
    assert dwf.induced_fit_settings is None


def test_induced_fit_settings_enablement(water: Molecule, gfp: str) -> None:
    """Verify induced fit settings enablement."""
    dwf = DockingWorkflow.model_validate(
        {
            "initial_molecule": water,
            "protein": gfp,
            "pocket": ((0, 0, 0), (10, 10, 10)),
            "induced_fit_settings": {},
        }
    )

    assert isinstance(dwf.induced_fit_settings, InducedFitSettings)
    assert dwf.induced_fit_settings.max_receptors == 6


def test_induced_fit_supports_qvina2(water: Molecule, gfp: str) -> None:
    """Verify induced fit supports qvina2."""
    dwf = DockingWorkflow(
        initial_molecule=water,
        protein=gfp,
        pocket=((0, 0, 0), (10, 10, 10)),
        docking_settings=VinaSettings(
            executable="qvina2",
            scoring_function="vina",
        ),
        induced_fit_settings=InducedFitSettings(),
    )

    assert isinstance(dwf.docking_settings, VinaSettings)
    assert dwf.docking_settings.executable == "qvina2"


def test_induced_fit_rejects_unsupported_engine(water: Molecule, gfp: str) -> None:
    """Verify induced fit rejects unsupported engine."""
    with raises(ValueError, match="Vina or QVina2"):
        DockingWorkflow(
            initial_molecule=water,
            protein=gfp,
            pocket=((0, 0, 0), (10, 10, 10)),
            docking_settings=VinaSettings(
                executable="qvina-w",
                scoring_function="vina",
            ),
            induced_fit_settings=InducedFitSettings(),
        )


def test_docked(water: Molecule, gfp: str) -> None:
    """Report docked poses and count valid docking results."""
    dwf = DockingWorkflow(
        initial_molecule=water,
        protein=gfp,
        pocket=((0, 0, 0), (10, 10, 10)),
    )

    dwf.scores = [
        Score(pose=None, score=0.0, posebusters_valid=True, complex_pdb=None, strain=0.0),
        Score(pose=None, score=1.0, posebusters_valid=False, complex_pdb=None, strain=0.0),
    ]

    assert dwf.pocket == ((0.0, 0.0, 0.0), (10.0, 10.0, 10.0))
    assert dwf.scores == [
        Score(pose=None, score=0.0, posebusters_valid=True, complex_pdb=None, strain=0.0),
        Score(pose=None, score=1.0, posebusters_valid=False, complex_pdb=None, strain=0.0),
    ]
    assert all(score.affinity_score is None for score in dwf.scores)


def test_posebusters_validity_can_be_unevaluated() -> None:
    """Verify posebusters validity can be unevaluated."""
    score = Score(pose=None, complex_pdb=None, score=0.0)

    assert score.posebusters_valid is None


def test_analogue_docking(water: Molecule, gfp: str) -> None:
    """Initialize analogue docking with molecular inputs and an empty score collection."""
    adwf = AnalogueDockingWorkflow(initial_molecule=water, protein=gfp, analogues=["CO", "COC", "CCO"])

    assert not adwf.analogue_scores
    assert isinstance(adwf.protein, PDB)


def test_gnina_settings_noncovalent(water: Molecule, gfp: PDB) -> None:
    """Choose noncovalent GNINA defaults without reactive atom indices."""
    s = GninaSettings()
    assert s.exhaustiveness == 8
    assert s.scoring_function == "gnina_cnn"
    assert not s.is_covalent

    dwf = DockingWorkflow(
        initial_molecule=water,
        protein=gfp,
        pocket=((0, 0, 0), (20, 20, 20)),
        docking_settings=s,
    )
    assert isinstance(dwf.docking_settings, GninaSettings)


def test_gnina_settings_covalent(water: Molecule, gfp: PDB) -> None:
    """Enable covalent GNINA docking when both reactive atom indices are set."""
    s = GninaSettings(
        scoring_function="vina",
        covalent_ligand_atom_index=3,
        covalent_protein_atom_index=142,
    )
    assert s.is_covalent
    assert s.covalent_ligand_atom_index == 3
    assert s.covalent_protein_atom_index == 142


def test_gnina_settings_covalent_requires_both(water: Molecule, gfp: PDB) -> None:
    """Verify gnina settings covalent requires both."""
    with raises(ValueError, match="must be set together"):
        GninaSettings(covalent_ligand_atom_index=3)

    with raises(ValueError, match="must be set together"):
        GninaSettings(covalent_protein_atom_index=142)


def test_gnina_settings_discriminator() -> None:
    """Deserialize GNINA settings through the docking settings discriminator."""
    settings = TypeAdapter(DockingSettingsUnion).validate_python({"settings_type": "gnina", "exhaustiveness": 16})
    assert isinstance(settings, GninaSettings)
    assert settings.exhaustiveness == 16


def test_vina_settings_discriminator() -> None:
    """Deserialize Vina settings through the docking settings discriminator."""
    settings = TypeAdapter(DockingSettingsUnion).validate_python({"settings_type": "vina", "exhaustiveness": 32})
    assert isinstance(settings, VinaSettings)
    assert settings.exhaustiveness == 32


def test_analogue_docking_rejects_qvina(water: Molecule, gfp: str) -> None:
    """Verify analogue docking rejects qvina."""
    for bad_executable in ("qvina2", "qvina-w"):
        with raises(ValueError, match="qvina2 and qvina-w are not supported"):
            AnalogueDockingWorkflow(
                initial_molecule=water,
                protein=gfp,
                analogues=["CO"],
                # qvina requires scoring_function="vina" to pass VinaSettings validation
                docking_settings=VinaSettings(executable=bad_executable, scoring_function="vina"),
            )


def test_analogue_docking_accepts_heron(water: Molecule, gfp: str) -> None:
    """Preserve Heron analogue docking through workflow serialization."""
    workflow = AnalogueDockingWorkflow(
        initial_molecule=water,
        protein=gfp,
        analogues=["CO"],
        docking_settings=VinaSettings(executable="heron"),
    )
    restored = AnalogueDockingWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.docking_settings.executable == "heron"


def test_heron_settings_roundtrip_and_scoring_validation() -> None:
    """Preserve Heron selection through JSON and reject unsupported scoring."""
    adapter = TypeAdapter(DockingSettingsUnion)
    settings = adapter.validate_python({"settings_type": "vina", "executable": "heron", "scoring_function": "vinardo"})
    assert adapter.validate_json(adapter.dump_json(settings)).executable == "heron"
    with raises(ValueError):
        VinaSettings(executable="heron", scoring_function="vina")


def test_private_state_workflow_roundtrips(water: Molecule, gfp: PDB) -> None:
    """Preserve dedicated Heron settings through docking and analogue JSON."""
    settings = HeronSettings(max_poses=3, seed=71)
    adapter = TypeAdapter(DockingSettingsUnion)
    assert adapter.validate_json(adapter.dump_json(settings)).model_dump() == settings.model_dump()
    workflow = DockingWorkflow(initial_molecule=water, protein=gfp, pocket=((0, 0, 0), (20, 20, 20)), docking_settings=settings)
    assert DockingWorkflow.model_validate_json(workflow.model_dump_json()).docking_settings.model_dump() == settings.model_dump()
    analogue = AnalogueDockingWorkflow(initial_molecule=water, protein=gfp, analogues=["CO"], docking_settings=settings)
    assert AnalogueDockingWorkflow.model_validate_json(analogue.model_dump_json()).docking_settings.model_dump() == settings.model_dump()
    with raises(ValueError):
        DockingWorkflow.model_validate(workflow.model_dump() | {"induced_fit_settings": {}})


@mark.parametrize("seed", [0, 2147483648])
def test_private_state_rejects_invalid_seed(seed: int) -> None:
    """Reject seeds outside the fixed recipe's public domain."""
    with raises(ValueError):
        HeronSettings(seed=seed)


@mark.parametrize("indices", [(None, 0), (0, None), (-1, 0), (0, -1)])
def test_heron_covalent_indices_require_a_valid_pair(indices: tuple[int | None, int | None]) -> None:
    """Reject incomplete or negative covalent atom selections."""
    with raises(ValueError):
        HeronSettings(covalent_ligand_atom_index=indices[0], covalent_protein_atom_index=indices[1])


def test_heron_covalent_restraints_roundtrip(water: Molecule, gfp: PDB) -> None:
    """Preserve covalent index zero and both restraint variants through workflow JSON."""
    settings = HeronSettings(
        covalent_ligand_atom_index=0,
        covalent_protein_atom_index=1,
        restraints=[
            DockingDistanceRestraint(ligand_atom_index=0, protein_atom_index=0, target=2.0),
            DockingPositionRestraint(ligand_atom_index=0, position=(1, 2, 3), force_constant=25),
        ],
    )
    workflow = DockingWorkflow(initial_molecule=water, protein=gfp, pocket=((0, 0, 0), (20, 20, 20)), docking_settings=settings)
    restored = DockingWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.docking_settings.model_dump() == settings.model_dump()
    assert settings.is_covalent
    assert settings.max_poses == VinaSettings().max_poses


@mark.parametrize(
    "value",
    [
        {"type": "distance", "ligand_atom_index": 0, "protein_atom_index": -1, "target": 1},
        {"type": "distance", "ligand_atom_index": -1, "protein_atom_index": 0, "target": 1},
        {"type": "distance", "ligand_atom_index": 0, "protein_atom_index": 0, "target": -1},
        {"type": "distance", "ligand_atom_index": 0, "protein_atom_index": ResidueRef("polymer", "A"), "target": 1},
        {"type": "distance", "ligand_atom_index": 0, "protein_atom_index": ResidueAtomRef(ResidueRef("polymer", "A", "A.12"), " "), "target": 1},
        {"type": "position", "ligand_atom_index": -1, "position": [0, 0, 0]},
        {"type": "position", "ligand_atom_index": 0, "position": [0, float("inf"), 0]},
        {"type": "position", "ligand_atom_index": 0, "position": [0, 0, 0], "force_constant": float("nan")},
    ],
)
def test_docking_restraints_reject_invalid_geometry(value: dict[str, object]) -> None:
    """Reject invalid selections, distances, coordinates and spring constants."""
    with raises(ValueError):
        TypeAdapter(DockingRestraint).validate_python(value)


@mark.parametrize("protein", [0, ResidueAtomRef(ResidueRef("polymer", "A", "A.12"), "SG")])
def test_docking_distance_protein_selection_roundtrip(protein: int | ResidueAtomRef) -> None:
    """Preserve independent index zero and named protein atoms through JSON."""
    settings = HeronSettings(restraints=[DockingDistanceRestraint(ligand_atom_index=0, protein_atom_index=protein, target=3)])
    restored = HeronSettings.model_validate_json(settings.model_dump_json())
    assert restored.restraints == settings.restraints


@mark.parametrize("settings_class", [HeronSettings, GninaSettings])
@mark.parametrize("protein", [0, ResidueAtomRef(ResidueRef("polymer", "A", "A.12"), "SG")])
def test_covalent_protein_atom_reference_roundtrip(settings_class: type[HeronSettings] | type[GninaSettings], protein: int | ResidueAtomRef) -> None:
    """Preserve reacting protein indices and named atoms through the settings discriminator."""
    options = {"scoring_function": "vina"} if settings_class is GninaSettings else {}
    settings = settings_class(covalent_ligand_atom_index=0, covalent_protein_atom_index=protein, **options)
    adapter = TypeAdapter(DockingSettingsUnion)
    restored = adapter.validate_json(adapter.dump_json(settings))
    assert restored == settings
    assert restored.is_covalent
    with raises(ValueError):
        settings_class(covalent_protein_atom_index=protein, **options)


@mark.parametrize("settings_class", [HeronSettings, GninaSettings])
@mark.parametrize("protein", [-1, ResidueAtomRef(ResidueRef("polymer", "A"), "SG"), ResidueAtomRef(ResidueRef("polymer", "A", "A.12"), " ")])
def test_covalent_protein_atom_reference_validation(settings_class: type[HeronSettings] | type[GninaSettings], protein: int | ResidueAtomRef) -> None:
    """Reject negative indices and incomplete named atoms for both covalent engines."""
    with raises(ValueError):
        settings_class(covalent_ligand_atom_index=0, covalent_protein_atom_index=protein)
