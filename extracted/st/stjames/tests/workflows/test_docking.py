"""Test docking behavior and validation."""

from pydantic import TypeAdapter
from pytest import fixture, raises

from stjames import Molecule
from stjames.pdb import PDB, read_pdb
from stjames.workflows.docking import (
    AnalogueDockingWorkflow,
    DockingSettingsUnion,
    DockingWorkflow,
    GninaSettings,
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
