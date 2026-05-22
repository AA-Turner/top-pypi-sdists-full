"""Unity engine adapter.

Full end-to-end pipeline gated on Unity Editor being installed locally.
We bundle a small C# `Editor/SageBuilder.cs` into the scaffold so the
`-executeMethod` flag in batchmode can drive the build:

    Unity -batchmode -quit -projectPath <out_dir>
          -executeMethod SageBuilder.BuildWebGL
          -logFile -

Unity licensing is the user's responsibility; we don't check for it.
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


_MAC_HUB_GLOB = "/Applications/Unity/Hub/Editor/*/Unity.app/Contents/MacOS/Unity"
_LINUX_HUB_GLOB = "/opt/Unity/Hub/Editor/*/Editor/Unity"
# Unity Hub on Windows installs editors under either Program Files or
# %LOCALAPPDATA% (depending on install scope). Glob both, newest version
# wins like the other platforms.
_WIN_HUB_GLOBS = (
    r"C:\Program Files\Unity\Hub\Editor\*\Editor\Unity.exe",
    r"C:\Program Files (x86)\Unity\Hub\Editor\*\Editor\Unity.exe",
)


class UnityAdapter:
    name = "unity"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        # 1. Plain `Unity` on PATH (rare but cheapest check).
        path = shutil.which("Unity")
        if path:
            return Path(path)
        # 2. Unity Hub-installed editors — newest version wins.
        from glob import glob
        sysname = platform.system()
        if sysname == "Darwin":
            patterns = (_MAC_HUB_GLOB,)
        elif sysname == "Windows":
            local_app = Path(os.environ.get("LOCALAPPDATA",
                                             str(Path.home() / "AppData" / "Local")))
            patterns = (
                *_WIN_HUB_GLOBS,
                str(local_app / "Unity" / "Hub" / "Editor" / "*" / "Editor" / "Unity.exe"),
            )
        else:
            patterns = (_LINUX_HUB_GLOB,)
        for pat in patterns:
            candidates = sorted(glob(pat), reverse=True)
            if candidates:
                return Path(candidates[0])
        return None

    def install_hint(self) -> str:
        return ("Install Unity Hub from https://unity.com/download, then "
                "install Unity 2022 LTS (or newer) via the Hub.")

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        """Write minimal Unity project layout. Unity Editor will hydrate
        the rest of the metadata on first open / batchmode build."""
        (out_dir / "Assets" / "Scripts").mkdir(parents=True, exist_ok=True)
        (out_dir / "Assets" / "Scenes").mkdir(parents=True, exist_ok=True)
        (out_dir / "Assets" / "Sprites").mkdir(parents=True, exist_ok=True)
        (out_dir / "Assets" / "Audio").mkdir(parents=True, exist_ok=True)
        (out_dir / "Assets" / "Meshes").mkdir(parents=True, exist_ok=True)
        (out_dir / "Assets" / "Editor").mkdir(parents=True, exist_ok=True)
        (out_dir / "ProjectSettings").mkdir(parents=True, exist_ok=True)
        (out_dir / "Packages").mkdir(parents=True, exist_ok=True)

        # ProjectVersion.txt — Unity checks this when opening. We write
        # whatever Unity version is actually installed so Unity doesn't
        # offer to upgrade on first open (which can break the build).
        # Falls back to a 2022 LTS pin if no Unity is detected at scaffold
        # time (e.g. the user is scaffolding for a teammate to build).
        version_line = _detect_unity_version() or "2022.3.20f1"
        (out_dir / "ProjectSettings" / "ProjectVersion.txt").write_text(
            f"m_EditorVersion: {version_line}\n",
            encoding="utf-8",
        )

        # Manifest for Unity's package manager. We declare the standard
        # built-in modules every 2D/3D game scaffold needs — Physics2D
        # for collisions, UI for HUD, AudioModule for SFX/music,
        # ParticleSystem for visual effects, InputLegacy for the simple
        # Input API the scaffold uses. Without these the LLM-emitted
        # gameplay scripts (which reference UnityEngine.UI, Physics2D,
        # AudioSource, etc.) fail to compile and Unity batchmode aborts.
        # Versions are pinned at 1.0.0 — Unity's built-in modules share
        # one version across the editor install.
        (out_dir / "Packages" / "manifest.json").write_text(
            json.dumps({
                "dependencies": {
                    "com.unity.modules.physics2d":   "1.0.0",
                    "com.unity.modules.physics":     "1.0.0",
                    "com.unity.modules.ui":          "1.0.0",
                    "com.unity.modules.uielements":  "1.0.0",
                    "com.unity.modules.audio":       "1.0.0",
                    "com.unity.modules.imgui":       "1.0.0",
                    "com.unity.modules.animation":   "1.0.0",
                    "com.unity.modules.particlesystem": "1.0.0",
                    "com.unity.modules.androidjni":  "1.0.0",
                    "com.unity.modules.jsonserialize": "1.0.0",
                    "com.unity.modules.unitywebrequest": "1.0.0",
                    "com.unity.modules.subsystems":  "1.0.0",
                    "com.unity.modules.unityanalytics": "1.0.0",
                    "com.unity.modules.video":       "1.0.0",
                    "com.unity.modules.tilemap":     "1.0.0",
                    "com.unity.modules.terrain":     "1.0.0",
                    "com.unity.modules.imageconversion": "1.0.0",
                },
            }, indent=2) + "\n",
            encoding="utf-8",
        )

        # SageBuilder.cs — driven by Unity batchmode `-executeMethod`.
        (out_dir / "Assets" / "Editor" / "SageBuilder.cs").write_text(
            _SAGE_BUILDER_CS, encoding="utf-8",
        )

        log(f"  [unity] scaffolded {out_dir.name}")

    def emit_scripts(
        self,
        plan: GamePlan,
        out_dir: Path,
        *,
        generate: GenerateFn,
        log: ProgressFn,
    ) -> list[Path]:
        """Write C# gameplay scripts under Assets/Scripts/."""
        prompt = _CS_PROMPT.format(
            title=plan.title,
            description=plan.description,
            genre=plan.request.genre or "platformer",
            perspective=plan.request.perspective or "2d",
            features="\n".join(f"  - {f}" for f in plan.features) or "  - (none)",
        )
        try:
            raw = generate(prompt)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"unity script generation failed: {exc}") from exc

        scripts = _parse_cs_blocks(raw)
        if not scripts:
            # No fallback template — silently shipping a stub
            # PlayerController would mask the LLM failure and pretend
            # the build is fine. Pipeline heal loop reads this error
            # and re-prompts.
            raise RuntimeError(
                "unity: LLM response had no parseable ```Name.cs``` "
                f"blocks. Raw response head:\n{raw[:600]!r}"
            )
        written: list[Path] = []
        for name, body in scripts.items():
            path = out_dir / "Assets" / "Scripts" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            written.append(path)
        log(f"  [unity] wrote {len(written)} C# script(s)")
        return written

    def consume_assets(
        self,
        manifest: AssetManifest,
        out_dir: Path,
        *,
        log: ProgressFn,
    ) -> None:
        # Sprite animation strips land alongside the static base sprite in
        # Assets/Sprites/. Unity's Sprite Editor can slice them into frames
        # at edit time; LLM-emitted scripts can also load them directly.
        # Mesh animation clips are baked into the GLB itself — Unity
        # auto-imports them as Animation Clip sub-assets.
        copied = 0
        for src in manifest.sprites.values():
            shutil.copy2(src, out_dir / "Assets" / "Sprites" / src.name); copied += 1
        for src in manifest.sprite_animations.values():
            shutil.copy2(src, out_dir / "Assets" / "Sprites" / src.name); copied += 1
        for src in manifest.audio.values():
            shutil.copy2(src, out_dir / "Assets" / "Audio" / src.name); copied += 1
        for src in manifest.meshes.values():
            shutil.copy2(src, out_dir / "Assets" / "Meshes" / src.name); copied += 1
        log(f"  [unity] consumed {copied} asset(s) "
            f"({len(manifest.sprite_animations)} anim strips)")

    def build(
        self,
        out_dir: Path,
        *,
        target: str,
        log: ProgressFn,
    ) -> BuildArtifact:
        binary = self.detect()
        if binary is None:
            raise EngineNotInstalled("unity", self.install_hint())

        method = _TARGET_TO_METHOD.get(target, "SageBuilder.BuildWebGL")

        # Wipe any previous build of this target so the artifact check can't
        # be fooled by stale output left behind by an earlier successful run.
        build_subdir = out_dir / "Build" / _TARGET_TO_BUILDTARGET.get(target, "WebGL")
        if build_subdir.exists():
            shutil.rmtree(build_subdir, ignore_errors=True)

        log(f"  [unity] batchmode build via {method} (cold start 1–3 min)...")
        start = time.monotonic()
        proc = subprocess.run(
            [
                str(binary), "-batchmode", "-quit", "-nographics",
                "-projectPath", str(out_dir),
                "-executeMethod", method,
                "-logFile", "-",
            ],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=1800, check=False,
        )
        duration = time.monotonic() - start

        # SageBuilder logs "is not supported by this Unity install" when
        # the matching build-support module isn't installed via Unity Hub
        # (the WebGL Build Support / Mac Build Support / etc. modules).
        # That's user-fixable in 60 seconds and isn't a code bug, so we
        # raise BuildNotSupported with a copy-pasteable hint instead of
        # exhausting heal rounds on a build that can't possibly succeed.
        if "is not supported by this Unity install" in (proc.stdout or ""):
            raise BuildNotSupported(
                "unity",
                f"Unity {target} build needs the matching 'Build Support' "
                f"module. Open Unity Hub → Installs → ⚙ → Add Modules and "
                f"install '{_TARGET_TO_MODULE_HINT.get(target, target)} "
                f"Build Support'.",
            )

        # Unity organises builds under Build/<BuildTarget>/. The artifact
        # we actually shipped depends on the target — for desktop builds
        # it's an exe/app/x86_64; for WebGL it's the directory itself.
        # CRITICAL: search ONLY within this run's per-target subdir, not
        # the whole Build/ tree. The previous bug here — `build_root.rglob`
        # — let a stale `game.app` from a Mac build show up as the
        # "artifact" of an Android build that actually produced nothing.
        build_subdir = (out_dir / "Build" /
                        _TARGET_TO_BUILDTARGET.get(target, "WebGL"))

        # Pick the platform-specific entry-point as the headline artifact —
        # the largest file is typically UnityPlayer.dll (~50 MB engine runtime)
        # which isn't what the user runs. Prefer game.exe / game.app / etc.
        preferred_names = {
            "web":     ("index.html",),
            "windows": ("game.exe",),
            "mac":     ("game.app",),
            "linux":   ("game.x86_64",),
            "android": ("game.apk",),
            "ios":     ("Unity-iPhone.xcodeproj",),
        }.get(target, ())
        output: Optional[Path] = None
        if build_subdir.exists():
            for name in preferred_names:
                for c in build_subdir.rglob(name):
                    if c.is_file() or c.is_dir():
                        output = c
                        break
                if output:
                    break
            if output is None:
                # Fall back to the largest file in THIS target's subdir
                # only — never reach across targets.
                candidates = sorted(
                    (c for c in build_subdir.rglob("*") if c.is_file()),
                    key=lambda p: p.stat().st_size, reverse=True,
                )
                output = candidates[0] if candidates else None

        # Truth source is the per-target artifact — Unity's batchmode rc is
        # unreliable (shader-compiler teardown, domain-reload crashes after a
        # successful BuildPlayer can leave rc != 0 even though the binary
        # shipped). If we have an artifact in the right subdir, the build
        # succeeded; otherwise complain with the log tail.
        if output is None or (output.is_file() and output.stat().st_size == 0):
            raise RuntimeError(
                f"unity batchmode produced no usable artifact under "
                f"{build_subdir} (rc={proc.returncode}). Common causes: "
                f"the Unity build-support module for `{target}` isn't "
                f"installed via Unity Hub. Log tail:\n"
                f"{(proc.stdout or '')[-1200:]}"
            )

        # For desktop Unity builds the headline "game.exe" / "game.x86_64"
        # is just the launcher (a few KB) — the real game payload lives in
        # the same dir as UnityPlayer.{dll,so,dylib} + game_Data/. Report
        # the per-target build subdir's total size so users see ~30–100 MB
        # rather than 4 KB.
        size = (output.stat().st_size if output.is_file()
                else _dir_size(output))
        if size < 1_000_000 and build_subdir.exists():
            size = _dir_size(build_subdir)
        if proc.returncode != 0:
            log(f"  [unity] note: unity exited rc={proc.returncode} but "
                f"produced {output.name} — treating as success")
        log(f"  [unity] build OK ({duration:.1f}s) → {output.name} ({size:,} bytes)")
        return BuildArtifact(
            output_path=output, target=target, size_bytes=size, duration_s=duration,
        )


def _dir_size(p: Path) -> int:
    """Recursive byte count for directory artifacts (WebGL build, xcodeproj)."""
    if not p.exists():
        return 0
    if p.is_file():
        return p.stat().st_size
    total = 0
    for child in p.rglob("*"):
        if child.is_file():
            try:
                total += child.stat().st_size
            except OSError:
                pass
    return total


# ─────────────────────────── helpers ───────────────────────────────────


_TARGET_TO_METHOD = {
    "web": "SageBuilder.BuildWebGL",
    "windows": "SageBuilder.BuildWindows",
    "mac": "SageBuilder.BuildMac",
    "linux": "SageBuilder.BuildLinux",
    "android": "SageBuilder.BuildAndroid",
    "ios": "SageBuilder.BuildIOS",
}

# Used to wipe stale per-target build dirs (Build/<BuildTarget>/) so the
# artifact-existence check can't pick up output from a previous run.
_TARGET_TO_BUILDTARGET = {
    "web": "WebGL",
    "windows": "StandaloneWindows64",
    "mac": "StandaloneOSX",
    "linux": "StandaloneLinux64",
    "android": "Android",
    "ios": "iOS",
}


# Friendly module names for the Unity Hub install hint we surface when a
# given target's Build Support module isn't installed.
_TARGET_TO_MODULE_HINT = {
    "web":     "WebGL",
    "windows": "Windows",
    "mac":     "Mac",
    "linux":   "Linux",
    "android": "Android",
    "ios":     "iOS",
}


_SAGE_BUILDER_CS = """using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

// sage-generated build driver. Invoked by Unity in batchmode via
//   Unity -batchmode -quit -executeMethod SageBuilder.BuildWebGL
// Add new platforms by following the same shape.
//
// Both success and failure paths call EditorApplication.Exit explicitly.
// Without that, Unity's batchmode sometimes returns a non-zero rc even
// on successful builds (e.g. shader-compiler subprocess teardown bugs),
// and sage's pipeline thinks the build crashed when it actually shipped.
public static class SageBuilder
{
    private static string OutDir(BuildTarget target)
        => Path.Combine(Application.dataPath, "..", "Build", target.ToString());

    // BuildPlayer requires at least one scene path RELATIVE to project root
    // (e.g. "Assets/Scenes/Main.unity"). Sage's scaffold doesn't write a
    // scene file because Unity's scene format is GUID-laden and generally
    // produced by the editor itself. So we materialize a minimal default
    // scene here on first build — subsequent runs reuse it.
    private static string[] AllScenes() {
        var scenesDir = Path.Combine(Application.dataPath, "Scenes");
        if (!Directory.Exists(scenesDir)) Directory.CreateDirectory(scenesDir);
        var existing = Directory.GetFiles(scenesDir, "*.unity",
                                          SearchOption.AllDirectories);
        if (existing.Length > 0) {
            // Convert absolute paths to project-relative for BuildPlayer.
            for (int i = 0; i < existing.Length; i++) {
                existing[i] = "Assets" + existing[i].Substring(
                    Application.dataPath.Length).Replace('\\\\', '/');
            }
            return existing;
        }
        // No scenes yet — create an empty one with the default Main Camera +
        // Directional Light setup. This is what File > New Scene produces.
        var scene = EditorSceneManager.NewScene(
            NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
        var relPath = "Assets/Scenes/Main.unity";
        EditorSceneManager.SaveScene(scene, relPath);
        return new[] { relPath };
    }

    public static void BuildWebGL()   => Build(BuildTarget.WebGL);
    public static void BuildWindows() => Build(BuildTarget.StandaloneWindows64);
    public static void BuildMac()     => Build(BuildTarget.StandaloneOSX);
    public static void BuildLinux()   => Build(BuildTarget.StandaloneLinux64);
    public static void BuildAndroid() => Build(BuildTarget.Android);
    public static void BuildIOS()     => Build(BuildTarget.iOS);

    private static void Build(BuildTarget target) {
        try {
            var targetGroup = BuildPipeline.GetBuildTargetGroup(target);

            // BuildResult.Unknown is what BuildPlayer returns when it
            // aborts before really starting — usually because the matching
            // build-support module isn't installed via Unity Hub. Surface
            // that BEFORE invoking BuildPlayer so the user gets a useful
            // error instead of a cryptic "result: Unknown".
            if (!BuildPipeline.IsBuildTargetSupported(targetGroup, target)) {
                Debug.LogError(
                    "Sage Unity build failed: build target " + target +
                    " is not supported by this Unity install. Open Unity Hub" +
                    " → Installs → ⚙ → Add Modules and install the matching" +
                    " 'Build Support' module (e.g. WebGL, Mac, Linux, Android," +
                    " iOS).");
                EditorApplication.Exit(3);
                return;
            }

            // Switch to the requested platform before BuildPlayer — Unity
            // refuses to build a target that isn't the active one. Skip
            // the switch when already active; switching triggers a domain
            // reload that can derail the rest of execution.
            if (EditorUserBuildSettings.activeBuildTarget != target) {
                EditorUserBuildSettings.SwitchActiveBuildTarget(targetGroup, target);
            }

            var outDir = OutDir(target);
            Directory.CreateDirectory(outDir);

            // BuildPlayer expects a FILE name (the .exe / .app), not a folder.
            var fileName = target switch {
                BuildTarget.WebGL => "",
                BuildTarget.StandaloneWindows64 => "game.exe",
                BuildTarget.StandaloneOSX => "game.app",
                BuildTarget.StandaloneLinux64 => "game.x86_64",
                BuildTarget.Android => "game.apk",
                BuildTarget.iOS => "",
                _ => "game",
            };
            var locationPath = fileName.Length == 0 ? outDir : Path.Combine(outDir, fileName);

            var options = new BuildPlayerOptions {
                scenes = AllScenes(),
                locationPathName = locationPath,
                target = target,
                options = BuildOptions.None,
            };
            var report = BuildPipeline.BuildPlayer(options);
            if (report.summary.result != UnityEditor.Build.Reporting.BuildResult.Succeeded) {
                Debug.LogError("Sage Unity build failed: " + report.summary.result +
                               " (errors=" + report.summary.totalErrors +
                               ", warnings=" + report.summary.totalWarnings + ")");
                EditorApplication.Exit(1);
                return;
            }
            Debug.Log("Sage Unity build OK -> " + locationPath);
            EditorApplication.Exit(0);
        } catch (System.Exception e) {
            Debug.LogError("Sage Unity build exception: " + e);
            EditorApplication.Exit(2);
        }
    }
}
"""


_CS_PROMPT = """You're writing Unity C# scripts for a small playable game.

Title: {title}
Description: {description}
Genre: {genre}
Perspective: {perspective}
Required features:
{features}

Write the gameplay scripts (PlayerController.cs and any other C# files
the game needs). Constraints:
  - Unity 2022 LTS C#. Use `MonoBehaviour`, `Update()`, `Start()`.
  - Reference assets under `Assets/Sprites/<name>.png` / `Assets/Audio/<n>.ogg`.
  - Each file under 200 lines.

Output format — one fenced block per file:

```PlayerController.cs
using UnityEngine;

public class PlayerController : MonoBehaviour {{ ... }}
```

Output ONLY the code blocks. No prose."""


_BLOCK_RE = __import__("re").compile(
    r"```([A-Za-z_][A-Za-z0-9_]*\.cs)\s*\n(.*?)```", __import__("re").DOTALL,
)


def _parse_cs_blocks(raw: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in _BLOCK_RE.finditer(raw):
        name = m.group(1)
        body = m.group(2).strip() + "\n"
        out[name] = body
    return out


def _detect_unity_version() -> Optional[str]:
    """Resolve the installed Unity's version string for ProjectVersion.txt.

    Reads it from the Hub install path (.../Editor/<version>/Editor/Unity.exe)
    rather than spawning `Unity -version` — that's a 30-60s cold start we
    don't want during scaffold. Returns None when no Unity is detected so
    the caller can fall back to a pinned 2022 LTS version."""
    adapter = UnityAdapter()
    binary = adapter.detect()
    if binary is None:
        return None
    # Hub path is .../Editor/<X.Y.Zfn>/Editor/Unity.exe; the version is
    # the parent-of-parent directory name.
    parts = binary.parts
    try:
        editor_idx = parts.index("Editor")
        return parts[editor_idx + 1]
    except (ValueError, IndexError):
        return None
