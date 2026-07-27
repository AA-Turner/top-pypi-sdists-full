"""Deployment artifact shape — what each engine actually produces.

"Production ready" means the build output is shippable as-is. For each
engine + target combination this verifies:

  * The export preset/config in the scaffold matches the target.
  * The build path (where the binary lands) follows the convention
    every static-host or store expects: itch.io expects index.html for
    web; Steam expects a single .exe / .x86_64 for Windows/Linux desktop.
  * Path naming is OS-friendly (no spaces / colons / non-ASCII in
    artifact names that a user has to manually edit before uploading).

Most of these are settings-file shape tests — checking that the scaffold
emits the right export_presets.cfg / SageBuilder.cs / .uproject content
so a downstream build won't fail with "no default preset" or similar.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sage.games.engines import get_adapter
from sage.games.engines.base import GamePlan, GameRequest


def _plan(engine: str, target: str = "web", title: str = "Deploy Test") -> GamePlan:
    req = GameRequest(
        task_type="game", engine=engine, genre="platformer",
        perspective="3d" if engine == "unreal" else "2d",
        target=target, raw_prompt="deploy test",
    )
    return GamePlan(
        request=req, title=title, description="x", features=[],
        sprite_roles=[], mesh_roles=[], audio_roles=[],
        target=target,
    )


# ───────────────────────── Godot deployment ───────────────────────────


def test_godot_export_presets_declares_web_target_correctly(tmp_path):
    """The export_presets.cfg must declare a Web preset that:
      - is runnable (otherwise --export-release errors out)
      - has empty include_filter/exclude_filter (Godot 4.6 strict requirement)
      - exports to build/index.html (itch.io / GitHub Pages convention)
    Catch regressions in the preset template here."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan("godot", "web"), tmp_path, log=lambda _: None)
    presets = (tmp_path / "export_presets.cfg").read_text(encoding="utf-8")

    assert 'platform="Web"' in presets
    assert "runnable=true" in presets
    assert 'include_filter=""' in presets
    assert 'exclude_filter=""' in presets
    assert 'export_path="build/index.html"' in presets
    # script_export_mode=2 means "compiled GDScript" — important for
    # web exports because GDScript source includes BOM-laden text Godot
    # doesn't ship to the browser.
    assert "script_export_mode=2" in presets


def test_godot_scaffold_project_godot_declares_main_scene(tmp_path):
    """project.godot must point to scenes/Main.tscn as run/main_scene.
    Without this Godot opens to an empty editor and the export emits no
    runnable content."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan("godot"), tmp_path, log=lambda _: None)
    project = (tmp_path / "project.godot").read_text(encoding="utf-8")
    assert 'run/main_scene="res://scenes/Main.tscn"' in project
    assert 'config/icon="res://icon.svg"' in project


def test_godot_main_scene_references_main_gd_script(tmp_path):
    """Main.tscn must have an ExtResource pointing at scripts/Main.gd.
    If the scene loads without the script attached, the engine boots a
    blank Node2D and nothing happens."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan("godot"), tmp_path, log=lambda _: None)
    scene = (tmp_path / "scenes" / "Main.tscn").read_text(encoding="utf-8")
    assert 'script = ExtResource("1")' in scene
    assert 'path="res://scripts/Main.gd"' in scene


@pytest.mark.parametrize("target,preset_name,export_path", [
    ("web",     "Web",             "build/index.html"),
])
def test_godot_web_target_export_path_is_static_host_friendly(
    target, preset_name, export_path, tmp_path,
):
    """Web exports MUST land at exactly `build/index.html` — any static
    host (itch.io, GitHub Pages, Cloudflare Pages) expects that path."""
    adapter = get_adapter("godot")
    adapter.scaffold(_plan("godot", target), tmp_path, log=lambda _: None)
    presets = (tmp_path / "export_presets.cfg").read_text(encoding="utf-8")
    assert f'export_path="{export_path}"' in presets
    assert f'platform="{preset_name}"' in presets


# ───────────────────────── Unity deployment ───────────────────────────


def test_unity_sage_builder_has_an_entry_per_supported_platform(tmp_path):
    """SageBuilder.cs must expose Build<Platform>() methods for every
    target the adapter's _TARGET_TO_METHOD map points to. Wrong entry
    point name → batchmode -executeMethod fails with TypeLoadException."""
    adapter = get_adapter("unity")
    adapter.scaffold(_plan("unity"), tmp_path, log=lambda _: None)
    body = (tmp_path / "Assets" / "Editor" / "SageBuilder.cs").read_text("utf-8")

    for method in ("BuildWebGL", "BuildWindows", "BuildMac", "BuildLinux"):
        assert f"public static void {method}" in body, f"missing {method}"

    # All four call into Build(BuildTarget.<...>) for the right target enum.
    assert "BuildTarget.WebGL" in body
    assert "BuildTarget.StandaloneWindows64" in body
    assert "BuildTarget.StandaloneOSX" in body
    assert "BuildTarget.StandaloneLinux64" in body


def test_unity_project_version_file_specifies_2022_lts(tmp_path):
    """Unity needs ProjectSettings/ProjectVersion.txt to declare a
    specific editor version (with revision hash). Without it the Hub
    refuses to open the project. We pin to 2022 LTS because that's
    sage's tested minimum."""
    adapter = get_adapter("unity")
    adapter.scaffold(_plan("unity"), tmp_path, log=lambda _: None)
    pvt = (tmp_path / "ProjectSettings" / "ProjectVersion.txt").read_text("utf-8")
    assert "m_EditorVersion:" in pvt
    # The version string format is X.Y.ZfN (where fN is the build number).
    assert "2022.3" in pvt or "2023." in pvt or "6000." in pvt


def test_unity_packages_manifest_is_valid_json(tmp_path):
    """Packages/manifest.json must be parseable JSON — Unity's package
    resolver fails the whole project load on a syntax error."""
    adapter = get_adapter("unity")
    adapter.scaffold(_plan("unity"), tmp_path, log=lambda _: None)
    body = (tmp_path / "Packages" / "manifest.json").read_text("utf-8")
    parsed = json.loads(body)
    assert "dependencies" in parsed


# ───────────────────────── Unreal deployment ──────────────────────────


def test_unreal_uproject_json_is_valid_and_declares_engine(tmp_path):
    """The .uproject file is JSON. Unreal validates it on first open and
    a malformed file blocks the editor from launching the project."""
    adapter = get_adapter("unreal")
    plan = _plan("unreal", title="MyDeployGame")
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    uprojects = list(tmp_path.glob("*.uproject"))
    assert len(uprojects) == 1
    body = json.loads(uprojects[0].read_text("utf-8"))
    assert body["FileVersion"] == 3
    assert body["EngineAssociation"]  # non-empty version string
    assert body["Modules"], "uproject must declare at least one module"


def test_unreal_build_cs_declares_runtime_dependencies(tmp_path):
    """The module's .Build.cs file must declare Engine + InputCore as
    PublicDependencyModuleNames — without those, the module won't link."""
    adapter = get_adapter("unreal")
    plan = _plan("unreal", title="MyDeployGame")
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    build_cs = (tmp_path / "Source" / "MyDeployGame"
                / "MyDeployGame.Build.cs").read_text("utf-8")
    for dep in ("Core", "CoreUObject", "Engine", "InputCore"):
        assert f'"{dep}"' in build_cs


# ───────────────────────── Bevy deployment ────────────────────────────


def test_bevy_cargo_toml_declares_bevy_dep_and_edition(tmp_path):
    """Cargo.toml drives `cargo build --release`. Wrong edition or
    missing bevy dep fails the build with confusing rustc errors."""
    adapter = get_adapter("bevy")
    adapter.scaffold(_plan("bevy"), tmp_path, log=lambda _: None)
    cargo = (tmp_path / "Cargo.toml").read_text(encoding="utf-8")
    assert "[package]" in cargo
    assert "edition = \"2021\"" in cargo
    assert "[dependencies]" in cargo
    assert "bevy =" in cargo


# ───────────────────────── Phaser deployment ──────────────────────────


def test_phaser_package_json_declares_vite_build_script(tmp_path):
    """The Phaser adapter runs `npm run build` which must map to `vite
    build` (or similar). Without it the build does nothing and dist/
    stays empty."""
    adapter = get_adapter("phaser")
    adapter.scaffold(_plan("phaser"), tmp_path, log=lambda _: None)
    pkg = json.loads((tmp_path / "package.json").read_text("utf-8"))
    assert "build" in pkg.get("scripts", {})
    assert "vite" in pkg["scripts"]["build"]
    assert "phaser" in pkg.get("dependencies", {})


def test_phaser_index_html_mounts_module_script(tmp_path):
    """The boot HTML must load /src/main.ts as a module — Phaser games
    can't bootstrap from a classic <script>."""
    adapter = get_adapter("phaser")
    adapter.scaffold(_plan("phaser"), tmp_path, log=lambda _: None)
    html = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert 'type="module"' in html
    assert "/src/main.ts" in html
    assert 'id="game"' in html


# ───────────────────────── LÖVE deployment ────────────────────────────


def test_love_conf_lua_sets_window_title(tmp_path):
    """The conf.lua is what gets baked into the `.love` archive and
    determines window title at runtime."""
    adapter = get_adapter("love2d")
    adapter.scaffold(_plan("love2d", title="My LÖVE Deploy"),
                     tmp_path, log=lambda _: None)
    conf = (tmp_path / "conf.lua").read_text(encoding="utf-8")
    assert "love.conf" in conf
    assert "My LÖVE Deploy" in conf
    assert "t.window" in conf


def test_love_build_produces_love_archive(tmp_path):
    """LÖVE's "build" is a .love file (a zip with a known extension).
    Verify the archive is created at build/game.love and contains the
    game's source files."""
    import zipfile

    adapter = get_adapter("love2d")
    plan = _plan("love2d")
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    # Drop a main.lua to be archived
    (tmp_path / "main.lua").write_text("function love.draw() end\n",
                                        encoding="utf-8")
    artifact = adapter.build(tmp_path, target="any", log=lambda _: None)

    assert artifact.output_path.name == "game.love"
    assert artifact.output_path.is_file()
    with zipfile.ZipFile(artifact.output_path) as zf:
        names = zf.namelist()
        assert "main.lua" in names
        assert "conf.lua" in names
        # Build directory MUST NOT be inside the archive (would loop).
        assert not any(n.startswith("build/") for n in names)


# ───────────────────────── Pygame deployment ──────────────────────────


def test_pygame_pyz_excludes_build_and_sage_assets(tmp_path):
    """The zipapp must NOT include build/ or .sage_assets/ — bundling
    them would either (a) loop infinitely (build inside build), or (b)
    leak temp prompts into the shipped artifact."""
    import zipfile

    adapter = get_adapter("pygame")
    plan = _plan("pygame")
    adapter.scaffold(plan, tmp_path, log=lambda _: None)
    (tmp_path / "main.py").write_text("import sys; sys.exit(0)\n",
                                       encoding="utf-8")
    (tmp_path / ".sage_assets").mkdir()
    (tmp_path / ".sage_assets" / "leak.txt").write_text("temp")
    artifact = adapter.build(tmp_path, target="any", log=lambda _: None)

    assert artifact.output_path.name == "game.pyz"
    with zipfile.ZipFile(artifact.output_path) as zf:
        names = zf.namelist()
        assert "main.py" in names
        assert "__main__.py" in names
        for n in names:
            assert not n.startswith("build/"), \
                f".pyz contains build/{n} — would loop on rebuild"
            assert ".sage_assets" not in n, \
                f".pyz leaked temp asset {n}"


def test_pygame_requirements_txt_pins_pygame_minimum_version(tmp_path):
    """The user runs `pip install -r requirements.txt` before launching
    — the pin needs to be tight enough to get a working version but
    loose enough to allow security patches."""
    adapter = get_adapter("pygame")
    adapter.scaffold(_plan("pygame"), tmp_path, log=lambda _: None)
    reqs = (tmp_path / "requirements.txt").read_text(encoding="utf-8")
    assert reqs.strip().startswith("pygame")
    # Either a `>=` floor or a `==` pin — both are fine for production.
    assert ">=" in reqs or "==" in reqs
