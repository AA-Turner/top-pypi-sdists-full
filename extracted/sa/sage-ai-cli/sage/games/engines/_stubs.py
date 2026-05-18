"""Scaffold-only adapters for tier-2 engines.

These all share the same shape: detect the toolchain, scaffold a real
project directory, emit gameplay scripts via the LLM. They diverge on
`build()`:

  - Bevy: full e2e via `cargo build` (sage already handles Rust toolchain).
  - Phaser: full e2e via `vite build` (sage already handles Node toolchain).
  - LÖVE 2D: "build" = zip the project directory (LÖVE's distribution model).
  - GameMaker / Construct / RPG Maker: GUI-only. `build()` raises
    `BuildNotSupported` with a clear "open it in the editor" message.

Keeping them in one file because each is ~40 lines — splitting per engine
would be more boilerplate than the engines themselves contain.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
import zipapp
import zipfile
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


# ─────────────────────────── Bevy ──────────────────────────────────────


class BevyAdapter:
    name = "bevy"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        # rustup user-scope install puts cargo at ~/.cargo/bin/cargo[.exe]
        # but doesn't always update PATH until the next shell restart. Fall
        # back to the canonical location so detection survives a fresh
        # install without sourcing $HOME/.cargo/env.
        import platform
        path = shutil.which("cargo")
        if path:
            return Path(path)
        from pathlib import Path as _P
        suffix = ".exe" if platform.system() == "Windows" else ""
        candidate = _P.home() / ".cargo" / "bin" / f"cargo{suffix}"
        if candidate.is_file():
            return candidate
        return None

    def install_hint(self) -> str:
        return "Install Rust + cargo: https://rustup.rs (one-liner installer)"

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        # `cargo new --bin .` won't run in a non-empty dir; do the layout
        # ourselves and let bevy pull deps via cargo build.
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "src").mkdir(exist_ok=True)
        (out_dir / "assets").mkdir(exist_ok=True)
        slug = (plan.title or "sage_game").lower().replace(" ", "_")
        (out_dir / "Cargo.toml").write_text(
            f"""[package]
name = "{slug}"
version = "0.1.0"
edition = "2021"

[dependencies]
bevy = "0.14"
""",
            encoding="utf-8",
        )
        log(f"  [bevy] scaffolded {slug} (Cargo.toml + src/)")

    def emit_scripts(
        self, plan: GamePlan, out_dir: Path, *, generate: GenerateFn, log: ProgressFn,
    ) -> list[Path]:
        raw = generate(
            f"Write Rust + bevy 0.14 main.rs for a small {plan.request.genre or 'game'}: "
            f"{plan.description}. Output ONLY the Rust code, no fences, no prose."
        )
        path = out_dir / "src" / "main.rs"
        path.write_text(raw.strip() + "\n", encoding="utf-8")
        log(f"  [bevy] wrote src/main.rs")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        for src in (*manifest.sprites.values(), *manifest.audio.values(), *manifest.meshes.values()):
            shutil.copy2(src, out_dir / "assets" / src.name)

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        cargo = self.detect()
        if cargo is None:
            raise EngineNotInstalled("bevy", self.install_hint())
        start = time.monotonic()
        # Use the resolved cargo path (not the bare name) so this works even
        # when PATH wasn't updated after a fresh rustup install.
        proc = subprocess.run(
            [str(cargo), "build", "--release"],
            cwd=out_dir, capture_output=True, text=True, timeout=900, check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"cargo build failed:\n{proc.stderr[-800:]}")
        binary = next(iter((out_dir / "target" / "release").glob("*")), None)
        size = binary.stat().st_size if binary and binary.is_file() else 0
        return BuildArtifact(
            output_path=binary or out_dir, target=target, size_bytes=size,
            duration_s=time.monotonic() - start,
        )


# ─────────────────────────── Phaser ────────────────────────────────────


class PhaserAdapter:
    name = "phaser"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        path = shutil.which("npm")
        return Path(path) if path else None

    def install_hint(self) -> str:
        return "Install Node + npm: https://nodejs.org or via your package manager"

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "src").mkdir(exist_ok=True)
        (out_dir / "public" / "assets").mkdir(parents=True, exist_ok=True)
        (out_dir / "package.json").write_text(json.dumps({
            "name": "sage-phaser-game",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
            },
            "dependencies": {"phaser": "^3.80.0"},
            "devDependencies": {"vite": "^5.0.0", "typescript": "^5.3.0"},
        }, indent=2) + "\n", encoding="utf-8")
        (out_dir / "index.html").write_text(
            '<!doctype html><html><head><title>Sage Phaser</title></head>'
            '<body><div id="game"></div><script type="module" src="/src/main.ts"></script></body></html>\n',
            encoding="utf-8",
        )
        log(f"  [phaser] scaffolded package.json + index.html")

    def emit_scripts(
        self, plan: GamePlan, out_dir: Path, *, generate: GenerateFn, log: ProgressFn,
    ) -> list[Path]:
        raw = generate(
            f"Write Phaser 3 TypeScript main.ts for a small {plan.request.genre or 'game'}: "
            f"{plan.description}. Mount on #game div. Output ONLY the TS, no fences."
        )
        path = out_dir / "src" / "main.ts"
        path.write_text(raw.strip() + "\n", encoding="utf-8")
        log(f"  [phaser] wrote src/main.ts")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        for src in (*manifest.sprites.values(), *manifest.audio.values()):
            shutil.copy2(src, out_dir / "public" / "assets" / src.name)

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        if self.detect() is None:
            raise EngineNotInstalled("phaser", self.install_hint())
        start = time.monotonic()
        subprocess.run(["npm", "install", "--no-audit"], cwd=out_dir, check=False, timeout=300)
        proc = subprocess.run(
            ["npm", "run", "build"], cwd=out_dir, capture_output=True, text=True,
            timeout=300, check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"vite build failed:\n{proc.stderr[-800:]}")
        index = out_dir / "dist" / "index.html"
        size = index.stat().st_size if index.exists() else 0
        return BuildArtifact(
            output_path=index, target=target, size_bytes=size,
            duration_s=time.monotonic() - start,
        )


# ─────────────────────────── LÖVE 2D ───────────────────────────────────


class Love2DAdapter:
    name = "love2d"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        import os, platform
        for n in ("love", "love2d"):
            p = shutil.which(n)
            if p:
                return Path(p)
        # macOS bundle install
        mac = Path("/Applications/love.app/Contents/MacOS/love")
        if mac.is_file():
            return mac
        # Windows: installed system-wide via winget, or our portable
        # `sage-tools` extraction under %LOCALAPPDATA%. Glob the common
        # locations so users don't have to add LÖVE to PATH manually.
        if platform.system() == "Windows":
            from glob import glob
            candidates = [
                r"C:\Program Files\LOVE\love.exe",
                r"C:\Program Files (x86)\LOVE\love.exe",
                str(Path(os.environ.get("LOCALAPPDATA",
                                          str(Path.home() / "AppData" / "Local")))
                     / "sage-tools" / "love" / "love.exe"),
            ]
            for c in candidates:
                hits = sorted(glob(c), reverse=True)
                if hits:
                    return Path(hits[0])
        return None

    def install_hint(self) -> str:
        import platform
        if platform.system() == "Windows":
            return ("Install LÖVE 11+ via `winget install Love2d.Love2d`, "
                    "or download the portable zip from https://love2d.org")
        if platform.system() == "Darwin":
            return "Install LÖVE 11+ via `brew install --cask love`"
        return "Install LÖVE 11+ via `apt install love` or https://love2d.org"

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "assets").mkdir(exist_ok=True)
        (out_dir / "conf.lua").write_text(
            f"""function love.conf(t)
    t.window.title = "{plan.title or 'Sage LÖVE Game'}"
    t.window.width = 800
    t.window.height = 600
end
""",
            encoding="utf-8",
        )
        log(f"  [love2d] scaffolded conf.lua")

    def emit_scripts(
        self, plan: GamePlan, out_dir: Path, *, generate: GenerateFn, log: ProgressFn,
    ) -> list[Path]:
        raw = generate(
            f"Write LÖVE 2D main.lua for a small {plan.request.genre or 'game'}: "
            f"{plan.description}. Use love.load/love.update/love.draw. "
            "Output ONLY Lua, no fences."
        )
        path = out_dir / "main.lua"
        path.write_text(raw.strip() + "\n", encoding="utf-8")
        log(f"  [love2d] wrote main.lua")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        for src in (*manifest.sprites.values(), *manifest.audio.values()):
            shutil.copy2(src, out_dir / "assets" / src.name)

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        # LÖVE "build" is just a zip of the project renamed to .love.
        start = time.monotonic()
        out = out_dir / "build" / "game.love"
        out.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in out_dir.rglob("*"):
                if "build" in p.parts:
                    continue
                if p.is_file():
                    zf.write(p, p.relative_to(out_dir))
        return BuildArtifact(
            output_path=out, target=target, size_bytes=out.stat().st_size,
            duration_s=time.monotonic() - start,
        )


# ─────────────────────────── Pygame ────────────────────────────────────


class PygameAdapter:
    """Pygame — Python-native game runtime.

    Detection succeeds anywhere Python runs (pygame is pip-installable).
    Build target is a `zipapp` `.pyz` that runs with `python game.pyz`,
    with a `requirements.txt` declaring pygame so the user just pip-installs
    once. We avoid bundling pygame itself into the .pyz because compiled
    C extensions don't run from zipapps reliably across platforms.
    """

    name = "pygame"
    capabilities = EngineCapability.full()

    def detect(self) -> Optional[Path]:
        return Path(sys.executable)

    def install_hint(self) -> str:
        return "Pygame ships via pip: `pip install pygame` (auto-installed at run time)."

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "assets" / "sprites").mkdir(parents=True, exist_ok=True)
        (out_dir / "assets" / "audio").mkdir(parents=True, exist_ok=True)
        (out_dir / "requirements.txt").write_text("pygame>=2.5\n", encoding="utf-8")
        (out_dir / "README.md").write_text(
            f"# {plan.title or 'Sage Pygame Game'}\n\n"
            f"Run with `pip install -r requirements.txt && python main.py`,\n"
            f"or `python game.pyz` after `sage` builds the zipapp.\n",
            encoding="utf-8",
        )
        log(f"  [pygame] scaffolded {out_dir.name}")

    def emit_scripts(
        self, plan: GamePlan, out_dir: Path, *, generate: GenerateFn, log: ProgressFn,
    ) -> list[Path]:
        prompt = (
            f"Write Pygame 2.x main.py for a small {plan.request.genre or 'game'}: "
            f"{plan.description}. Use pygame.init(), a 60-fps game loop, "
            f"and load sprites from `assets/sprites/<role>.png` "
            f"and audio from `assets/audio/<role>.ogg`. "
            f"Output ONLY the Python code, no fences, no prose."
        )
        try:
            raw = generate(prompt)
        except Exception as exc:  # noqa: BLE001 — pipeline catches/retries
            raise RuntimeError(f"pygame script generation failed: {exc}") from exc
        path = out_dir / "main.py"
        body = (raw or "").strip()
        if not body:
            body = _DEFAULT_PYGAME_MAIN
        path.write_text(body + "\n", encoding="utf-8")
        log(f"  [pygame] wrote main.py ({len(body):,} bytes)")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        copied = 0
        for src in manifest.sprites.values():
            shutil.copy2(src, out_dir / "assets" / "sprites" / src.name); copied += 1
        for src in manifest.audio.values():
            shutil.copy2(src, out_dir / "assets" / "audio" / src.name); copied += 1
        log(f"  [pygame] consumed {copied} asset(s)")

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        # zipapp.create_archive needs a __main__.py at the top level; we
        # have main.py, so write a tiny shim that re-exports.
        start = time.monotonic()
        shim = out_dir / "__main__.py"
        shim.write_text(
            "import runpy, sys, os\n"
            "sys.path.insert(0, os.path.dirname(__file__))\n"
            "runpy.run_module('main', run_name='__main__')\n",
            encoding="utf-8",
        )
        build_dir = out_dir / "build"
        build_dir.mkdir(exist_ok=True)
        archive = build_dir / "game.pyz"
        # We pass `filter` to keep the .pyz lean — exclude build/, .sage_assets/,
        # and any __pycache__ directories.
        def keep(p: Path) -> bool:
            parts = set(p.parts)
            return "build" not in parts and ".sage_assets" not in parts \
                and "__pycache__" not in parts
        zipapp.create_archive(
            out_dir, target=archive, interpreter="/usr/bin/env python3", filter=keep,
        )
        size = archive.stat().st_size
        log(f"  [pygame] build OK: game.pyz ({size:,} bytes)")
        return BuildArtifact(
            output_path=archive, target=target, size_bytes=size,
            duration_s=time.monotonic() - start,
        )


_DEFAULT_PYGAME_MAIN = """import os
import sys
import pygame

# Placeholder Pygame game. The LLM didn't produce parseable code,
# so this minimal loop runs so the build still produces a usable artifact.
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Sage Pygame Game")
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 60))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit(0)
"""


# ─────────────────────────── GUI-only engines ──────────────────────────


class _GuiOnly:
    """Shared base for engines without a headless build path.

    Subclasses provide `name`, `_editor_name`, `_install_url`. They
    scaffold a starter project (so the user can open it in the editor)
    but raise `BuildNotSupported` from `build()`.
    """

    capabilities = EngineCapability.SCAFFOLD | EngineCapability.SCRIPTS
    _editor_name: str = ""
    _install_url: str = ""

    def detect(self) -> Optional[Path]:
        return None

    def install_hint(self) -> str:
        return f"Install {self._editor_name} from {self._install_url}"

    def scaffold(self, plan: GamePlan, out_dir: Path, *, log: ProgressFn) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "README.md").write_text(
            f"# {plan.title or 'Sage Game'}\n\n"
            f"Scaffolded for **{self._editor_name}**.\n\n"
            f"Open this folder in {self._editor_name} and use the editor's "
            f"export/deploy workflow — this engine doesn't support a "
            f"headless build, so sage can't compile it for you.\n",
            encoding="utf-8",
        )
        log(f"  [{self.name}] scaffolded {out_dir.name} (open in {self._editor_name})")  # type: ignore[attr-defined]

    def emit_scripts(
        self, plan: GamePlan, out_dir: Path, *, generate: GenerateFn, log: ProgressFn,
    ) -> list[Path]:
        # Engine-specific subclasses override this with the right file format.
        return []

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        target = out_dir / "assets"
        target.mkdir(exist_ok=True)
        for src in (*manifest.sprites.values(), *manifest.audio.values(),
                    *manifest.meshes.values()):
            shutil.copy2(src, target / src.name)

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        raise BuildNotSupported(
            self.name,  # type: ignore[attr-defined]
            f"{self._editor_name} only builds via its GUI editor. Open "
            f"the scaffold at {out_dir} and use {self._editor_name}'s "
            f"export workflow.",
        )


class GameMakerAdapter(_GuiOnly):
    name = "gamemaker"
    _editor_name = "GameMaker Studio 2"
    _install_url = "https://gamemaker.io"


class ConstructAdapter(_GuiOnly):
    name = "construct"
    _editor_name = "Construct 3"
    _install_url = "https://www.construct.net"


class RpgMakerAdapter(_GuiOnly):
    name = "rpgmaker"
    _editor_name = "RPG Maker MZ"
    _install_url = "https://www.rpgmakerweb.com"
