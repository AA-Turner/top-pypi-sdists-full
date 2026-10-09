"""Test basic calculation behavior and validation."""

from pytest import fixture, raises

from stjames.engine import Engine
from stjames.method import Method
from stjames.molecule import Molecule
from stjames.settings import Settings
from stjames.task import Task
from stjames.workflows import BasicCalculationWorkflow


def test_basic_calculation() -> None:
    """Test the basic calculation workflow."""
    mol = Molecule.from_xyz("He 0 0 0")
    workflow = BasicCalculationWorkflow(
        initial_molecule=mol,
        settings=Settings(method=Method.GFN2_XTB),
    )

    assert workflow.engine == Engine.XTB
    assert workflow.calculation_uuid is None


def test_engine_setting() -> None:
    """Test the deprecated Engine setting."""
    mol = Molecule.from_xyz("He 0 0 0")

    workflow = BasicCalculationWorkflow(
        initial_molecule=mol,
        engine=Engine.PYSCF,
        settings=Settings(method=Method.PBE),
    )
    assert workflow.engine == Engine.PYSCF

    workflow = BasicCalculationWorkflow(
        initial_molecule=mol,
        settings=Settings(method=Method.PBE, engine=Engine.PYSCF),
    )
    assert workflow.engine == Engine.PYSCF

    workflow = BasicCalculationWorkflow(
        initial_molecule=mol,
        engine=Engine.GPU4PYSCF,
        settings=Settings(method=Method.PBE, engine=Engine.PYSCF),
    )
    assert workflow.engine == Engine.GPU4PYSCF


@fixture
def periodic_helium() -> Molecule:
    """Single He atom in a 3 Å cubic cell."""
    return Molecule.from_xyz_lines(["1", "charge: 0; multiplicity: 1; cell: [[3, 0, 0], [0, 3, 0], [0, 0, 3]]", "He 0 0 0"])


def test_elastic_tensor_requires_periodic_cell() -> None:
    """Elastic tensor on a non-periodic molecule is rejected."""
    mol = Molecule.from_xyz("He 0 0 0")
    with raises(ValueError, match="periodic"):
        BasicCalculationWorkflow(
            initial_molecule=mol,
            settings=Settings(method=Method.GFN2_XTB, engine=Engine.TBLITE, tasks=[Task.ELASTIC_TENSOR]),
        )


def test_elastic_tensor_rejects_unsupported_engine(periodic_helium: Molecule) -> None:
    """Elastic tensor on an engine that does not support it is rejected."""
    with raises(ValueError, match="does not support"):
        BasicCalculationWorkflow(
            initial_molecule=periodic_helium,
            settings=Settings(method=Method.GFN2_XTB, engine=Engine.XTB, tasks=[Task.ELASTIC_TENSOR]),
        )


def test_elastic_tensor_allows_periodic_supported_engine(periodic_helium: Molecule) -> None:
    """Elastic tensor on a periodic molecule with a supporting engine is accepted."""
    workflow = BasicCalculationWorkflow(
        initial_molecule=periodic_helium,
        settings=Settings(method=Method.GFN2_XTB, engine=Engine.TBLITE, tasks=[Task.ELASTIC_TENSOR]),
    )

    assert workflow.engine == Engine.TBLITE


def test_band_structure_requires_periodic_cell() -> None:
    """Band structure on a non-periodic molecule is rejected."""
    mol = Molecule.from_xyz("He 0 0 0")
    with raises(ValueError, match="periodic"):
        BasicCalculationWorkflow(
            initial_molecule=mol,
            settings=Settings(method=Method.GFN2_XTB, engine=Engine.TBLITE, tasks=[Task.BAND_STRUCTURE]),
        )
