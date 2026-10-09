"""Test conformer search behavior and validation."""

from pydantic import ValidationError
from pytest import fixture, raises

from stjames import Constraint, Molecule
from stjames.conformers import ETKDGSettings, iMTDSettings
from stjames.constraint import ConstraintType
from stjames.workflows.conformer_search import ConformerSearchWorkflow


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


@fixture
def chloroethane() -> Molecule:
    """Provide chloroethane geometry with distinct bond environments."""
    return Molecule.from_xyz("""\
C  -0.75  0.00  0.00
C   0.75  0.00  0.00
Cl -1.15  0.00 -1.00
H  -1.15 -1.00  0.50
H  -1.15  0.85  0.50
H   1.15 -0.85 -0.50
H   1.15  0.85 -0.50
H   1.15  0.00  1.10
""")


def test_conformer_search_workflow(water: Molecule) -> None:
    """Accept supported generation settings in conformer search workflows."""
    ConformerSearchWorkflow(initial_molecule=water, conf_gen_settings=ETKDGSettings())
    ConformerSearchWorkflow(
        initial_molecule=water,
        conf_gen_settings=iMTDSettings(constraints=[Constraint(constraint_type=ConstraintType.BOND, atoms=[1, 2])]),
    )

    constraints = [Constraint(constraint_type=ConstraintType.BOND, atoms=[1, 2])]
    workflow = ConformerSearchWorkflow(
        initial_molecule=water,
        conf_gen_settings=ETKDGSettings(constraints=constraints),
    )
    assert isinstance(workflow.conf_gen_settings, ETKDGSettings)
    assert workflow.conf_gen_settings.constraints == tuple(constraints)
    restored = ConformerSearchWorkflow.model_validate_json(workflow.model_dump_json())
    assert restored.conf_gen_settings == workflow.conf_gen_settings

    with raises(ValidationError, match="ETKDG does not support NCI"):
        ConformerSearchWorkflow(
            initial_molecule=water,
            conf_gen_settings=ETKDGSettings(nci=True),
        )


def test_no_conformer_gen(water: Molecule, chloroethane: Molecule) -> None:
    """Require initial conformers when conformer generation is disabled."""
    ConformerSearchWorkflow(initial_conformers=[chloroethane, chloroethane], conf_gen_settings=None)

    with raises(ValueError, match="Need initial_conformers to be set without a conformer-generation method"):
        ConformerSearchWorkflow(initial_molecule=water, conf_gen_settings=None)

    with raises(ValueError, match="Not all molecules in initial_conformers have the same atomic formula"):
        ConformerSearchWorkflow(initial_conformers=[chloroethane, water], conf_gen_settings=None)
