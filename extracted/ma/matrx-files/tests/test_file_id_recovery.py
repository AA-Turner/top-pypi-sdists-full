"""The ONE recovery of a cld_files id from a URL we minted.

A signed URL is a handoff, never an identity — but a producer that already
handed one out has not structurally lost the identity, because every URL this
platform mints carries the id in its object key. This is what lets a consumer
holding one of our URLs get back to the durable handle instead of persisting a
link that dies. Pinned here because the failure mode is silent: reading the
FIRST UUID in the key hands back the OWNER's id, which looks perfectly valid
and names the wrong row forever.
"""

from __future__ import annotations

import pytest

import matrx_files.cloud_sync.cdn as cdn
import matrx_files.cloud_sync.url_resolver as url_resolver
from matrx_files import file_id_from_our_url

OWNER = "00000000-0000-4000-8000-0000000fffe1"
FILE = "db22f2a2-9548-4eb7-946b-19b267bdee09"


@pytest.fixture(autouse=True)
def _configured_deployment(monkeypatch):
    """CDN + bucket names are deployment inputs; pin them so the shapes resolve."""
    monkeypatch.setattr(cdn, "cdn_base_host", lambda: "cdn.matrxserver.com")
    monkeypatch.setattr(cdn, "public_bucket", lambda: "matrx-public")
    monkeypatch.setattr(url_resolver, "_our_bucket_set", lambda: {"matrx-user-files"})


@pytest.mark.parametrize(
    "url",
    [
        f"https://cdn.matrxserver.com/{OWNER}/{FILE}?v=84f485d6",
        f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE}?X-Amz-Signature=abc",
        f"s3://matrx-user-files/{OWNER}/{FILE}",
        f"https://app.aimatrx.com/files/{FILE}",
        f"https://app.aimatrx.com/files/{FILE}/download",
        FILE,  # the bare id — already the canonical internal handle
    ],
)
def test_recovers_the_file_id_never_the_owner_id(url: str):
    assert file_id_from_our_url(url) == FILE


@pytest.mark.parametrize(
    "url",
    [
        None,
        "",
        "https://example.com/some/image.png",
        "https://app.aimatrx.com/s/sometoken",  # a share token is not a file id
        "not a url",
    ],
)
def test_returns_none_rather_than_guessing(url: str | None):
    """None means 'this URL does not name a file of ours' — never a reason for a
    caller to drop the URL it already holds."""
    assert file_id_from_our_url(url) is None


def test_the_url_we_mint_for_private_files_is_recognized_as_ours(monkeypatch):
    """``durable_inline_url`` is the ONE builder of private-file render URLs.
    Whatever it mints, ``classify_url`` must call ours — otherwise the media
    funnel fetches our own authenticated route anonymously and gets 401
    (podcast W8 compose, 2026-10-07: ``server.app.matrxserver.com`` was not in
    the our-host set)."""
    import matrx_files.cloud_sync.render_urls as render_urls

    for base in ("https://server.app.matrxserver.com", "https://files.newdomain.example"):
        monkeypatch.setattr(render_urls, "files_public_base_url", lambda b=base: b)
        url = render_urls.durable_inline_url(FILE)
        info = url_resolver.classify_url(url)
        assert info.get("is_ours") is True, (base, info)
        assert info.get("kind") == "file_id_download"
        assert file_id_from_our_url(url) == FILE
