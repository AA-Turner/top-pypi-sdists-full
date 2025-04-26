import sys
from unittest import mock

import pytest

# This test should be run in a separate interpreter, and needed mostly only for coverage.
if not any([str(i).find("import_error_test") != -1 for i in sys.argv]):  # noqa
    pytest.skip(allow_module_level=True)


def test_no_c_module(monkeypatch):
    original_import = __import__

    def import_mock(name, *args):
        if name == "_pi_heif":
            name = "_pi_heif_miss"
        return original_import(name, *args)

    with mock.patch("builtins.__import__", side_effect=import_mock):
        import pi_heif

    with pytest.raises(ModuleNotFoundError):
        pi_heif.libheif_version()

    with pytest.raises(ModuleNotFoundError):
        pi_heif.misc.CtxEncode(pi_heif.constants.HeifCompressionFormat.AV1)

    assert pi_heif.get_file_mimetype(b"\x00\x00\x00\x20\x66\x74\x79\x70\x61\x76\x69\x73") == "image/avif-sequence"
