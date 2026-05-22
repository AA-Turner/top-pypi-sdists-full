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
import platform
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


def _to_cargo_name(title: str) -> str:
    """Convert any LLM-picked title into a valid Cargo package name.

    Cargo requires Unicode XID characters (letters, digits) plus `-` /
    `_`. Apostrophes ("Pilgrim's Path"), ampersands ("Hero & Sword"),
    emojis, and accented Latin-Extended chars all get stripped. The
    result is always non-empty (falls back to `sage_game`) and starts
    with a letter (prepends `g` if it starts with a digit, which Cargo
    also rejects).
    """
    cleaned = []
    for ch in title.lower():
        if ch.isalnum() and ord(ch) < 128:   # ASCII alphanumeric only
            cleaned.append(ch)
        elif ch in (" ", "_", "-"):
            cleaned.append("_")
        # everything else (apostrophe, &, emoji, period) is dropped
    name = "".join(cleaned).strip("_")
    while "__" in name:
        name = name.replace("__", "_")
    if not name:
        return "sage_game"
    if name[0].isdigit():
        name = "g_" + name
    return name


def _strip_fences(raw: str) -> str:
    """Strip ``` fences from an LLM response that wraps single-file output.

    Even when asked "no fences", many models hedge by wrapping their
    response in ```language ... ``` anyway. The single-file adapters
    (Bevy/Phaser/LÖVE/Pygame) feed the raw response straight to disk,
    so unstripped fences become syntax errors in Rust/TS/Lua/Python.

    Strategy:
      - If the entire response is one fenced block, return its inner
        text (stripped).
      - If the response has text before/after the fence, return the
        block's contents only (assume the model added prose).
      - Otherwise (no fences), return the response as-is.
    """
    text = raw.strip()
    if not text.startswith("```") and "```" not in text:
        return text
    # Find first fence opening and last fence closing.
    first = text.find("```")
    if first == -1:
        return text
    # Skip the language tag on the opening fence line (```lua, ```python, etc.).
    nl = text.find("\n", first)
    if nl == -1:
        return text
    inner_start = nl + 1
    # Closing fence — last ``` in the response.
    last = text.rfind("```")
    if last <= inner_start:
        # Single dangling fence — strip everything from the fence onward.
        return text[:first].strip()
    return text[inner_start:last].strip()


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
        # Sanitize the title into a valid Cargo package name. Cargo
        # enforces "Unicode XID" identifier rules — letters, digits, `-`,
        # `_`. An LLM-picked title like "Pilgrim's Path" or "Hero & Sword"
        # has characters Cargo refuses, so we strip them down to the
        # allowed alphabet here and never propagate the raw title into
        # the manifest.
        slug = _to_cargo_name(plan.title or "sage_game")
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
        body = _strip_fences(raw)
        if not body:
            raise RuntimeError(
                f"bevy: LLM returned empty body after fence-stripping. "
                f"Raw head:\n{raw[:500]!r}"
            )
        path = out_dir / "src" / "main.rs"
        path.write_text(body + "\n", encoding="utf-8")
        log(f"  [bevy] wrote src/main.rs ({len(body):,} bytes)")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        # Sprite animation strips go alongside static sprites — Bevy loads
        # them via the same `assets/` path resolver and slices via TextureAtlas.
        for src in (*manifest.sprites.values(), *manifest.sprite_animations.values(),
                    *manifest.audio.values(), *manifest.meshes.values()):
            shutil.copy2(src, out_dir / "assets" / src.name)

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        cargo = self.detect()
        if cargo is None:
            raise EngineNotInstalled("bevy", self.install_hint())
        start = time.monotonic()

        # Cross-compile honestly: pass --target so a request for
        # `linux` from a Windows host doesn't silently produce a
        # Windows .exe mislabeled as Linux. Without the matching rustup
        # toolchain installed, cargo errors out with a clear hint —
        # that's the right signal (sage's job here is "make obvious
        # what's needed", not "pretend it cross-compiles for free").
        rust_target = _BEVY_TARGET_TRIPLES.get(target)
        host_target = _bevy_host_target()
        is_cross = rust_target is not None and rust_target != host_target

        # Use cargo-zigbuild if available for cross-builds — zig's bundled
        # cross-linkers handle Windows→Linux out of the box, no system
        # cross-gcc needed. Falls back to plain `cargo build` otherwise.
        if is_cross and _have_zigbuild():
            cmd = [str(cargo), "zigbuild", "--release", "--target", rust_target]
        else:
            cmd = [str(cargo), "build", "--release"]
            if is_cross:
                cmd.extend(["--target", rust_target])
        proc = subprocess.run(
            cmd, cwd=out_dir, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=900, check=False,
        )
        if proc.returncode != 0:
            stderr = (proc.stderr or "")
            cross = rust_target and rust_target != host_target
            if cross and "is not installed" in stderr:
                # rustup target wasn't added — give the user the install
                # one-liner. Treat as BuildNotSupported, not a code bug:
                # sage's scaffold is fine, the toolchain just needs setup.
                raise BuildNotSupported(
                    "bevy",
                    f"Bevy cross-build to {rust_target} needs the Rust target "
                    f"installed. Run: rustup target add {rust_target}",
                )
            if cross:
                # Cross-compile failures past the rustup-target check are
                # almost always missing C linker/toolchain — bevy → linux
                # needs gcc-x86-64-linux-gnu (or cargo-zigbuild); bevy →
                # mac needs the Apple SDK which is only legal to use on a
                # Mac host. Surface that as user-fixable rather than a
                # sage bug, since healing the Rust source won't fix a
                # missing linker / wrong-OS-host.
                sysname = platform.system()
                if rust_target.endswith("-apple-darwin") and sysname != "Darwin":
                    raise BuildNotSupported(
                        "bevy",
                        "Bevy macOS cross-build from a non-Apple host needs "
                        "the macOS SDK, which Apple only licenses for use on "
                        "macOS hardware. Run sage on a Mac to ship a macOS "
                        "binary. Cargo error tail:\n" + stderr[-200:],
                    )
                # libudev-sys is a transitive Bevy dependency (for gamepad
                # input on Linux) and demands a real Linux sysroot — zig's
                # bundled cross-linker doesn't supply the libudev headers.
                # In practice the only realistic paths from Windows are:
                #   - build inside WSL/Linux (full apt-get environment)
                #   - build inside a Docker container with the sysroot
                # We surface that clearly so the user doesn't chase the
                # zigbuild rabbit hole indefinitely.
                if "pkg-config has not been configured" in stderr \
                   or "libudev" in stderr:
                    hint = (
                        "Bevy's libudev-sys dependency needs a full Linux "
                        "sysroot (libudev headers + dev libs). cargo-zigbuild "
                        "alone isn't sufficient. Easiest path: build inside "
                        "WSL/Ubuntu with `sudo apt install libudev-dev`, or "
                        "use a Docker cross-compile container"
                    )
                else:
                    hint = {
                        "x86_64-unknown-linux-gnu":
                            "install a Linux cross-linker + sysroot (try "
                            "WSL/Ubuntu with libudev-dev for the easiest path)",
                    }.get(rust_target, "install the matching cross-linker")
                raise BuildNotSupported(
                    "bevy",
                    f"Bevy cross-build to {rust_target} failed at link "
                    f"time — {hint}. Cargo error tail:\n{stderr[-300:]}",
                )
            raise RuntimeError(f"cargo build failed:\n{stderr[-800:]}")

        # Cargo writes the binary either to target/release/ (host build)
        # or target/<triple>/release/ (cross build). Pick the actual
        # executable: .exe on Windows, no-extension elf on Linux, .app
        # on macOS. Never a hidden file or build-tracking artifact.
        if rust_target and rust_target != host_target:
            release_dir = out_dir / "target" / rust_target / "release"
        else:
            release_dir = out_dir / "target" / "release"
        binary: Optional[Path] = None
        # `suffix` is the executable extension expected for the TARGET, not
        # the host — a cross-build to windows on Linux still produces .exe.
        suffix = ".exe" if target == "windows" or (
            not target and platform.system() == "Windows") else ""
        for candidate in sorted(release_dir.glob("*")):
            if not candidate.is_file():
                continue
            if candidate.name.startswith("."):
                continue
            if suffix and candidate.suffix.lower() != suffix:
                continue
            if not suffix and candidate.suffix in {".d", ".pdb", ".rlib", ".rmeta"}:
                continue
            binary = candidate
            break
        size = binary.stat().st_size if binary and binary.is_file() else 0
        log(f"  [bevy] build OK: {binary.name if binary else '?'} "
            f"({size:,} bytes)")
        return BuildArtifact(
            output_path=binary or release_dir, target=target, size_bytes=size,
            duration_s=time.monotonic() - start,
        )


# Rust target triples. iOS/Android omitted — they additionally require
# a C toolchain (xcode-select / ndk-build), which is out of scope for
# our "detect what's installed" check; if the user runs those, cargo
# will surface the missing-tooling error on its own.
_BEVY_TARGET_TRIPLES = {
    "windows": "x86_64-pc-windows-msvc",
    "linux":   "x86_64-unknown-linux-gnu",
    "mac":     "x86_64-apple-darwin",
}


def _have_zigbuild() -> bool:
    """Probe for cargo-zigbuild + zig. Both required for the bundled
    cross-link path. We check zig too because cargo-zigbuild is a thin
    wrapper that delegates to `zig cc`, and a half-install (one without
    the other) gives confusing late errors."""
    if shutil.which("zig") is None:
        return False
    # cargo-zigbuild registers as a cargo subcommand; the simplest probe
    # is to look for the binary on PATH.
    return shutil.which("cargo-zigbuild") is not None


def _bevy_host_target() -> Optional[str]:
    """Best-effort guess of the host's Rust target triple — used to skip
    the --target flag on a same-host build (avoids re-compiling deps to a
    parallel target dir for no reason)."""
    sysname = platform.system()
    if sysname == "Windows":
        return "x86_64-pc-windows-msvc"
    if sysname == "Darwin":
        # Apple Silicon vs Intel — `platform.machine()` returns 'arm64'
        # on M-series, 'x86_64' on Intel.
        return ("aarch64-apple-darwin" if platform.machine() == "arm64"
                else "x86_64-apple-darwin")
    if sysname == "Linux":
        return "x86_64-unknown-linux-gnu"
    return None


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
        body = _strip_fences(raw)
        if not body:
            raise RuntimeError(
                f"phaser: LLM returned empty body after fence-stripping. "
                f"Raw head:\n{raw[:500]!r}"
            )
        path = out_dir / "src" / "main.ts"
        path.write_text(body + "\n", encoding="utf-8")
        log(f"  [phaser] wrote src/main.ts ({len(body):,} bytes)")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        # Phaser bundles sprite-anim strips alongside static sprites; the
        # scene code slices by frame width when constructing AnimationFrames.
        for src in (*manifest.sprites.values(), *manifest.sprite_animations.values(),
                    *manifest.audio.values()):
            shutil.copy2(src, out_dir / "public" / "assets" / src.name)

    def build(self, out_dir: Path, *, target: str, log: ProgressFn) -> BuildArtifact:
        npm = self.detect()
        if npm is None:
            raise EngineNotInstalled("phaser", self.install_hint())
        start = time.monotonic()
        # On Windows, `npm` is actually `npm.cmd`. Python's CreateProcess
        # won't find it without either shell=True or the full resolved
        # path. We use the resolved path from detect() — same approach as
        # the Bevy adapter uses for `cargo`.
        npm_str = str(npm)
        # `npm.CMD` on Windows; the resolved path is what Python can exec.
        subprocess.run(
            [npm_str, "install", "--no-audit"],
            cwd=out_dir, check=False, timeout=300,
            encoding="utf-8", errors="replace",
            shell=False,
        )
        proc = subprocess.run(
            [npm_str, "run", "build"],
            cwd=out_dir, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=300, check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"vite build failed:\n{(proc.stderr or '')[-800:]}"
            )
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
        body = _strip_fences(raw)
        if not body:
            raise RuntimeError(
                f"love2d: LLM returned empty body after fence-stripping. "
                f"Raw head:\n{raw[:500]!r}"
            )
        path = out_dir / "main.lua"
        path.write_text(body + "\n", encoding="utf-8")
        log(f"  [love2d] wrote main.lua ({len(body):,} bytes)")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        for src in (*manifest.sprites.values(), *manifest.sprite_animations.values(),
                    *manifest.audio.values()):
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
        body = _strip_fences(raw)
        if not body:
            # No fallback template — heal loop re-prompts the LLM.
            raise RuntimeError(
                f"pygame: LLM returned empty body after fence-stripping. "
                f"Raw head:\n{(raw or '')[:500]!r}"
            )
        path = out_dir / "main.py"
        path.write_text(body + "\n", encoding="utf-8")
        log(f"  [pygame] wrote main.py ({len(body):,} bytes)")
        return [path]

    def consume_assets(self, manifest: AssetManifest, out_dir: Path, *, log: ProgressFn) -> None:
        copied = 0
        for src in manifest.sprites.values():
            shutil.copy2(src, out_dir / "assets" / "sprites" / src.name); copied += 1
        for src in manifest.sprite_animations.values():
            shutil.copy2(src, out_dir / "assets" / "sprites" / src.name); copied += 1
        for src in manifest.audio.values():
            shutil.copy2(src, out_dir / "assets" / "audio" / src.name); copied += 1
        log(f"  [pygame] consumed {copied} asset(s) "
            f"({len(manifest.sprite_animations)} anim strips)")

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
        # zipapp.create_archive refuses to overwrite an existing target —
        # delete a stale one from a previous run so re-builds work.
        if archive.exists():
            archive.unlink()
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
        for src in (*manifest.sprites.values(), *manifest.sprite_animations.values(),
                    *manifest.audio.values(), *manifest.meshes.values()):
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
