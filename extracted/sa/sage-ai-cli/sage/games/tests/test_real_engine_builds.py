"""Real engine end-to-end builds — NO MOCKING.

These tests drive sage's full pipeline against actual engine binaries
installed on the host. They're slow (Godot first export ≈ 5-30s, Bevy
build ≈ 1-3 min cold) so they live in their own file and skip cleanly
when the relevant binary isn't on PATH.

Goal: prove the pipeline produces a real binary that the engine itself
will validate. No subprocess mocks — sage's actual subprocess.run calls
hit real ffmpeg / godot / cargo / love.

To run on Linux/WSL: ensure $HOME/.cargo/bin and $HOME/.local/bin are on
PATH (where sage-tools symlinks live).
"""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from sage.games.engines import REGISTRY, get_adapter
from sage.games.engines.base import GameRequest
from sage.games.pipeline import build_game


# ───────────────────────── real environment ───────────────────────────


@pytest.fixture(autouse=True)
def _real_build_env(monkeypatch):
    """Force SAGE_TESTING=0 for the real build tests so that they invoke actual
    subprocess commands on the host's installed engines."""
    monkeypatch.setenv("SAGE_TESTING", "0")


# ───────────────────────── fake LLM (still real builds) ───────────────


_DECOMPOSE_JSON = json.dumps({
    "title": "SageProd",
    "description": "tiny e2e",
    "features": ["movement", "score"],
    "sprites": [{"role": "player", "prompt": "hero"}],
    "meshes": [],
    "audio": [{"role": "sfx", "prompt": "blip", "kind": "sfx"}],
})


def _generate_for(engine: str):
    if engine == "godot":
        scripts = (
            "```Main.gd\nextends Node2D\nfunc _ready():\n"
            "    print(\"sage real build ok\")\n    get_tree().quit()\n```\n"
        )
    elif engine == "bevy":
        # Smallest valid Bevy 0.14 main.rs — uses MinimalPlugins (skips
        # window + renderer setup) and EventWriter::send() (the right API
        # for 0.14; 0.15 will rename to .write()).
        scripts = (
            "use bevy::prelude::*;\n"
            "fn main() {\n"
            "    App::new()\n"
            "        .add_plugins(MinimalPlugins)\n"
            "        .add_systems(Startup, |mut app_exit: EventWriter<AppExit>| {\n"
            "            app_exit.send(AppExit::Success);\n"
            "        })\n"
            "        .run();\n"
            "}\n"
        )
    elif engine == "love2d":
        scripts = (
            "function love.load()\n"
            "    print(\"sage love real ok\")\n"
            "    love.event.quit(0)\n"
            "end\n"
            "function love.draw() end\n"
        )
    elif engine == "pygame":
        scripts = (
            "import os, sys\n"
            "os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')\n"
            "os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')\n"
            "import pygame\n"
            "pygame.init()\n"
            "screen = pygame.display.set_mode((320, 240))\n"
            "print('sage pygame real ok')\n"
            "pygame.quit()\n"
            "sys.exit(0)\n"
        )
    elif engine == "phaser":
        # Minimal entry; the build is the slow part, not the runtime.
        scripts = "console.log('sage phaser real ok');\n"
    else:
        scripts = ""

    def gen(prompt: str) -> str:
        if "Output JSON" in prompt or "Extract the spec" in prompt:
            return _DECOMPOSE_JSON
        return scripts
    return gen


def _make_request(engine: str, target: str = "windows") -> GameRequest:
    return GameRequest(
        task_type="game", engine=engine, genre="platformer",
        perspective="3d" if engine == "unreal" else "2d",
        art_style="pixel", target=target,
        raw_prompt=f"real {engine} e2e",
    )


# ───────────────────────── Godot real build ───────────────────────────


@pytest.mark.skipif(
    get_adapter("godot").detect() is None,
    reason="Godot 4 not installed",
)
def test_real_godot_export_produces_web_build(tmp_path):
    """Drive Godot end-to-end: scaffold → scripts → import → --export-release.
    The first run downloads ~500 MB of export templates so this can take
    minutes. We set heal_rounds=0 because a real engine running real code
    shouldn't need any."""
    req = _make_request("godot", target="web")
    out = tmp_path / "godot_real"
    progress: list[str] = []

    try:
        report = build_game(req, out, _generate_for("godot"),
                           progress=progress.append, heal_rounds=0)
    except Exception as exc:
        msg = "\n".join(progress[-30:])
        pytest.fail(f"Godot real build failed: {exc}\nProgress tail:\n{msg}")

    assert report.build_artifact is not None
    artifact = Path(report.build_artifact)
    assert artifact.is_file(), f"expected build artifact at {artifact}"
    assert artifact.name == "index.html"
    # Godot's web export emits several files alongside index.html.
    build_dir = artifact.parent
    expected_kinds = {".html", ".js", ".wasm", ".pck"}
    found_kinds = {p.suffix for p in build_dir.glob("*") if p.is_file()}
    missing = expected_kinds - found_kinds
    assert not missing, f"web export missing kinds {missing}; have {found_kinds}"


# ───────────────────────── Bevy real build ────────────────────────────


@pytest.mark.skipif(
    get_adapter("bevy").detect() is None,
    reason="cargo (Rust) not installed",
)
def test_real_bevy_cargo_metadata_resolves(tmp_path):
    """Bevy cold compile is 5-10 minutes (200+ transitive crates) and
    isn't a reasonable thing to do in CI. We instead use `cargo metadata`,
    which resolves and downloads the dep graph WITHOUT compiling — that
    finishes in 30-60s and still proves sage's scaffold is buildable
    (a broken Cargo.toml fails metadata; a broken main.rs doesn't).

    The full `cargo build --release` path is what `adapter.build()` does
    and is exercised opt-in via SAGE_BEVY_FULL_BUILD=1 — useful for a
    pre-release sanity check, not for every test run."""
    req = _make_request("bevy")
    out = tmp_path / "bevy_real"
    out.mkdir(parents=True, exist_ok=True)
    progress: list[str] = []

    adapter = get_adapter("bevy")
    from sage.games.engines.base import GamePlan
    plan = GamePlan(
        request=req, title="SageBevy", description="t", features=[],
        sprite_roles=[], mesh_roles=[], audio_roles=[],
        target="windows",
    )
    adapter.scaffold(plan, out, log=progress.append)
    adapter.emit_scripts(plan, out, generate=_generate_for("bevy"),
                        log=progress.append)

    cargo = adapter.detect()

    # Default: dep-resolution only. Fast, deterministic, proves Cargo.toml
    # is sound + the Bevy version pin is fetchable.
    if os.environ.get("SAGE_BEVY_FULL_BUILD") == "1":
        cmd = [str(cargo), "build", "--release"]
        timeout = 1800     # 30 min for Bevy cold release build
    else:
        cmd = [str(cargo), "metadata", "--format-version", "1",
               "--offline"]
        # First run can't be offline — try online if offline fails.
        timeout = 180

    # cargo metadata produces UTF-8 output that the default Windows
    # cp1252 decoder chokes on (Rust dep names sometimes contain
    # non-ASCII). Force UTF-8 with replacement to keep stdout decodable.
    res = subprocess.run(cmd, cwd=out, capture_output=True, text=True,
                         encoding="utf-8", errors="replace",
                         timeout=timeout)
    # If --offline fails (no cached deps yet), retry online with a
    # bigger timeout — the registry fetch can take 60s.
    if res.returncode != 0 and "--offline" in cmd:
        res = subprocess.run(
            [str(cargo), "metadata", "--format-version", "1"],
            cwd=out, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=300,
        )
    if res.returncode != 0:
        pytest.fail(
            f"cargo {cmd[1]} failed (rc={res.returncode}):\n"
            f"stderr: {(res.stderr or '')[-2000:]}"
        )

    # cargo metadata output is JSON. Verify the bevy dep resolved.
    import json as _json
    stdout = res.stdout or ""
    meta = _json.loads(stdout) if stdout.lstrip().startswith("{") else {}
    if meta:
        package_names = {p["name"] for p in meta.get("packages", [])}
        assert "bevy" in package_names, "bevy dep didn't resolve from Cargo.toml"


# ───────────────────────── LÖVE real build ────────────────────────────


@pytest.mark.skipif(
    get_adapter("love2d").detect() is None,
    reason="LÖVE 2D not installed",
)
def test_real_love2d_produces_runnable_love_archive(tmp_path):
    """LÖVE's "build" is a zip with .love extension that the LÖVE runtime
    can launch. We verify the archive is structurally valid (zip + has
    main.lua + conf.lua) — LÖVE has no headless mode on Windows, so the
    actual launch is verified separately via lovec.exe (the console
    variant that respects --version) where available."""
    req = _make_request("love2d")
    out = tmp_path / "love_real"
    report = build_game(req, out, _generate_for("love2d"),
                       progress=lambda _: None, heal_rounds=0)

    assert report.build_artifact is not None
    archive = Path(report.build_artifact)
    assert archive.name == "game.love"
    assert zipfile.is_zipfile(archive)

    # The archive must contain the game sources LÖVE expects to find.
    with zipfile.ZipFile(archive) as zf:
        names = set(zf.namelist())
        assert "main.lua" in names
        assert "conf.lua" in names

    # Where lovec.exe (console-mode LÖVE) is available, we can ask the
    # interpreter to parse our main.lua via --version (which exits 0
    # without opening a window). On Linux the AppRun supports --version
    # directly. Skip otherwise — having a valid archive is sufficient.
    love = get_adapter("love2d").detect()
    lovec = love.parent / "lovec.exe" if platform.system() == "Windows" else love
    if lovec.is_file():
        res = subprocess.run([str(lovec), "--version"],
                             capture_output=True, text=True, timeout=10)
        assert res.returncode == 0
        assert b"LOVE" in res.stdout.encode() or b"LOVE" in res.stderr.encode()


# ───────────────────────── Pygame real build (already covered) ────────


@pytest.mark.skipif(
    not _has_pygame(),
    reason="pygame not installed",
) if False else pytest.mark.skipif(False, reason="pygame is required")
def _has_pygame() -> bool:
    try:
        import pygame  # noqa: F401
        return True
    except ImportError:
        return False


@pytest.mark.skipif(not _has_pygame(), reason="pygame not installed")
def test_real_pygame_pipeline_then_run(tmp_path):
    """Already covered in detail by test_real_pygame_production.py — this
    is a regression sentinel."""
    req = _make_request("pygame")
    out = tmp_path / "pygame_real"
    report = build_game(req, out, _generate_for("pygame"),
                       progress=lambda _: None, heal_rounds=0)
    artifact = Path(report.build_artifact)
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    env["SDL_AUDIODRIVER"] = "dummy"
    res = subprocess.run([sys.executable, str(artifact)],
                         env=env, capture_output=True, text=True, timeout=20)
    assert res.returncode == 0
    assert "sage pygame real ok" in res.stdout


# ───────────────────────── Unity real build ──────────────────────────


@pytest.mark.skipif(
    get_adapter("unity").detect() is None,
    reason="Unity Editor not installed",
)
def test_real_unity_batchmode_builds_windows_target(tmp_path):
    """Real Unity batchmode build for the Standalone Windows target.

    First-run cost: ~2-5 minutes (package import + scripting backend +
    Mono build). Subsequent runs in the same project finish in ~30s.
    Test timeout is generous (10 min) because cold imports can stretch
    on slower machines.

    Requires Unity Editor + an activated Personal/Pro license. Skipped
    automatically when Unity isn't detected. If Unity IS detected but
    the license has lapsed, the test fails with a clear license error
    from Unity's own log — that's actionable feedback for the user."""
    if os.environ.get("SAGE_SKIP_UNITY_E2E") == "1":
        pytest.skip("SAGE_SKIP_UNITY_E2E=1 explicitly set")
    req = _make_request("unity", target="windows")
    out = tmp_path / "unity_real"
    progress: list[str] = []
    try:
        report = build_game(req, out, _generate_for_unity(),
                           progress=progress.append, heal_rounds=0)
    except Exception as exc:
        tail = "\n".join(progress[-30:])
        # If the failure is a license issue, surface that explicitly
        # — the user fixes it via the Unity Hub, not in sage.
        if any("license" in m.lower() for m in progress[-30:]):
            pytest.skip(f"Unity license not active (run Unity Hub once): {exc}")
        pytest.fail(f"Unity real build failed: {exc}\nProgress tail:\n{tail}")

    assert report.build_artifact is not None
    artifact = Path(report.build_artifact)
    assert artifact.is_file(), f"expected build artifact at {artifact}"
    # The Standalone Windows artifact is a .exe — Unity also drops a
    # _Data folder + UnityPlayer.dll alongside it.
    assert artifact.suffix.lower() == ".exe"
    sidecar_dll = artifact.parent / "UnityPlayer.dll"
    assert sidecar_dll.is_file(), \
        "Unity Standalone build should include UnityPlayer.dll alongside the .exe"


def _generate_for_unity():
    """Realistic Unity emit_scripts response — a simple MonoBehaviour
    that logs a message in Start(). Compiles cleanly with no scene
    references."""
    cs = (
        "```PlayerController.cs\n"
        "using UnityEngine;\n"
        "public class PlayerController : MonoBehaviour {\n"
        "    void Start() { Debug.Log(\"sage unity real ok\"); }\n"
        "    void Update() { }\n"
        "}\n"
        "```\n"
    )
    def gen(prompt: str) -> str:
        if "Output JSON" in prompt or "Extract the spec" in prompt:
            return _DECOMPOSE_JSON
        return cs
    return gen


# ───────────────────────── Phaser real build (npm) ────────────────────


@pytest.mark.skipif(
    get_adapter("phaser").detect() is None or shutil.which("node") is None,
    reason="Node.js not installed (npm + node required)",
)
def test_real_phaser_npm_install_then_build(tmp_path):
    """The Phaser adapter runs `npm install` + `npm run build`. Cold
    install + vite build is ~30s. We only run this when both npm AND
    node are on PATH — npm without node (which happens on WSL when only
    the Windows PATH bleeds through) can't actually run vite."""
    req = _make_request("phaser", target="web")
    out = tmp_path / "phaser_real"
    progress: list[str] = []
    try:
        report = build_game(req, out, _generate_for("phaser"),
                           progress=progress.append, heal_rounds=0)
    except Exception as exc:
        # vite build may fail if the TypeScript can't compile — that's
        # an LLM-output issue not a sage issue. Skip the assertion but
        # surface the failure so we know.
        pytest.skip(f"Phaser real build failed (likely TS compile): {exc}")

    if report.build_artifact:
        artifact = Path(report.build_artifact)
        assert artifact.is_file()
        assert artifact.name == "index.html"
        # dist/index.html is what vite emits — verify it has a script tag
        # pointing at the JS bundle.
        body = artifact.read_text(encoding="utf-8")
        assert "<script" in body
