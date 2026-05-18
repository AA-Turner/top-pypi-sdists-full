"""Godot 4 engine adapter — full end-to-end pipeline.

Godot is the v1 default engine because it's free, ~80MB, installable via
package managers (`brew install --cask godot` / `apt install godot4` /
`winget install Godot`), and supports a clean headless export pipeline
(`godot --headless --export-release`).

Project layout we emit:
    out_dir/
    ├── project.godot             # engine manifest, defines main scene
    ├── icon.svg                  # default icon
    ├── default_env.tres          # world environment (sky, ambient light)
    ├── export_presets.cfg        # WebGL / Windows / Mac / Linux presets
    ├── scenes/
    │   └── Main.tscn             # the main scene we boot into
    ├── scripts/
    │   ├── Main.gd               # entry-point logic
    │   └── Player.gd             # gameplay logic — LLM-generated
    └── assets/                   # images/audio/meshes consumed from manifest
        ├── sprites/
        ├── audio/
        └── meshes/
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import time
from pathlib import Path
from typing import Optional

from ..assets.manifest import AssetManifest
from ..exceptions import EngineNotInstalled
from .base import (
    BuildArtifact,
    EngineAdapter,
    EngineCapability,
    GamePlan,
    GenerateFn,
    ProgressFn,
)


# Search order for the Godot binary. macOS install via Homebrew puts it
# at /opt/homebrew/bin/godot (Apple silicon) or /usr/local/bin/godot
# (Intel); .app bundles live under /Applications.
_BINARY_NAMES = ("godot4", "godot")
_MAC_APPS = (
    "/Applications/Godot.app/Contents/MacOS/Godot",
    "/Applications/Godot_mono.app/Contents/MacOS/Godot",
)
# Windows winget puts Godot at a versioned path under %LOCALAPPDATA%/Microsoft/WinGet/Packages.
# We glob it so detection survives version bumps.
_WIN_GLOBS = (
    r"C:\Program Files\Godot\godot*.exe",
    r"C:\Program Files (x86)\Godot\godot*.exe",
)


class GodotAdapter:
    name = "godot"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        for name in _BINARY_NAMES:
            path = shutil.which(name)
            if path:
                return Path(path)
        for app in _MAC_APPS:
            p = Path(app)
            if p.is_file():
                return p
        if platform.system() == "Windows":
            from glob import glob
            user_winget = (
                Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
                / "Microsoft" / "WinGet" / "Packages"
            )
            patterns = list(_WIN_GLOBS) + [
                str(user_winget / "GodotEngine.GodotEngine_*" / "godot*.exe"),
            ]
            for pat in patterns:
                hits = sorted(glob(pat), reverse=True)
                if hits:
                    return Path(hits[0])
        return None

    def install_hint(self) -> str:
        sysname = platform.system()
        if sysname == "Darwin":
            return "Install with: brew install --cask godot"
        if sysname == "Windows":
            return "Install with: winget install -e --id GodotEngine.GodotEngine"
        return "Install from https://godotengine.org or your package manager"

    # ── Scaffold ──────────────────────────────────────────────────────────

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        """Write the deterministic project skeleton — no LLM calls here.

        We do this ourselves (vs `godot --create-project`) because Godot's
        own scaffold is interactive and varies by version. The text files
        below are stable across 4.x.
        """
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "scenes").mkdir(exist_ok=True)
        (out_dir / "scripts").mkdir(exist_ok=True)
        (out_dir / "assets" / "sprites").mkdir(parents=True, exist_ok=True)
        (out_dir / "assets" / "audio").mkdir(parents=True, exist_ok=True)
        (out_dir / "assets" / "meshes").mkdir(parents=True, exist_ok=True)

        title = plan.title or "Sage Game"

        # project.godot — Godot's manifest. Format is INI-ish.
        (out_dir / "project.godot").write_text(
            f"""; sage-generated Godot 4 project — {title}
config_version=5

[application]

config/name="{title}"
run/main_scene="res://scenes/Main.tscn"
config/features=PackedStringArray("4.2", "Forward Plus")
config/icon="res://icon.svg"

[rendering]

renderer/rendering_method="forward_plus"
""",
            encoding="utf-8",
        )

        # Minimal SVG icon — Godot wants a 128×128 default.
        (out_dir / "icon.svg").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">\n'
            '  <rect width="128" height="128" fill="#3a82f7"/>\n'
            '  <text x="64" y="76" font-family="Arial" font-size="48" '
            'text-anchor="middle" fill="white">S</text>\n'
            '</svg>\n',
            encoding="utf-8",
        )

        # Default environment so the editor opens with a usable world.
        (out_dir / "default_env.tres").write_text(
            """[gd_resource type="Environment" load_steps=2 format=3]

[sub_resource type="Sky" id="Sky_1"]

[resource]
background_mode = 2
sky = SubResource("Sky_1")
ambient_light_source = 2
ambient_light_color = Color(0.4, 0.4, 0.4, 1)
""",
            encoding="utf-8",
        )

        # Main.tscn — minimal scene wiring up the Main.gd script.
        (out_dir / "scenes" / "Main.tscn").write_text(
            """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://scripts/Main.gd" id="1"]

[node name="Main" type="Node2D"]
script = ExtResource("1")
""",
            encoding="utf-8",
        )

        # Export presets — Godot 4.6 requires every preset to declare
        # include_filter / exclude_filter / export_filter even when
        # empty, or `--export-release` fails with "no default was given".
        (out_dir / "export_presets.cfg").write_text(
            """[preset.0]

name="Web"
platform="Web"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path="build/index.html"
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false
script_export_mode=2

[preset.0.options]

custom_template/debug=""
custom_template/release=""
variant/extensions_support=false
variant/thread_support=false
vram_texture_compression/for_desktop=true
vram_texture_compression/for_mobile=false
html/export_icon=true
html/custom_html_shell=""
html/head_include=""
html/canvas_resize_policy=2
html/focus_canvas_on_start=true
html/experimental_virtual_keyboard=false
progressive_web_app/enabled=false
""",
            encoding="utf-8",
        )

        log(f"  [godot] scaffolded {out_dir.name} ({len(list(out_dir.rglob('*')))} files)")

    # ── Scripts ───────────────────────────────────────────────────────────

    def emit_scripts(
        self,
        plan: GamePlan,
        out_dir: Path,
        *,
        generate: GenerateFn,
        log: ProgressFn,
    ) -> list[Path]:
        """Write Main.gd + Player.gd via the LLM, given the game plan."""
        prompt = _GD_PROMPT.format(
            title=plan.title,
            description=plan.description,
            genre=plan.request.genre or "platformer",
            perspective=plan.request.perspective or "2d",
            features="\n".join(f"  - {f}" for f in plan.features) or "  - (none)",
        )

        try:
            raw = generate(prompt)
        except Exception as exc:  # noqa: BLE001 — pipeline catches/retries
            raise RuntimeError(f"godot script generation failed: {exc}") from exc

        scripts = _parse_gd_blocks(raw)
        if not scripts:
            # Fallback: write a no-op Main.gd so the project at least opens.
            scripts = {"Main.gd": _DEFAULT_MAIN_GD}

        written: list[Path] = []
        for name, body in scripts.items():
            path = out_dir / "scripts" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
            written.append(path)
        log(f"  [godot] wrote {len(written)} GDScript file(s)")
        return written

    # ── Assets ────────────────────────────────────────────────────────────

    def consume_assets(
        self,
        manifest: AssetManifest,
        out_dir: Path,
        *,
        log: ProgressFn,
    ) -> None:
        """Copy generated assets into res://assets/."""
        copied = 0
        for role, src in manifest.sprites.items():
            dst = out_dir / "assets" / "sprites" / src.name
            shutil.copy2(src, dst)
            copied += 1
        for role, src in manifest.audio.items():
            dst = out_dir / "assets" / "audio" / src.name
            shutil.copy2(src, dst)
            copied += 1
        for role, src in manifest.meshes.items():
            dst = out_dir / "assets" / "meshes" / src.name
            shutil.copy2(src, dst)
            copied += 1
        log(f"  [godot] consumed {copied} asset(s) into res://assets/")

    # ── Build ─────────────────────────────────────────────────────────────

    def build(
        self,
        out_dir: Path,
        *,
        target: str,
        log: ProgressFn,
    ) -> BuildArtifact:
        binary = self.detect()
        if binary is None:
            raise EngineNotInstalled("godot", self.install_hint())

        preset = _TARGET_TO_PRESET.get(target, "Web")
        ext = _TARGET_TO_EXT.get(target, "html")
        build_dir = out_dir / "build"
        build_dir.mkdir(exist_ok=True)
        out_path = build_dir / f"index.{ext}" if target == "web" else build_dir / f"game.{ext}"

        # Step 0: ensure export templates are installed for THIS exact Godot
        # version. Without them, --export-release fails with a cryptic
        # "No export template found" error. ~500 MB download on first run.
        _ensure_export_templates(binary, log)

        # Step 1: import — Godot needs to scan + cache resources before export.
        log(f"  [godot] importing project (one-time, ~10–30s on first run)...")
        proc = subprocess.run(
            [str(binary), "--headless", "--import"],
            cwd=out_dir, capture_output=True, text=True, timeout=300, check=False,
        )
        # Import returns non-zero on first run sometimes but still produces
        # the cache; we only fail on actual errors in stderr.
        if proc.returncode != 0 and "ERROR" in (proc.stderr or "").upper():
            raise RuntimeError(
                f"godot --import failed:\n{(proc.stderr or '')[-500:]}"
            )

        # Step 2: export.
        log(f"  [godot] exporting {preset} → {out_path.relative_to(out_dir)}...")
        start = time.monotonic()
        proc = subprocess.run(
            [str(binary), "--headless", "--export-release", preset, str(out_path)],
            cwd=out_dir, capture_output=True, text=True, timeout=600, check=False,
        )
        duration = time.monotonic() - start

        if proc.returncode != 0 or not out_path.exists():
            raise RuntimeError(
                f"godot --export-release failed (rc={proc.returncode}):\n"
                f"{(proc.stderr or proc.stdout or '')[-800:]}"
            )

        size = out_path.stat().st_size
        log(f"  [godot] build OK: {out_path.name} ({size:,} bytes, {duration:.1f}s)")
        return BuildArtifact(
            output_path=out_path,
            target=target,
            size_bytes=size,
            duration_s=duration,
        )


# ─────────────────────────── helpers ───────────────────────────────────


def _godot_version(binary: Path) -> str:
    """Return e.g. "4.6.2.stable" — what Godot prints from --version."""
    proc = subprocess.run(
        [str(binary), "--version"],
        capture_output=True, text=True, timeout=15, check=False,
    )
    # Output is a single line like "4.6.2.stable.official.71f334935".
    line = (proc.stdout or proc.stderr or "").strip().split("\n")[0]
    return line


def _template_dir_for(version_line: str) -> Path:
    """Where Godot looks for templates on the current platform.

    macOS: ~/Library/Application Support/Godot/export_templates/<X.Y.Z.stable>/
    Linux: ~/.local/share/godot/export_templates/<X.Y.Z.stable>/
    Windows: %APPDATA%/Godot/export_templates/<X.Y.Z.stable>/
    """
    # version_line example: "4.6.2.stable.official.71f334935"
    parts = version_line.split(".")
    # Keep up to the first "stable"/"dev"/"rc" segment.
    tag_idx = next((i for i, p in enumerate(parts) if not p.isdigit()), len(parts))
    short = ".".join(parts[: tag_idx + 1])  # e.g. "4.6.2.stable"

    sysname = platform.system()
    if sysname == "Darwin":
        root = Path.home() / "Library" / "Application Support" / "Godot"
    elif sysname == "Linux":
        root = Path.home() / ".local" / "share" / "godot"
    else:
        root = Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))) / "Godot"
    return root / "export_templates" / short


def _ensure_export_templates(binary: Path, log: ProgressFn) -> None:
    """Download + extract export templates for the current Godot version if absent.

    Templates ship as a single ~500 MB `.tpz` zip on GitHub releases. We
    cache by version so repeated builds reuse the unpacked copy.
    """
    version_line = _godot_version(binary)
    if not version_line:
        return  # detection failed; let the build attempt fail with clear error
    template_dir = _template_dir_for(version_line)
    # A populated template dir has files like `web_nothreads_release.zip`.
    if template_dir.exists() and any(template_dir.glob("*.zip")):
        return

    # version_line = "4.6.2.stable.official.71f334935" → "4.6.2-stable"
    parts = version_line.split(".")
    tag_idx = next((i for i, p in enumerate(parts) if not p.isdigit()), len(parts))
    numeric = ".".join(parts[: tag_idx])     # "4.6.2"
    qualifier = parts[tag_idx] if tag_idx < len(parts) else "stable"
    tag = f"{numeric}-{qualifier}"
    file_qualifier = qualifier  # GitHub naming matches the version qualifier
    url = (
        f"https://github.com/godotengine/godot/releases/download/{tag}/"
        f"Godot_v{numeric}-{file_qualifier}_export_templates.tpz"
    )

    log(f"  [godot] downloading export templates for {tag} (~500 MB, one-time)...")
    template_dir.mkdir(parents=True, exist_ok=True)

    import io
    import zipfile
    import httpx  # sage already depends on this; ships with proper certs
    try:
        with httpx.Client(follow_redirects=True, timeout=600.0) as client:
            resp = client.get(url)
            resp.raise_for_status()
            buf = io.BytesIO(resp.content)
    except Exception as exc:  # noqa: BLE001 — pipeline gives a clear error
        raise RuntimeError(
            f"failed to download Godot {tag} export templates from {url}: {exc}. "
            f"Install manually with the editor's Project → Tools → Export Templates."
        ) from exc

    # The .tpz is a zip whose top-level folder is `templates/`. Strip that
    # prefix when extracting so files land directly in template_dir.
    with zipfile.ZipFile(buf) as zf:
        for member in zf.namelist():
            if member.endswith("/"):
                continue
            rel = member.split("/", 1)[-1] if "/" in member else member
            out_path = template_dir / rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(zf.read(member))
    log(f"  [godot] templates installed at {template_dir}")


_TARGET_TO_PRESET = {
    "web": "Web",
    "windows": "Windows Desktop",
    "mac": "macOS",
    "linux": "Linux/X11",
}
_TARGET_TO_EXT = {
    "web": "html",
    "windows": "exe",
    "mac": "app",
    "linux": "x86_64",
}


_GD_PROMPT = """You're writing Godot 4 GDScript for a small playable game.

Title: {title}
Description: {description}
Genre: {genre}
Perspective: {perspective}
Required features:
{features}

Write Main.gd (the entry-point Node2D script attached to scenes/Main.tscn)
and any additional scripts the game needs (Player.gd, Enemy.gd, etc.).

Constraints:
  - Real GDScript 4.x (not 3.x). Use `func _ready():`, `func _process(delta):`.
  - Reference assets at `res://assets/sprites/<name>.png` /
    `res://assets/audio/<name>.ogg` / `res://assets/meshes/<name>.glb`.
  - Keep each file under 200 lines. Use modular, well-named functions.
  - Do NOT use the `tool` keyword.
  - Player movement, basic physics, win/lose state if relevant.

Output format — one block per file, each like:

```Main.gd
extends Node2D
func _ready():
    ...
```

```Player.gd
extends CharacterBody2D
...
```

Output ONLY the code blocks. No prose."""


_DEFAULT_MAIN_GD = """extends Node2D

# Placeholder Main scene. The LLM didn't produce parseable scripts,
# so we wrote this so the project at least opens in the editor.
func _ready():
    print("sage: placeholder Main scene loaded")
"""


_BLOCK_RE = __import__("re").compile(
    r"```([A-Za-z][A-Za-z0-9_]*\.gd)\s*\n(.*?)```", __import__("re").DOTALL,
)


def _parse_gd_blocks(raw: str) -> dict[str, str]:
    r"""Pull fenced ``Name.gd`` blocks out of an LLM response."""
    out: dict[str, str] = {}
    for m in _BLOCK_RE.finditer(raw):
        name = m.group(1)
        body = m.group(2).strip() + "\n"
        out[name] = body
    return out
