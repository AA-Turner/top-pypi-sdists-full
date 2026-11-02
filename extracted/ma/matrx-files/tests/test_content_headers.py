"""Regression tests for the Content-Type / Content-Disposition write contract.

The bug these lock down: cloud objects were written with NO ContentType, so
S3 stored them as ``binary/octet-stream`` and bare public CDN URLs downloaded
instead of rendering. Every S3 PUT path must now stamp a definitive
ContentType + a policy-correct ContentDisposition, sourced from the one
``resolve_object_headers`` SSOT.

``build_content_disposition`` is the per-REQUEST header (download_stream,
aidream vault + versions routers). Its expected strings below are written by
hand from RFC 6266 §4.1 (``disposition-type; filename=quoted-string;
filename*=ext-value``) and RFC 5987 §3.2 (``ext-value = charset "'" [language]
"'" value-chars``; ``attr-char`` excludes space, ``"``, ``/``, ``:``, ``=``,
``\\`` — each must be percent-encoded as UTF-8 octets).
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from matrx_files.content_headers import (
    ObjectHeaders,
    build_content_disposition,
    resolve_object_headers,
    sniffed_content_type,
)
from matrx_files.backends.s3_backend import S3Backend


# --------------------------------------------------------------------------
# Policy SSOT — resolve_object_headers
# --------------------------------------------------------------------------

def test_declared_mime_on_extensionless_key_is_authoritative():
    # The canonical org-logo case: key is <owner>/<file_id> (no extension),
    # so the declared mime is the ONLY source. Must NOT be octet-stream.
    h = resolve_object_headers(mime_type="image/png", file_name="4cf62e4e/b093954c")
    assert h == ObjectHeaders(content_type="image/png", content_disposition="inline")


def test_declared_mime_wins_over_conflicting_extension():
    # file_name's extension says PDF; the declared mime says PNG. The mime
    # must win — a mutation preferring the extension would flip this to
    # application/pdf.
    h = resolve_object_headers(mime_type="image/png", file_name="x.pdf")
    assert h.content_type == "image/png"


def test_guess_from_extension_when_no_declared_mime():
    h = resolve_object_headers(mime_type=None, file_name="logo/v/logo_lg.png")
    assert h.content_type == "image/png"
    assert h.content_disposition == "inline"


def test_pdf_is_inline():
    h = resolve_object_headers(mime_type="application/pdf", file_name="x")
    assert h.content_disposition == "inline"


def test_dangerous_svg_is_coerced_to_attachment():
    # SVG can carry script — stored-XSS guard forces octet-stream + attachment.
    h = resolve_object_headers(mime_type="image/svg+xml", file_name="logo.svg")
    assert h.content_type == "application/octet-stream"
    assert h.content_disposition == "attachment"


def test_dangerous_html_is_coerced_to_attachment():
    h = resolve_object_headers(mime_type="text/html", file_name="page.html")
    assert h.content_type == "application/octet-stream"
    assert h.content_disposition == "attachment"


def test_unknown_bytes_fall_back_to_octet_attachment():
    h = resolve_object_headers(mime_type=None, file_name="blob")
    assert h.content_type == "application/octet-stream"
    assert h.content_disposition == "attachment"


def test_non_renderable_known_type_is_attachment():
    h = resolve_object_headers(mime_type="application/zip", file_name="a.zip")
    assert h.content_type == "application/zip"
    assert h.content_disposition == "attachment"


def test_read_side_policy_shares_the_same_decision():
    # download_stream re-exports this; write + read must agree.
    ct, force_attach = sniffed_content_type(
        {"mime_type": "image/png", "file_name": "a.png"}, allow_inline=True
    )
    assert ct == "image/png"
    assert force_attach is False


def test_read_side_forces_attachment_for_renderable_type_when_inline_not_requested():
    # The download route defaults to allow_inline=False: even a PNG downloads.
    assert sniffed_content_type(
        {"mime_type": "image/png", "file_name": "a.png"}, allow_inline=False
    ) == ("image/png", True)


# --------------------------------------------------------------------------
# build_content_disposition — the per-request download header
# --------------------------------------------------------------------------

def test_content_disposition_is_inline_when_attachment_not_forced():
    assert build_content_disposition("report.pdf", force_attachment=False) == (
        "inline; filename=\"report.pdf\"; filename*=UTF-8''report.pdf"
    )


def test_content_disposition_is_attachment_when_forced():
    assert build_content_disposition("report.pdf", force_attachment=True) == (
        "attachment; filename=\"report.pdf\"; filename*=UTF-8''report.pdf"
    )


def test_content_disposition_percent_encodes_non_ascii_name_as_utf8_octets():
    # é = U+00E9 = UTF-8 C3 A9; space = %20. ASCII fallback replaces é with "_".
    assert build_content_disposition("résumé final.pdf", force_attachment=True) == (
        "attachment; filename=\"r_sum_ final.pdf\"; "
        "filename*=UTF-8''r%C3%A9sum%C3%A9%20final.pdf"
    )


def test_content_disposition_percent_encodes_rfc5987_non_attr_chars():
    # ':' '/' ' ' '"' are not attr-chars → %3A %2F %20 %22. In the quoted
    # fallback only '"' is unsafe (would close the quoted-string) → "_".
    assert build_content_disposition('Q3: a/b "draft".txt', force_attachment=False) == (
        "inline; filename=\"Q3: a/b _draft_.txt\"; "
        "filename*=UTF-8''Q3%3A%20a%2Fb%20%22draft%22.txt"
    )


@pytest.mark.parametrize(
    ("file_name", "expected"),
    [
        # CR LF would split the header (response-splitting / Set-Cookie injection).
        (
            "evil\r\nSet-Cookie: s=1.txt",
            "attachment; filename=\"evil__Set-Cookie: s=1.txt\"; "
            "filename*=UTF-8''evil%0D%0ASet-Cookie%3A%20s%3D1.txt",
        ),
        # A backslash is the quoted-pair escape — it would escape the closing quote.
        (
            "a\\\".txt",
            "attachment; filename=\"a__.txt\"; filename*=UTF-8''a%5C%22.txt",
        ),
        # TAB and DEL are CTLs (RFC 7230 §3.2.6 qdtext excludes them).
        (
            "a\tb\x7fc.txt",
            "attachment; filename=\"a_b_c.txt\"; filename*=UTF-8''a%09b%7Fc.txt",
        ),
    ],
)
def test_content_disposition_ascii_fallback_never_carries_header_breaking_chars(
    file_name: str, expected: str
):
    assert build_content_disposition(file_name, force_attachment=True) == expected


# --------------------------------------------------------------------------
# S3Backend stamps the headers on every PUT path
# --------------------------------------------------------------------------

def _fake_s3() -> S3Backend:
    b = S3Backend.__new__(S3Backend)  # bypass __init__ (no creds needed)
    b._client = MagicMock()
    b._configured = True
    b._default_bucket = "cdn.matrxserver.com"
    b._region = "us-east-1"
    return b


def test_write_stamps_content_type_and_inline_disposition():
    b = _fake_s3()
    b.write("cdn.matrxserver.com/owner/fileid", b"\x89PNG data", content_type="image/png")
    b._client.put_object.assert_called_once()
    kw = b._client.put_object.call_args.kwargs
    assert kw["ContentType"] == "image/png"
    assert kw["ContentDisposition"] == "inline"


def test_write_without_content_type_never_emits_octet_for_known_extension():
    b = _fake_s3()
    b.write("cdn.matrxserver.com/owner/logo.png", b"data")  # no content_type kwarg
    kw = b._client.put_object.call_args.kwargs
    assert kw["ContentType"] == "image/png"


def test_multipart_upload_stamps_content_type():
    b = _fake_s3()
    b._client.create_multipart_upload.return_value = {"UploadId": "uid"}
    b._client.upload_part.return_value = {"ETag": "etag"}
    headers = resolve_object_headers(mime_type="image/png", file_name="key")
    b._multipart_upload(b._client, "cdn.matrxserver.com", "owner/fileid", b"x" * 16, None, headers)
    kw = b._client.create_multipart_upload.call_args.kwargs
    assert kw["ContentType"] == "image/png"
    assert kw["ContentDisposition"] == "inline"


def test_restamp_headers_uses_copy_object_replace():
    b = _fake_s3()
    ok = b.restamp_headers(
        "cdn.matrxserver.com/owner/fileid",
        content_type="image/png",
        content_disposition="inline",
    )
    assert ok is True
    b._client.copy_object.assert_called_once()
    kw = b._client.copy_object.call_args.kwargs
    assert kw["MetadataDirective"] == "REPLACE"
    assert kw["ContentType"] == "image/png"
    assert kw["ContentDisposition"] == "inline"
    assert kw["CopySource"] == {"Bucket": "cdn.matrxserver.com", "Key": "owner/fileid"}
