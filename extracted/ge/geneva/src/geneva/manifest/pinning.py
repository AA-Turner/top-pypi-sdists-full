# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Dependency pinning checks for pip manifests.

Manifest dependencies are installed by Ray on the workers, not copied from
the local environment. A ranged or unversioned specifier (``numpy``,
``torch>=2.1``) therefore resolves to whatever version is newest at install
time, which drifts away from the local environment and surfaces later as
serialization errors, missing attributes, or wrong results. These helpers
detect such specifiers so callers can recommend exact pins instead.

Entries are classified by :mod:`packaging`, the PEP 508 parser pip itself
uses, rather than by pattern matching here. Anything it rejects -- a URL, a
local path, a ``-r``/``--flag`` line, a comment -- carries no version to
check and is skipped.

Conda is deliberately not covered. Its grammar has no comparably light
parser (conda's own requires conda installed), and hand-reading channel and
URL syntax well enough to advise on it costs far more than the advice is
worth.
"""

import codecs
import logging
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from packaging.requirements import InvalidRequirement, Requirement

_LOG = logging.getLogger(__name__)

# Advice appended to every unpinned-dependency warning.
PINNING_ADVICE = (
    "Ranged or unversioned dependencies resolve to whatever version is "
    "newest when Ray installs them on the workers, which may not match the "
    "local environment. Pin exact versions instead (e.g. 'numpy==2.1.3')."
)

# Operators that name one release rather than a family of them.
_EXACT_OPERATORS = ("==", "===")

_INLINE_COMMENT = re.compile(r"\s+#")

# Credentials that can ride along in a URL. A direct reference counts as
# pinned and a bare URL does not parse, so neither reaches the warning
# today; this stays as a backstop on the log boundary itself.
_URL_USERINFO = re.compile(r"(?<=://)[^/\s@]+@")
# The whole query component, redacted piece by piece below. A secret can be
# called anything ('?jwt=', '?sig='), or carry no name at all ('?=secret',
# '?opaque-token'), so nothing here may depend on 'key=value' syntax.
_URL_QUERY = re.compile(r"(?<=\?)[^\s#]+")
_REDACTED = "***"


def _redact_query(match: re.Match[str]) -> str:
    """Replace every value in a matched URL query component."""
    redacted = []
    for component in match.group(0).split("&"):
        key, sep, _ = component.partition("=")
        # A keyless component ('=secret', 'opaque') is value all the way.
        redacted.append(f"{key}{sep}{_REDACTED}" if key and sep else _REDACTED)
    return "&".join(redacted)


def _redact(spec: str) -> str:
    """Return ``spec`` with any embedded credentials replaced."""
    spec = _URL_USERINFO.sub(f"{_REDACTED}@", spec)
    return _URL_QUERY.sub(_redact_query, spec)


def _is_pinned(requirement: Requirement) -> bool:
    """Whether a parsed requirement names exactly one version."""
    # A direct reference ('pkg @ https://...') already names one artifact.
    if requirement.url is not None:
        return True
    specifiers = list(requirement.specifier)
    if len(specifiers) != 1:
        return False
    only = specifiers[0]
    return only.operator in _EXACT_OPERATORS and "*" not in only.version


def unpinned_pip_requirements(pip: Iterable[Any]) -> list[str]:
    """Return the pip specifiers in ``pip`` that are not pinned to a version."""
    unpinned = []
    for raw in pip:
        spec = _INLINE_COMMENT.split(str(raw), maxsplit=1)[0].strip()
        if not spec:
            continue
        try:
            requirement = Requirement(spec)
        except InvalidRequirement:
            # Not a version-constrained requirement: a URL, a local path, an
            # option line, or a comment. Those already name one artifact.
            continue
        if not _is_pinned(requirement):
            unpinned.append(spec)
    return unpinned


# Byte-order marks pip accepts, longest first: the UTF-32 marks start with
# the UTF-16 ones, so a shorter match would win and mis-decode the file.
_BOMS = (
    (codecs.BOM_UTF32_LE, "utf-32"),
    (codecs.BOM_UTF32_BE, "utf-32"),
    (codecs.BOM_UTF8, "utf-8-sig"),
    (codecs.BOM_UTF16_LE, "utf-16"),
    (codecs.BOM_UTF16_BE, "utf-16"),
)


def _decode(raw: bytes) -> str | None:
    """Decode a requirements file, or ``None`` if its encoding is unknown.

    pip honours byte-order marks and a declared encoding. Those marks are
    cheap to handle; the rest of that grammar is not, and this is advice
    rather than a gate. So anything else is refused here and reported by the
    caller -- decoding it leniently would turn a real dependency into
    replacement characters and quietly drop it from the advice.
    """
    for bom, encoding in _BOMS:
        if raw.startswith(bom):
            try:
                return raw.decode(encoding)
            except UnicodeDecodeError:
                return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _logical_lines(text: str) -> list[str]:
    """Join trailing-backslash continuations into single logical lines.

    pip drops the backslash and newline but keeps the surrounding spacing.
    It does not continue a line that is a comment, so a ``# note \\`` must
    not swallow the requirement written under it.
    """
    lines: list[str] = []
    pending = ""
    for raw_line in text.splitlines():
        line = pending + raw_line.rstrip("\r")
        if line.endswith("\\") and not line.lstrip().startswith("#"):
            pending = line[:-1]
            continue
        lines.append(line)
        pending = ""
    if pending:
        lines.append(pending)
    return lines


def unpinned_requirements_file(path: str) -> list[str]:
    """Return the unpinned specifiers in the requirements file at ``path``.

    Returns an empty list when the file cannot be read; a missing file is
    reported by the install itself, not by this advisory check. A file whose
    encoding this cannot determine is warned about rather than skipped
    silently -- an empty result otherwise reads as "everything is pinned".
    """
    try:
        raw = Path(path).read_bytes()
    except OSError as e:
        _LOG.debug("Skipping pinning check for %s: %s", path, e)
        return []
    text = _decode(raw)
    if text is None:
        _LOG.warning(
            "Could not check %s for unpinned dependencies: its encoding is "
            "neither UTF-8 nor a form carrying a byte-order mark. Check the "
            "pins in it by hand.",
            path,
        )
        return []
    return unpinned_pip_requirements(_logical_lines(text))


def warn_unpinned(name: str | None, unpinned: list[str], source: str) -> None:
    """Log a recommendation to pin the specifiers listed in ``unpinned``."""
    if not unpinned:
        return
    _LOG.warning(
        "Manifest %s: %d unpinned dependency specifier(s) in %s: %s. %s",
        name or "<unnamed>",
        len(unpinned),
        source,
        ", ".join(_redact(spec) for spec in unpinned),
        PINNING_ADVICE,
    )
