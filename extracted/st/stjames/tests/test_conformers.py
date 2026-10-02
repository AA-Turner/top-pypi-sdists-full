from pydantic import ValidationError
from pytest import mark, raises

from stjames import Constraint, Method, Settings, Task
from stjames.conformers import ConformerGenMixin, ConformerSearchMixin, ETKDGSettings, OpenConfSettings, iMTDSettings, iMTDSpeeds
from stjames.constraint import ConstraintType
from stjames.workflows.multistage_opt import MultiStageOptSettings


def test_etkdg() -> None:
    settings = ETKDGSettings()

    assert settings.num_initial_confs == 300

    with raises(ValidationError, match="ETKDG does not support NCI"):
        ETKDGSettings(nci=True)


def test_imtdgc() -> None:
    settings = iMTDSettings()

    assert settings.speed == iMTDSpeeds.QUICK
    assert not settings.reopt
    assert settings.mtd_method == Method.GFN_FF


def test_conformer_gen_mixin() -> None:
    settings = ConformerGenMixin(conf_gen_settings=ETKDGSettings(num_initial_confs=150))
    assert settings.conf_gen_settings == ETKDGSettings(num_initial_confs=150)


def test_conformer_search_mixin() -> None:
    msos = MultiStageOptSettings(
        optimization_settings=[Settings(method=Method.GFN2_XTB, tasks=[Task.OPTIMIZE])],
        singlepoint_settings=Settings(method=Method.R2SCAN3C),
    )
    settings = ConformerSearchMixin(multistage_opt_settings=msos, conf_gen_settings=ETKDGSettings())

    assert settings.multistage_opt_settings == msos


@mark.parametrize("settings_cls", [OpenConfSettings, ETKDGSettings])
def test_conformer_constraints(settings_cls: type[OpenConfSettings] | type[ETKDGSettings]) -> None:
    constraints = [
        Constraint(constraint_type=ConstraintType.FREEZE_ATOMS, atoms=[1]),
        Constraint(constraint_type=ConstraintType.BOND, atoms=[1, 2], value=1.6),
        Constraint(constraint_type=ConstraintType.ANGLE, atoms=[1, 2, 3], value=120),
        Constraint(constraint_type=ConstraintType.DIHEDRAL, atoms=[1, 2, 3, 4]),
    ]
    settings = settings_cls(constraints=constraints)
    assert settings.constraints == tuple(constraints)
    assert settings_cls.model_validate_json(settings.model_dump_json()) == settings
    mixin = ConformerGenMixin.model_validate({"conf_gen_settings": settings.model_dump()})
    assert mixin.conf_gen_settings == settings
