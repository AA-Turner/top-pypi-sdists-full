"""Windows browser registrations point only at the packaged identity host."""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

WINDOWS = Path(__file__).parents[1] / "packaging" / "windows"
NS = {"w": "http://wixtoolset.org/schemas/v4/wxs"}


@pytest.mark.parametrize("view", ["always32", "always64"])
def test_native_host_registration_for_each_browser(view):
    root = ET.parse(WINDOWS / "aiwatch.wxs").getroot()
    registrations = {}
    for component in root.findall(".//w:Component", NS):
        if component.get("Bitness") != view:
            continue
        for value in component.findall("w:RegistryValue", NS):
            if "NativeMessagingHosts" in value.get("Key", ""):
                assert value.get("Root") == "HKLM"
                assert value.get("Type") == "string"
                assert value.get("Name") is None
                registrations[value.get("Key")] = value.get("Value")
        if component.findall("w:RegistryValue", NS):
            assert component.get("Permanent") != "yes"
            if view == "always32":
                assert component.get("Directory") == "TARGETDIR"
    for browser in (r"Google\Chrome", r"Microsoft\Edge", "Mozilla"):
        family = "firefox" if browser == "Mozilla" else "chromium"
        key = rf"Software\{browser}\NativeMessagingHosts\com.runlayer.aiwatch"
        assert registrations[key] == f"[INSTALLDIR]native-host-{family}.json"


@pytest.mark.parametrize("family", ["chromium", "firefox"])
def test_native_manifests_are_shipped_and_restrict_callers(family):
    root = ET.parse(WINDOWS / "aiwatch.wxs").getroot()
    sources = {file.get("Source") for file in root.findall(".//w:File", NS)}
    filename = f"native-host-{family}.json"
    assert filename in sources
    component = next(
        component
        for component in root.findall(".//w:Component", NS)
        if any(
            file.get("Source") == filename for file in component.findall("w:File", NS)
        )
    )
    # WiX cannot generate a GUID for multiple files with an unversioned keypath.
    assert len(component.findall("w:File", NS)) == 1
    assert component.find("w:File", NS).get("KeyPath") == "yes"
    manifest = json.loads((WINDOWS / filename).read_text())
    assert manifest["name"] == "com.runlayer.aiwatch"
    assert manifest["path"] == "aiwatch-native-messaging-host.bat"
    assert manifest["type"] == "stdio"
    if family == "chromium":
        assert manifest["allowed_origins"] == [
            "chrome-extension://jijfcalfdbnjfpfcalkodmgmfijpfddi/"
        ]
        assert "allowed_extensions" not in manifest
    else:
        assert manifest["allowed_extensions"] == ["aiwatch@runlayer.com"]
        assert "allowed_origins" not in manifest
    assert "aiwatch-native-messaging-host.bat" in sources
    launcher = (WINDOWS / "aiwatch-native-messaging-host.bat").read_text()
    assert '"%~dp0aiwatch.exe" native-host' in launcher
    assert "%*" not in launcher
    assert "@echo off" in launcher
