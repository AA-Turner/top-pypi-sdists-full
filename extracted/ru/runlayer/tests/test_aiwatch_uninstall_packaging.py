"""Static contracts for the disposable macOS AI Watch uninstall package."""

from __future__ import annotations

from pathlib import Path
import shlex
import stat

import yaml

from runlayer_cli import regex_safe as re


ROOT = Path(__file__).parents[2]
CLI_ROOT = ROOT / "cli"
SPEC = CLI_ROOT / "packaging" / "aiwatch_uninstall.spec"
BUILD_SCRIPT = CLI_ROOT / "packaging" / "macos" / "build_uninstall_pkg.sh"
POSTINSTALL = CLI_ROOT / "packaging" / "macos" / "uninstall-pkg" / "postinstall"
MAKEFILE = CLI_ROOT / "Makefile"
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "release-aiwatch.yml"


def test_release_keychain_allows_every_package_signer() -> None:
    workflow = yaml.safe_load(RELEASE_WORKFLOW.read_text())
    import_step = next(
        step
        for step in workflow["jobs"]["build-macos"]["steps"]
        if step.get("name") == "Import signing certificates"
    )
    trusted_apps = set(re.findall(r"-T\s+(\S+)", import_step["run"]))

    for script in (BUILD_SCRIPT.with_name("build_pkg.sh"), BUILD_SCRIPT):
        for line in script.read_text().replace("\\\n", " ").splitlines():
            if re.match(r"\s*(codesign|pkgbuild|productbuild|productsign)\b", line):
                command = shlex.split(line, comments=True)
                if "--sign" in command:
                    signer = f"/usr/bin/{command[0]}"
                    assert signer in trusted_apps, (
                        f"{script.name} signs with {signer}, but the release keychain "
                        "does not permit it to access the signing identity unattended"
                    )


def test_uninstall_spec_is_minimal_onedir_without_upx() -> None:
    spec = SPEC.read_text()

    assert '["../runlayer_cli/aiwatch_uninstall.py"]' in spec
    assert "Analysis(" in spec
    assert "PYZ(" in spec
    assert "EXE(" in spec
    assert "exclude_binaries=True" in spec
    assert "COLLECT(" in spec
    assert spec.count('name="aiwatch-uninstall"') == 2
    assert spec.count("upx=False") == 2
    assert "collect_all" not in spec
    assert "collect_submodules" not in spec
    assert "copy_metadata" not in spec
    assert "hiddenimports=[]" in spec
    assert "binaries=[]" in spec
    assert "datas=[]" in spec


def test_uninstall_pkg_is_payload_free_signed_and_disposable() -> None:
    build = BUILD_SCRIPT.read_text()
    postinstall = POSTINSTALL.read_text()

    assert BUILD_SCRIPT.stat().st_mode & stat.S_IXUSR
    assert POSTINSTALL.stat().st_mode & stat.S_IXUSR
    assert 'SOURCE_MAIN="$SOURCE_BUNDLE/aiwatch-uninstall"' in build
    assert '[ ! -x "$SOURCE_MAIN" ]' in build
    assert 'STAGED_BUNDLE="$BUILD_DIR/scripts/aiwatch-uninstall"' in build
    assert 'ditto --noextattr --noqtn "$SOURCE_BUNDLE" "$STAGED_BUNDLE"' in build
    assert "--nopayload" in build
    assert "--root" not in build
    assert 'PACKAGE_ID="com.runlayer.aiwatch.uninstall"' in build
    assert '--identifier "$PACKAGE_ID"' in build
    assert "AIWATCH_SIGN_IDENTITY_APP" in build
    assert "AIWATCH_SIGN_IDENTITY_PKG" in build
    assert 'find "$STAGED_BUNDLE" -type f -print0' in build
    assert "file -b" in build
    assert "codesign --force --options=runtime --timestamp" in build
    assert (
        "codesign --force --options=runtime --timestamp \\\n"
        '        --identifier "$PACKAGE_ID" \\\n'
        '        --entitlements "$SCRIPT_DIR/entitlements.plist" \\\n'
        '        --sign "$SIGN_APP" \\\n'
        '        "$STAGED_MAIN"'
    ) in build
    assert "notarytool submit" in build
    assert "stapler staple" in build
    assert 'OUT="$DIST_DIR/aiwatch-uninstall-${VERSION}.pkg"' in build

    run = '"$SCRIPT_DIR/aiwatch-uninstall/aiwatch-uninstall"'
    forget = "/usr/sbin/pkgutil --forget com.runlayer.aiwatch.uninstall"
    assert postinstall.index(run) < postinstall.index(forget)


def test_make_and_release_publish_uninstall_pkg_as_deployment_asset() -> None:
    makefile = MAKEFILE.read_text()
    workflow = RELEASE_WORKFLOW.read_text()

    target = makefile[makefile.index("\npackage-aiwatch-uninstall-macos:") :]
    target = target[: target.index("\n\n")]
    assert "packaging/aiwatch_uninstall.spec" in target
    assert "./packaging/macos/build_uninstall_pkg.sh" in target

    assert "make package-aiwatch-uninstall-macos" in workflow
    assert "name: aiwatch-macos-uninstall-pkg" in workflow
    release_path = (
        "aiwatch-assets/aiwatch-uninstall-${{ steps.version.outputs.version }}.pkg"
    )
    assert release_path in workflow

    build = workflow.index("make package-aiwatch-uninstall-macos")
    signature_check = workflow.index('pkgutil --check-signature "$UNINSTALL_PKG"')
    notarization_check = workflow.index('xcrun stapler validate "$UNINSTALL_PKG"')
    upload = workflow.index("name: Upload uninstall .pkg artifact")
    assert build < signature_check < notarization_check < upload
