from pytest import raises

from stjames import Constraint, ConstraintType


def test_invalid_constraint_settings() -> None:
    Constraint(constraint_type=ConstraintType.BOND, atoms=[1, 2])

    with raises(ValueError):
        Constraint(constraint_type=ConstraintType.BOND, atoms=[1, 2, 3])

    with raises(ValueError):
        Constraint(constraint_type=ConstraintType.BOND, atoms=[1, 2, 3, 4])

    Constraint(constraint_type=ConstraintType.ANGLE, atoms=[1, 2, 3])

    with raises(ValueError):
        Constraint(constraint_type=ConstraintType.ANGLE, atoms=[1, 2])

    with raises(ValueError):
        Constraint(constraint_type=ConstraintType.ANGLE, atoms=[1, 2, 3, 4])

    Constraint(constraint_type=ConstraintType.DIHEDRAL, atoms=[1, 2, 3, 4])

    with raises(ValueError):
        Constraint(constraint_type=ConstraintType.DIHEDRAL, atoms=[1, 2])

    with raises(ValueError):
        Constraint(constraint_type=ConstraintType.DIHEDRAL, atoms=[1, 2, 3])
