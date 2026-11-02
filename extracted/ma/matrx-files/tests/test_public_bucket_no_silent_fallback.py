"""A PUBLIC write with no public bucket FAILS. It never lands in the private one.

THE BUG THIS LOCKS OUT. Four write sites in `sync_engine` resolved their bucket
as::

    bucket = public_bucket() or self._config.resolve_s3_bucket()

`public_bucket()` returns None whenever the CDN feature is off. So a caller that
asked for a PUBLIC file got its bytes written into the DEFAULT bucket — the
private one, with S3 Block Public Access fully ON — while the row was still
stamped as published to the web.

Nothing failed. Nothing logged. The result is a file the platform believes is
world-readable whose bytes no anonymous reader can ever fetch, so every URL
minted for it is a signed one that expires. The podcast cover, the blog image,
the OG card: all fine for an hour, all dead after, with a green run behind them.

WHY IT IS NOT A FALLBACK. A fallback substitutes an EQUIVALENT — a second CDN
serving the same bytes to the same audience. Writing a public asset into a
private bucket substitutes something that does not do the job at all, and says
nothing. There is no correct silent degradation: a "public" file that cannot be
read publicly is a lie. Store it publicly, or refuse.

If a test here fails, the fix is to configure `CDN_PUBLIC_BASE_URL` +
`AWS_S3_PUBLIC_BUCKET` (both — either alone leaves the feature OFF), or to write
the file `personal`. It is NEVER to restore the `or` .
"""

from __future__ import annotations

import pytest

from matrx_files.cloud_sync import cdn
from matrx_files.cloud_sync.cdn import (
    PublicBucketUnconfiguredError,
    public_bucket_or_raise,
)


@pytest.fixture
def cdn_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """The CDN feature unconfigured — the state that used to fall back."""
    monkeypatch.setattr(cdn, "_cdn_base_url", lambda: None)


@pytest.fixture
def cdn_on(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cdn, "_cdn_base_url", lambda: "https://cdn.matrxserver.com")
    monkeypatch.setattr(cdn, "_setting", lambda *names: "cdn.matrxserver.com")


class TestTheResolver:
    def test_it_raises_when_there_is_nowhere_public_to_write(self, cdn_off: None) -> None:
        with pytest.raises(PublicBucketUnconfiguredError):
            public_bucket_or_raise("test")

    def test_the_error_names_the_cause_and_both_settings(self, cdn_off: None) -> None:
        # A loud failure nobody can act on is only half a fix.
        with pytest.raises(PublicBucketUnconfiguredError) as exc:
            public_bucket_or_raise("test")
        message = str(exc.value)
        assert "CDN_PUBLIC_BASE_URL" in message
        assert "AWS_S3_PUBLIC_BUCKET" in message
        assert "private bucket" in message

    def test_the_error_carries_the_callers_context(self, cdn_off: None) -> None:
        with pytest.raises(PublicBucketUnconfiguredError, match="set_published_to_web"):
            public_bucket_or_raise("set_published_to_web")

    def test_it_returns_the_bucket_when_configured(self, cdn_on: None) -> None:
        assert public_bucket_or_raise("test") == "cdn.matrxserver.com"


class TestNoWriteSiteCanSilentlyDegrade:
    """The set-level rule — a NEW public write site cannot reintroduce the bug."""

    def test_no_silent_public_bucket_fallback_survives_anywhere_in_cloud_sync(
        self,
    ) -> None:
        """Scans the WHOLE cloud_sync package, not one file.

        The first version of this guard scanned only `sync_engine.py` — and two
        live sites survived it in `transports/presigned.py` and `transports/tus.py`,
        the paths every BROWSER upload goes through. A guard narrower than the
        bug is how a bug comes back. If a new module needs a bucket for a public
        write, it uses `public_bucket_or_raise` like everything else.
        """
        from pathlib import Path

        import matrx_files.cloud_sync as cloud_sync_pkg

        root = Path(cloud_sync_pkg.__file__).parent
        offenders = [
            f"{path.relative_to(root)}:{i}"
            for path in sorted(root.rglob("*.py"))
            for i, line in enumerate(path.read_text().splitlines(), 1)
            if "public_bucket() or" in line
        ]
        assert not offenders, (
            "A public write is resolving its bucket with `public_bucket() or "
            "<private bucket>`. That silently stores a public asset where no "
            "anonymous reader can reach it, while the row still says "
            "published to the web. Use public_bucket_or_raise():\n  " + "\n  ".join(offenders)
        )

    def test_a_public_write_raises_rather_than_using_the_private_bucket(
        self, cdn_off: None, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The real method, not the helper — proving the call site is wired."""
        from matrx_files.cloud_sync.sync_engine import SyncEngine

        engine = SyncEngine.__new__(SyncEngine)
        monkeypatch.setattr(
            type(engine), "_resolve_user_id", lambda self, uid: uid or "u", raising=False
        )
        object.__setattr__(
            engine,
            "_config",
            type(
                "C",
                (),
                {"storage_backend": "s3", "resolve_s3_bucket": lambda self: "matrx-user-files"},
            )(),
        )

        # personal still works — this must not become a blanket outage.
        assert "matrx-user-files" in engine._storage_uri("f.png", "u", published_to_web=False)

        with pytest.raises(PublicBucketUnconfiguredError):
            engine._storage_uri("f.png", "u", published_to_web=True)
