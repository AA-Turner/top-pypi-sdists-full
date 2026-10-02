"""Real encrypted ZIP members warn; later readable credentials still refuse."""

import base64
import io
import zipfile

import pytest

from probe.sdk.secret_gate import (
    ArtifactInspectionWarning,
    CredentialBlocked,
    ScanPolicy,
    inspect_bytes,
    read_upload,
)

# Generated with `zip -P fabricated-fixture-only encrypted.zip hidden.txt`.
# The password and contents are fabricated; this is actual ZipCrypto ciphertext,
# not a cleartext ZIP with only its encryption flag changed.
ENCRYPTED_ZIP = base64.b64decode(
    "UEsDBAoACQAAAJthMl3iZ/h9LQAAACEAAAAKABwAaGlkZGVuLnR4dFVUCQADNo2tajaNrWp1eAsA"
    "AQT1AQAABBQAAABPcN3NWF/aAIOMSmGhM6sCvQeOb5ozB7evMdUdmPaSwJpKSSCoIG5MgQkUpaxQ"
    "SwcI4mf4fS0AAAAhAAAAUEsBAh4DCgAJAAAAm2EyXeJn+H0tAAAAIQAAAAoAGAAAAAAAAQAAAKSB"
    "AAAAAGhpZGRlbi50eHRVVAUAAzaNrWp1eAsAAQT1AQAABBQAAABQSwUGAAAAAAEAAQBQAAAAgQAAAAAA"
)


def _mixed_archive(visible: bytes) -> bytes:
    stream = io.BytesIO(ENCRYPTED_ZIP)
    with zipfile.ZipFile(stream, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("visible.txt", visible)
    return stream.getvalue()


def test_real_encrypted_archive_warns_and_preserves_bytes(tmp_path, monkeypatch):
    monkeypatch.delenv("PROBE_ARTIFACT_OPAQUE_POLICY", raising=False)
    raw = _mixed_archive(b"learning_rate=0.003\n")
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        assert archive.infolist()[0].flag_bits & 1
        with pytest.raises(RuntimeError, match="password required"):
            archive.read("hidden.txt")
        assert archive.read("hidden.txt", pwd=b"fabricated-fixture-only") == (
            b"ordinary hidden checkpoint state\n"
        )
        assert archive.read("visible.txt") == b"learning_rate=0.003\n"
    result = inspect_bytes(raw)
    assert not result.fully_inspected
    assert "encrypted archive" in result.warning_message
    source = tmp_path / "encrypted.zip"
    source.write_bytes(raw)
    with pytest.warns(ArtifactInspectionWarning, match="cannot confirm"):
        assert read_upload(source) == raw


def test_real_encrypted_archive_is_refused_by_explicit_strict_policy():
    with pytest.raises(CredentialBlocked, match="encrypted archive"):
        inspect_bytes(ENCRYPTED_ZIP, scan_policy=ScanPolicy(allow_opaque=False))


def test_real_encrypted_member_does_not_hide_later_readable_credential():
    raw = _mixed_archive(b"password=FabricatedLaterMemberOnly123!\n")
    # Recorded, not refused: a credential never costs the upload.
    assert inspect_bytes(raw, scan_policy=ScanPolicy(allow_opaque=True)).has_findings
