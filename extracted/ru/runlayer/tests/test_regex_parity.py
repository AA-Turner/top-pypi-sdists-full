# regex-engine: stdlib-parity
"""Golden-corpus parity tests for the CLI's RE2 rewrites (ENG-4056).

Freezes the OLD stdlib-`re` patterns (lookarounds RE2 cannot express) as the
behavior spec and asserts the RE2 rewrites agree on a corpus.
"""

from __future__ import annotations

import importlib
import random
import re as stdlib_re
import zlib

import pytest

from runlayer_cli import regex_safe
from runlayer_cli.scan.agents.detect import _is_word_char, _needle_pattern
from runlayer_cli.verified_local_proxy.verification.macos import MacOSVerifier


def _old_needle_pattern(needle: str) -> stdlib_re.Pattern[str]:
    """Pre-RE2 detect.py construction, frozen verbatim."""
    if not needle:
        return stdlib_re.compile(r"(?!x)x")  # matches nothing
    prefix = r"(?<![A-Za-z0-9_])" if _is_word_char(needle[0]) else ""
    suffix = r"(?![A-Za-z0-9_])" if _is_word_char(needle[-1]) else ""
    return stdlib_re.compile(prefix + stdlib_re.escape(needle) + suffix)


NEEDLES = [
    "tool",
    "a",
    "_private",
    "x_",
    "openai(",
    "@scope/pkg",
    "crew.ai",
    "langchain.agents",
    "(paren",
    "tool)",
    "ünïcode",
]

HAYSTACKS = [
    "",
    "tool",
    "tools",
    "mytool",
    "my_tool",
    "a tool b",
    " tool",
    "tool ",
    ".tool.",
    "(tool)",
    "tool\ntools",
    "étool",  # unicode boundary char (non-word in both engines' guard class)
    "toolé",
    "a",
    "aa",
    "a.",
    ".a",
    "_a_",
    "x_",
    "x__",
    "_private var",
    "public_private",
    "openai(x)",
    "xopenai(y)",
    "from crew.ai import x",
    "crewxai",
    "crew.aix",
    "import langchain.agents\n",
    "@scope/pkg!",
    "y@scope/pkg",
    "(paren)",
    "((paren",
    "use ünïcode here",
    "xünïcodey",
]


@pytest.mark.parametrize("needle", NEEDLES)
def test_needle_pattern_matches_stdlib_lookaround_form(needle: str) -> None:
    _needle_pattern.cache_clear()
    old = _old_needle_pattern(needle)
    new = _needle_pattern(needle)
    for haystack in HAYSTACKS:
        assert (new.search(haystack) is not None) == (
            old.search(haystack) is not None
        ), f"needle={needle!r} haystack={haystack!r}"


def test_empty_needle_pattern_matches_nothing() -> None:
    _needle_pattern.cache_clear()
    pattern = _needle_pattern("")
    for haystack in ["", "x", "\n", "anything at all", "\x00"]:
        assert pattern.search(haystack) is None


APP_PATHS = [
    "/Applications/Figma.app/Contents/MacOS/Figma",
    "/Applications/Legit.app.evil/Contents/MacOS/binary",
    "/Applications/Legit.app.evil/Real.app/Contents/MacOS/binary",
    "/a/b.app/c.app/d",
    "/nested/Foo.app/Bar.app/Contents/x",
    "/x.app",
    "/x.app/",
    ".app/",
    "no-app-here",
    "/Applications/App With Spaces.app/Contents/MacOS/bin",
    "/x.appx/y",
    "",
]


@pytest.mark.parametrize("path", APP_PATHS)
def test_extract_app_bundle_path_matches_stdlib_lookahead_form(path: str) -> None:
    # Pre-RE2 pattern, frozen verbatim: group(1) of the first match, or None.
    old_match = stdlib_re.search(r"(.+\.app)(?=/)", path)
    old = old_match.group(1) if old_match else None
    assert MacOSVerifier()._extract_app_bundle_path(path) == old


# ---------------------------------------------------------------------------
# redact.py (agent-report scrubbing) — frozen pre-RE2 stdlib spec vs the new
# production functions. Security-relevant: a missed redaction leaks a secret
# or a username off the device.
# ---------------------------------------------------------------------------

OLD_REDACT_TOKENS = [
    r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b",
    r"\bgithub_pat_[A-Za-z0-9_]{72,255}\b",
    r"(?i)\bsk[-_](?:[a-z]+[-_])?[A-Za-z0-9_-]{20,}\b",
    r"\brk_(?:live|test)_[A-Za-z0-9]{20,}\b",
    r"\bAKIA[A-Z0-9]{16}\b",
    r"\bAIza[A-Za-z0-9_-]{35}\b",
    r"\bnpm_[A-Za-z0-9]{36,}\b",
    r"\bxox[bpras]-[A-Za-z0-9-]{10,}(?![A-Za-z0-9-])",
    r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
    r"(?![A-Za-z0-9_-])",
    r"\bSG\.[A-Za-z0-9_-]{22,}\.[A-Za-z0-9_-]{22,}(?![A-Za-z0-9_-])",
    r"-----BEGIN(?:.+?)PRIVATE KEY-----[^-]+-----END(?:.+?)PRIVATE KEY-----",
]
OLD_REDACT_KV = [
    r"(api[_-]?key|apikey|access[_-]?key)(?:[\"']|\\[\"'])?\s*[:=]\s*"
    r"(?:[\"']|\\[\"'])?([A-Za-z0-9_\-]{16,})(?![A-Za-z0-9_\-(])",
    r"(password|passwd|pwd)(?:[\"']|\\[\"'])?\s*[:=]\s*"
    r"(?:[\"']|\\[\"'])?([^\s\"'\\]{6,})",
    r"(auth[_-]?token|token|bearer)(?:[\"']|\\[\"'])?\s*[:=]\s*"
    r"(?:[\"']|\\[\"'])?([A-Za-z0-9_\-.]{10,})(?![A-Za-z0-9_\-.(])",
]
OLD_URL_CREDENTIALS = r"(?P<scheme>[a-zA-Z][\w+.\-]*://)[^/@\s]+@"

_JWT = (
    "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0"
    ".dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
)
REDACT_CORPUS = [
    # prefixed tokens + trailing-run boundary cases (the dropped-vacuous check)
    "ghp_" + "A1" * 20, "xoxb-1234567890-1234567890123-AbCd",
    "xoxb-1234567890-x", "xoxb-short", _JWT, _JWT + ".", _JWT + "=",
    "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",
    "sk-proj-" + "a1" * 15, "AKIAIOSFODNN7EXAMPLE", "npm_" + "b2" * 18,
    # kv shapes incl. the "(" call-site guard and quoted/escaped keys
    'api_key="sk8dj3n4m5k6j7h8g9f0a1s2d3f4g5h6"',
    'api_key=get_secret_from_vault("API_KEY_NAME")',
    "api_key=abcdef1234567890abcdef(", "token=abc123.def456-ghi789_jkl",
    "auth_token=abcdefghij(", "password: hunter2hunter2", "pwd=short",
    'password="p@ss w0rd!"', "bearer eyJhbGciOiJIUzI1NiJ9",
    # Unicode whitespace separators / values (STDLIB_WS parity — fail-open
    # if narrowed to ASCII \s)
    "password = hunter2hunter2", "api_key = abcdef1234567890abcd",
    "password=hunt er2er2",
    # URL credentials incl. NBSP in userinfo (stdlib \s stops the run there)
    "https://user:pass@host/x", "postgres://admin@db/x",
    "https://user name:pw@host/", "no secrets here", "",
]  # fmt: skip


def test_redact_token_patterns_parity():
    from runlayer_cli.scan.agents import redact as new

    assert len(new._SECRET_TOKEN_PATTERNS) == len(OLD_REDACT_TOKENS)
    for new_p, old_src in zip(new._SECRET_TOKEN_PATTERNS, OLD_REDACT_TOKENS):
        old_p = stdlib_re.compile(old_src)
        for text in REDACT_CORPUS:
            got = [m.span() for m in new_p.finditer(text)]
            want = [m.span() for m in old_p.finditer(text)]
            assert got == want, f"{old_src!r} diverged on {text!r}"


def test_redact_secrets_output_parity():
    """End-to-end: _redact_secrets output equals the frozen stdlib pipeline."""
    from runlayer_cli.scan.agents import redact as new

    def old_redact_secrets(text: str) -> str:
        for src_ in OLD_REDACT_TOKENS:
            text = stdlib_re.compile(src_).sub(new._REDACTED, text)
        for src_ in OLD_REDACT_KV:
            pat = stdlib_re.compile(src_, stdlib_re.IGNORECASE)

            def mask(m: stdlib_re.Match[str]) -> str:
                whole = m.group(0)
                return (
                    whole[: m.start(2) - m.start(0)]
                    + new._REDACTED
                    + whole[m.end(2) - m.start(0) :]
                )

            text = pat.sub(mask, text)
        return text

    for text in REDACT_CORPUS:
        assert new._redact_secrets(text) == old_redact_secrets(text), repr(text)


def test_redact_url_credentials_parity():
    from runlayer_cli.scan.agents import redact as new

    old = stdlib_re.compile(OLD_URL_CREDENTIALS)
    for text in REDACT_CORPUS:
        assert new._strip_url_credentials(text) == old.sub(r"\g<scheme>", text), repr(
            text
        )


def test_redact_known_usernames_parity():
    """The dynamic (?<![^/\\])name(?![^/\\]) lookarounds (RE2-incompatible)
    now run as a sub_filtered segment-bound accept — output-identical."""
    from runlayer_cli.scan.agents import redact as new

    cases = [
        "/Users/alice/project/x.py", "C:\\Users\\Alice\\x", "/home/alice/",
        "/opt/work/alice/agent", "/opt/alice-cache/agent", "alice",
        "alice/x", "x/alice", "not-alice-here", "/Users/ALICE/y", "",
    ]  # fmt: skip
    for text in cases:
        old_pat = stdlib_re.compile(
            rf"(?<![^/\\]){stdlib_re.escape('alice')}(?![^/\\])",
            stdlib_re.IGNORECASE,
        )
        want = old_pat.sub(new._REDACTED, text)
        got = new._redact_known_usernames(text, ["alice"])
        assert got == want, repr(text)


# ---------------------------------------------------------------------------
# Mechanical swaps (command_contract / update_source / windows_installer_
# verifier): pattern strings kept verbatim, `re.X` -> regex_safe.X. Introspect
# the live module-level patterns and assert RE2 == stdlib over the ASCII/
# no-newline operating domain; the anchored-$ fail-safe divergence is pinned.
# ---------------------------------------------------------------------------

_RE2_TYPE = type(regex_safe.compile("x"))
_SWAP_MODULES = [
    "runlayer_cli.command_contract",
    "runlayer_cli.update_source",
    "runlayer_cli.windows_installer_verifier",
    "runlayer_cli.hook.dispatch",
    "runlayer_cli.scan.client_presence",
    "runlayer_cli.scan.config_redact",
    "runlayer_cli.scan.containers.inspect_parse",
    "runlayer_cli.scan.device",
    "runlayer_cli.scan.processes.probes",
    "runlayer_cli.skills.device_sync",
    "runlayer_cli.updater",
]


def _harvest_cli():
    out = []
    for name in _SWAP_MODULES:
        mod = importlib.import_module(name)
        for attr, val in vars(mod).items():
            if isinstance(val, _RE2_TYPE):
                out.append((name, attr, val.pattern))
    return out


_CLI_PATTERNS = _harvest_cli()


def test_harvest_covers_every_swapped_module_pattern():
    """Guards the harvest itself: a parametrized body cannot.

    If `_harvest_cli` returns nothing, the fuzz below yields zero test cases
    and pytest reports a skip, not a failure -- so the floor has to live in a
    test of its own. Raise the count when modules join `_SWAP_MODULES`.
    """
    assert len(_CLI_PATTERNS) >= 16
    assert len({m for m, _, _ in _CLI_PATTERNS}) >= len(_SWAP_MODULES) - 1


@pytest.mark.parametrize(
    ("module", "attr", "source"),
    _CLI_PATTERNS,
    ids=[f"{m.split('.')[-1]}.{a}" for m, a, s in _CLI_PATTERNS],
)
def test_cli_swap_preserves_stdlib_behavior(module, attr, source):
    old = stdlib_re.compile(source)
    new = regex_safe.compile(source)
    rng = random.Random(zlib.crc32(f"{module}.{attr}".encode()))
    # Covers the syntax the swapped patterns are built from: env-var sigils
    # (`%..%`, `${..}`), launchctl `k = v` rows, markdown fences, semver.
    alphabet = "aA0-_.+@:/ %${}*=#`einpstv13"
    # `\n` only for multiline patterns. Under `(?m)` both engines anchor `$`
    # at line ends, so they agree; without it stdlib's `$` also matches before
    # a trailing newline and RE2's does not — a deliberate divergence pinned
    # by test_cli_anchored_validators_reject_trailing_newline_fail_safe.
    if "(?m" in source:
        alphabet += "\n"
    for _ in range(300):
        text = "".join(rng.choices(alphabet, k=rng.randint(0, 20)))
        assert [m.span() for m in new.finditer(text)] == [
            m.span() for m in old.finditer(text)
        ], f"{module}:{attr} diverged on {text!r}"
# ---------------------------------------------------------------------------
# Patterns compiled at the call site rather than module level, so
# `_harvest_cli` cannot see them and they need their own frozen stdlib spec.
# ---------------------------------------------------------------------------

_INLINE_SWAPS = [
    # mcp_lookup._sanitize_cline_mcp_name — mirrors Cline's tool-name sanitizer
    ("mcp_lookup.sanitize", r"[^a-zA-Z0-9_-]+", "sub"),
    # client_presence._template_has_specific_parent — %VAR%/rest and $VAR/rest
    ("client_presence.pct_template", r"^%[^%]+%/(.+)$", "match"),
    ("client_presence.dollar_template", r"^\$[A-Za-z_][A-Za-z0-9_]*/(.+)$", "match"),
]

_INLINE_CORPUS = [
    "",
    "a b.c/d",
    "ok-name_1",
    "üñî",
    "a/b",
    "%APPDATA%/Foo/config.json",
    "%A%/",
    "%A%%B%/x",
    "%/x",
    "%%/x",
    "$HOME/Foo/config.json",
    "$HOME/",
    "$_x/y",
    "$9bad/y",
    "$/x",
    "~/x",
    "no-sigil-here",
    "%APPDATA%\\Foo",
]


@pytest.mark.parametrize(
    ("name", "source", "mode"), _INLINE_SWAPS, ids=[s[0] for s in _INLINE_SWAPS]
)
def test_inline_swap_preserves_stdlib_behavior(name, source, mode):
    old = stdlib_re.compile(source)
    new = regex_safe.compile(source)
    for text in _INLINE_CORPUS:
        if mode == "sub":
            assert new.sub("_", text) == old.sub("_", text), f"{name} on {text!r}"
        else:
            got, want = new.match(text), old.match(text)
            assert (got is None) == (want is None), f"{name} on {text!r}"
            if want is not None:
                assert got.span() == want.span(), f"{name} span on {text!r}"
                assert got.groups() == want.groups(), f"{name} groups on {text!r}"


def test_inline_path_templates_reject_trailing_newline_fail_safe():
    # Same `$` divergence as the module-level validators: stdlib's `$` also
    # matches before a trailing newline, RE2's does not. A config path template
    # carrying one is malformed, so rejecting it is fail-safe.
    for name, source, mode in _INLINE_SWAPS:
        if mode != "match":
            continue
        base = "%A%/x" if "%" in source else "$HOME/x"
        assert stdlib_re.compile(source).match(base) is not None
        assert stdlib_re.compile(source).match(base + "\n") is not None
        assert regex_safe.compile(source).match(base) is not None
        assert regex_safe.compile(source).match(base + "\n") is None


# The fuzz above draws from a generic alphabet, so it only reaches patterns
# whose language that alphabet spans. A UUID, a 64-char Cline hash and the
# literal "running" are unreachable from it, leaving those patterns asserting
# [] == [] forever. Every harvested pattern needs a seed that really matches;
# the coverage test below fails when one is missing.
_POSITIVE_SEEDS: dict[str, list[str]] = {
    "command_contract.ERROR_TYPE_RE": ["ValueError", "a", "A_b.c1"],
    "command_contract._UUID_RE": ["3f2504e0-4f89-11d3-9a0c-0305e82c3301"],
    "update_source._RELEASE_VERSION_PATTERN": ["1.2.3", "v1.2.3-rc.1"],
    "windows_installer_verifier._GUID_PATTERN": [
        "{3F2504E0-4F89-11D3-9A0C-0305E82C3301}"
    ],
    # Built from parts: a literal dotted OID is rewritten in transit by the
    # evidence masker, which reads it as an IP address.
    "windows_installer_verifier._OID_PATTERN": [
        ".".join(("1", "3", "6", "1", "4", "1")),
        ".".join(("2", "5", "29", "19")),
    ],
    "dispatch._CLINE_HASHED_MCP_TOOL_NAME": ["a" * 55 + "_deadbeef"],
    "dispatch._SKILL_NAME_RE": ["sol", "release-notes", "a1._-b"],
    "client_presence._WINDOWS_ENV_PATTERN": ["%APPDATA%", "%A%"],
    "client_presence._DOLLAR_ENV_PATTERN": ["${HOME}", "$HOME"],
    "config_redact._PLACEHOLDER": ["${env:API_KEY}", "{env:TOKEN}"],
    "config_redact._SCAFFOLD_WORD": ["Bearer", "token"],
    "inspect_parse._ENV_VAR_RE": ["${A}", "$B_1"],
    "device._WSL_VERBOSE_ROW": ["* Ubuntu   Running  2"],
    "probes._LAUNCHCTL_PID_RE": ["  pid = 42  ", "pid=7"],
    "probes._LAUNCHCTL_RUNNING_RE": ["  state = running  "],
    "device_sync._MANAGED_INSTALL_NAME_RE": ["ok-name1", "a"],
    "updater._SEMVER_RE": ["1.2.3", "v0.1.0-rc1+b2"],
}


# A trailing newline is deliberately absent: stdlib's `$` also matches before
# one and RE2's does not, so anchored patterns diverge by design. That case
# is pinned by test_trailing_newline_divergence_is_fail_safe below.
_SEED_MUTATIONS = (
    lambda s: s,
    lambda s: f"prefix {s} suffix",
    lambda s: f"\n{s}",
    lambda s: s[:-1],
    lambda s: s + s,
)


def _seed_key(module: str, attr: str) -> str:
    return f"{module.split('.')[-1]}.{attr}"


def test_every_harvested_pattern_has_a_matching_seed():
    """A pattern with no reachable input is not being parity-tested at all."""
    missing = [
        _seed_key(m, a)
        for m, a, _ in _CLI_PATTERNS
        if _seed_key(m, a) not in _POSITIVE_SEEDS
    ]
    assert not missing, f"no positive seed for: {missing}"
    unmatched = [
        (_seed_key(m, a), seed)
        for m, a, source in _CLI_PATTERNS
        for seed in _POSITIVE_SEEDS[_seed_key(m, a)]
        if not regex_safe.compile(source).search(seed)
    ]
    assert not unmatched, f"seed does not match its own pattern: {unmatched}"


@pytest.mark.parametrize(
    ("module", "attr", "source"),
    _CLI_PATTERNS,
    ids=[f"{m.split('.')[-1]}.{a}" for m, a, s in _CLI_PATTERNS],
)
def test_seeded_inputs_preserve_stdlib_behavior(module, attr, source):
    old = stdlib_re.compile(source)
    new = regex_safe.compile(source)
    for seed in _POSITIVE_SEEDS[_seed_key(module, attr)]:
        for mutate in _SEED_MUTATIONS:
            text = mutate(seed)
            assert [m.span() for m in new.finditer(text)] == [
                m.span() for m in old.finditer(text)
            ], f"{module}:{attr} spans diverged on {text!r}"
            assert [m.groups() for m in new.finditer(text)] == [
                m.groups() for m in old.finditer(text)
            ], f"{module}:{attr} groups diverged on {text!r}"


def test_trailing_newline_divergence_is_fail_safe():
    """Classify every pattern/seed under a trailing newline.

    Only two outcomes are allowed: identical behavior, or stdlib matching
    where RE2 does not (fail-safe -- the value is junk and now gets rejected).
    RE2 matching where stdlib did not would be fail-open and must never occur.
    The divergent set is asserted non-empty so this cannot pass vacuously.
    """
    diverged = set()
    for module, attr, source in _CLI_PATTERNS:
        old = stdlib_re.compile(source)
        new = regex_safe.compile(source)
        for seed in _POSITIVE_SEEDS[_seed_key(module, attr)]:
            text = seed + "\n"
            old_hit = old.search(text) is not None
            new_hit = new.search(text) is not None
            if old_hit == new_hit:
                continue
            assert old_hit and not new_hit, (
                f"{module}:{attr} matches under RE2 but not stdlib on {text!r} "
                "-- fail-open, not the documented tightening"
            )
            diverged.add(_seed_key(module, attr))
    assert diverged, "no pattern exercised the trailing-newline tightening"


_FOLD_CASES = [
    ("alice", "/opt/work/alice/agent"), ("Alice", "/ALICE/x"),
    ("Sam", "/ſam/x"), ("ſam", "/Sam/x"),
    ("istanbul", "/İstanbul/x"), ("istanbul", "/ıstanbul/x"),
    ("İstanbul", "/istanbul/x"), ("i", "/İ/x"), ("i", "/ı/x"),
    ("straße", "/STRASSE/x"), ("strasse", "/straße/x"),
    ("Σ", "/ς/x"), ("σ", "/ς/x"), ("ς", "/Σ/x"),
    ("µ", "/Μ/x"), ("Μ", "/µ/x"), ("µ", "/μ/x"),
    ("alice", "alice-cache"), ("alice", "/alice/alice/"),
]


@pytest.mark.parametrize(("username", "text"), _FOLD_CASES)
def test_username_redaction_folds_like_stdlib_ignorecase(username, text):
    """`_fold` must reproduce re.IGNORECASE, including the odd codepoints.

    U+0130/U+0131 (Turkish dotted/dotless i) and U+017F (long s) all fold into
    an ASCII class under IGNORECASE; U+00DF does NOT fold to "ss", so casefold
    would over-redact. Getting any of these wrong is a leak: the username
    survives into a report that leaves the device.
    """
    from runlayer_cli.scan.agents.redact import _REDACTED, _redact_known_usernames

    old = stdlib_re.sub(
        r"(?<![^/\\])" + stdlib_re.escape(username) + r"(?![^/\\])",
        _REDACTED, text, flags=stdlib_re.IGNORECASE,
    )
    assert _redact_known_usernames(text, [username]) == old


def test_fold_matches_ignorecase_across_all_codepoints():
    """Sweep, not sample: the exception list was wrong twice when hand-derived.

    Once for missing U+0131, once for deriving reps only against ASCII and so
    never examining Greek sigma or the micro sign.
    """
    from runlayer_cli.scan.agents.redact import _fold

    for cp in range(0x20, 0x2FFFF):
        ch = chr(cp)
        for other in {ch.lower(), ch.upper(), ch.casefold(), ch.title()}:
            if len(other) != 1:
                continue
            expected = stdlib_re.fullmatch(stdlib_re.escape(ch), other, stdlib_re.I)
            assert (expected is not None) == (_fold(ch) == _fold(other)), (
                f"U+{cp:04X} {ch!r} vs {other!r}"
            )


_CI_KEY_CASES = [
    "APİ_KEY=abcdef1234567890abcd", "apı_key=abcdef1234567890abcd",
    "PAſSWORD=abcdef1234567890abcd", "AUTH_TOKEN=********",
    "acceſs_key=abcdef1234567890abcd", "api_key=********",
]


@pytest.mark.parametrize("text", _CI_KEY_CASES)
def test_secret_key_labels_match_stdlib_ignorecase(text):
    """RE2 `(?i)` is ASCII-only; stdlib also folded U+0130/U+0131/U+017F/U+212A.

    A key label carrying one of those stopped matching, so the secret survived
    into a report that leaves the device — fail-open, hence the widened
    literals rather than relying on the flag.
    """
    from runlayer_cli.scan.agents.redact import _REDACTED, _redact_secrets

    expected = text
    for src in OLD_REDACT_KV:
        pat = stdlib_re.compile(src, stdlib_re.IGNORECASE)

        def mask(m: stdlib_re.Match[str]) -> str:
            whole = m.group(0)
            return (
                whole[: m.start(2) - m.start(0)]
                + _REDACTED
                + whole[m.end(2) - m.start(0) :]
            )

        expected = pat.sub(mask, expected)
    assert _redact_secrets(text) == expected


_URL_CRED_CASES = [
    "https://user:pass@host/x", "postgres://admin@db/x",
    "httpé://user:secret@host/x", "httpı://u:pw@h/", "a中://user:pass@host/",
    "httṕ://u:p@h/", "ht_tp://u:p@h/", "ht+tp://u:p@h/", "ht.tp://u:p@h/",
    "https://user name:pw@host/", "no-scheme user@host", "1http://u:p@h/",
]


@pytest.mark.parametrize("text", _URL_CRED_CASES)
def test_url_credential_strip_matches_stdlib_word_class(text):
    """RE2 narrows `\\w` to ASCII; here that is a credential leak.

    A scheme whose last character before `://` is non-ASCII stops matching
    entirely — RE2 cannot restart later either, because that character is not
    in its `\\w` — so `user:secret@` survives into a report that leaves the
    device. `\\p{M}` is excluded on purpose: stdlib `\\w` has no combining
    marks, and including it made RE2 strip credentials stdlib left alone.
    """
    from runlayer_cli.scan.agents.redact import _strip_url_credentials

    expected = stdlib_re.sub(OLD_URL_CREDENTIALS, r"\g<scheme>", text)
    assert _strip_url_credentials(text) == expected


def test_sanitize_path_survives_surrogateescape_names():
    """os.walk yields U+DCxx for filenames that are not valid UTF-8.

    RE2 works on UTF-8 and raises UnicodeEncodeError on those; stdlib `re`
    operated on the str and never did. Unguarded, one such directory takes
    down the whole scan at to_agent_report_payload.
    """
    from runlayer_cli.scan.agents.redact import sanitize_path

    assert sanitize_path("/home/u/\udcff/x") == "/home/<redacted>/?/x"
    # the redaction layers still run on the rest of the path
    assert sanitize_path("https://u:pw@h/\udcfe") == "https://h/?"
