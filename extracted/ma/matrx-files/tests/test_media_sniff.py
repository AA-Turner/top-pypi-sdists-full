from matrx_files.media_sniff import sniff_mime_type


def test_textual_ts_overrides_platform_transport_stream_guess() -> None:
    assert (
        sniff_mime_type(
            claimed="application/octet-stream",
            head_bytes=b"export const answer: number = 42;\n",
            filename="answer.ts",
        )
        == "text/typescript"
    )


def test_explicit_typescript_claim_handles_empty_source() -> None:
    assert (
        sniff_mime_type(
            claimed="text/typescript",
            head_bytes=b"",
            filename="empty.mts",
        )
        == "text/typescript"
    )


def test_textual_mts_overrides_a_wrong_transport_stream_claim() -> None:
    assert (
        sniff_mime_type(
            claimed="video/mp2t",
            head_bytes=b"export default function main(): void {}\n",
            filename="main.mts",
        )
        == "text/typescript"
    )


def test_tsx_and_cts_are_unambiguously_typescript() -> None:
    for filename in ("component.tsx", "module.cts"):
        assert (
            sniff_mime_type(
                claimed="application/octet-stream",
                head_bytes=b"",
                filename=filename,
            )
            == "text/typescript"
        )


def test_binary_ts_remains_mpeg_transport_stream_when_host_mime_db_calls_it_qt_linguist(
    monkeypatch,
) -> None:
    # Ubuntu's shared-mime-info maps `.ts` to Qt Linguist while macOS maps it
    # to MPEG-TS. The bytes are two valid 188-byte MPEG transport packets, so
    # this classification must not depend on the host MIME database.
    monkeypatch.setattr(
        "matrx_files.media_sniff.mimetypes.guess_type",
        lambda _: ("text/vnd.trolltech.linguist", None),
    )
    transport_packet = b"\x47" + (b"A" * 187)
    assert (
        sniff_mime_type(
            claimed="video/mp2t",
            head_bytes=transport_packet * 2,
            filename="recording.ts",
        )
        == "video/mp2t"
    )
