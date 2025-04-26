from LbEnv import getPackageNames, getProjectNames


def test_getProjectNames():
    names = list(getProjectNames())
    assert "Gaudi" in names
    assert "DaVinci" in names
    assert "Gauss" in names
    assert "AppConfig" not in names
    assert "WG/SemilepConfig" not in names


def test_getPackageNames():
    names = list(getPackageNames())
    assert "Gaudi" not in names
    assert "DaVinci" not in names
    assert "Gauss" not in names
    assert "AppConfig" in names
    assert "WG/SemilepConfig" in names
