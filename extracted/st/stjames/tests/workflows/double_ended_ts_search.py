"""Test double ended ts search behavior and validation."""

from pytest import raises

from stjames import Method, Settings
from stjames.molecule import Molecule
from stjames.optimization.string_method import FSMSettings, Interpolation, StringMethodSettings
from stjames.workflows.double_ended_ts_search import DoubleEndedTSSearchWorkflow


def test_setup() -> None:
    """Validate reactant and product compatibility for transition-state searches."""
    ammonia = Molecule.from_xyz("""\
N  0.0  0.0  0.3
H -0.5 -0.8 -0.1
H -0.4  0.8 -0.1
H  0.9  0.0 -0.1""")
    ammonia_flipped = Molecule.from_xyz("""\
N  0.0  0.0 -0.3
H -0.5 -0.8  0.1
H -0.4  0.8  0.1
H  0.9  0.0  0.1""")
    hcn = Molecule.from_xyz("""\
H 0 0 -1.1
C 0 0 0
N 0 0 1.2""")

    with raises(ValueError, match="Reactant and product must have the same number of atoms"):
        DoubleEndedTSSearchWorkflow(
            reactant=ammonia,
            product=hcn,
            calculation_settings=Settings(method=Method.GFN0_XTB),
            search_settings=FSMSettings(),
            optimize_inputs=True,
            optimize_ts=False,
        )

    DoubleEndedTSSearchWorkflow(
        reactant=ammonia,
        product=ammonia_flipped,
        calculation_settings=Settings(method=Method.HF3C),
        search_settings=FSMSettings(
            interpolation_method=Interpolation.LINEAR_SYNCHRONOUS_TRANSIT,
        ),
        optimize_inputs=False,
        optimize_ts=True,
    )


def _ammonia_flip() -> tuple[Molecule, Molecule]:
    ammonia = Molecule.from_xyz("""\
N  0.0  0.0  0.3
H -0.5 -0.8 -0.1
H -0.4  0.8 -0.1
H  0.9  0.0 -0.1""")
    ammonia_flipped = Molecule.from_xyz("""\
N  0.0  0.0 -0.3
H -0.5 -0.8  0.1
H -0.4  0.8  0.1
H  0.9  0.0  0.1""")
    return ammonia, ammonia_flipped


def test_gsm_search_settings() -> None:
    """Preserve string-method search settings and their freeze option."""
    reactant, product = _ammonia_flip()

    wf = DoubleEndedTSSearchWorkflow(
        reactant=reactant,
        product=product,
        calculation_settings=Settings(method=Method.GFN0_XTB),
        search_settings=StringMethodSettings(freeze=False),
    )

    assert isinstance(wf.search_settings, StringMethodSettings)
    assert wf.search_settings.freeze is False

    # freeze flag survives a serialization round-trip
    reloaded = DoubleEndedTSSearchWorkflow.model_validate(wf.model_dump())
    assert isinstance(reloaded.search_settings, StringMethodSettings)
    assert reloaded.search_settings.freeze is False


def test_legacy_search_settings_without_freeze() -> None:
    """Validate legacy fixed-string search data without a freeze field."""
    reactant, product = _ammonia_flip()

    wf = DoubleEndedTSSearchWorkflow(
        reactant=reactant,
        product=product,
        calculation_settings=Settings(method=Method.GFN0_XTB),
        search_settings=FSMSettings(),
    )

    # Simulate data saved before `freeze` existed (<=0.0.226 defaults to FSM)
    data = wf.model_dump()
    del data["search_settings"]["freeze"]

    reloaded = DoubleEndedTSSearchWorkflow.model_validate(data)
    assert isinstance(reloaded.search_settings, StringMethodSettings)
    assert reloaded.search_settings.freeze is True
