# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for the manifest dependency pinning recommendation."""

import codecs
import logging
from pathlib import Path
from typing import NoReturn

import pytest

from geneva.manifest import GenevaManifest
from geneva.manifest.pinning import (
    unpinned_pip_requirements,
    unpinned_requirements_file,
    warn_unpinned,
)

# Entries that must draw no advice: exact pins, direct references, and
# lines carrying no version to check at all (flags, comments, bare URLs).
NO_ADVICE_PIP = [
    "numpy==2.1.3",
    "geneva===0.15.0",
    "pillow==12.1.1  # inline comment",
    "fsspec[gcs]==2024.10.0",
    "requests[security,socks]==2.28.0",
    'torch==2.10.0; python_version<"3.13"',
    "mypkg @ https://example.com/mypkg-1.0-py3-none-any.whl",
    "mypkg@https://example.com/mypkg-1.0-py3-none-any.whl",
    "mypkg[extra]@https://example.com/mypkg-1.0-py3-none-any.whl",
    "mypkg [extra] @ https://example.com/mypkg-1.0-py3-none-any.whl",
    "mypkg [extra]@https://example.com/mypkg-1.0-py3-none-any.whl",
    "privatepkg@git+https://example.com/org/repo.git@main",
    "--extra-index-url=https://pypi.fury.io/lancedb/",
    "--pre",
    "-r other-requirements.txt",
    "# a comment",
    "",
    "   ",
    "./local-wheelhouse/mypkg-1.0-py3-none-any.whl",
    "https://example.com/mypkg-1.0.tar.gz",
    "HTTPS://example.com/mypkg-1.0-py3-none-any.whl",
    "ftp://example.com/mypkg-1.0.tar.gz",
    "ftp:example.com/mypkg-1.0.tar.gz",
    "https:example.com/mypkg-1.0.tar.gz",
    "FTP://example.com/capability-token/mypkg-1.0.tar.gz",
    "ftps://example.com/mypkg-1.0.tar.gz",
    "sftp://example.com/mypkg-1.0.tar.gz",
    "hg+ssh://example.com/repo",
    "Git+https://example.com/org/repo.git",
]

# Entries that must be reported, verbatim, as unpinned.
UNPINNED_PIP = [
    "geneva",
    "torch>=2.1",
    "torch>=2.1,<3",
    "numpy>=1.26,<2.0",
    "transformers~=4.49",
    "uvicorn[standard,http2]>=0.30",
    "pandas!=2.0.0",
    "numpy==1.26.*",
    'tomli>=2.0; python_version<"3.11"',
]


@pytest.mark.parametrize("spec", NO_ADVICE_PIP)
def test_no_advice_specifiers_are_not_reported(spec: str) -> None:
    assert unpinned_pip_requirements([spec]) == []


@pytest.mark.parametrize("spec", UNPINNED_PIP)
def test_unpinned_specifiers_are_reported(spec: str) -> None:
    assert unpinned_pip_requirements([spec]) == [spec.strip()]


def test_inline_comment_is_stripped_before_classification() -> None:
    """A pinned spelling cannot show this: unstripped, it simply fails to
    parse, and a skipped line draws no advice either."""
    assert unpinned_pip_requirements(["pillow>=12.1.1  # note"]) == ["pillow>=12.1.1"]


def test_a_range_beside_an_exact_pin_is_not_pinned() -> None:
    """'torch>=2.1,<3' fails on its operator alone. Only an exact pin beside
    a range reaches the count check, and specifier order is not guaranteed."""
    assert unpinned_pip_requirements(["numpy==2.0,<3"]) == ["numpy==2.0,<3"]


def test_requirements_file_is_checked(tmp_path: Path) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("# deps\nnumpy==2.1.3\ntorch>=2.1\n\ngeneva\n")
    assert unpinned_requirements_file(str(req)) == ["torch>=2.1", "geneva"]


def test_missing_requirements_file_is_ignored(tmp_path: Path) -> None:
    assert unpinned_requirements_file(str(tmp_path / "nope.txt")) == []


def test_pip_builder_warns_on_unpinned(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("m").pip(["pandas==2.2.3", "torch>=2.1"]).build()

    assert "torch>=2.1" in caplog.text
    assert "pandas" not in caplog.text
    assert "Pin exact versions" in caplog.text


def test_pip_builder_silent_when_pinned(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("m").pip(["numpy==2.1.3"]).build()

    assert caplog.text == ""


def test_pip_builder_warning_can_be_silenced(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("m").pip(["torch>=2.1"]).allow_unpinned().build()

    assert caplog.text == ""


def test_pip_builder_warns_on_unpinned_requirements_file(
    caplog: pytest.LogCaptureFixture, tmp_path: Path
) -> None:
    req = tmp_path / "requirements.txt"
    req.write_text("torch>=2.1\n")

    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("m").requirements_path(str(req)).build()

    assert "torch>=2.1" in caplog.text
    assert str(req) in caplog.text


def test_site_builder_does_not_warn(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_site("m").build()

    assert caplog.text == ""


# ---------------------------------------------------------------------------
# Credential handling
# ---------------------------------------------------------------------------

_SECRET = "example-secret"  # noqa: S105


def test_credential_bearing_direct_reference_is_not_flagged() -> None:
    """A compact direct reference is exact, so it never reaches the log."""
    spec = f"privatepkg@git+https://user:{_SECRET}@example.com/org/repo.git@main"
    assert unpinned_pip_requirements([spec]) == []


def test_warning_redacts_url_userinfo(caplog: pytest.LogCaptureFixture) -> None:
    spec = f"privatepkg@git+https://user:{_SECRET}@example.com/org/repo.git"
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        warn_unpinned("demo", [spec], "pip")

    assert _SECRET not in caplog.text
    assert "user" not in caplog.text
    assert "example.com/org/repo.git" in caplog.text


@pytest.mark.parametrize(
    "query",
    ["token=SECRET", "jwt=SECRET", "=SECRET", "SECRET", "a=1&=SECRET&b=2"],
)
def test_warning_redacts_keyless_query_components(
    caplog: pytest.LogCaptureFixture, query: str
) -> None:
    """Redaction does not depend on 'key=value' syntax."""
    spec = f"mypkg @ https://example.com/pkg.whl?{query.replace('SECRET', _SECRET)}"
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        warn_unpinned("demo", [spec], "pip")

    assert _SECRET not in caplog.text


def test_uppercase_scheme_url_is_not_flagged() -> None:
    """URL schemes are case-insensitive, so an upper-case one is still a URL."""
    spec = f"HTTPS://example.com/pkg-1.0-py3-none-any.whl?={_SECRET}"
    assert unpinned_pip_requirements([spec]) == []


def test_builder_does_not_log_uppercase_scheme_credentials(
    caplog: pytest.LogCaptureFixture,
) -> None:
    spec = f"HTTPS://example.com/pkg-1.0-py3-none-any.whl?={_SECRET}"
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("demo").pip([spec]).build()

    assert _SECRET not in caplog.text


@pytest.mark.parametrize("key", ["token", "jwt", "sig", "anything"])
def test_warning_redacts_every_query_value(
    caplog: pytest.LogCaptureFixture, key: str
) -> None:
    """Redaction covers all query values, not a list of credential names."""
    spec = f"mypkg @ https://example.com/mypkg.whl?{key}={_SECRET}"
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        warn_unpinned("demo", [spec], "pip")

    assert _SECRET not in caplog.text
    # The key survives so the warning still identifies the specifier.
    assert f"{key}=***" in caplog.text


def test_builder_does_not_log_query_credentials(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """End-to-end: a spelling the classifier may miss still cannot leak."""
    spec = f"mypkg [extra] @ https://example.com/pkg.whl?jwt={_SECRET}"
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("demo").pip([spec]).build()

    assert _SECRET not in caplog.text


def test_warning_leaves_ordinary_specs_intact(
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        warn_unpinned("demo", ["torch>=2.1"], "pip")

    assert "torch>=2.1" in caplog.text


@pytest.mark.parametrize("sep", ["://", ":"])
def test_authority_less_url_spellings_bypass_the_advisory(sep: str) -> None:
    """pip accepts 'ftp:host/path' as well as 'ftp://host/path'."""
    spec = f"ftp{sep}example.com/{_SECRET}/pkg-1.0.tar.gz"
    assert unpinned_pip_requirements([spec]) == []


@pytest.mark.parametrize("scheme", ["ftp", "FTP", "ftps", "sftp", "http", "HTTPS"])
def test_bare_url_schemes_bypass_the_advisory(scheme: str) -> None:
    """A path token cannot be redacted without destroying the dependency
    identity, so URL-only specifiers must never reach the warning."""
    spec = f"{scheme}://example.com/{_SECRET}/pkg-1.0.tar.gz"
    assert unpinned_pip_requirements([spec]) == []


def test_builder_does_not_log_url_path_tokens(
    caplog: pytest.LogCaptureFixture,
) -> None:
    spec = f"FTP://example.com/{_SECRET}/pkg-1.0.tar.gz"
    with caplog.at_level(logging.WARNING, logger="geneva.manifest.pinning"):
        GenevaManifest.create_pip("demo").pip([spec]).build()

    assert _SECRET not in caplog.text


# ---------------------------------------------------------------------------
# Agreement with pip's own URL recognizer
# ---------------------------------------------------------------------------

# Every bare-URL spelling raised during review, plus the schemes around them.
_URL_CORPUS = [
    "https://example.com/pkg-1.0.tar.gz",
    "HTTPS://example.com/pkg-1.0.tar.gz",
    "http://example.com/pkg-1.0.tar.gz",
    "ftp://example.com/token/pkg-1.0.tar.gz",
    "FTP://example.com/token/pkg-1.0.tar.gz",
    "ftp:example.com/token/pkg-1.0.tar.gz",
    "https:example.com/pkg-1.0.tar.gz",
    "file:///wheels/pkg-1.0.tar.gz",
    "git+https://example.com/org/repo.git",
    "hg+ssh://example.com/repo",
]


@pytest.mark.parametrize("spec", _URL_CORPUS)
def test_agrees_with_pip_on_bare_urls(spec: str) -> None:
    """Anything pip resolves as a URL must bypass the version advisory.

    pip's URL recognizer is private API, so skip rather than fail if it
    moves; the corpus above still covers the behaviour on its own.
    """
    is_url = pytest.importorskip("pip._internal.vcs.versioncontrol").is_url

    assert is_url(spec), f"corpus entry is no longer a pip URL: {spec}"
    assert unpinned_pip_requirements([spec]) == []


# ---------------------------------------------------------------------------
# The advisory fails open
# ---------------------------------------------------------------------------


def test_undecodable_requirements_file_does_not_break_build(tmp_path: Path) -> None:
    """A file pip accepts must never fail to build because of the advisory."""
    req = tmp_path / "latin-requirements.txt"
    req.write_bytes(
        "# -*- coding: latin-1 -*-\n# caf\xe9\nnumpy==2.1.3\n".encode("latin-1")
    )

    GenevaManifest.create_pip("demo").requirements_path(str(req)).build()
    assert unpinned_requirements_file(str(req)) == []


def test_backslash_continuation_is_one_logical_line(tmp_path: Path) -> None:
    """pip joins 'numpy \\' + '>=1' into one range; so must the advisory."""
    req = tmp_path / "continued-requirements.txt"
    req.write_text("numpy \\\n>=1\n")

    assert unpinned_requirements_file(str(req)) == ["numpy >=1"]


def test_advisory_failure_does_not_break_build(monkeypatch) -> None:
    """Any error while working out the advice is swallowed, not raised."""
    import geneva.manifest.builder as builder_mod

    def _boom(*_args, **_kwargs) -> NoReturn:
        raise RuntimeError("classifier exploded")

    monkeypatch.setattr(builder_mod, "unpinned_pip_requirements", _boom)

    manifest = GenevaManifest.create_pip("demo").pip(["numpy"]).build()
    assert manifest.pip == ["numpy"]


def test_a_comment_continuation_does_not_swallow_the_next_line(
    tmp_path: Path,
) -> None:
    """pip does not continue a full-line comment ending in a backslash.

    Joining it would fold the requirement below into the comment, and the
    advisory would report nothing for a file pip installs unpinned.
    """
    req = tmp_path / "comment-requirements.txt"
    req.write_text("# comment \\\npackaging\n")

    assert unpinned_requirements_file(str(req)) == ["packaging"]


@pytest.mark.parametrize(
    ("bom", "encoding"),
    [
        (codecs.BOM_UTF8, "utf-8"),
        (codecs.BOM_UTF16_LE, "utf-16-le"),
        (codecs.BOM_UTF16_BE, "utf-16-be"),
        (codecs.BOM_UTF32_LE, "utf-32-le"),
        (codecs.BOM_UTF32_BE, "utf-32-be"),
    ],
)
def test_byte_order_marked_files_are_read(
    tmp_path: Path, bom: bytes, encoding: str
) -> None:
    """pip honours these marks, so a dependency behind one is still advice."""
    req = tmp_path / "bom-requirements.txt"
    req.write_bytes(bom + "packaging\n".encode(encoding))

    assert unpinned_requirements_file(str(req)) == ["packaging"]


def test_an_undecodable_file_warns_rather_than_reading_as_pinned(
    tmp_path: Path, caplog
) -> None:
    """An empty result would read as 'everything is pinned'. Say so instead."""
    req = tmp_path / "binary-requirements.txt"
    req.write_bytes(b"\xff\x00\xfe\x81packaging")

    with caplog.at_level(logging.WARNING):
        assert unpinned_requirements_file(str(req)) == []

    assert "Could not check" in caplog.text
    assert str(req) in caplog.text


def test_a_missing_file_stays_quiet(tmp_path: Path, caplog) -> None:
    """Unlike an unreadable encoding, the install itself reports this one."""
    with caplog.at_level(logging.WARNING):
        assert unpinned_requirements_file(str(tmp_path / "nope.txt")) == []

    assert caplog.text == ""
