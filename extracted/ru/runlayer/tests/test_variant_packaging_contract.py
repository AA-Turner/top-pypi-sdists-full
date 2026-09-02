"""Cross-asset contract: variant marker reader == Linux packaging output.

The build scripts write the marker into the PyInstaller dist tree and it
rides the nfpm ``type: tree`` entries into the installed package;
``runlayer_cli.variant`` reads it back at the installed path. The two sides
share no constant — a path or vocabulary drift is silent at runtime (the
reader sees "no marker" and treats a legacy device as standard), so this
test derives the installed path and the marker vocabulary from the packaging
assets and asserts lockstep with the reader.
"""

from __future__ import annotations

from pathlib import Path

from runlayer_cli import regex_safe, variant

_CLI_ROOT = Path(__file__).parent.parent
_LINUX = _CLI_ROOT / "packaging" / "linux"
_BUILD_CLI = _LINUX / "build_packages.sh"
_BUILD_AIWATCH = _LINUX / "build_aiwatch_packages.sh"
_NFPM_CLI = _LINUX / "nfpm.yaml"
_NFPM_AIWATCH = _LINUX / "nfpm-aiwatch.yaml"

_READER = _CLI_ROOT / "runlayer_cli" / "variant.py"

# Shared behavior samples for the marker-content vocabulary.
_ACCEPTED = ("glibc2.17", "glibc10.4")
_REJECTED = ("", "GLIBC2.17", "musl1.2", "el7", "glibc2", "glibc2.17.1", "glibc2.17-fips")


def _marker_dist_subpath(script: Path) -> str:
    """The dist-tree path the build script writes the marker to."""
    match = regex_safe.compile(r'> "\$DIST_DIR/([\w-]+/variant)"').search(
        script.read_text()
    )
    assert match is not None, f"no variant marker write in {script.name}"
    return match.group(1)


def _tree_dst(nfpm: Path, bundle: str) -> str:
    """The install prefix nfpm maps ./dist/<bundle> onto."""
    match = regex_safe.compile(
        rf"-\s+src:\s+\./dist/{regex_safe.escape(bundle)}"
        rf"\s*\n\s+dst:\s+(\S+)\s*\n\s+type:\s+tree"
    ).search(nfpm.read_text())
    assert match is not None, f"no tree entry for ./dist/{bundle} in {nfpm.name}"
    return match.group(1)


def _installed_marker_path(script: Path, nfpm: Path) -> Path:
    bundle, filename = _marker_dist_subpath(script).split("/")
    return Path(_tree_dst(nfpm, bundle)) / filename


def _suffix_shape(script: Path) -> regex_safe.Pattern:
    """The VARIANT_SUFFIX validation regex the build script enforces.

    Extracted verbatim from the ``[[ "$VARIANT_SUFFIX" =~ ... ]]`` guard; the
    bash ERE it uses (anchors, ``[0-9]``, ``+``, ``\\.``) is also valid RE2
    syntax, so it compiles as-is.
    """
    match = regex_safe.compile(r"=~ (\S+) \]\]").search(script.read_text())
    assert match is not None, f"no VARIANT_SUFFIX shape check in {script.name}"
    return regex_safe.compile(match.group(1))


def test_cli_marker_path_matches_packaging() -> None:
    installed = _installed_marker_path(_BUILD_CLI, _NFPM_CLI)
    assert variant._VARIANT_MARKER_PATHS["cli"] == installed
    # desktop shares the CLI marker: both ship in the single runlayer package.
    assert variant._VARIANT_MARKER_PATHS["desktop"] == installed


def test_aiwatch_marker_path_matches_packaging() -> None:
    installed = _installed_marker_path(_BUILD_AIWATCH, _NFPM_AIWATCH)
    assert variant._VARIANT_MARKER_PATHS["ai-watch"] == installed


def test_reader_covers_exactly_the_packaged_markers() -> None:
    packaged = {
        _installed_marker_path(_BUILD_CLI, _NFPM_CLI),
        _installed_marker_path(_BUILD_AIWATCH, _NFPM_AIWATCH),
    }
    assert set(variant._VARIANT_MARKER_PATHS.values()) == packaged


def _reader_pattern_literal() -> str:
    """The reader's pattern string, extracted from the variant module source."""
    match = regex_safe.compile(
        r'_VARIANT_PATTERN = regex_safe\.compile\(r"([^"]+)"\)'
    ).search(_READER.read_text())
    assert match is not None, "reader _VARIANT_PATTERN not found"
    return match.group(1)


def test_marker_vocabulary_matches_build_suffix_shape() -> None:
    """What the build scripts will write, the reader must accept — exactly.

    Exact expression equality (not just samples): a one-sided widening like
    accepting ``glibc2.17-fips`` in the build guard would ship markers the
    reader fails closed on; samples alone cannot catch every such widening.
    """
    reader = _reader_pattern_literal()
    for script in (_BUILD_CLI, _BUILD_AIWATCH):
        shape = _suffix_shape(script)  # anchored ERE; honor its own ^...$
        assert f"^{reader}$" == shape.pattern
        for value in _ACCEPTED:
            assert shape.search(value), f"{script.name} rejects {value!r}"
            assert variant._VARIANT_PATTERN.fullmatch(value) is not None
        for value in _REJECTED:
            assert not shape.search(value), f"{script.name} accepts {value!r}"
            assert variant._VARIANT_PATTERN.fullmatch(value) is None
