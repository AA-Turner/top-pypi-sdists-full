"""Test scan behavior and validation."""

from pytest import fixture, raises

from stjames import Engine, Method, Molecule, Settings
from stjames.workflows import ScanWorkflow
from stjames.workflows.scan import ScanSettings


@fixture
def water() -> Molecule:
    """Provide water geometry for workflow validation."""
    return Molecule.from_xyz("H 0 0 0\nO 0 0 1\nH 0 1 1")


def test_concerted_scan(water: Molecule) -> None:
    """Verify concerted scan."""
    ss1 = ScanSettings(type="bond", atoms=[0, 1], start=0.5, stop=1.5, num=11)
    calc_settings = Settings(method=Method.GFN2_XTB)

    scan1d = ScanWorkflow(initial_molecule=water, scan_settings=ss1, calc_settings=calc_settings, calc_engine=Engine.XTB)
    assert isinstance(scan1d.scan_settings, list)

    ss2 = ScanSettings(type="bond", atoms=[2, 1], start=0.5, stop=1.5, num=21)
    with raises(ValueError):
        ScanWorkflow(initial_molecule=water, scan_settings=[ss1, ss2], calc_settings=calc_settings, calc_engine=Engine.XTB)

    ss3 = ScanSettings(type="bond", atoms=[2, 1], start=0.5, stop=1.5, num=11)
    scan1d_concerted = ScanWorkflow(initial_molecule=water, scan_settings=[ss1, ss3], calc_settings=calc_settings, calc_engine=Engine.XTB)
    assert isinstance(scan1d_concerted.scan_settings, list)

    scan2d = ScanWorkflow(initial_molecule=water, scan_settings=ss1, scan_settings_2d=ss2, calc_settings=calc_settings, calc_engine=Engine.XTB)
    assert isinstance(scan2d.scan_settings, list)
    assert isinstance(scan2d.scan_settings_2d, list)

    scan2d_concerted = ScanWorkflow(
        initial_molecule=water, scan_settings=[ss1, ss3], scan_settings_2d=[ss1, ss3], calc_settings=calc_settings, calc_engine=Engine.XTB
    )
    assert isinstance(scan2d_concerted.scan_settings, list)
    assert isinstance(scan2d_concerted.scan_settings_2d, list)
