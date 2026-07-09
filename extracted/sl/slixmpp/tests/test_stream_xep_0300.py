import io
import tempfile
import unittest

from slixmpp.test import SlixTest


class TestGetHash(SlixTest):
    def setUp(self) -> None:
        self.stream_start(plugins={"xep_0300"})

    def test_bytes(self) -> None:
        h = self.xmpp.plugin["xep_0300"].compute_hash(data=_DATA, function="sha-512")
        assert h["value"] == _EXPECTED_HASH

    def test_filename(self) -> None:
        with tempfile.NamedTemporaryFile("wb") as tmp_file:
            tmp_file.write(_DATA)
            tmp_file.flush()
            h = self.xmpp.plugin["xep_0300"].compute_hash(
                filename=tmp_file.name, function="sha-512"
            )
        assert h["value"] == _EXPECTED_HASH

    def test_file(self) -> None:
        h = self.xmpp.plugin["xep_0300"].compute_hash(
            file=io.BytesIO(_DATA), function="sha-512"
        )
        assert h["value"] == _EXPECTED_HASH, h["value"]


_DATA = b"xxxxx"
_EXPECTED_HASH = "Ri5hZ55iLirYzzOafJOYAM2zF/B6inZAYyWF3RMpTeTcpoD9JMwrMPr6goYqG54HwOSvrNxtkOa0u1v8VchYqw=="

suite = unittest.TestLoader().loadTestsFromTestCase(TestGetHash)
