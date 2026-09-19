"""App-bundle ``Info.plist`` decoding survives hostile input (ISS-01).

``~/Applications/*.app`` bundles are user-owned, so their ``Info.plist`` is
attacker-writable. ``_macos_app_version`` used to catch only
``plistlib.InvalidFileException``; a non-numeric ``<integer>`` (bare
``ValueError``), truncated XML (``ExpatError``), a malformed ``<date>``
(``AttributeError``) or a ``<key>`` outside any ``<dict>`` (``IndexError``)
escaped before ``add_detection`` ran, dropping the app and every later probe
for that client.

The read is bounded as well as the decode: a multi-GiB ``Info.plist`` or a
symlink pointing outside the bundle must be refused before any bytes reach
``plistlib``.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

import pytest

from runlayer_cli.scan.client_presence import (
    MAX_INFO_PLIST_BYTES,
    DetectedClient,
    _macos_app_version,
    detect_client_presence,
)
from runlayer_cli.scan.clients import InstallProbe, MCPClientDefinition

_VALID_PLIST = (
    b"<plist><dict><key>CFBundleShortVersionString</key>"
    b"<string>1.2.3</string></dict></plist>"
)

_BAD_INTEGER = (
    b"<plist><dict><key>CFBundleShortVersionString</key>"
    b"<integer>invalid</integer></dict></plist>"
)
_TRUNCATED_XML = b"<plist><dict><key>CFBundleShortVersionString</key>"
_BAD_DATE = (
    b"<plist><dict><key>CFBundleShortVersionString</key>"
    b"<date>invalid</date></dict></plist>"
)
_KEY_OUTSIDE_DICT = b"<plist><key>CFBundleShortVersionString</key></plist>"
_NOT_A_DICT = b"<plist><array/></plist>"

InfoPlistWriter = Callable[[Path], None]


def _bytes_writer(info_plist: bytes) -> InfoPlistWriter:
    def write(target: Path) -> None:
        target.write_bytes(info_plist)

    return write


def _oversized_writer(target: Path) -> None:
    # Well-formed XML that plistlib would happily decode; only the size trips.
    padding = b" " * (MAX_INFO_PLIST_BYTES + 1 - len(_VALID_PLIST))
    target.write_bytes(_VALID_PLIST + padding)


def _symlink_writer(target: Path) -> None:
    real = target.parent / "real.plist"
    real.write_bytes(_VALID_PLIST)
    os.symlink(real, target)


_HOSTILE_PLISTS = pytest.mark.parametrize(
    "write_info_plist",
    [
        _bytes_writer(_BAD_INTEGER),
        _bytes_writer(_TRUNCATED_XML),
        _bytes_writer(_BAD_DATE),
        _bytes_writer(_KEY_OUTSIDE_DICT),
        _bytes_writer(_NOT_A_DICT),
        _oversized_writer,
        pytest.param(
            _symlink_writer,
            marks=pytest.mark.skipif(
                os.name == "nt", reason="symlink creation needs privileges"
            ),
        ),
    ],
    ids=[
        "bad-integer",
        "truncated-xml",
        "bad-date",
        "key-outside-dict",
        "not-a-dict",
        "oversized",
        "symlink",
    ],
)


def _write_bundle(root: Path, name: str, write_info_plist: InfoPlistWriter) -> Path:
    bundle = root / name
    contents = bundle / "Contents"
    contents.mkdir(parents=True)
    write_info_plist(contents / "Info.plist")
    return bundle


def test_macos_app_version_reads_a_wellformed_plist(tmp_path):
    bundle = _write_bundle(tmp_path, "Example.app", _bytes_writer(_VALID_PLIST))
    assert _macos_app_version(bundle) == "1.2.3"


@_HOSTILE_PLISTS
def test_macos_app_version_returns_none_for_undecodable_plist(
    tmp_path, write_info_plist
):
    bundle = _write_bundle(tmp_path, "Example.app", write_info_plist)
    assert _macos_app_version(bundle) is None


@_HOSTILE_PLISTS
def test_undecodable_plist_still_records_the_app_detection(
    tmp_path, monkeypatch, write_info_plist
):
    applications = tmp_path / "Applications"
    _write_bundle(applications, "Test.app", write_info_plist)
    monkeypatch.setattr(
        "runlayer_cli.scan.client_presence._macos_app_roots",
        lambda _home: (applications,),
    )
    client = MCPClientDefinition(
        name="test",
        display_name="Test",
        paths=[],
        install_probe=InstallProbe(macos_app_bundles=["Test.app"]),
    )

    detected = detect_client_presence([client], home=tmp_path, system="Darwin")

    assert detected == [
        DetectedClient(
            client="test",
            display_name="Test",
            client_version=None,
            detected_via=["app"],
        )
    ]
