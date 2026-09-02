"""Static release/package checks for the native AI Watch hook shim."""

from __future__ import annotations

from pathlib import Path


_ROOT = Path(__file__).parents[2]
_RELEASE_WORKFLOW = _ROOT / ".github" / "workflows" / "release-aiwatch.yml"
_WINDOWS_SIGN_ACTION = (
    _ROOT / ".github" / "actions" / "sign-windows-payload" / "action.yml"
)
_WINDOWS_SIGN_SCRIPT = _WINDOWS_SIGN_ACTION.with_name("sign-shards.ps1")
_TEST_WORKFLOW = _ROOT / ".github" / "workflows" / "aiwatch-hook-shim-test.yml"
_BUILD_PKG = _ROOT / "cli" / "packaging" / "macos" / "build_pkg.sh"
_WINDOWS_WIX = _ROOT / "cli" / "packaging" / "windows" / "aiwatch.wxs"
_MAKEFILE = _ROOT / "cli" / "Makefile"
_WINDOWS_SHIM_BUILD = _ROOT / "cli" / "packaging" / "windows" / "build_hook_shim.ps1"


def _job(workflow: str, name: str, next_name: str) -> str:
    start = workflow.index(f"\n  {name}:")
    end = workflow.index(f"\n  {next_name}:", start)
    return workflow[start:end]


def _rule(makefile: str, name: str) -> str:
    start = makefile.index(f"\n{name}:")
    end = makefile.index("\n\n", start)
    return makefile[start:end]


def test_release_builds_shim_before_signing_and_packaging() -> None:
    workflow = _RELEASE_WORKFLOW.read_text()

    assert workflow.count("go-version-file: aiwatch-hook-shim/go.mod") == 4
    assert workflow.count("CGO_ENABLED=0") >= 5
    assert workflow.count("go build -trimpath") >= 5
    assert workflow.count('-ldflags "-X main.version=${VERSION}"') >= 5
    assert workflow.count("./cmd/aiwatch-hook") >= 5
    assert "./cmd/aiwatch-hook-shim" not in workflow

    macos = _job(workflow, "build-macos", "build-windows")
    assert macos.index("Build onedir bundle") < macos.index(
        "Build universal2 hook shim"
    )
    assert macos.index("Build universal2 hook shim") < macos.index("Build .pkg")
    assert "GOOS=darwin GOARCH=arm64" in macos
    assert "GOOS=darwin GOARCH=amd64" in macos
    assert "lipo -create" in macos
    assert 'lipo -archs "$SHIM"' in macos

    windows = _job(workflow, "build-windows", "build-linux")
    assert windows.index("Build onedir bundle") < windows.index(
        "Build hook shim (windows/amd64)"
    )
    assert windows.index("Build hook shim (windows/amd64)") < windows.index(
        "Sign exes + dlls"
    )
    assert "GOOS=windows GOARCH=amd64" in windows
    assert "aiwatch-hook.exe" in windows
    assert "uses: ./.github/actions/sign-windows-payload" in windows
    assert "files-folder: cli\\dist\\aiwatch" in windows

    linux = _job(workflow, "build-linux", "build-linux-legacy")
    assert linux.index("Build onedir bundle") < linux.index(
        "Build hook shim (linux/amd64)"
    )
    assert linux.index("Build hook shim (linux/amd64)") < linux.index(
        "Build .deb + .rpm"
    )
    assert "GOOS=linux GOARCH=amd64" in linux

    legacy = _job(workflow, "build-linux-legacy", "build-container")
    assert legacy.index("Build onedir bundle") < legacy.index(
        "Build hook shim (linux/amd64)"
    )
    assert legacy.index("Build hook shim (linux/amd64)") < legacy.index(
        "Build legacy .deb + .rpm"
    )


def test_windows_sign_action_recurses_executable_payloads() -> None:
    action = _WINDOWS_SIGN_ACTION.read_text()
    script = _WINDOWS_SIGN_SCRIPT.read_text()

    assert action.count('$extensions = @(".exe", ".dll", ".pyd")') == 2
    assert action.count("Get-ChildItem -LiteralPath $folder -Recurse -File") == 2
    assert 'Join-Path $env:ACTION_PATH "sign-shards.ps1"' in action
    assert "TimeStamperCertificate" in action
    assert "ShardStartDelayMilliseconds = 1000" in script
    assert "[System.Threading.Tasks.Task]::WaitAll" in script
    assert "MaxCommandLineLength = 30000" in script


def test_macos_pkg_requires_universal_shim_and_signs_it_separately() -> None:
    script = _BUILD_PKG.read_text()

    assert 'HOOK_SHIM="$DIST_DIR/aiwatch/aiwatch-hook"' in script
    assert '[ ! -x "$HOOK_SHIM" ]' in script
    assert 'lipo -archs "$HOOK_SHIM"' in script
    assert "grep -qw arm64" in script
    assert "grep -qw x86_64" in script
    assert 'chmod 755 "$PAYLOAD_HOOK_SHIM"' in script
    assert '[ "$f" = "$MAIN_BIN" ] || [ "$f" = "$PAYLOAD_HOOK_SHIM" ]' in script

    shim_start = script.index(
        'echo "  Signing hook shim with identifier=com.runlayer.aiwatch.hook'
    )
    main_start = script.index(
        'echo "  Signing aiwatch binary with identifier=com.runlayer.aiwatch'
    )
    shim_signing = script[shim_start:main_start]
    assert "--options=runtime --timestamp" in shim_signing
    assert "--identifier com.runlayer.aiwatch.hook" in shim_signing
    assert "--entitlements" not in shim_signing
    assert 'codesign --verify --strict --verbose=2 "$PAYLOAD_HOOK_SHIM"' in (
        shim_signing
    )

    main_signing = script[main_start:]
    assert '--entitlements "$ENTITLEMENTS"' in main_signing
    assert "--identifier com.runlayer.aiwatch" in main_signing
    assert 'codesign --verify --deep --strict --verbose=2 "$MAIN_BIN"' in main_signing


def test_windows_wix_harvests_hook_shim() -> None:
    wix = _WINDOWS_WIX.read_text()
    start = wix.index('<ComponentGroup Id="Files"')
    end = wix.index("</ComponentGroup>", start)
    harvest = wix[start:end]

    assert r'<Files Include="..\..\dist\aiwatch\**">' in harvest
    assert r'<Exclude Files="..\..\dist\aiwatch\aiwatch.exe"/>' in harvest
    assert "aiwatch-hook.exe" not in harvest


def test_local_package_targets_build_the_shim_after_the_onedir() -> None:
    makefile = _MAKEFILE.read_text()
    phony = makefile.split("\n", 1)[0]

    for platform in ("macos", "windows", "linux"):
        shim_target = f"package-aiwatch-hook-{platform}"
        assert shim_target in phony
        # The onedir freeze wipes dist/aiwatch, so the shim must be built after
        # it and before the platform packaging step.
        assert f"\n{shim_target}: package-aiwatch-binary\n" in makefile
        assert f"\npackage-aiwatch-{platform}: {shim_target}\n" in makefile

    macos = _rule(makefile, "package-aiwatch-hook-macos")
    assert "GOOS=darwin GOARCH=arm64" in macos
    assert "GOOS=darwin GOARCH=amd64" in macos
    assert "lipo -create" in macos
    assert "dist/aiwatch/aiwatch-hook" in macos

    linux = _rule(makefile, "package-aiwatch-hook-linux")
    assert "GOOS=linux GOARCH=amd64" in linux
    assert "dist/aiwatch/aiwatch-hook" in linux

    windows = _rule(makefile, "package-aiwatch-hook-windows")
    assert "build_hook_shim.ps1" in windows

    for rule in (macos, linux):
        assert "-trimpath" in rule
        assert "-X main.version=" in rule
        assert "./cmd/aiwatch-hook" in rule
        assert "CGO_ENABLED=0" in rule


def test_windows_shim_script_builds_into_the_onedir() -> None:
    script = _WINDOWS_SHIM_BUILD.read_text()

    assert '$env:CGO_ENABLED = "0"' in script
    assert '$env:GOOS = "windows"' in script
    assert '$env:GOARCH = "amd64"' in script
    assert "-trimpath" in script
    assert "-X main.version=$Version" in script
    assert "aiwatch-hook.exe" in script
    assert "./cmd/aiwatch-hook" in script


def test_shim_ci_checks_and_cross_builds_all_release_targets() -> None:
    workflow = _TEST_WORKFLOW.read_text()

    assert '"aiwatch-hook-shim/**"' in workflow
    assert "go-version-file: aiwatch-hook-shim/go.mod" in workflow
    assert "gofmt -l ." in workflow
    assert "go vet ./..." in workflow
    assert "go test ./..." in workflow
    assert "CGO_ENABLED=0 go build -trimpath" in workflow
    assert workflow.count("./cmd/aiwatch-hook") == 5
    assert "./cmd/aiwatch-hook-shim" not in workflow
    for target in (
        "GOOS=darwin GOARCH=arm64",
        "GOOS=darwin GOARCH=amd64",
        "GOOS=windows GOARCH=amd64",
        "GOOS=linux GOARCH=amd64",
    ):
        assert target in workflow
    assert '"cli/tests/test_hook_shim_protocol.py"' in workflow
    assert '"cli/Makefile"' in workflow
    assert '"cli/packaging/windows/build_hook_shim.ps1"' in workflow
    assert "sfw uv sync --frozen" in workflow
    assert "uv run pytest tests/test_hook_shim_protocol.py" in workflow
    assert "uv run pytest tests/test_aiwatch_hook_shim_packaging.py" in workflow
