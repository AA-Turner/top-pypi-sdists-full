"""macOS package installer tests."""

import hashlib
import shlex
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from runlayer_cli.installer_common import (
    InstallerVerificationError,
    UnsupportedInstallerError,
    default_command_runner,
    posix_installer_environment,
)
from runlayer_cli.macos_installer import MacOSPackageInstaller, _read_package_metadata
from runlayer_cli.platform_installers import MACOS_PACKAGE_ID_BY_PACKAGE
from runlayer_cli.updater import Artifact, InstallDisposition
from tests.macos_installer_helpers import (
    AIWATCH_PACKAGE_ID,
    ExpandingMacPackageRunner,
)
from tests.platform_installer_helpers import (
    RecordingRunner,
    artifact,
    artifact_path,
    assert_argv_without_shell,
    result,
)


@pytest.mark.parametrize(
    ("from_version", "to_version"),
    [("1.0.0", "2.0.0"), ("2.0.0", "1.0.0")],
)
def test_pins_trust_and_metadata_before_install(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    from_version: str,
    to_version: str,
) -> None:
    for name in ("RUNLAYER_API_KEY", "AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN"):
        monkeypatch.setenv(name, "secret")
    value = artifact("macos", "pkg", "aiwatch-2.0.0-macos-arm64.pkg")
    path = artifact_path(tmp_path, value)
    runner = ExpandingMacPackageRunner(
        AIWATCH_PACKAGE_ID,
        result(
            stdout="""Package "aiwatch.pkg":
   Status: signed by a developer certificate issued by Apple for distribution
   Certificate Chain:
    1. Developer ID Installer: Anysource Inc. (AF2M8HC7A2)
    2. Developer ID Certification Authority
"""
        ),
        result(stderr=f"{path}: accepted\nsource=Notarized Developer ID\n"),
        result(),
        result(),
        version=to_version,
    )

    MacOSPackageInstaller(
        package_id=AIWATCH_PACKAGE_ID,
        runner=runner,
    ).verify_and_install(
        path,
        artifact=value,
        from_version=from_version,
        to_version=to_version,
    )

    resolved = str(path.resolve())
    assert [call[0] for call in runner.calls] == [
        ["/usr/sbin/pkgutil", "--check-signature", resolved],
        [
            "/usr/sbin/spctl",
            "--assess",
            "--type",
            "install",
            "--verbose=4",
            resolved,
        ],
        ["/usr/sbin/pkgutil", "--expand", resolved, runner.calls[2][0][-1]],
        ["/usr/sbin/installer", "-pkg", resolved, "-target", "/"],
    ]
    expected_env = {
        "LANG": "C",
        "LC_ALL": "C",
        "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
    }
    for _, kwargs in runner.calls:
        assert kwargs["env"] == expected_env
    assert_argv_without_shell(runner)


def test_accepts_legacy_pkgutil_trust_wording(tmp_path: Path) -> None:
    value = artifact("macos", "pkg", "aiwatch.pkg")
    path = artifact_path(tmp_path, value)
    runner = ExpandingMacPackageRunner(
        AIWATCH_PACKAGE_ID,
        result(
            stdout="""Status: signed by a certificate trusted by Mac OS X
    1. Developer ID Installer: Anysource Inc. (AF2M8HC7A2)
"""
        ),
        result(stderr=f"{path}: accepted\nsource=Notarized Developer ID\n"),
        result(),
        result(),
    )

    MacOSPackageInstaller(
        package_id=AIWATCH_PACKAGE_ID,
        runner=runner,
    ).verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    assert len(runner.calls) == 4


def test_rejects_wrong_team_before_assessment_or_install(tmp_path: Path) -> None:
    value = artifact("macos", "pkg", "aiwatch.pkg")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(
            stdout="""Package "aiwatch.pkg":
   Status: signed by a developer certificate issued by Apple for distribution
   Certificate Chain:
    1. Developer ID Installer: Lookalike Inc. (EVILTEAM123)
"""
        )
    )

    with pytest.raises(InstallerVerificationError, match="AF2M8HC7A2"):
        MacOSPackageInstaller(
            package_id=AIWATCH_PACKAGE_ID,
            runner=runner,
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 1


def test_rejects_package_without_notarized_assessment(tmp_path: Path) -> None:
    value = artifact("macos", "pkg", "aiwatch.pkg")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(
            stdout="""Status: signed by a developer certificate issued by Apple for distribution
    1. Developer ID Installer: Anysource Inc. (AF2M8HC7A2)
"""
        ),
        result(stderr=f"{path}: accepted\nsource=Developer ID\n"),
    )

    with pytest.raises(InstallerVerificationError, match="notarized"):
        MacOSPackageInstaller(
            package_id=AIWATCH_PACKAGE_ID,
            runner=runner,
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 2


def test_rejects_other_runlayer_product_before_install(tmp_path: Path) -> None:
    value = artifact("macos", "pkg", "aiwatch.pkg")
    path = artifact_path(tmp_path, value)
    runner = ExpandingMacPackageRunner(
        "com.runlayer.cli",
        result(
            stdout="""Status: signed by a developer certificate issued by Apple for distribution
    1. Developer ID Installer: Anysource Inc. (AF2M8HC7A2)
"""
        ),
        result(stderr=f"{path}: accepted\nsource=Notarized Developer ID\n"),
        result(),
    )

    with pytest.raises(InstallerVerificationError, match="requested product"):
        MacOSPackageInstaller(
            package_id=AIWATCH_PACKAGE_ID,
            runner=runner,
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 3


@pytest.mark.parametrize(
    ("version", "arch", "message"),
    [
        ("1.9.0", "arm64", "version"),
        ("2.0.0", "x86_64", "architecture"),
    ],
)
def test_rejects_package_metadata_mismatch(
    tmp_path: Path,
    version: str,
    arch: str,
    message: str,
) -> None:
    value = artifact("macos", "pkg", "aiwatch.pkg")
    path = artifact_path(tmp_path, value)
    runner = ExpandingMacPackageRunner(
        AIWATCH_PACKAGE_ID,
        result(
            stdout="""Status: signed by a developer certificate issued by Apple
    1. Developer ID Installer: Anysource Inc. (AF2M8HC7A2)
"""
        ),
        result(stderr=f"{path}: accepted\nsource=Notarized Developer ID\n"),
        result(),
        result(),
        version=version,
        arch=arch,
    )

    with pytest.raises(InstallerVerificationError, match=message):
        MacOSPackageInstaller(
            package_id=AIWATCH_PACKAGE_ID,
            runner=runner,
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 3


def test_rejects_non_native_format(tmp_path: Path) -> None:
    value = artifact("macos", "zip", "aiwatch.zip")
    path = artifact_path(tmp_path, value)

    with pytest.raises(UnsupportedInstallerError):
        MacOSPackageInstaller(
            package_id=AIWATCH_PACKAGE_ID,
            runner=RecordingRunner(),
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )


_TRUSTED_SIGNATURE = """Status: signed by a developer certificate issued by Apple for distribution
    1. Developer ID Installer: Anysource Inc. (AF2M8HC7A2)
"""
_PACKAGING_MACOS = Path(__file__).parent.parent / "packaging" / "macos"


def _trusted_runner(
    package_id: str,
    path: Path,
    *,
    component_ids: tuple[str, ...] | None = None,
) -> ExpandingMacPackageRunner:
    """A runner whose signature + notarization stages pass, so identity decides."""
    return ExpandingMacPackageRunner(
        package_id,
        result(stdout=_TRUSTED_SIGNATURE),
        result(stderr=f"{path}: accepted\nsource=Notarized Developer ID\n"),
        result(),
        result(),
        component_ids=component_ids,
    )


@pytest.mark.parametrize("package_id", ["com.runlayer.cli", "com.runlayer.desktop"])
def test_installs_single_component_runlayer_archive(
    tmp_path: Path,
    package_id: str,
) -> None:
    """CLI and desktop archives carry only their requested product component."""
    value = artifact("macos", "pkg", "runlayer-2.0.0-macos-arm64.pkg")
    path = artifact_path(tmp_path, value)
    runner = _trusted_runner(package_id, path)

    disposition = MacOSPackageInstaller(
        package_id=package_id,
        runner=runner,
    ).verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    assert disposition is InstallDisposition.APPLIED
    assert runner.calls[-1][0] == [
        "/usr/sbin/installer",
        "-pkg",
        str(path.resolve()),
        "-target",
        "/",
    ]


def test_installs_single_component_archive(tmp_path: Path) -> None:
    """AI Watch uses the same single-component identity contract."""
    value = artifact("macos", "pkg", "aiwatch-2.0.0-macos-arm64.pkg")
    path = artifact_path(tmp_path, value)
    runner = _trusted_runner(
        AIWATCH_PACKAGE_ID,
        path,
        component_ids=(AIWATCH_PACKAGE_ID,),
    )

    disposition = MacOSPackageInstaller(
        package_id=AIWATCH_PACKAGE_ID,
        runner=runner,
    ).verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    assert disposition is InstallDisposition.APPLIED


@pytest.mark.parametrize(
    "component_ids",
    [
        pytest.param(
            (AIWATCH_PACKAGE_ID, f"{AIWATCH_PACKAGE_ID}.remove-uv-tool"),
            id="legacy-cleanup-component",
        ),
        pytest.param(
            (f"{AIWATCH_PACKAGE_ID}.remove-uv-tool",),
            id="primary-component-missing",
        ),
        pytest.param(
            (AIWATCH_PACKAGE_ID, "com.runlayer.cli"),
            id="other-runlayer-product-smuggled-in",
        ),
    ],
)
def test_rejects_component_set_other_than_requested_product(
    tmp_path: Path,
    component_ids: tuple[str, ...],
) -> None:
    value = artifact("macos", "pkg", "aiwatch.pkg")
    path = artifact_path(tmp_path, value)
    runner = _trusted_runner(
        AIWATCH_PACKAGE_ID,
        path,
        component_ids=component_ids,
    )

    with pytest.raises(InstallerVerificationError, match="requested product"):
        MacOSPackageInstaller(
            package_id=AIWATCH_PACKAGE_ID,
            runner=runner,
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 3


@pytest.mark.skipif(sys.platform != "darwin", reason="requires PackageKit tools")
@pytest.mark.parametrize("package_id", ["com.runlayer.cli", "com.runlayer.desktop"])
def test_built_archive_is_single_component(
    tmp_path: Path,
    package_id: str,
) -> None:
    """Pin the productbuild archive to the deployed verifier contract.

    The unit tests above drive a fake `pkgutil --expand`, so only a real
    `productbuild` archive proves the two sides agree. Adding a component breaks
    self-update in every already-installed macOS binary.
    """
    product = tmp_path / "runlayer.pkg"
    distribution = tmp_path / "distribution.xml"
    subprocess.run(
        [
            "/usr/bin/pkgbuild",
            "--nopayload",
            "--identifier",
            package_id,
            "--version",
            "1",
            str(tmp_path / "runlayer-component.pkg"),
        ],
        check=True,
        capture_output=True,
    )

    distribution.write_text(
        (_PACKAGING_MACOS / "distribution.runlayer.xml")
        .read_text()
        .replace("__VERSION__", "1")
        .replace("__ARCH__", "arm64")
        .replace("__PACKAGE_ID__", package_id)
        .replace("__PACKAGE_NAME__", "Runlayer")
    )
    subprocess.run(
        [
            "/usr/bin/productbuild",
            "--distribution",
            str(distribution),
            "--package-path",
            str(tmp_path),
            str(product),
        ],
        check=True,
        capture_output=True,
    )

    calls: list[list[str]] = []

    def runner(argv: list[str], **kwargs: object):
        calls.append(argv)
        if argv[:2] == ["/usr/sbin/pkgutil", "--check-signature"]:
            response = result(stdout=_TRUSTED_SIGNATURE)
        elif argv[:2] == ["/usr/sbin/spctl", "--assess"]:
            response = result(
                stderr=f"{product}: accepted\nsource=Notarized Developer ID\n"
            )
        elif argv[:2] == ["/usr/sbin/pkgutil", "--expand"]:
            response = default_command_runner(argv, **kwargs)
        elif argv[:2] == ["/usr/sbin/installer", "-pkg"]:
            response = result()
        else:
            raise AssertionError(f"unexpected command: {argv}")
        return response

    product_bytes = product.read_bytes()
    artifact_value = Artifact(
        platform="macos",
        arch="arm64",
        filename=product.name,
        sha256=hashlib.sha256(product_bytes).hexdigest(),
        size_bytes=len(product_bytes),
        format="pkg",
    )
    disposition = MacOSPackageInstaller(
        package_id=package_id,
        runner=runner,
    ).verify_and_install(
        product,
        artifact=artifact_value,
        from_version="0",
        to_version="1",
    )
    metadata = _read_package_metadata(
        product,
        default_command_runner,
        posix_installer_environment(),
    )

    assert disposition is InstallDisposition.APPLIED
    assert calls[-1][:2] == ["/usr/sbin/installer", "-pkg"]
    assert metadata["identifiers"] == {package_id}
    assert metadata["versions"] == {"1"}
    assert metadata["architectures"] == {"arm64"}


_BUILD_PKG_RUNLAYER = _PACKAGING_MACOS / "build_pkg_runlayer.sh"
_BUILD_PKG_AIWATCH = _PACKAGING_MACOS / "build_pkg.sh"
_DISTRIBUTION_RUNLAYER = _PACKAGING_MACOS / "distribution.runlayer.xml"


def _pkgbuild_identifiers(script_path: Path) -> frozenset[str]:
    """Every `--identifier` a build script passes to `pkgbuild`.

    Only `pkgbuild` counts. The same flag on `codesign` sets a code-signing
    identifier, which is a different namespace from a component receipt id, and
    the scripts use both.
    """
    # Invocations are line-continued, so fold them into one line before scanning.
    folded = script_path.read_text().replace("\\\n", " ")
    identifiers: set[str] = set()
    for line in folded.splitlines():
        stripped = line.strip()
        if not stripped.startswith("pkgbuild"):
            continue
        tokens = shlex.split(stripped)
        identifiers.update(
            value
            for flag, value in zip(tokens, tokens[1:], strict=False)
            if flag == "--identifier"
        )
    assert identifiers, f"no pkgbuild --identifier found in {script_path.name}"
    return frozenset(identifiers)


def _shell_string_assignments(script: str, name: str) -> frozenset[str]:
    """Every double-quoted literal the script assigns to `name`."""
    prefix = f'{name}="'
    values = {
        stripped[len(prefix) : -1]
        for stripped in (line.strip() for line in script.splitlines())
        if stripped.startswith(prefix) and stripped.endswith('"')
    }
    assert values, f"no {name} assignment found"
    return frozenset(values)


def _distribution_pkg_ref_ids(path: Path) -> frozenset[str]:
    """Component ids the distribution references, including inside <choice>."""
    root = ET.parse(path).getroot()
    ids = {ref.get("id", "") for ref in root.iter("pkg-ref")}
    assert "" not in ids, f"pkg-ref without an id in {path.name}"
    return frozenset(ids)


def _expand_package_id(identifier: str, package_id: str) -> str:
    resolved = identifier.replace("${PACKAGE_ID}", package_id).replace(
        "$PACKAGE_ID", package_id
    )
    # An identifier built from a variable this test does not know how to resolve
    # would otherwise silently compare unequal and read as ordinary drift.
    assert "$" not in resolved, (
        f"unresolved shell variable in pkgbuild identifier {identifier!r}"
    )
    return resolved


def test_runlayer_build_script_emits_one_component_per_product() -> None:
    """Pin packaging output to the deployed updater contract on every platform.

    A second component breaks self-update on every already-installed macOS
    device because the failing identity check runs before the new package can
    replace the binary. The real-productbuild test proves the same property on
    macOS; this static check also runs on Linux.
    """
    product_ids = _shell_string_assignments(
        _BUILD_PKG_RUNLAYER.read_text(), "PACKAGE_ID"
    )

    assert product_ids == {
        MACOS_PACKAGE_ID_BY_PACKAGE["cli"],
        MACOS_PACKAGE_ID_BY_PACKAGE["desktop"],
    }

    template_identifiers = _pkgbuild_identifiers(_BUILD_PKG_RUNLAYER)
    for package_id in product_ids:
        built = frozenset(
            _expand_package_id(identifier, package_id)
            for identifier in template_identifiers
        )
        assert built == {package_id}


def test_aiwatch_build_script_emits_one_component() -> None:
    built = _pkgbuild_identifiers(_BUILD_PKG_AIWATCH)

    assert built == {MACOS_PACKAGE_ID_BY_PACKAGE["ai-watch"]}


def test_distribution_template_references_exactly_the_built_components() -> None:
    """productbuild fails on a `pkg-ref` with no matching component, and a
    component absent from the distribution is silently dropped from the archive.
    Either drift changes what the verifier sees, so pin the two together."""
    pkg_refs = _distribution_pkg_ref_ids(_DISTRIBUTION_RUNLAYER)
    package_id = MACOS_PACKAGE_ID_BY_PACKAGE["cli"]

    # The build script renders this placeholder via sed; keep that mapping here
    # so a renamed placeholder fails rather than quietly matching nothing.
    rendered = frozenset(ref.replace("__PACKAGE_ID__", package_id) for ref in pkg_refs)

    assert "__" not in "".join(rendered), f"unrendered placeholder in {pkg_refs}"
    assert rendered == {package_id}
    assert rendered == frozenset(
        _expand_package_id(identifier, package_id)
        for identifier in _pkgbuild_identifiers(_BUILD_PKG_RUNLAYER)
    )
