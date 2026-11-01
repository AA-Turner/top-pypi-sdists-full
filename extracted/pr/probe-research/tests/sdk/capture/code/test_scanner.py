"""SecretScanner: the code snapshot reads the shared credential rules only through it, with the same findings."""

from __future__ import annotations

import ast
import base64
from pathlib import Path

import pytest

from probe.sdk.capture.code import scanner as scanner_module
from probe.sdk.capture.code.scanner import ScanDepth, SecretScanner, get_scanner
from probe.sdk.capture.code.scanners import source_code
from probe.sdk.capture.code.scanners.patterns import PatternScanner
from probe.sdk.capture.code.scanners.quick import QuickScanner
from probe.tap_core import secrets

#: Synthetic, assembled at runtime (push protection blocks token-shaped literals).
GITHUB_TOKEN = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
HF_TOKEN = "hf_" + "AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh"
CAPTURE = Path(source_code.__file__).resolve().parents[2]
#: The only capture files that may import the engine: the SecretScanner variants and their registry.
ENGINE_READERS = {"code/scanner.py", "code/scanners/patterns.py", "code/scanners/quick.py"}


def _texts() -> list[str]:
    short = f'token = "{GITHUB_TOKEN}"\nHF_TOKEN={HF_TOKEN}\n'
    padded = "x = compute(alpha, beta)\n" * 400 + short  # past 4 KiB: the keyword windows engage
    encoded = "blob: " + base64.b64encode(short.encode()).decode() + "\n"
    return [short, padded, encoded, "print('clean')\n"]


def test_each_depth_has_one_scanner_and_both_are_secret_scanners():
    assert isinstance(get_scanner(ScanDepth.FULL), PatternScanner)
    assert isinstance(get_scanner(ScanDepth.QUICK), QuickScanner)
    assert get_scanner(ScanDepth.FULL) is get_scanner(ScanDepth.FULL)
    for depth in ScanDepth:
        scanner: SecretScanner = get_scanner(depth)
        assert callable(scanner.scan)


@pytest.mark.parametrize("text", _texts(), ids=["short", "past-4kib", "base64", "clean"])
def test_the_variants_find_what_the_engine_finds(text):
    assert get_scanner(ScanDepth.FULL).scan(text) == secrets.scan(text, _accel=secrets._keyword_windows)
    assert get_scanner(ScanDepth.QUICK).scan(text) == secrets.scan_quick(text)


def test_the_full_scanner_finds_a_credential_the_quick_one_cannot_decode():
    encoded = _texts()[2]
    assert get_scanner(ScanDepth.FULL).scan(encoded)
    assert not get_scanner(ScanDepth.QUICK).scan(encoded)


def test_credential_rules_read_through_the_registry(monkeypatch):
    raw = f'TOKEN = "{GITHUB_TOKEN}"\n'.encode()
    assert source_code.credential_rules(raw, "notes.txt")

    class _Blind:
        def scan(self, text: str) -> list:
            return []

    monkeypatch.setattr(source_code, "_FULL_SCANNER", _Blind())
    monkeypatch.setattr(source_code, "_QUICK_SCANNER", _Blind())
    assert source_code.credential_rules(raw, "notes.txt") == ()
    assert source_code._chunk_rules(raw, "notes.txt") == set()


def test_no_capture_module_reads_the_engine_past_the_scanner():
    readers = set()
    for path in CAPTURE.rglob("*.py"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ImportFrom) and (node.module or "").endswith("tap_core.secrets"):
                readers.add(path.relative_to(CAPTURE).as_posix())
            elif isinstance(node, ast.Import) and any(a.name.endswith("tap_core.secrets") for a in node.names):
                readers.add(path.relative_to(CAPTURE).as_posix())
    assert readers == ENGINE_READERS, readers
    assert scanner_module.__file__.endswith("code/scanner.py")
