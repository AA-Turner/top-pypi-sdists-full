"""Unreal Engine 5 adapter.

Full end-to-end pipeline gated on UE5 being installed. We scaffold a
minimal C++ project (a `.uproject` JSON, `Source/<Game>/Game.Build.cs`,
and a default `GameMode`/`PlayerController`). Build via UAT:

    RunUAT.bat BuildCookRun -project=<path> -clientconfig=Development
               -platform=Win64 -build -cook -stage -package

WARNING: first build of a fresh UE5 project is 30–60 minutes even on
modern hardware. Timeout cap is 90 min.
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

from ..assets.manifest import AssetManifest
from ..exceptions import BuildNotSupported, EngineNotInstalled
from .base import (
    BuildArtifact,
    EngineCapability,
    GamePlan,
    GenerateFn,
    ProgressFn,
)


_MAC_UE_GLOB = "/Users/Shared/Epic Games/UE_*/Engine/Build/BatchFiles/RunUAT.sh"
_LINUX_UE_GLOB = "/opt/UnrealEngine/Engine/Build/BatchFiles/RunUAT.sh"
# Epic Games Launcher installs UE on Windows under Program Files. UAT
# is the `.bat` wrapper here, not `.sh`.
_WIN_UE_GLOBS = (
    r"C:\Program Files\Epic Games\UE_*\Engine\Build\BatchFiles\RunUAT.bat",
    r"D:\Program Files\Epic Games\UE_*\Engine\Build\BatchFiles\RunUAT.bat",
)


class UnrealAdapter:
    name = "unreal"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        if os.environ.get("SAGE_TESTING") == "1":
            return Path("/usr/local/bin/unreal-dummy")
        from glob import glob
        sysname = platform.system()
        if sysname == "Darwin":
            patterns: tuple[str, ...] = (_MAC_UE_GLOB,)
        elif sysname == "Windows":
            patterns = _WIN_UE_GLOBS
        else:
            patterns = (_LINUX_UE_GLOB,)
        for pat in patterns:
            candidates = sorted(glob(pat), reverse=True)
            if candidates:
                return Path(candidates[0])
        return None

    def install_hint(self) -> str:
        return ("Install Unreal Engine 5 via the Epic Games Launcher "
                "(https://www.unrealengine.com/download). Reserve ~150 GB.")

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        project_name = _sanitize_name(plan.title or "SageGame")
        (out_dir / "Source" / project_name).mkdir(parents=True, exist_ok=True)
        (out_dir / "Content").mkdir(parents=True, exist_ok=True)
        (out_dir / "Content" / "Sprites").mkdir(parents=True, exist_ok=True)
        (out_dir / "Content" / "Audio").mkdir(parents=True, exist_ok=True)
        (out_dir / "Content" / "Meshes").mkdir(parents=True, exist_ok=True)

        # Bind to whatever UE version is actually installed so .uproject
        # doesn't try to associate with a missing engine. Falls back to a
        # pinned LTS-ish version for users scaffolding without UE5 on the
        # box (a teammate will hydrate it later).
        engine_assoc = _detect_ue_version() or "5.4"

        # .uproject manifest — Unreal reads this to find the project.
        (out_dir / f"{project_name}.uproject").write_text(json.dumps({
            "FileVersion": 3,
            "EngineAssociation": engine_assoc,
            "Category": "",
            "Description": plan.description,
            "Modules": [{
                "Name": project_name,
                "Type": "Runtime",
                "LoadingPhase": "Default",
                "AdditionalDependencies": ["Engine"],
            }],
        }, indent=2), encoding="utf-8")

        # Source/<Name>/<Name>.Build.cs — module build config.
        (out_dir / "Source" / project_name / f"{project_name}.Build.cs").write_text(
            f"""using UnrealBuildTool;

public class {project_name} : ModuleRules {{
    public {project_name}(ReadOnlyTargetRules Target) : base(Target) {{
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[] {{
            "Core", "CoreUObject", "Engine", "InputCore"
        }});
    }}
}}
""",
            encoding="utf-8",
        )

        # Bare minimum module + game-mode entry points.
        (out_dir / "Source" / project_name / f"{project_name}.cpp").write_text(
            f"""#include "{project_name}.h"
#include "Modules/ModuleManager.h"

IMPLEMENT_PRIMARY_GAME_MODULE(FDefaultGameModuleImpl, {project_name}, "{project_name}");
""",
            encoding="utf-8",
        )
        (out_dir / "Source" / project_name / f"{project_name}.h").write_text(
            f"""#pragma once
#include "CoreMinimal.h"
""",
            encoding="utf-8",
        )

        # Source/<Name>.Target.cs + <Name>Editor.Target.cs — UE5 REQUIRES
        # these next to the module folder. Without them, UAT prints the
        # cryptic "looks like a uproject file but no targets have been
        # found" and aborts. The Target file tells UE what kind of binary
        # to build (Game / Editor / Server) and which ExtraModuleNames to
        # include. Without one Target.cs per target type, BuildCookRun
        # can't even find a starting point.
        (out_dir / "Source" / f"{project_name}.Target.cs").write_text(
            f"""using UnrealBuildTool;
using System.Collections.Generic;

public class {project_name}Target : TargetRules
{{
    public {project_name}Target(TargetInfo Target) : base(Target)
    {{
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("{project_name}");
    }}
}}
""",
            encoding="utf-8",
        )
        (out_dir / "Source" / f"{project_name}Editor.Target.cs").write_text(
            f"""using UnrealBuildTool;
using System.Collections.Generic;

public class {project_name}EditorTarget : TargetRules
{{
    public {project_name}EditorTarget(TargetInfo Target) : base(Target)
    {{
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("{project_name}");
    }}
}}
""",
            encoding="utf-8",
        )

        log(f"  [unreal] scaffolded {project_name} (.uproject + module + "
            f"Target.cs pair, engine={engine_assoc})")

    def emit_scripts(
        self,
        plan: GamePlan,
        out_dir: Path,
        *,
        generate: GenerateFn,
        log: ProgressFn,
    ) -> list[Path]:
        project_name = _sanitize_name(plan.title or "SageGame")
        prompt = _CPP_PROMPT.format(
            project_name=project_name,
            description=plan.description,
            genre=plan.request.genre or "platformer",
            perspective=plan.request.perspective or "3d",
            features="\n".join(f"  - {f}" for f in plan.features) or "  - (none)",
        )
        try:
            raw = generate(prompt)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"unreal script generation failed: {exc}") from exc

        scripts = _parse_cpp_blocks(raw)
        if not scripts:
            # No fallback template — pipeline heals on RuntimeError.
            raise RuntimeError(
                "unreal: LLM response had no parseable ```Name.cpp``` "
                f"or ```Name.h``` blocks. Raw response head:\n{raw[:600]!r}"
            )

        written: list[Path] = []
        for name, body in scripts.items():
            path = out_dir / "Source" / project_name / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            written.append(path)
        log(f"  [unreal] wrote {len(written)} C++ file(s)")
        return written

    def consume_assets(
        self,
        manifest: AssetManifest,
        out_dir: Path,
        *,
        log: ProgressFn,
    ) -> None:
        # Unreal: sprite/audio/mesh assets land under Content/<Type>/ for the
        # Content Browser to auto-import. Sprite-anim strips ride alongside
        # static sprites; UE's Flipbook can slice frames at edit time. Mesh
        # animation tracks travel inside the GLB and import as AnimationSequence
        # sub-assets automatically.
        copied = 0
        for src in manifest.sprites.values():
            shutil.copy2(src, out_dir / "Content" / "Sprites" / src.name); copied += 1
        for src in manifest.sprite_animations.values():
            shutil.copy2(src, out_dir / "Content" / "Sprites" / src.name); copied += 1
        for src in manifest.audio.values():
            shutil.copy2(src, out_dir / "Content" / "Audio" / src.name); copied += 1
        for src in manifest.meshes.values():
            shutil.copy2(src, out_dir / "Content" / "Meshes" / src.name); copied += 1
        log(f"  [unreal] consumed {copied} asset(s) "
            f"({len(manifest.sprite_animations)} anim strips)")

    def build(
        self,
        out_dir: Path,
        *,
        target: str,
        log: ProgressFn,
    ) -> BuildArtifact:
        uat = self.detect()
        if uat is None:
            raise EngineNotInstalled("unreal", self.install_hint())

        project_files = list(out_dir.glob("*.uproject"))
        if not project_files:
            raise RuntimeError("no .uproject file found — scaffold didn't run?")
        uproject = project_files[0]

        if os.environ.get("SAGE_TESTING") == "1":
            build_root = out_dir / "Build"
            build_root.mkdir(parents=True, exist_ok=True)
            output = build_root / "game.exe"
            output.write_text("dummy", encoding="utf-8")
            return BuildArtifact(
                output_path=output,
                target=target,
                size_bytes=1000,
                duration_s=0.1,
            )

        if target == "web":
            # UE5 dropped HTML5 — there's no usable web exporter. Surface
            # this BEFORE doing the 30-min cook so the user can switch
            # engines (Godot/Phaser both target web cleanly).
            raise BuildNotSupported(
                "unreal",
                "Unreal Engine 5 dropped HTML5/web support in 4.24. "
                "Use Godot or Phaser for web builds, or build a desktop "
                "target instead (windows/mac/linux).",
            )

        # Cross-platform toolchain pre-flight. UAT itself takes 60+ sec to
        # initialize before noticing a missing toolchain — that's a big
        # tax to pay 4× per matrix run. Detect the obvious cases up front
        # and raise BuildNotSupported so the heal loop doesn't try at all.
        sysname = platform.system()
        if target == "ios" and sysname != "Darwin":
            raise BuildNotSupported(
                "unreal",
                "Unreal iOS builds require a macOS host (Xcode + provisioning). "
                "Cross-build from Windows/Linux isn't supported by UE5.",
            )
        if target == "mac" and sysname != "Darwin":
            raise BuildNotSupported(
                "unreal",
                "Unreal macOS builds require either a macOS host or a "
                "configured Remote Build server in Editor Preferences. "
                "Cross-build from a Windows host alone isn't supported.",
            )
        if target == "linux" and sysname == "Windows":
            # UE5's Linux cross-compile needs the Linux clang toolchain
            # ("v22_clang-..._centos7") under Engine/Extras/ThirdPartyNotUE.
            # If the user didn't install it via the Epic Launcher's
            # "Target Platforms" page, UAT prints a vague clang error 30s
            # in. Fast-fail with the install pointer.
            sdk_root = uat.parent.parent.parent / "Extras" / "ThirdPartyNotUE" / "SDKs"
            linux_sdks = list(sdk_root.glob("HostWin64/Linux_x64/v*"))
            if not linux_sdks:
                raise BuildNotSupported(
                    "unreal",
                    "Unreal Linux cross-build needs the bundled Linux clang "
                    "toolchain under Engine/Extras/ThirdPartyNotUE/SDKs/"
                    "HostWin64/Linux_x64/. Install it via Epic Games Launcher "
                    "→ UE5 install → Options → Target Platforms → Linux.",
                )
        if target == "android" and not (
            os.environ.get("ANDROID_HOME")
            or os.environ.get("ANDROID_SDK_ROOT")
            or os.environ.get("NDKROOT")
        ):
            raise BuildNotSupported(
                "unreal",
                "Unreal Android build needs the Android SDK + NDK installed "
                "and ANDROID_HOME / ANDROID_SDK_ROOT set. Run UE5's "
                "Engine/Extras/Android/SetupAndroid.bat to set them up, "
                "then re-run.",
            )
        # Renamed from `platform` to `ue_platform` so we don't shadow the
        # `platform` stdlib module (the pre-flight checks above call
        # `platform.system()`, and Python's local-variable hoisting turns
        # any assignment-later-in-function into UnboundLocalError up top).
        ue_platform = _TARGET_TO_PLATFORM.get(target, "Win64")
        log(f"  [unreal] UAT BuildCookRun for {ue_platform} (30–60 min first build)...")
        start = time.monotonic()
        proc = subprocess.run(
            [str(uat), "BuildCookRun",
             f"-project={uproject}",
             "-clientconfig=Development",
             f"-platform={ue_platform}",
             "-build", "-cook", "-stage", "-package", "-pak", "-archive",
             f"-archivedirectory={out_dir / 'Build'}"],
            capture_output=True, text=True, timeout=5400, check=False,
        )
        duration = time.monotonic() - start

        if proc.returncode != 0:
            log_tail = proc.stdout or ""
            # Visual Studio toolchain version mismatch is by far the most
            # common UE5 build error on a clean Windows install — VS 2022
            # ships a "14.44.x" MSVC that UE5 explicitly bans, and the
            # actual fix is one GUI click in VS Installer (Individual
            # Components → MSVC v143). Surface that as BuildNotSupported
            # so the heal loop doesn't burn another 30-min cook, and
            # surface the exact component name the user needs.
            if ("UnrealBuildTool has banned" in log_tail
                or "missing a valid C++ toolchain" in log_tail):
                raise BuildNotSupported(
                    "unreal",
                    "Unreal Windows build needs a compatible MSVC toolchain. "
                    "Your installed version is on UBT's banned list. Open "
                    "Visual Studio Installer → Modify VS 2022 → Individual "
                    "Components, tick the latest 'MSVC v143 - VS 2022 C++ "
                    "x64/x86 build tools (Spectre-mitigated)' (not v14.44.0-"
                    "14.44.35210, which is banned). Then re-run sage.",
                )
            raise RuntimeError(
                f"unreal UAT failed (rc={proc.returncode}):\n"
                f"{log_tail[-1200:]}"
            )

        build_root = out_dir / "Build"
        output = next((c for c in build_root.rglob("*") if c.is_file()), build_root)
        size = output.stat().st_size if output.is_file() else 0
        log(f"  [unreal] build OK ({duration / 60:.1f} min)")
        return BuildArtifact(
            output_path=output, target=target, size_bytes=size, duration_s=duration,
        )


# ─────────────────────────── helpers ───────────────────────────────────


# UE5 supports Win64, Mac, Linux, plus mobile (Android/iOS). HTML5 was
# removed in 4.24, so `web` is intentionally absent — `build()` raises
# BuildNotSupported up front instead of letting UAT fail 30 minutes in.
_TARGET_TO_PLATFORM = {
    "windows": "Win64",
    "mac": "Mac",
    "linux": "Linux",
    "android": "Android",
    "ios": "IOS",
}


def _detect_ue_version() -> Optional[str]:
    """Read the installed UE major.minor from the Epic Games install path.

    `UE_5.7\\Engine\\Build\\BatchFiles\\RunUAT.bat` → "5.7". Used to fill
    .uproject's `EngineAssociation` so the project binds to whatever the
    user actually has installed instead of a hardcoded "5.4" that might
    not even exist on their machine."""
    adapter = UnrealAdapter()
    uat = adapter.detect()
    if uat is None:
        return None
    # uat path looks like .../UE_<X.Y>/Engine/Build/BatchFiles/RunUAT.bat
    for part in uat.parts:
        if part.startswith("UE_"):
            return part[3:]
    return None


def _sanitize_name(title: str) -> str:
    """Unreal module names must be alphanumeric, PascalCase, start with letter.

    If the user already wrote a chunk in mixed/upper case (e.g. "MyRPG",
    "FPSGame", "MyAwesomeRPG"), we preserve their casing — `.capitalize()`
    would otherwise destroy it ("Myrpg", "Fpsgame", "Myawesomerpg")."""
    def _cap(chunk: str) -> str:
        # If the chunk has any uppercase letter, assume user-provided
        # casing is intentional (PascalCase, acronyms like RPG/FPS, or
        # mixed like "123Numeric"). Only chunks that are entirely
        # lowercase get capitalize()'d to PascalCase.
        if any(c.isupper() for c in chunk):
            return chunk
        return chunk.capitalize()

    chunks = "".join(c if c.isalnum() else " " for c in title).split()
    name = "".join(_cap(c) for c in chunks if c) or "SageGame"
    return name if name[0].isalpha() else f"Sage{name}"


_CPP_PROMPT = """You're writing UE5 C++ for a small playable game.

Project name: {project_name}
Description: {description}
Genre: {genre}
Perspective: {perspective}
Required features:
{features}

Write the gameplay header + cpp pairs the game needs (GameMode, Pawn,
PlayerController, etc.). Constraints:
  - UE5.4 C++. UCLASS / UFUNCTION / UPROPERTY macros where required.
  - Reference assets under `Content/Sprites/`, `Content/Audio/`, `Content/Meshes/`.
  - Header + impl in matching named pairs.

Output format — one fenced block per file:

```{project_name}GameMode.h
#pragma once
#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
...
```

```{project_name}GameMode.cpp
#include "{project_name}GameMode.h"
...
```

Output ONLY the code blocks. No prose."""


_BLOCK_RE = __import__("re").compile(
    r"```([A-Za-z_][A-Za-z0-9_]*\.(?:cpp|h|hpp))\s*\n(.*?)```", __import__("re").DOTALL,
)


def _parse_cpp_blocks(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in _BLOCK_RE.finditer(raw):
        name = m.group(1)
        body = m.group(2).strip() + "\n"
        out[name] = body
    return out
