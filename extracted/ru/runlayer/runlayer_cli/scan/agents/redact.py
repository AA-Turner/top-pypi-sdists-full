"""Redaction helpers for the agent-report submission.

The agent report leaves the device, so scan-derived paths and matched tokens are
scrubbed before submission: never file contents or environment variables (those
are never collected), and any path/URL that would leak a home-directory username
or an embedded credential is stripped. Fingerprints are computed over normalized
project markers (dependency set), not paths, so scrubbing the path never affects
per-org catalog dedupe.

Scrubbing layers, in order: the container mount-prefix strip (shared with the MCP
scan payload), URL-credential removal, home-directory username redaction, the
*known* scan username (the authoritative path owner, redacted as a whole path
segment wherever it appears), and finally a credential/secret token pass. The
secret patterns are a stdlib-only mirror of the backend security scanner
(``backend/app/domains/security/engine/scanners/token_masking.py``); we can't
import that module across the service boundary (and it pulls in ``structlog`` /
``app.*``, which the frozen ``aiwatch`` closure forbids), so the high-signal
subset is copied here -- keep the two in sync when either changes.

Standard-library plus the RE2 ``regex_safe`` wrapper (same closure footing as
``detect.py``; ``re2`` ships in the frozen ``aiwatch`` bundle) and
``runlayer_cli.paths``.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import PurePosixPath, PureWindowsPath

from runlayer_cli import regex_safe
from runlayer_cli.paths import strip_reported_path_prefix

_WSB = regex_safe.STDLIB_WS_BODY

# URL userinfo: ``scheme://user:pass@host`` or ``scheme://user@host`` -> drop the
# credential, keep the scheme + host.
# Both classes are spelled Unicode-exact, because RE2 narrows `\s` AND `\w`
# to ASCII and each narrowing leaks in the same direction. `\s`: the userinfo
# run would swallow Unicode whitespace. `\w`: a scheme whose last character
# before `://` is non-ASCII (`http\u00e9://user:secret@host`) stops matching
# entirely -- RE2 cannot restart later either, since the char before `:` is
# not in its `\w` -- so the credential survives into a report that leaves the
# device. `\p{L}\p{N}_` is stdlib `\w`. Neither `\p{M}` nor `\p{Pc}` belongs:
# stdlib `\w` takes no combining mark, and of the connector punctuation it
# takes only underscore -- U+203F and kin are not `\w` to Python. Either
# would make RE2 strip credentials stdlib left alone.
_URL_SCHEME_WORD = r"\p{L}\p{N}_"
_URL_CREDENTIALS = regex_safe.compile(
    rf"(?P<scheme>[a-zA-Z][{_URL_SCHEME_WORD}+.\-]*://)[^/@{_WSB}]+@"
)

# The account segment in a POSIX or Windows home path: the component right after
# ``Users``/``home`` is the username. Replace it so the path shape (which
# framework lives where) survives without leaking who owns it. This is the
# fallback for users whose name we don't know (e.g. a stray path from another
# profile); the running scan's own user is handled precisely below.
_HOME_SEGMENT = regex_safe.compile(
    r"(?P<root>[/\\](?:Users|home)[/\\])(?P<user>[^/\\]+)",
    regex_safe.IGNORECASE,
)

_REDACTED = "<redacted>"

# RE2's `(?i)` is ASCII-only, but stdlib `IGNORECASE` also folded three
# non-ASCII characters into ASCII letters: U+0130/U+0131 into "i", U+017F into
# "s", U+212A into "k". Key labels match case-insensitively, so without this a
# token written `API_KEY` with a Turkish dotted I matched under the old engine
# and stops matching under RE2 -- the secret then survives into a report that
# leaves the device. Fail-OPEN, so the literals are widened rather than left
# to `(?i)`. The three characters come from sweeping every non-ASCII codepoint
# for ones an ASCII letter matches under IGNORECASE; the sweep is a test.
_CI_EXTRAS = {"i": "\u0130\u0131", "s": "\u017f", "k": "\u212a"}


def _ci(word: str) -> str:
    """A literal matching like stdlib IGNORECASE, including those extras."""
    out = []
    for char in word:
        if char.isalpha():
            low = char.lower()
            out.append(f"[{low}{low.upper()}{_CI_EXTRAS.get(low, '')}]")
        else:
            out.append(regex_safe.escape(char))
    return "".join(out)


# Credential/secret token patterns whose ENTIRE match is masked. Mirror of the
# high-signal, low-false-positive prefixed-token subset of the backend
# TokenMaskingScanner (see module docstring). Deliberately omitted: the bare
# 40-char base64 "AWS Secret Key" (over-redacts ordinary path/hash segments) and
# the database-URL matcher (its credential is already stripped by
# _strip_url_credentials). Registry evidence tokens (``langchain``, ``openai(``)
# are far too short to match any of these, so this is safe to run over evidence.
_SECRET_TOKEN_PATTERNS: tuple[regex_safe.Pattern, ...] = (
    regex_safe.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),  # GitHub token
    regex_safe.compile(r"\bgithub_pat_[A-Za-z0-9_]{72,255}\b"),  # GitHub PAT
    regex_safe.compile(
        # Left on `(?i)`: widening `sk` the way the KV keys are widened buys
        # nothing, because the leading `\b` is ASCII-only under RE2 and
        # already refuses a non-ASCII first character. Closing that needs
        # the `\b` narrowing solved, which is broader than this pattern.
        r"(?i)\bsk[-_](?:[a-z]+[-_])?[A-Za-z0-9_-]{20,}\b"
    ),  # sk-/sk_ keys
    regex_safe.compile(r"\brk_(?:live|test)_[A-Za-z0-9]{20,}\b"),  # Stripe key
    regex_safe.compile(r"\bAKIA[A-Z0-9]{16}\b"),  # AWS access key id
    regex_safe.compile(r"\bAIza[A-Za-z0-9_-]{35}\b"),  # Google API key
    regex_safe.compile(r"\bnpm_[A-Za-z0-9]{36,}\b"),  # npm token
    # Was ...(?![A-Za-z0-9-]) / (?![A-Za-z0-9_-]) on the next three — vacuous
    # (the guard class equals the final quantifier's class, and a maximal
    # greedy run already guarantees the next char is outside it); same drop
    # as the backend token_masking rewrite.
    regex_safe.compile(r"\bxox[bpras]-[A-Za-z0-9-]{10,}"),  # Slack token
    regex_safe.compile(  # JWT (three base64url segments)
        r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
    ),
    regex_safe.compile(  # SendGrid key
        r"\bSG\.[A-Za-z0-9_-]{22,}\.[A-Za-z0-9_-]{22,}"
    ),
    regex_safe.compile(  # PEM private key block
        r"-----BEGIN(?:.+?)PRIVATE KEY-----[^-]+-----END(?:.+?)PRIVATE KEY-----"
    ),
)

# Secret patterns of the ``key = value`` shape: keep the key (group 1) so the
# finding stays legible, mask only the value (group 2). Mirror of the backend
# scanner's keyed patterns.
# The `\s*` separators and the password value class are spelled with the
# stdlib-exact WS body: narrowing to RE2's ASCII `\s` would be fail-OPEN
# (an NBSP-separated `password = ...` stops being redacted). The trailing
# `(?![...(])` guards are vacuous for their class part (a maximal greedy run
# already guarantees the next char is outside it) — only the "(" member is
# real, enforced inside the replacement in _redact_secrets (rejects
# call-sites like get_secret_from_vault("...")). The bool marks patterns
# that carry that former "(" guard.
_SECRET_KV_PATTERNS: tuple[tuple[regex_safe.Pattern, bool], ...] = (
    (
        regex_safe.compile(
            rf"({_ci('api')}[_-]?{_ci('key')}|{_ci('apikey')}"
            rf"|{_ci('access')}[_-]?{_ci('key')})"
            r"(?:[\"']|\\[\"'])?"
            + rf"[{_WSB}]*[:=][{_WSB}]*"
            + r"(?:[\"']|\\[\"'])?([A-Za-z0-9_\-]{16,})",
            regex_safe.IGNORECASE,
        ),
        True,
    ),
    (
        regex_safe.compile(
            rf"({_ci('password')}|{_ci('passwd')}|{_ci('pwd')})"
            r"(?:[\"']|\\[\"'])?"
            + rf"[{_WSB}]*[:=][{_WSB}]*"
            + rf"(?:[\"']|\\[\"'])?([^{_WSB}\"'\\]{{6,}})",
            regex_safe.IGNORECASE,
        ),
        False,
    ),
    (
        regex_safe.compile(
            rf"({_ci('auth')}[_-]?{_ci('token')}|{_ci('token')}"
            rf"|{_ci('bearer')})"
            r"(?:[\"']|\\[\"'])?"
            + rf"[{_WSB}]*[:=][{_WSB}]*"
            + r"(?:[\"']|\\[\"'])?([A-Za-z0-9_\-.]{10,})",
            regex_safe.IGNORECASE,
        ),
        True,
    ),
)


def _strip_url_credentials(text: str) -> str:
    return _URL_CREDENTIALS.sub(r"\g<scheme>", text)


def _redact_home_username(text: str) -> str:
    return _HOME_SEGMENT.sub(rf"\g<root>{_REDACTED}", text)


# Case folding that matches stdlib `re.IGNORECASE`, which is what the pre-RE2
# code used. Per character: use ``casefold()`` when it yields a single char --
# that is what groups the non-obvious classes (Greek final vs medial sigma,
# micro sign vs Greek mu, long s vs s). When it yields several, IGNORECASE
# does NOT fold that character, so fall back to ``lower()``: U+00DF casefolds
# to "ss" but IGNORECASE never matched it against "ss", and folding it would
# make a username "strasse" redact segments reading "stra\u00dfe".
#
# Two codepoints resist both: U+0130 casefolds to i + combining dot, and
# U+0131 casefolds to itself, while IGNORECASE treats each as "i".
#
# Verified by sweeping every codepoint in BMP+SMP against its lower/upper/
# casefold/title forms -- 0 divergences from IGNORECASE. Do not simplify this
# to plain ``casefold()`` or plain ``lower()``; each is wrong in one direction
# and the failure leaks a username into a report that leaves the device.
_FOLD_EXCEPTIONS = {"\u0130": "i", "\u0131": "i"}


def _fold_char(char: str) -> str:
    if char in _FOLD_EXCEPTIONS:
        return _FOLD_EXCEPTIONS[char]
    folded = char.casefold()
    if len(folded) == 1:
        return folded
    lowered = char.lower()
    return lowered if len(lowered) == 1 else char


def _fold(value: str) -> str:
    return "".join(_fold_char(char) for char in value)


def _redact_known_usernames(text: str, usernames: Sequence[str]) -> str:
    """Redact each known username, but only as a whole path segment.

    The running scan knows its own account name (device context), and under
    ``--all-users`` each profile is scanned in its own ``scan --username <user>``
    child -- so the report's paths have a single authoritative owner. Redact that
    name wherever it forms a full path component (bounded by a separator or the
    string edge on both sides) so it is caught in non-home layouts too
    (``/opt/work/alice/agent`` -> ``/opt/work/<redacted>/agent``). Segment
    bounding keeps ``alice-cache`` / ``alice-agent`` intact -- only the exact
    component is the username. Case-insensitive so a Windows path's casing can't
    slip past.

    Split rather than matched: "whole path component" is exactly "segment
    between separators", so comparing split segments is both simpler and
    linear. The regex form this replaced needed the segment bounds as a
    reject-filter (RE2 has no lookbehind), and a rejected candidate resumes
    one char later -- so a token densely repeating the username rescanned the
    tail per occurrence: 8KB took 72ms, 32KB 770ms, 64KB 2.5s. Argv tokens
    reach here before ``redact_argv`` truncates them, so a long command line
    could stall a scan.

    Comparison uses ``_fold``, which reproduces stdlib ``IGNORECASE``.
    RE2's is ASCII-only; ``lower()`` misses the multi-codepoint folds stdlib
    ``IGNORECASE`` performed, so a profile named ``\u017fam`` would not have
    matched ``Sam`` and the username would survive into the report.
    """
    wanted = {_fold(username) for username in usernames if username}
    if not wanted:
        return text

    parts: list[str] = []
    start = 0
    for index, char in enumerate(text):
        if char in "/\\":
            segment = text[start:index]
            parts.append(_REDACTED if _fold(segment) in wanted else segment)
            parts.append(char)
            start = index + 1
    tail = text[start:]
    parts.append(_REDACTED if _fold(tail) in wanted else tail)
    return "".join(parts)


def _mask_value_group(match: regex_safe.Match) -> str:
    """Replacement that masks only capture group 2, preserving the key prefix."""
    whole = match.group(0)
    value_start = match.start(2) - match.start(0)
    value_end = match.end(2) - match.start(0)
    return whole[:value_start] + _REDACTED + whole[value_end:]


def _redact_secrets(text: str) -> str:
    for pattern in _SECRET_TOKEN_PATTERNS:
        text = pattern.sub(_REDACTED, text)
    for pattern, guards_call_paren in _SECRET_KV_PATTERNS:
        if guards_call_paren:
            # The former (?![...(]) lookahead's one real member: a value
            # immediately followed by "(" is a function call in evidence text
            # (get_secret_from_vault("...")), not a secret.
            #
            # Declined as a candidate INSIDE the replacement rather than via
            # sub_filtered's accept: rejecting there resumes with another
            # search(), which re-encodes the whole string per rejection --
            # 64KB of repeated "api_key=...(" cost 224ms and grew
            # quadratically, on argv any local process can shape. Returning
            # the match unchanged is one linear pass. Equivalent because the
            # guard class contains the value class, so backtracking to a
            # shorter run cannot satisfy it either: stdlib rejected the whole
            # start position too.
            text = pattern.sub(
                lambda m, _t=text: (
                    m.group(0)
                    if m.end() < len(_t) and _t[m.end()] == "("
                    else _mask_value_group(m)
                ),
                text,
            )
        else:
            text = pattern.sub(_mask_value_group, text)
    return text


def _replace_surrogates(value: str) -> str:
    """Drop surrogateescape code points RE2 cannot encode.

    Cheap common path: strings without surrogates round-trip and are returned
    unchanged, so this costs one encode attempt per call.
    """
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        return value.encode("utf-8", "replace").decode("utf-8")
    return value


def sanitize_path(value: str | None, *, usernames: Sequence[str] = ()) -> str | None:
    """Scrub a scan-derived path/token before it leaves the device.

    Applies, in order: the container mount-prefix strip shared with the MCP scan
    payload, URL-credential removal, home-directory username redaction, the
    *known* scan username(s) (as whole path segments), and a credential/secret
    token pass. A plain token (dependency name / import / symbol) carries none of
    these and passes through unchanged, so this is safe to run over evidence
    values too.

    ``usernames`` is the report's authoritative path owner(s) (from device
    context); pass them so the account name is scrubbed even outside the standard
    home layout. Empty (the default) falls back to home-segment redaction only.
    """
    if not value:
        return value
    # os.walk hands back surrogateescape code points (U+DCxx) for filenames
    # that are not valid UTF-8, and RE2 works on UTF-8: every substitution
    # below would raise UnicodeEncodeError and take the whole scan down.
    # stdlib `re` operated on the str directly and never saw this. Replacing
    # the undecodable bytes loses nothing that belongs in a report.
    value = _replace_surrogates(value)
    scrubbed = strip_reported_path_prefix(value) or value
    scrubbed = _strip_url_credentials(scrubbed)
    scrubbed = _redact_home_username(scrubbed)
    scrubbed = _redact_known_usernames(scrubbed, usernames)
    scrubbed = _redact_secrets(scrubbed)
    return scrubbed


def redact_basename(value: str | None) -> str | None:
    """Reduce an evidence source to its bare filename.

    Evidence ``source`` is the file where a signal matched; only the basename is
    needed downstream and the full path would leak the host directory layout.
    Both separators are handled so a Windows-style ``a\\b\\c.py`` collapses to
    ``c.py`` even when this runs on a POSIX host: whichever separator actually
    split the path yields the shorter trailing component.
    """
    if not value:
        return value
    posix_name = PurePosixPath(value).name
    windows_name = PureWindowsPath(value).name
    return windows_name if len(windows_name) < len(posix_name) else posix_name
