"""Guard: the legacy build's RE2_TAG must match the locked google-re2 pin.

The manylinux2014 (glibc 2.17) release variant cannot use google-re2 wheels,
so build_onedir_manylinux.sh compiles RE2 itself from RE2_TAG and installs
the google-re2 sdist on top (ENG-4579). google-re2's version number IS the
RE2 release date — 1.1.20251105 wraps RE2 2025-11-05 — so if the pin moves
without the tag (or vice versa) the frozen legacy binary silently ships a
DIFFERENT regex engine than every other platform: different Unicode tables,
different syntax acceptance, and parity tests that validated one engine
while customers run another.

The locked version (uv.lock) is compared, not the pyproject specifier: the
lock is what the build actually installs, and a range specifier would make
the pyproject side ambiguous.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli import regex_safe

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

CLI_DIR = Path(__file__).parents[1]
_BUILD_SCRIPT = CLI_DIR / "packaging" / "linux" / "build_onedir_manylinux.sh"

# google-re2 versions: MAJOR.MINOR.YYYYMMDD (the date IS the RE2 release).
_PIN_DATE = regex_safe.compile(r"^\d+\.\d+\.(\d{4})(\d{2})(\d{2})$")

# The guard is an EXACT-LINE ALLOWLIST: every logical line of the build script
# containing the token RE2_TAG must equal one of these, verbatim. Bash offers
# endlessly many ways to write a variable (assignment words, declaration
# builtins, `printf -v`, `read`, namerefs, indexed/expansion assignments,
# comment-hiding tricks) — enumerating or lexing them is a losing game, so the
# guard doesn't try: ANY new, moved, or edited RE2_TAG-bearing line fails,
# whatever it means to Bash. The cost is that editing one of these three lines
# (even the comment) requires updating this constant — which is the point: it
# forcibly re-points the editor at the pin coupling. The remaining blind spot
# is a write that never mentions the token (`source other.sh`, a constructed
# name via eval); no static check on this file can close that.
_EXPECTED_RE2_TAG_LINES = (
    "        # pinned sources first. RE2_TAG must stay in step with the",
    "        RE2_TAG=2025-11-05",
    # The read is a LOGICAL line: the script's `for pkg in … \` continuation
    # splices with the next physical line, and the allowlist compares what
    # Bash executes.
    '        for pkg in "abseil-cpp:$ABSL_TAG:https://github.com/abseil/abseil-cpp"'
    '                    "re2:$RE2_TAG:https://github.com/google/re2"; do',
)
# The single assignment above, re-parsed so the DATE flows from the same
# constant the allowlist enforces (a non-literal edit fails here).
_TAG_LINE = regex_safe.compile(r"^\s*RE2_TAG=(\d{4}-\d{2}-\d{2})$")


def _re2_tag_lines(text: str) -> list[str]:
    """Every logical line of ``text`` containing the token ``RE2_TAG``.

    Backslash-newline continuations are spliced first so a token split
    across physical lines (``RE2_\\`` + ``TAG=…``, which Bash joins into one
    assignment) is still seen. Splicing where Bash would not (through a
    comment or single quotes) can only CREATE RE2_TAG-bearing lines, which
    fail the allowlist — the safe direction; it can never hide one.
    """
    return [line for line in text.replace("\\\n", "").splitlines() if "RE2_TAG" in line]


def _script_re2_tag() -> str:
    assert _BUILD_SCRIPT.is_file(), _BUILD_SCRIPT
    lines = _re2_tag_lines(_BUILD_SCRIPT.read_text())
    assert lines == list(_EXPECTED_RE2_TAG_LINES), (
        f"RE2_TAG-bearing lines in {_BUILD_SCRIPT.name} changed:\n"
        f"  found:    {lines}\n"
        f"  expected: {list(_EXPECTED_RE2_TAG_LINES)}\n"
        "Any new or edited use of RE2_TAG (any Bash form) must be reviewed "
        "against the google-re2 pin coupling, then mirrored in "
        "_EXPECTED_RE2_TAG_LINES. Keep the tag one plain literal assignment."
    )
    m = _TAG_LINE.match(_EXPECTED_RE2_TAG_LINES[1])
    assert m, (
        "the allowlisted assignment line is no longer a plain literal "
        "RE2_TAG=YYYY-MM-DD; a variable/override means the effective RE2 "
        "release can't be verified against the google-re2 pin"
    )
    return m.group(1)


def _locked_google_re2_version() -> str:
    lock = tomllib.loads((CLI_DIR / "uv.lock").read_text())
    versions = [
        p["version"] for p in lock.get("package", []) if p.get("name") == "google-re2"
    ]
    assert len(versions) == 1, f"expected exactly one google-re2 in uv.lock: {versions}"
    return versions[0]


def test_re2_tag_matches_locked_google_re2_pin() -> None:
    version = _locked_google_re2_version()
    m = _PIN_DATE.match(version)
    assert m, (
        f"google-re2 version {version!r} no longer follows MAJOR.MINOR.YYYYMMDD; "
        "the date-coupling convention changed upstream — update this guard AND "
        "verify how build_onedir_manylinux.sh should now pick its RE2 source"
    )
    pin_date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    tag = _script_re2_tag()
    assert tag == pin_date, (
        f"RE2_TAG={tag} in {_BUILD_SCRIPT.name} but uv.lock pins "
        f"google-re2=={version} (RE2 {pin_date}). The legacy binary would "
        "ship a different regex engine than every other platform — move both "
        "together."
    )


def test_any_new_re2_tag_line_fails_the_allowlist() -> None:
    # Representative shadowing forms from every direction Bash offers: a
    # second assignment, declaration builtins, builtin writes with no `=`,
    # expansion assignment, a token spliced across a continuation, and an
    # assignment hidden behind a quoted hash. The allowlist doesn't interpret
    # any of them — each adds an RE2_TAG-bearing line, so each mismatches.
    baseline = "\n".join(_EXPECTED_RE2_TAG_LINES)
    for injected in (
        "RE2_TAG=2026-01-01",
        "export RE2_TAG=2026-01-01",
        "readonly RE2_TAG=2026-01-01",
        "export OTHER=x RE2_TAG=2026-01-01",
        "RE2_TAG[0]=2026-01-01",
        "printf -v RE2_TAG %s 2026-01-01",
        "read RE2_TAG < /tmp/tag",
        ': "${RE2_TAG:=2026-01-01}"',
        "RE2_\\\nTAG=2026-01-01",
        "printf '%s' ' # data'; RE2_TAG=2026-01-01",
    ):
        lines = _re2_tag_lines(baseline + "\n" + injected)
        assert lines != list(_EXPECTED_RE2_TAG_LINES), injected

    # And the splice itself: a token split across physical lines is joined,
    # so it cannot hide by never appearing whole on one line.
    assert _re2_tag_lines("RE2_\\\nTAG=2026-01-01") == ["RE2_TAG=2026-01-01"]
