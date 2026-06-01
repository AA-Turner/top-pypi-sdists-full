from email.parser import Parser
from importlib.metadata import distribution
from pathlib import Path

from src import vtherm_api


def _package_metadata_version() -> str:
    package_root = Path(vtherm_api.__file__).resolve().parent
    local_pkg_info = package_root.parent / "vtherm_api.egg-info" / "PKG-INFO"

    if local_pkg_info.exists():
        return Parser().parsestr(local_pkg_info.read_text(encoding="utf-8"))["Version"]

    return distribution("vtherm_api").version


def test_package_exports_algorithm_plugin_api() -> None:
    assert vtherm_api.VThermAPI is not None
    assert vtherm_api.PluginClimate is not None
    assert vtherm_api.InterfaceThermostat is not None
    assert vtherm_api.InterfaceThermostatRuntime is not None
    assert vtherm_api.InterfaceCycleScheduler is not None
    assert vtherm_api.InterfacePropAlgorithmHandler is not None
    assert vtherm_api.InterfacePropAlgorithmFactory is not None
    assert vtherm_api.__version__ == _package_metadata_version()
