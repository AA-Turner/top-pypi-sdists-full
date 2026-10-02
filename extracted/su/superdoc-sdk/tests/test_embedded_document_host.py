from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from superdoc.embedded_document_host import resolve_embedded_document_host_path
from superdoc.errors import SuperDocError


class EmbeddedDocumentHostTests(unittest.TestCase):
    def test_resolves_and_marks_the_platform_host_executable(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            host = Path(raw_directory) / 'superdoc-document-host'
            host.write_bytes(b'host')
            host.chmod(0o644)

            with (
                patch(
                    'superdoc.embedded_document_host.resolve_embedded_target',
                    return_value='darwin-arm64',
                ),
                patch(
                    'superdoc.embedded_document_host.resolve_companion_binary',
                    return_value=str(host),
                ) as resolve_binary,
            ):
                self.assertEqual(resolve_embedded_document_host_path(), str(host))

            resolve_binary.assert_called_once_with('darwin-arm64', 'superdoc-document-host')
            self.assertNotEqual(host.stat().st_mode & 0o111, 0)

    def test_reports_a_missing_companion_host(self) -> None:
        with (
            patch(
                'superdoc.embedded_document_host.resolve_embedded_target',
                return_value='linux-x64',
            ),
            patch(
                'superdoc.embedded_document_host.resolve_companion_binary',
                return_value=None,
            ),
            self.assertRaises(SuperDocError) as raised,
        ):
            resolve_embedded_document_host_path()

        self.assertEqual(raised.exception.code, 'DOCUMENT_HOST_BINARY_MISSING')
        self.assertEqual(raised.exception.details, {'target': 'linux-x64'})


if __name__ == '__main__':
    unittest.main()
