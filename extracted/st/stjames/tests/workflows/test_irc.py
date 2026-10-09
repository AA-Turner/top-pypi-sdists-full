"""Test irc behavior and validation."""

from pytest import fixture, raises

from stjames import Method, Molecule, Settings
from stjames.workflows import IRCWorkflow


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


@fixture
def settings() -> Settings:
    """Provide energy and gradient settings for IRC validation."""
    return Settings(method=Method.GFN2_XTB)


def test_raise(water: Molecule, settings: Settings) -> None:
    """Reject IRC settings without the required gradient task."""
    with raises(ValueError):
        IRCWorkflow(initial_molecule=water, settings=settings, step_size=1.0)


def test_smoke(water: Molecule, settings: Settings) -> None:
    """Accept IRC workflow with energy and gradient calculations."""
    ircwf = IRCWorkflow(initial_molecule=water, settings=settings)

    assert not ircwf.preopt
    assert ircwf.max_irc_steps == 30
    assert ircwf.level_of_theory == "gfn2_xtb"
