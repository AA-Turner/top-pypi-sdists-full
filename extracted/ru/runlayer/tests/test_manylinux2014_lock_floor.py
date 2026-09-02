"""Guard: uv.lock must stay installable inside manylinux2014 (glibc 2.17).

The legacy Linux release variant (ENG-4579) freezes the CLI inside
quay.io/pypa/manylinux2014_x86_64 via packaging/linux/build_onedir_manylinux.sh.
That build breaks silently at release time if a dependency bump drops its
glibc-2.17-compatible (manylinux2014-or-older) x86_64 wheel without shipping an
sdist to compile from (the PyData ecosystem is trending toward manylinux_2_28).
This test fails the offending PR instead, so the drift is caught at review time;
the centos:7 exec check in the release workflows remains the runtime backstop.

Not covered here:
- PyInstaller itself (installed ad hoc by the build scripts, not locked) and
  the python-build-standalone interpreter uv provisions (targets glibc 2.17 on
  x86_64 by upstream policy).
- A dep whose only Linux x86_64 wheels are musllinux (or none) with no sdist —
  that breaks the standard Linux build too and surfaces there.

If a dependency legitimately cannot keep a 2.17-compatible path, don't delete
this test — revisit the legacy variant floor (see ENG-4579; fallback is
manylinux_2_28).
"""

from __future__ import annotations

from pathlib import Path

from packaging.utils import parse_wheel_filename

from runlayer_cli import regex_safe

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10
    import tomli as tomllib

CLI_DIR = Path(__file__).parents[1]

GLIBC_FLOOR = (2, 17)
_MANYLINUX_LEGACY_FLOORS = {
    "manylinux1_x86_64": (2, 5),
    "manylinux2010_x86_64": (2, 12),
    "manylinux2014_x86_64": (2, 17),
}
_MANYLINUX_PEP600 = regex_safe.compile(r"^manylinux_(\d+)_(\d+)_x86_64$")


def _glibc_floor(platform_tag: str) -> tuple[int, int] | None:
    """glibc floor of one platform tag, or None for non-glibc-x86_64 tags."""
    match = _MANYLINUX_PEP600.match(platform_tag)
    if match:
        return int(match.group(1)), int(match.group(2))
    return _MANYLINUX_LEGACY_FLOORS.get(platform_tag)


def _build_cpython_minor() -> int:
    """Minor version of the interpreter the frozen build actually uses.

    Derived from cli/.python-version (not requires-python, which floors at
    3.10) so an interpreter bump moves this guard automatically instead of
    letting it silently stop matching any wheels.
    """
    pinned = (CLI_DIR / ".python-version").read_text().strip()
    match = regex_safe.match(r"^3\.(\d+)", pinned)
    assert match, f"cannot parse cli/.python-version: {pinned!r}"
    return int(match.group(1))


def _runs_on_build_python(interpreter: str, abi: str, minor: int) -> bool:
    if interpreter in ("py3", f"cp3{minor}"):
        return True
    if abi == "abi3":
        match = regex_safe.match(r"^cp3(\d+)$", interpreter)
        return match is not None and int(match.group(1)) <= minor
    return False


# Packages the legacy build installs FROM SDIST (no glibc-2.17 wheel). An
# sdist is only as good as its build requirements: a thin native binding
# (google-re2 is a pybind11 shim over RE2 + abseil) fails at release time
# unless build_onedir_manylinux.sh provisions the libraries first. Each entry
# maps to the exact locked version it was vetted at plus the marker strings
# that must appear in that script; an empty marker tuple documents a
# self-contained sdist (pure python / vendored sources). Keying on the version
# means a dependency bump — whose sdist may change build requirements — fails
# the test until someone re-vets the provisioning and updates the pin here. A
# new sdist-reliant dep likewise fails until reviewed and added.
SDIST_PROVISIONED: dict[str, tuple[str, tuple[str, ...]]] = {
    "google-re2": ("1.1.20251105", ("abseil-cpp", "re2")),
}

_BUILD_SCRIPT = CLI_DIR / "packaging" / "linux" / "build_onedir_manylinux.sh"


def test_uv_lock_keeps_glibc_217_compatible_linux_wheels() -> None:
    lock = tomllib.loads((CLI_DIR / "uv.lock").read_text())
    minor = _build_cpython_minor()
    guarded = 0
    offenders: list[str] = []
    sdist_reliant: set[str] = set()

    for package in lock.get("package", []):
        floors: list[tuple[int, int]] = []
        for wheel in package.get("wheels", []):
            filename = wheel["url"].rsplit("/", 1)[-1]
            if not filename.endswith(".whl"):
                continue
            for tag in parse_wheel_filename(filename)[3]:
                floor = _glibc_floor(tag.platform)
                if floor is not None and _runs_on_build_python(
                    tag.interpreter, tag.abi, minor
                ):
                    floors.append(floor)

        if not floors:
            continue  # pure-python or no glibc x86_64 wheels — see docstring
        guarded += 1
        if min(floors) <= GLIBC_FLOOR:
            continue  # a compatible wheel installs directly
        lowest = ".".join(map(str, min(floors)))
        name = package["name"]
        if "sdist" in package:
            # An sdist is NOT automatically buildable under manylinux2014 —
            # a binding-only sdist needs its native libraries provisioned
            # (ENG-4927: this arm was an unconditional pass, so google-re2
            # stayed green while the release build would have failed).
            if name in SDIST_PROVISIONED:
                vetted_version = SDIST_PROVISIONED[name][0]
                if package["version"] != vetted_version:
                    offenders.append(
                        f"{name}=={package['version']} is allowlisted in "
                        f"SDIST_PROVISIONED but vetted at {vetted_version} — a "
                        "version bump can change the sdist's build requirements; "
                        "re-vet the provisioning in build_onedir_manylinux.sh and "
                        "update the pinned version in SDIST_PROVISIONED"
                    )
                    continue
                sdist_reliant.add(name)
                continue
            offenders.append(
                f"{name}=={package['version']} (lowest wheel floor glibc "
                f"{lowest}; sdist present but not vetted — if it builds "
                "self-contained under manylinux2014, allowlist it in "
                "SDIST_PROVISIONED; if it needs native libraries, provision "
                "them in build_onedir_manylinux.sh and list the markers)"
            )
            continue
        offenders.append(
            f"{name}=={package['version']} "
            f"(lowest wheel floor glibc {lowest}, no sdist)"
        )

    # If the parser or lock format drifts, this fails loudly instead of the
    # whole guard degrading into a vacuous pass (13 guarded packages today).
    assert guarded > 0, "no glibc x86_64 wheels recognized in uv.lock at all"
    # Offenders first: a version-bumped allowlist entry lands here with a
    # precise "vetted at X" message and must win over the coarser stale-entry
    # check below (a bumped dep is absent from sdist_reliant, so it would
    # otherwise trip the stale assert with a misleading reason).
    assert not offenders, (
        "These locked deps have Linux x86_64 wheels only above glibc "
        f"{'.'.join(map(str, GLIBC_FLOOR))} and no sdist, which breaks the "
        "legacy manylinux2014 release build (ENG-4579):\n  "
        + "\n  ".join(offenders)
        + "\nPin an older version with a manylinux2014 wheel, or revisit the "
        "legacy variant floor."
    )
    # The allowlist ratchets: an entry no longer sdist-reliant is stale and
    # must be removed, so the vetted set can only mirror reality.
    assert sdist_reliant == set(SDIST_PROVISIONED), (
        f"stale SDIST_PROVISIONED entries: "
        f"{sorted(set(SDIST_PROVISIONED) - sdist_reliant)}"
    )


def test_sdist_provisioning_markers_exist_in_build_script() -> None:
    """Every native-binding sdist's provisioning must actually be present.

    Deleting the abseil/RE2 build steps from build_onedir_manylinux.sh (or
    renaming the script) would silently re-open the release-time failure the
    allowlist vouches against; each marker string ties the allowlist entry to
    the provisioning that justifies it.
    """
    assert _BUILD_SCRIPT.is_file(), _BUILD_SCRIPT
    script = _BUILD_SCRIPT.read_text()
    for name, (_version, markers) in SDIST_PROVISIONED.items():
        for marker in markers:
            assert marker in script, (
                f"SDIST_PROVISIONED[{name!r}] expects {marker!r} in "
                f"{_BUILD_SCRIPT.name}, not found"
            )
