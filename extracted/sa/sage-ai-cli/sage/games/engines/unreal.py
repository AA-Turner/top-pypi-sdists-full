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

        # .uproject manifest — Unreal reads this to find the project.
        (out_dir / f"{project_name}.uproject").write_text(json.dumps({
            "FileVersion": 3,
            "EngineAssociation": "5.4",
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

        log(f"  [unreal] scaffolded {project_name} (.uproject + module)")

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
            scripts = {
                f"{project_name}GameMode.h": _DEFAULT_GM_H.format(project_name=project_name),
                f"{project_name}GameMode.cpp": _DEFAULT_GM_CPP.format(project_name=project_name),
            }

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
        copied = 0
        for src in manifest.sprites.values():
            shutil.copy2(src, out_dir / "Content" / "Sprites" / src.name); copied += 1
        for src in manifest.audio.values():
            shutil.copy2(src, out_dir / "Content" / "Audio" / src.name); copied += 1
        for src in manifest.meshes.values():
            shutil.copy2(src, out_dir / "Content" / "Meshes" / src.name); copied += 1
        log(f"  [unreal] consumed {copied} asset(s)")

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
        platform = _TARGET_TO_PLATFORM.get(target, "Win64")
        log(f"  [unreal] UAT BuildCookRun for {platform} (30–60 min first build)...")
        start = time.monotonic()
        proc = subprocess.run(
            [str(uat), "BuildCookRun",
             f"-project={uproject}",
             "-clientconfig=Development",
             f"-platform={platform}",
             "-build", "-cook", "-stage", "-package", "-pak", "-archive",
             f"-archivedirectory={out_dir / 'Build'}"],
            capture_output=True, text=True, timeout=5400, check=False,
        )
        duration = time.monotonic() - start

        if proc.returncode != 0:
            raise RuntimeError(
                f"unreal UAT failed (rc={proc.returncode}):\n"
                f"{(proc.stdout or '')[-1200:]}"
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


_DEFAULT_GM_H = """#pragma once
#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "{project_name}GameMode.generated.h"

UCLASS()
class A{project_name}GameMode : public AGameModeBase {{
    GENERATED_BODY()
public:
    A{project_name}GameMode();
}};
"""

_DEFAULT_GM_CPP = """#include "{project_name}GameMode.h"

A{project_name}GameMode::A{project_name}GameMode() {{
    // Placeholder game mode — LLM didn't produce parseable scripts.
}}
"""


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
