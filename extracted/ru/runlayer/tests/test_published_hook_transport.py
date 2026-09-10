"""The release guard checks published source without executing wheel code."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts/check_published_hook_transport.py"
)
_SPEC = importlib.util.spec_from_file_location("published_hook_transport", _SCRIPT)
assert _SPEC and _SPEC.loader
guard = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(guard)

_CLI = """
from runlayer_sdk.hook_transport import KNOWN_WIRE_ENCODINGS, encode_wire_body as encode
encode('body', compress=True, encodings=('gzip',))
"""
_SDK = """
KNOWN_WIRE_ENCODINGS = {'gzip'}
def encode_wire_body(payload, *, compress=False, encodings=('gzip',)):
    return payload
raise RuntimeError('source must not execute')
"""


class PublishedHookTransportTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.source = Path(self.directory.name)
        (self.source / "relay.py").write_text(_CLI)

    def test_matching_contract_does_not_execute_source(self):
        guard.check_transport(self.source, _SDK)

    def test_missing_symbol_fails(self):
        with self.assertRaisesRegex(ValueError, "KNOWN_WIRE_ENCODINGS"):
            guard.check_transport(self.source, _SDK.split("\n", 2)[2])

    def test_unpublished_keyword_fails(self):
        with self.assertRaisesRegex(ValueError, "encodings"):
            guard.check_transport(
                self.source, _SDK.replace(", encodings=('gzip',)", "")
            )

    def test_new_cli_keyword_is_discovered(self):
        (self.source / "relay.py").write_text(_CLI.replace("compress=True", "level=1"))
        with self.assertRaisesRegex(ValueError, "level"):
            guard.check_transport(self.source, _SDK)

    def test_compatible_sdk_additions_pass(self):
        guard.check_transport(
            self.source, _SDK.replace("compress=False", "level=1, compress=False")
        )
        guard.check_transport(
            self.source, _SDK.replace("encodings=('gzip',)", "**kwargs")
        )

    def test_download_verifies_pypi_hash(self):
        wheel = b"wheel contents"
        metadata = {
            "urls": [
                {
                    "filename": "runlayer_hooks_sdk-0.2.3-py3-none-any.whl",
                    "packagetype": "bdist_wheel",
                    "url": "https://files.pythonhosted.org/packages/sdk.whl",
                    "digests": {"sha256": hashlib.sha256(wheel).hexdigest()},
                }
            ]
        }
        for content in (wheel, wheel + b"changed"):
            with patch.object(
                guard, "download", side_effect=[json.dumps(metadata).encode(), content]
            ):
                if content == wheel:
                    self.assertEqual(guard.published_wheel("0.2.3"), wheel)
                else:
                    with self.assertRaisesRegex(ValueError, "SHA256"):
                        guard.published_wheel("0.2.3")

    def test_download_rejects_other_hosts(self):
        with self.assertRaisesRegex(ValueError, "URL"):
            guard.download("https://example.com/sdk.whl")


if __name__ == "__main__":
    unittest.main()
