"""Cross-platform proof of the Windows stdio bug MECHANISM (no Windows needed).

The real bug: the MS C runtime opens inherited pipe stdio in TEXT mode (O_TEXT),
translating \\n<->\\r\\n and corrupting the binary Content-Length framing. msvcrt
and O_TEXT only exist on Windows, so the actual __main__.py msvcrt.setmode() fix
can only RUN on Windows — validate THAT on a windows-latest CI job or a Windows
PC via lifecycle_test / windows_stdio_test.

This test instead reproduces the CRT translation IN MEMORY and proves the
protocol requires untranslated (binary) streams: a translated frame no longer
parses. It is the executable form of the diagnosis and a guard against anyone
assuming text streams are fine. Runs everywhere, including this dev machine.
"""

import io
import unittest

from abstra_internals.repositories.linter.sidecar.protocol import (
    ProtocolError,
    encode_frame,
    read_frame,
)


def _crt_text_write(frame: bytes) -> bytes:
    # Windows CRT text-mode WRITE: every \n -> \r\n, unconditionally (so an
    # existing \r\n becomes \r\r\n). What the child's text-mode stdout emits.
    return frame.replace(b"\n", b"\r\n")


def _crt_text_read(frame: bytes) -> bytes:
    # Windows CRT text-mode READ: every \r\n -> \n. What text-mode stdin would
    # hand to the child's read_frame.
    return frame.replace(b"\r\n", b"\n")


class ProtocolWindowsTextModeTest(unittest.TestCase):
    def setUp(self):
        self.msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"checks": [{"name": "CssSyntax", "issues": []}]},
        }
        self.frame = encode_frame(self.msg)

    def test_binary_stream_round_trips(self):
        # Control: an untranslated (binary) frame parses back exactly. This is
        # the path the msvcrt.setmode(O_BINARY) fix restores on Windows.
        self.assertEqual(read_frame(io.BytesIO(self.frame)), self.msg)

    def test_text_mode_write_corrupts_frame(self):
        # child -> editor: text-mode stdout mangles the \r\n\r\n header so the
        # peer never finds a frame terminator.
        corrupted = _crt_text_write(self.frame)
        self.assertNotEqual(corrupted, self.frame)
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(corrupted))

    def test_text_mode_read_corrupts_frame(self):
        # editor -> child: text-mode stdin collapses \r\n -> \n, destroying both
        # the header terminator and the Content-Length byte count.
        corrupted = _crt_text_read(self.frame)
        self.assertNotEqual(corrupted, self.frame)
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(corrupted))


if __name__ == "__main__":
    unittest.main()
